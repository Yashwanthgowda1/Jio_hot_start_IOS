import subprocess
import os
import time


def get_adb_devices_uudi():
    '''
    This function is help full to take the device if present in the terminal
    '''
    try:
        devices=[]
        result_list=subprocess.run(["adb", "devices"], capture_output=True, text=True)
        lines=result_list.stdout.strip().splitlines()[1:]   # stat from 2nd lines skkip the starting
        for line in lines:
            if "device" in line:
                devices.append(line.split()[0])
        return devices

    except Exception as e:
        raise (f" Erro is occure during the list of device collect {e}")
        return []

def check_device_is_onine(uuid):
    '''
    this function help to known the device is acutall in online or getting ofline 
    '''
    cmd=["adb", "-s",uuid,"get-state"]
    status=subprocess.run(cmd, capture_output=True, text=True)
    if "device" in status.stdout:
        print(f"[Sucess] Device {uuid} is [online]")
        return True
    print(f"[ERROR] Device {uuid} is in [Offline]")
    return False

def collect_and_perform_the_device_status():
    devices=get_adb_devices_uudi()
    print("\nConnected devices:")
    # enumarter return index and key not value
    for i, dev in enumerate(devices):
        print(f"{i}. {dev}")
        check_device_is_onine(dev)
    
if __name__ == "__main__":
    collect_and_perform_the_device_status()
