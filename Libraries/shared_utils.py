import json
import time
import subprocess
from robot.api import logger
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
import device_manager
from  selenium.webdriver.common.by import  By
from  selenium.webdriver.support import  expected_conditions as EC
from  selenium.common.exceptions import  NoSuchElementException, StaleElementReferenceException, ElementNotInteractableException, ElementNotVisibleException
from error_handler_utils import auto_handle_appium_errors, for_each_device


def _init_config(file_name: str):
    """
    Returns: parsed configuration object from "config.json"
    """
    return json.loads(open(file_name).read())
file_path="C:\\New folder\\JIO__hotstar_apllication\\Jio_hot_start_IOS\\config.json"
config=_init_config(file_path)
print(f"the config is loded crtly    {config}")


def getconfig_device_class(device_name):
    device_name = device_name.split(":", 2)[0]
    print("Checking device class for:", device_name)
    print("Devices available:", list(config.get("devices", {}).keys()))

    if device_name in config["devices"]:
        return "devices"
    if "browsers" in config and device_name in config["browsers"]:
        return "browsers"



def sleep_with_msg(device, wait_seconds, why_message):
    """Sleep after emitting a message why"""
    if device:
        print(f"{device}: sleeping {wait_seconds}: {why_message}")
    else:
        print(f"Sleeping {wait_seconds}: {why_message}")

    time.sleep(wait_seconds)     

def appium_endpoint_suffix(device):
    # Get Appium version
    appium_current_version = subprocess.check_output("appium -v", shell=True).decode("utf-8").rstrip()
    
    # Convert major version to integer
    major_version = int(appium_current_version.split(".")[0])
    
    # Set endpointSuffix based on Appium version
    if major_version < 2:
        endpoint_suffix = "/wd/hub"
    else:
        endpoint_suffix = ""  # For Appium 2.x
    
    print(f"{device}: Appium version: {appium_current_version}, endpointSuffix: {endpoint_suffix}")
    return endpoint_suffix



def decode_device_specifier(device):
    """
    This method decodes a 'device' specifier.
    Any device specifier can be encoded as '[device name]:[account type]'.
    If not specified, the default account type is 'user'.
    It returns device name and account type.
    """
    if type(device) != str:
        raise AssertionError(f"'{device}' is not a str type")

    _pieces = device.split(":", 2)

    device_name = _pieces[0]

    if len(_pieces) > 1:
        account_type = _pieces[1]
    else:
        account_type = "user"

    # Sanity checks, test for KeyError:
    devices = getconfig_device_class(device_name)

    if device_name not in config[devices]:
        raise ValueError(f"Config error: referenced device: '{device_name}' in not defined")
    if account_type not in config[devices][device_name]:
        raise ValueError(f"Config error: device '{device_name}' has no '{account_type}' defined")

    return device_name, account_type

def get_configured_device_property(device, propname):
    device_name, _ = decode_device_specifier(device)
    devices = getconfig_device_class(device_name)

    if propname not in config[devices][device_name]:
        raise ValueError(f"{device_name}: Config has no '{propname}' defined  for '{devices}/{device_name}'")

    return config[devices][device_name][propname]

def get_top_level_device_port(device):
    device_name = device.split(":", 1)[0]  # remove account_type suffix
    devices_dict = config.get("devices", {})
    device_config = devices_dict.get(device_name)
    
    print("Device config (top-level):", device_config)  # debug

    if not device_config:
        raise ValueError(f"Device '{device_name}' not found in config['devices']")

    port = device_config.get("port")
    if not port or port == "-":
        raise ValueError(f"Top-level 'port' missing or invalid for '{device_name}'")

    return port

def take_screenshot_on_error(device_name, message):
    """Take screenshot for a specific device."""
    driver=device_manager.get_driver(device_name)
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    screenshot_name = f"screenshot_{device_name}_{timestamp}.png"
    screenshot_path = os.path.join(os.getcwd(), screenshot_name)

    if driver:
        driver.save_screenshot(screenshot_path)
        logger.error(message)
        logger.info(
            f'<a href="{screenshot_name}"><img src="{screenshot_name}" width="800px"></a>',
            html=True
        )
    else:
        logger.error(f"Driver for {device_name} not initialized, cannot take screenshot.")


@auto_handle_appium_errors()
def find_element(devices,locator_dict, locator_key,  timeout=10 , single_elemnt=True):
    devices=[]
    if isinstance(devices, str):
        devices=[devices]
    for device in devices:
        name_device=getconfig_device_class(device)
        driver=device_manager.get_driver(device)
        if name_device=="devices":   # it choice the appium
            by_map = {

                "xpath": AppiumBy.XPATH,
                "id": AppiumBy.ACCESSIBILITY_ID,
                "class_name": AppiumBy.CLASS_NAME,
                "android_ui_automator": AppiumBy.ANDROID_UIAUTOMATOR
            }
        else:  # Web driver
            by_map = {
                "id": By.ID,
                "xpath": By.XPATH,
                "text": By.LINK_TEXT,
            }
        locator_all_keypairs = locator_dict[locator_key]
        for loc_type, loc_value in locator_all_keypairs.items():
            by = by_map.get(loc_type.lower())
            if by and single_element:
                try:
                    return WebDriverWait(driver, timeout).until(
                        EC.presence_of_element_located((by, loc_value))
                    )
                except Exception:
                    take_screenshot_on_error(device, "failure because elemnt not found")
                    continue
            elif single_elemnt==False:
                if by:
                    try:
                        return  WebDriverWait(driver, timeout).until(
                        EC.presence_of_all_elements_located((by, loc_value)))
                    except Exception as e:
                        raise  print(f"the list weblemnts {e}")

        take_screenshot_on_error(device, f"Element '{locator_key}' not found after {timeout}s")
        raise Exception(f"Element '{locator_key}' not found")


def find_elements(devices,locator_dict, locator_key,  timeout=10,single_elemnt=False):
    return  find_element(devices,locator_dict,  locator_key,  timeout=10, single_elemnt=False)


def load_loctors(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return json.loads(f.read())

def click_if_visible(devices, locator_dict, locator_key):
    if isinstance(devices , str):
        _devices=[devices]
        for device in _devices:
            try:
                print("here trying to wrraping up the device findelemnt")
                _element=find_element(devices, locator_dict, locator_key, timeout=10, single_elemnt=True)
                if _element and _element.is_displayed():
                    _element.click()
                else:
                    print(f"️ Element '{_element}' is not visible on {device}")
            except ElementNotVisibleException as e:
                raise  print(f" the click the visible of the elemnt {device} is  {e}")


