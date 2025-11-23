import subprocess
import os
import time
from Libraries import shared_utils
from appium.webdriver.common.appiumby import AppiumBy

from Libraries import device_manager
from Libraries.shared_utils import sleep_with_msg

def clear_cache_the_app(devices):
    _devices=[]
    if isinstance(devices, str):
        _devices = [devices]
    result_devices_connected=subprocess.run(["adb", "devices"],capture_output= True, text=True)
    '''

    :param device: this function help to clear cahce the apk adb shell pm clear <apknane?>
    :return:
    '''
    result_eache_row=result_devices_connected.stdout.strip().splitlines()[1:]  # need the all the deatils expect the fisrt row
    apppackage = shared_utils.config['common_desired_caps']['appPackage']
    if apppackage is None:
        raise  Exception("the apppacking is not found by the cofigfile recheck")
    for device in range(len(_devices)):
        try:
            # Run adb command for that specific device
            print(f" before clear cahing checking the device existing { result_eache_row[device].split()[0]}")
            result = subprocess.run(
                ["adb", "-s", result_eache_row[device].split()[0], "shell", "pm", "clear", apppackage],
                capture_output=True,
                text=True,
                timeout=15
            )

            # Check if success
            if "Success" in result.stdout:
                print(f" Cache cleared successfully on {device}")
            else:
                print(f" Failed to clear cache on {device}: {result.stdout or result.stderr}")

        except subprocess.TimeoutExpired:
            print(f"Timeout while clearing cache on {device}")
        except Exception as e:
            print(f" Error clearing cache on {device}: {str(e)}")

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


def launch_jio_hotstar_application(device):
    """
    Launches the Jio Hotstar (Disney + Hotstar) app on the given connected device
    using the driver instance managed by device_manager.

    """

    # Get driver from device manager
    driver = device_manager.get_driver(device)

    print(f"Launching Jio Hotstar app on {device}...")

    # Optional: Wait for app to fully load
    sleep_with_msg(device, 30, "waiting to load the driver application")

    try:
        # Verify app is launched by checking for a key UI element
        # (Example: The "Search" or "Home" icon — update locator as per your app)
        home_element = driver.find_element(AppiumBy.XPATH, "//android.widget.Button[@content-desc='Continue']")

        if home_element.is_displayed():
            print("✅ Jio Hotstar app launched successfully.")
        else:
            print("⚠️ App launched, but home element not visible yet.")

    except Exception as e:
        print(f"❌ Failed to verify app launch: {e}")

    return driver


def click_continue_and_sigin_to_device(device):
    driver = device_manager.get_driver(device)
    webelemnt=driver.find_element(AppiumBy.XPATH, "//android.widget.Button[@content-desc='Continue']")
    webelemnt.click()
    sleep_with_msg(device, 20, "continue the application and waiting to singin pages")


    





