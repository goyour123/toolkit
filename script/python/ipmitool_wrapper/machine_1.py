#!/usr/bin/env python3

import subprocess
import json
import os, sys

if __name__ == '__main__':
    with open('machines.json', 'r') as j:
        config = json.load(j)

    script_name = os.path.splitext(os.path.basename(__file__))[0]

    ipmi_cmd = ['ipmitool', '-I', 'lanplus', '-H', config[script_name], '-U', 'admin', '-P', 'admin']
    ipmi_cmd.extend(sys.argv[1:])

    result = subprocess.run(ipmi_cmd, capture_output=True, text=True)
    print (result.stdout)
