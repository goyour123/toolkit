#!/usr/bin/env python3

import subprocess
import json
import os
import argparse

if __name__ == '__main__':
    with open('machines.json', 'r') as j:
        config = json.load(j)

    parser = argparse.ArgumentParser()
    parser.add_argument('ipmi_args', type=str, nargs='+')
    args = parser.parse_args()

    script_name = os.path.splitext(os.path.basename(__file__))[0]

    ipmi_cmd = ['ipmitool', '-I', 'lanplus', '-H', config[script_name], '-U', 'admin', '-P', 'admin']
    ipmi_cmd.extend(args.ipmi_args)

    result = subprocess.run(ipmi_cmd, capture_output=True, text=True)
    print (result.stdout)
