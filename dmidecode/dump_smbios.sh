#!/bin/bash
TARGET_PATH="."
TARGET_DIR="OUTPUT"
mkdir -p "$TARGET_PATH/$TARGET_DIR"

echo "Dump SMBIOS files..."
sudo ./dmidecode -t 0  > "$TARGET_PATH/$TARGET_DIR/smbios_type_0.txt"
sudo ./dmidecode -t 1  > "$TARGET_PATH/$TARGET_DIR/smbios_type_1.txt"
sudo ./dmidecode -t 3  > "$TARGET_PATH/$TARGET_DIR/smbios_type_3.txt"
sudo ./dmidecode -t 4  > "$TARGET_PATH/$TARGET_DIR/smbios_type_4.txt"
sudo ./dmidecode -t 7  > "$TARGET_PATH/$TARGET_DIR/smbios_type_7.txt"
sudo ./dmidecode -t 9  > "$TARGET_PATH/$TARGET_DIR/smbios_type_9.txt"
sudo ./dmidecode -t 11 > "$TARGET_PATH/$TARGET_DIR/smbios_type_11.txt"
sudo ./dmidecode -t 16 > "$TARGET_PATH/$TARGET_DIR/smbios_type_16.txt"
sudo ./dmidecode -t 17 > "$TARGET_PATH/$TARGET_DIR/smbios_type_17.txt"
sudo ./dmidecode -t 19 > "$TARGET_PATH/$TARGET_DIR/smbios_type_19.txt"
sudo ./dmidecode -t 32 > "$TARGET_PATH/$TARGET_DIR/smbios_type_32.txt"

echo "Pack SMBIOS dump files..."
tar zcvf $TARGET_DIR.tar.gz $TARGET_DIR

