import tarfile
import os
import json
import re

TAR_GZ_PATH = "OUTPUT.tar.gz"
OUTPUT_JSON_PATH = "dmidecode_output.json"

SMBIOS_PARSER_CFG = {
    "smbios_type_0": {
        "keywords": {
            "Version:": "Version", 
            "Release Date:": "Release Date"
        },
        "features": {
            "Firmware Characteristics": [ 
                "PCI is supported", 
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
                "Manufacturing mode is enabled"
            ]
        }
    },
    "smbios_type_1": {
        "keywords": {
            "Manufacturer:": "Manufacturer", 
            "Product Name:": "Product Name", 
            "UUID:": "UUID", 
            "Wake-up Type:": "Wake-up Type"
        }
    },
    "smbios_type_3": {
        "keywords": {
            "Manufacturer:": "Manufacturer",
            "Type:": "Type"
        }
    },
    "smbios_type_4": {
        "keywords": {
            "Socket Designation:": "Socket Designation",
            "Type:": "Type",
            "Family:": "Family",
            "Manufacturer:": "Manufacture",
            "Max Speed:": "Max Speed",
            "Upgrade:": "Upgrade",
            "L1 Cache Handle:": "L1 Cache Handle",
            "L2 Cache Handle:": "L2 Cache Handle",
            "L3 Cache Handle:": "L3 Cache Handle"
        }
    },
    "smbios_type_7": {
        "keywords": {
            "Socket Designation:": "Socket Designation",
            "Configuration:": "Configuration",
            "Operational Mode:": "Operational Mode",
            "Location:": "Location"
        }
    },
    "smbios_type_9": {
        "keywords": {
            "Designation:": "Designation",
            "Type:": "Type",
            "Data Bus Width:": "Data Bus Width",
            "Current Usage:": "Current Usage",
            "ID:": "ID"
        },
        "features": {
            "Slot Characteristics": [
                "3.3 V is provided", 
                "PME signal is supported"
            ]
        }
    },
    "smbios_type_11": {
        "keywords": {
            "String 4:": "String 4"
        }
    },
    "smbios_type_16": {
        "keywords": {
            "Use:": "Use",
            "Location:": "Location",
            "Error Correction Type:": "Error Correction Type",
            "Maximum Capacity:": "Maximum Capacity",
            "Number Of Devices:": "Number Of Devices"
        }
    },
    "smbios_type_17": {
        "keywords": {
            "Total Width:": "Total Width",
            "Data Width:": "Data Width",
            "Size:": "Size",
            "Form Factor:": "Form Factor",
            "Set:": "Set",
            "Locator:": "Locator"
        }
    },
    "smbios_type_19": {
        "keywords": {
            "Starting Address:": "Starting Address",
            "Ending Address:": "Ending Address",
            "Partition Width:": "Partition Width"
        }
    },
    "smbios_type_32": {
        "keywords": {
            "Status:": "Status"
        }
    }
}

class DmicodeParser:
    def __init__(self, tar_gz_path):
        self.parser_dict = {}
        self.smbios_parser_cfg = SMBIOS_PARSER_CFG
        with tarfile.open(tar_gz_path, 'r:gz') as tar:
            for file in tar.getnames():
                if not file.endswith('.txt'):
                    continue
                file_name = os.path.basename(file).split('.')[0]
                if file_name not in self.smbios_parser_cfg:
                    continue
                with tar.extractfile(file) as f:
                    self.parser_dict[file_name] = self.parse_smbios(f, file_name)

    def header_info(self, line):
        match = re.search(r'Handle\s(\S+),\sDMI\stype\s(\S+),\s(\d+)\sbytes', line)
        if match:
            return {
                "Handle": match.group(1),
                #"DMI Type": match.group(2),
                "Size (bytes)": match.group(3)
            }
        return None

    def parse_smbios(self, file, smbios_type):
        smbios_data = {}

        for line in file:
            line = line.decode('utf-8').strip()

            if self.header_info(line):
                handle = self.header_info(line)["Handle"]
                smbios_data[handle] = {}
                smbios_data[handle]["Header"] = self.header_info(line)

            for k, v in self.smbios_parser_cfg[smbios_type]["keywords"].items():
                if line.startswith(k):
                    smbios_data[handle][v] = line.split(":", 1)[1].strip()
            for feature, values in self.smbios_parser_cfg[smbios_type].get("features", {}).items():
                if line.strip() in values:
                    if feature not in smbios_data[handle]:
                        smbios_data[handle][feature] = []
                    smbios_data[handle][feature].append(line.strip())
        return smbios_data

if __name__ == "__main__":
    script_path = os.path.abspath(__file__)
    script_dir = os.path.dirname(script_path)
    tar_gz_path = os.path.join(script_dir, TAR_GZ_PATH)
    dmidecode = DmicodeParser(tar_gz_path)
    print(json.dumps(dmidecode.parser_dict, indent=4))

    output_json_path = os.path.join(script_dir, OUTPUT_JSON_PATH)
    with open(output_json_path, 'w') as json_file:
        json.dump(dmidecode.parser_dict, json_file, indent=4)
