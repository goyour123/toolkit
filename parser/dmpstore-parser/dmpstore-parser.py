
#
## In UEFI shell
# dmpstore [Variable] -s [File]
# 
## Use dmpstore-parser
# dmpstore-parser.py [File]
#

import sys
import re

def byte2hex(byte):
    return (byte[::-1]).hex()

def strLen2int(leng):
    return int(leng[::-1].hex(), 16)

def readstring(file_cursor):
    char16_read = file_cursor.read(2)
    char16 = char16_read
    while char16_read != b'\x00\x00':
        char16_read = file_cursor.read(2)
        char16 += char16_read
    return char16.decode('utf-16')

def read_fpath_node(file_cursor):
    fpath_node = []
    efi_device_path_protocol = {
        'Type': None,
        'SubType': None,
        'Length': []
    }

    efi_device_path_protocol['Type'] = byte2hex(file_cursor.read(1))

    while efi_device_path_protocol['Type'] != '7f':
        efi_device_path_protocol['SubType'] = byte2hex(file_cursor.read(1))
        efi_device_path_protocol['Length'].append(byte2hex(file_cursor.read(1)))
        efi_device_path_protocol['Length'].append(byte2hex(file_cursor.read(1)))
        fpath_node.append(efi_device_path_protocol)
        efi_device_path_protocol['Type'] = file_cursor.read(1)

    efi_device_path_protocol['SubType'] = byte2hex(file_cursor.read(1))
    efi_device_path_protocol['Length'].append(byte2hex(file_cursor.read(1)))
    efi_device_path_protocol['Length'].append(byte2hex(file_cursor.read(1)))
    fpath_node.append(efi_device_path_protocol)
    return fpath_node

def data_printer(data):
    for index, value in enumerate(data):
        if index % 15 == 0 and index != 0:
            print(end='\n')
        print(value, end=' ')

def main():
    var_file = open(sys.argv[1], 'rb')
    var_name_len = var_file.read(4)
    var_data_len = var_file.read(4)

    data_len = strLen2int(var_data_len)

    var_name = (var_file.read(strLen2int(var_name_len))).decode('utf-16')

    var_guid = (byte2hex(var_file.read(4)) + '-' + \
                byte2hex(var_file.read(2)) + '-' + \
                byte2hex(var_file.read(2)) + '-' + \
                byte2hex(var_file.read(8))).upper()
    var_attr = byte2hex(var_file.read(4))

    # #print 'Length: 0x' + var_name_len[::-1].encode('hex')
    # #print 'Data Length: 0x' + var_data_len[::-1].encode('hex')
    print('Name: {0}'.format(var_name))
    print('Guid: {0}'.format(var_guid))
    print('Attributes: 0x{0}'.format(var_attr))

    if re.match('Boot[0-9]*', var_name):
        efi_load_option = {
            'Attributes': None,
            'FilePathListLength': None,
            'Description': None,
            'FilePathList': [],
            'OptionalData': []
        }
        efi_load_option['Attributes'] = byte2hex(var_file.read(4))
        efi_load_option['FilePathListLength'] = int(byte2hex(var_file.read(2)))
        efi_load_option['Description'] = readstring(var_file)
        efi_load_option['FilePathList'] = read_fpath_node(var_file)
        efi_load_option['OptionalData'] = [var_file.read(1).hex() for index in range(0, data_len)]

        print('EFI_LOAD_OPTION')
        print('Attributes: 0x{0}'.format(efi_load_option['Attributes']))
        print('FilePathLength: {0} byte(s)'.format(efi_load_option['FilePathListLength']))
        print('Description: {0}'.format(efi_load_option['Description']))
        for index, fpath in enumerate(efi_load_option['FilePathList']):
            print('FilePathList[{0}]: {1}'.format(index, fpath))
        print('OptionalData:')
        data_printer(efi_load_option['OptionalData'])

    else:
        var_data = [var_file.read(1).hex() for index in range(0, data_len)]
        print('Data: ')
        for index, data in enumerate(var_data):
            if index % 15 == 0 and index != 0:
                print(end='\n')
            print(data, end=' ')

if __name__ == '__main__':
    main()
