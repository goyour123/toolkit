import tarfile
import os
import json
import re

TAR_GZ_PATH = "OUTPUT.tar.gz"
OUTPUT_JSON_PATH = "dmidecode_output.json"

class DmicodeParser:
    def __init__(self, tar_gz_path):
        self.parser_dict = {}
        with tarfile.open(tar_gz_path, 'r:gz') as tar:
            for file in tar.getnames():
                if not file.endswith('.txt'):
                    continue
                file_name = os.path.basename(file).split('.')[0]
                with tar.extractfile(file) as f:
                    if "smbios_type_0" == file_name:
                        self.parser_dict[file_name] = self.parse_smbios_0(f)
                    elif "smbios_type_1" == file_name:
                        self.parser_dict[file_name] = self.parse_smbios_1(f)
                    elif "smbios_type_3" == file_name:
                        self.parser_dict[file_name] = self.parse_smbios_3(f)
                    elif "smbios_type_4" == file_name:
                        self.parser_dict[file_name] = self.parse_smbios_4(f)
                    elif "smbios_type_7" == file_name:
                        self.parser_dict[file_name] = self.parse_smbios_7(f)
                    elif "smbios_type_9" == file_name:
                        self.parser_dict[file_name] = self.parse_smbios_9(f)
                    elif "smbios_type_11" == file_name:
                        self.parser_dict[file_name] = self.parse_smbios_11(f)
                    elif "smbios_type_16" == file_name:
                        self.parser_dict[file_name] = self.parse_smbios_16(f)
                    elif "smbios_type_17" == file_name:
                        self.parser_dict[file_name] = self.parse_smbios_17(f)
                    elif "smbios_type_19" == file_name:
                        self.parser_dict[file_name] = self.parse_smbios_19(f)
                    elif "smbios_type_32" == file_name:
                        self.parser_dict[file_name] = self.parse_smbios_32(f)

    def header_info(self, line):
        match = re.search(r'Handle\s(\S+),\sDMI\stype\s(\S+),\s(\d+)\sbytes', line)
        if match:
            return {
                "Handle": match.group(1),
                #"DMI Type": match.group(2),
                "Size (bytes)": match.group(3)
            }
        return None

    def parse_smbios_0 (self, file):
        ##
        ## TODO: Parse BIN file to get Firmware Characteristics
        ##
        smbios_data = {}
        fm_chars = ["PCI is supported", 
                    "BIOS is upgradeable", 
                    "BIOS shadowing is allowed", 
                    "Boot from CD is supported", 
                    "Selectable boot is supported", 
                    "BIOS ROM is socketed", 
                    "EDD is supported", 
                    "ACPI is supported", 
                    "BIOS boot specification is supported", 
                    "Targeted content distribution is supported", 
                    "UEFI is supported", 
                    "Manufacturing mode is supported", 
                    "Manufacturing mode is enabled"]
        for line in file:
            line = line.decode('utf-8').strip()

            if self.header_info(line):
                handle = self.header_info(line)["Handle"]
                smbios_data[handle] = {}
                smbios_data[handle]["Header"] = self.header_info(line)

            keywords = {
                "Version:": "Version", 
                "Release Date:": "Release Date"
            }

            for k, v in keywords.items():
                if line.startswith(k):
                    smbios_data[handle][v] = line.split(":", 1)[1].strip()

            if line.strip() in fm_chars:
                if "Firmware Characteristics" not in smbios_data[handle]:
                    smbios_data[handle]["Firmware Characteristics"] = []
                smbios_data[handle]["Firmware Characteristics"].append(line.strip())
        return smbios_data

    def parse_smbios_1 (self, file):
        smbios_data = {}
        for line in file:
            line = line.decode('utf-8').strip()

            if self.header_info(line):
                handle = self.header_info(line)["Handle"]
                smbios_data[handle] = {}
                smbios_data[handle]["Header"] = self.header_info(line)

            if line.startswith("Manufacturer:"):
                smbios_data[handle]["Manufacturer"] = line.split(":", 1)[1].strip()
            elif line.startswith("Product Name:"):
                smbios_data[handle]["Product Name"] = line.split(":", 1)[1].strip()
            elif line.startswith("UUID:"):
                smbios_data[handle]["UUID"] = line.split(":", 1)[1].strip()
            elif line.startswith("Wake-up Type:"):
                smbios_data[handle]["Wake-up Type"] = line.split(":", 1)[1].strip()
        return smbios_data

    def parse_smbios_3 (self, file):
        smbios_data = {}
        for line in file:
            line = line.decode('utf-8').strip()

            if self.header_info(line):
                handle = self.header_info(line)["Handle"]
                smbios_data[handle] = {}
                smbios_data[handle]["Header"] = self.header_info(line)

            if line.startswith("Manufacturer:"):
                smbios_data[handle]["Manufacturer"] = line.split(":", 1)[1].strip()
            elif line.startswith("Type:"):
                smbios_data[handle]["Type"] = line.split(":", 1)[1].strip()
        return smbios_data

    def parse_smbios_4 (self, file):
        smbios_data = {}
        for line in file:
            line = line.decode('utf-8').strip()

            if self.header_info(line):
                handle = self.header_info(line)["Handle"]
                smbios_data[handle] = {}
                smbios_data[handle]["Header"] = self.header_info(line)

            if line.startswith("Type:"):
                smbios_data[handle]["Type"] = line.split(":", 1)[1].strip()
            elif line.startswith("Socket Designation:"):
                smbios_data[handle]["Socket Designation"] = line.split(":", 1)[1].strip()
            elif line.startswith("Family:"):
                smbios_data[handle]["Family"] = line.split(":", 1)[1].strip()
            elif line.startswith("Manufacturer:"):
                smbios_data[handle]["Manufacture"] = line.split(":", 1)[1].strip()
            elif line.startswith("Max Speed:"):
                smbios_data[handle]["Max Speed"] = line.split(":", 1)[1].strip()
            elif line.startswith("Upgrade:"):
                smbios_data[handle]["Upgrade"] = line.split(":", 1)[1].strip()
            elif line.startswith("L1 Cache Handle:"):
                smbios_data[handle]["L1 Cache Handle"] = line.split(":", 1)[1].strip()
            elif line.startswith("L2 Cache Handle:"):
                smbios_data[handle]["L2 Cache Handle"] = line.split(":", 1)[1].strip()
            elif line.startswith("L3 Cache Handle:"):
                smbios_data[handle]["L3 Cache Handle"] = line.split(":", 1)[1].strip()
        return smbios_data

    def parse_smbios_7 (self, file):
        smbios_data = {}
        for line in file:
            line = line.decode('utf-8').strip()

            if self.header_info(line):
                handle = self.header_info(line)["Handle"]
                smbios_data[handle] = {}
                smbios_data[handle]["Header"] = self.header_info(line)

            if line.startswith("Socket Designation:"):
                smbios_data[handle]["Socket Designation"] = line.split(":", 1)[1].strip()
            elif line.startswith("Configuration:"):
                smbios_data[handle]["Configuration"] = line.split(":", 1)[1].strip()
            elif line.startswith("Operational Mode:"):
                smbios_data[handle]["Operational Mode"] = line.split(":", 1)[1].strip()
            elif line.startswith("Location:"):
                smbios_data[handle]["Location"] = line.split(":", 1)[1].strip()
        return smbios_data

    def parse_smbios_9 (self, file):
        smbios_data = {}
        slot_chars = ["3.3 V is provided", 
                      "PME signal is supported"]
        for line in file:
            line = line.decode('utf-8').strip()

            if self.header_info(line):
                handle = self.header_info(line)["Handle"]
                smbios_data[handle] = {}
                smbios_data[handle]["Header"] = self.header_info(line)

            if line.startswith("Designation:"):
                smbios_data[handle]["Designation"] = line.split(":", 1)[1].strip()
            elif line.startswith("Type:"):
                smbios_data[handle]["Type"] = line.split(":", 1)[1].strip()
            elif line.startswith("Data Bus Width:"):
                smbios_data[handle]["Data Bus Width"] = line.split(":", 1)[1].strip()
            elif line.startswith("Current Usage:"):
                smbios_data[handle]["Current Usage"] = line.split(":", 1)[1].strip()
            elif line.startswith("ID:"):
                smbios_data[handle]["ID"] = line.split(":", 1)[1].strip()
            elif line.strip() in slot_chars:
                if "Slot Characteristics" not in smbios_data[handle]:
                    smbios_data[handle]["Slot Characteristics"] = []
                smbios_data[handle]["Slot Characteristics"].append(line.strip())
        return smbios_data

    def parse_smbios_11 (self, file):
        smbios_data = {}
        for line in file:
            line = line.decode('utf-8').strip()

            if self.header_info(line):
                handle = self.header_info(line)["Handle"]
                smbios_data[handle] = {}
                smbios_data[handle]["Header"] = self.header_info(line)

            if line.startswith("String 4:"):
                smbios_data[handle]["String 4"] = line.split(":", 1)[1].strip()
        return smbios_data

    def parse_smbios_16 (self, file):
        smbios_data = {}
        for line in file:
            line = line.decode('utf-8').strip()

            if self.header_info(line):
                handle = self.header_info(line)["Handle"]
                smbios_data[handle] = {}
                smbios_data[handle]["Header"] = self.header_info(line)

            if line.startswith("Use:"):
                smbios_data[handle]["Use"] = line.split(":", 1)[1].strip()
            elif line.startswith("Location:"):
                smbios_data[handle]["Location"] = line.split(":", 1)[1].strip()
            elif line.startswith("Error Correction Type:"):
                smbios_data[handle]["Error Correction Type"] = line.split(":", 1)[1].strip()
            elif line.startswith("Maximum Capacity:"):
                smbios_data[handle]["Maximum Capacity"] = line.split(":", 1)[1].strip()
            elif line.startswith("Number Of Devices:"):
                smbios_data[handle]["Number Of Devices"] = line.split(":", 1)[1].strip()
        return smbios_data

    def parse_smbios_17 (self, file):
        smbios_data = {}
        for line in file:
            line = line.decode('utf-8').strip()

            if self.header_info(line):
                handle = self.header_info(line)["Handle"]
                smbios_data[handle] = {}
                smbios_data[handle]["Header"] = self.header_info(line)

            if line.startswith("Total Width:"):
                smbios_data[handle]["Total Width"] = line.split(":", 1)[1].strip()
            elif line.startswith("Data Width:"):
                smbios_data[handle]["Data Width"] = line.split(":", 1)[1].strip()
            elif line.startswith("Size:"):
                smbios_data[handle]["Size"] = line.split(":", 1)[1].strip()
            elif line.startswith("Form Factor:"):
                smbios_data[handle]["Form Factor"] = line.split(":", 1)[1].strip()
            elif line.startswith("Set:"):
                smbios_data[handle]["Set"] = line.split(":", 1)[1].strip()
            elif line.startswith("Locator:"):
                smbios_data[handle]["Locator"] = line.split(":", 1)[1].strip()
        return smbios_data

    def parse_smbios_19 (self, file):
        smbios_data = {}
        for line in file:
            line = line.decode('utf-8').strip()

            if self.header_info(line):
                handle = self.header_info(line)["Handle"]
                smbios_data[handle] = {}
                smbios_data[handle]["Header"] = self.header_info(line)

            if line.startswith("Starting Address:"):
                smbios_data[handle]["Starting Address"] = line.split(":", 1)[1].strip()
            elif line.startswith("Ending Address:"):
                smbios_data[handle]["Ending Address"] = line.split(":", 1)[1].strip()
            elif line.startswith("Partition Width:"):
                smbios_data[handle]["Partition Width"] = line.split(":", 1)[1].strip()
        return smbios_data

    def parse_smbios_32 (self, file):
        smbios_data = {}
        for line in file:
            line = line.decode('utf-8').strip()

            if self.header_info(line):
                handle = self.header_info(line)["Handle"]
                smbios_data[handle] = {}
                smbios_data[handle]["Header"] = self.header_info(line)

            if line.startswith("Status:"):
                smbios_data[handle]["Status"] = line.split(":", 1)[1].strip()
        return smbios_data

if __name__ == "__main__":
    tar_gz_path = TAR_GZ_PATH
    dmidecode = DmicodeParser(tar_gz_path)
    print(json.dumps(dmidecode.parser_dict, indent=4))

    with open(OUTPUT_JSON_PATH, 'w') as json_file:
        json.dump(dmidecode.parser_dict, json_file, indent=4)
