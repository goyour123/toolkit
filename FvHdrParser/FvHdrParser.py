import os
import argparse
import ctypes
import uuid

FV_HEADER_SIZE = 0x48
FV_SIGNATURE = b'_FVH'
FV_BLOCK_SIZE = 0x1000

class Guid(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Data1', ctypes.c_uint32),
        ('Data2', ctypes.c_uint16),
        ('Data3', ctypes.c_uint16),
        ('Data4', ctypes.c_ubyte * 8),
    ]

class EfiFvBlockMap(ctypes.LittleEndianStructure):
    _fields_ = [
        ('NumBlocks', ctypes.c_uint32),
        ('Length', ctypes.c_uint32),
    ]

class FvHeader(ctypes.LittleEndianStructure):
    _fields_ = [
        ('ZeroVector', ctypes.c_uint8 * 16),
        ('FileSystemGuid', Guid),
        ('FvLength', ctypes.c_uint64),
        ('Signature', ctypes.c_char * 4),
        ('Attributes', ctypes.c_uint32),
        ('HeaderLength', ctypes.c_uint16),
        ('Checksum', ctypes.c_uint16),
        ('ExtHeaderOffset', ctypes.c_uint16),
        ('Reserved', ctypes.c_uint8 * 1),
        ('Revision', ctypes.c_uint8),
        ('BlockMap', EfiFvBlockMap),
    ]

def calculate_checksum(fv_header):
    header_bytes = bytearray(fv_header)
    checksum = 0
    for i in range(0, len(header_bytes), 2):
        if i == FvHeader.Checksum.offset:
            continue
        word = header_bytes[i] | (header_bytes[i + 1] << 8)
        checksum = ((checksum + word) & 0xFFFF)
    checksum = 0x10000 - checksum
    return checksum

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file_path', type=os.path.abspath, required=True)
    parser.add_argument('-g', '--fv_guid', type=uuid.UUID, required=False)
    args = parser.parse_args()

    file_size = os.stat(args.file_path).st_size
    print (f"File Size: {hex(file_size)} bytes")

    with open(args.file_path, 'rb') as f:
        for block_offset in range(0, file_size, FV_BLOCK_SIZE):
            f.seek(block_offset)

            fv_header = FvHeader.from_buffer_copy(f.read(FV_HEADER_SIZE))

            if fv_header.Signature != FV_SIGNATURE:
                continue

            if args.fv_guid and uuid.UUID(bytes_le=bytes(fv_header.FileSystemGuid)) != args.fv_guid:
                continue

            print (f"Found FV Header at offset: {hex(block_offset)}")
            print (f"  Header Length: {hex(fv_header.HeaderLength)} bytes")
            print (f"  GUID: {str(uuid.UUID(bytes_le=bytes(fv_header.FileSystemGuid)))}")
            print (f"  Checksum: {hex(fv_header.Checksum)}")
            calculated_checksum = calculate_checksum(fv_header)
            print (f"  Calculated Checksum: {hex(calculated_checksum)}")