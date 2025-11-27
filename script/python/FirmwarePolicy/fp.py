from edk2toollib.windows.policy.firmware_policy import FirmwarePolicy
import json

policy = FirmwarePolicy()

with open('fp.json', 'r') as f:
    json_data = json.load(f)

device_target = json_data['DeviceTarget']
device_target['Nonce'] = int(device_target['Nonce'], 16)

policy.SetDeviceTarget(device_target)

device_policy = int(json_data['DevicePolicy'], 16)
policy.SetDevicePolicy(device_policy)

with open('Policy.bin', 'wb') as f:
    policy.SerializeToStream(stream=f)