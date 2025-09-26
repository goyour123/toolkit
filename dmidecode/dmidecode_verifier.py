import tarfile
import os
import json
import re

class DmicodeParser:
    def __init__(self, tar_gz_path, smbios_parser_cfg):
        self.parser_dict = {}
        self.smbios_parser_cfg = smbios_parser_cfg
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
    script_name = os.path.splitext(os.path.basename(script_path))[0]
    json_path = os.path.join(script_dir, f"{script_name}.json")
    with open(json_path, 'r') as json_file:
        config = json.load(json_file)

    tar_gz_path = os.path.join(script_dir, config["tar_gz_path"])
    smbios_parser_cfg = config["smbios_parser_cfg"]
    dmidecode = DmicodeParser(tar_gz_path=tar_gz_path, smbios_parser_cfg=smbios_parser_cfg)
    print(json.dumps(dmidecode.parser_dict, indent=4))

    output_json_path = os.path.join(script_dir, config["output_json_path"])
    with open(output_json_path, 'w') as json_file:
        json.dump(dmidecode.parser_dict, json_file, indent=4)
