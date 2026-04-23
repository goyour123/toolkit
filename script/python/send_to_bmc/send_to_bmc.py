import argparse
import subprocess
import json
import os

HOST_IP = ""
HOST_USER = ""
HOST_PASS = ""

if __name__ == "__main__":
    argParser = argparse.ArgumentParser()
    argParser.add_argument("--machine_name", type=str, required=True)
    argParser.add_argument("--file_path", type=str, required=True)
    args = argParser.parse_args()

    print(f"Retrieving information for machine: {args.machine_name}")
    cmd = f"sshpass -v -p {HOST_PASS} ssh -o StrictHostKeyChecking=no {HOST_USER}@{HOST_IP} jq -r '.{args.machine_name}' ~/lab_script/machines.json"
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, text=True)
    stdout, stderr = process.communicate()
    if process.returncode != 0:
        print(f"Failed to retrieve machine information. Error: {stderr}")
        exit(1)

    raw_output = stdout.strip().split('}')[0] + '}'
    machine_json_data = json.loads(raw_output)

    if os.path.splitext(args.file_path)[-1] != os.path.splitext(machine_json_data['bios_path'])[-1]:
        print(f"File type mismatch: {args.file_path} and {machine_json_data['bios_path']}")
        exit(1)

    print (f"Sending file to {args.machine_name} at {machine_json_data['ip']}...")
    dest_path = f"{machine_json_data['user']}@{machine_json_data['ip']}:{machine_json_data['bios_path']}"
    cmd = f"sshpass -p {machine_json_data['password']} scp -o StrictHostKeyChecking=no -P {machine_json_data['port']} {args.file_path} {dest_path}"
    print(f"Running command: {cmd}")
    process = subprocess.Popen(cmd)
    process.wait()
    if process.returncode == 0:
        print(f"File sent successfully to {args.machine_name}.")
    else:
        print(f"Failed to send file to {args.machine_name}.")
