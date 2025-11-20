import json
import time
import subprocess
import os


from robot.api import logger
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import (
    NoSuchElementException, StaleElementReferenceException,
    ElementNotInteractableException, ElementNotVisibleException
)
from Libraries import device_manager
from Libraries.error_handler_utils import auto_handle_appium_errors, for_each_device


# ---------------- CONFIG ---------------- #

def _init_config(file_name: str):
    """Load config.json"""
    with open(file_name, "r") as f:
        return json.load(f)

file_path = r"C:\python_study\Jio_hot_start_IOS\config.json"
config = _init_config(file_path)
print(f"Config loaded: {config}")


def getconfig_device_class(device_name):
    """Return whether config belongs to devices or browsers"""
    device_name = device_name.split(":", 1)[0]

    if "devices" in config and device_name in config["devices"]:
        return "devices"
    if "browsers" in config and device_name in config["browsers"]:
        return "browsers"

    raise ValueError(f"{device_name}: Not found under devices or browsers")


# ---------------- HELPERS ---------------- #

def sleep_with_msg(device, wait_seconds, why_message):
    msg = f"{device}: " if device else ""
    print(f"{msg}Sleeping {wait_seconds}s: {why_message}")
    time.sleep(wait_seconds)


def appium_endpoint_suffix(device):
    version = subprocess.check_output("appium -v", shell=True).decode().strip()
    major = int(version.split(".")[0])
    suffix = "" if major >= 2 else "/wd/hub"
    print(f"{device}: Appium version {version}, endpointSuffix={suffix}")
    return suffix


def decode_device_specifier(device):
    if not isinstance(device, str):
        raise AssertionError("Device specifier must be string")

    pieces = device.split(":", 1)
    device_name = pieces[0]
    account_type = pieces[1] if len(pieces) > 1 else "user"

    device_class = getconfig_device_class(device_name)

    if device_name not in config[device_class]:
        raise ValueError(f"{device_name} not in config")

    if account_type not in config[device_class][device_name]:
        raise ValueError(f"{device_name} has no account type {account_type}")

    return device_name, account_type


def get_configured_device_property(device, propname):
    device_name, _ = decode_device_specifier(device)
    device_class = getconfig_device_class(device_name)

    if propname not in config[device_class][device_name]:
        raise ValueError(f"{device_name} missing property {propname}")

    return config[device_class][device_name][propname]


def get_top_level_device_port(device):
    device_name = device.split(":", 1)[0]

    device_data = config.get("devices", {}).get(device_name)
    if not device_data:
        raise ValueError(f"{device_name} not in config devices")

    port = device_data.get("port")
    if not port or port == "-":
        raise ValueError(f"{device_name}: Invalid port")

    return port

def take_screenshot(driver, device_name, base_log_dir):
    timestamp = time.strftime("%Y%m%d_%H%M%S")

    # Make device-specific screenshot folder
    screenshot_dir = os.path.join(base_log_dir, device_name)
    os.makedirs(screenshot_dir, exist_ok=True)

    # File Path
    file_path = os.path.join(screenshot_dir, f"screenshot_{timestamp}.png")

    # Capture
    driver.get_screenshot_as_file(file_path)

    return file_path

# ---------------- LOCATOR METHODS ---------------- #

@auto_handle_appium_errors()
def find_element(device, locator_dict, locator_key, timeout=10, single_element=True):

    # Convert single device → list
    devices = [device] if isinstance(device, str) else device

    for dev in devices:

        # --------------------------------------
        # 1️⃣ Ensure driver exists
        # --------------------------------------
        driver = device_manager.get_existing_driver(dev)

        if driver is None:
            print(f"[{dev}] ⚠ Driver not initialized — starting...")
            driver = device_manager.DriverManger.initiate_driver(dev)
            sleep_with_msg(dev, 5, "Waiting after driver start")

        # --------------------------------------
        # 2️⃣ Determine locator type map
        # --------------------------------------
        device_type = getconfig_device_class(dev)

        if device_type == "devices":  # Appium
            by_map = {
                "xpath": AppiumBy.XPATH,
                "id": AppiumBy.ACCESSIBILITY_ID,
                "class_name": AppiumBy.CLASS_NAME,
                "android_ui_automator": AppiumBy.ANDROID_UIAUTOMATOR
            }
        else:  # Browser
            by_map = {
                "id": By.ID,
                "xpath": By.XPATH,
                "text": By.LINK_TEXT
            }

        locators = locator_dict[locator_key]

        # --------------------------------------
        # 3️⃣ Try each locator until success
        # --------------------------------------
        for loc_type, loc_value in locators.items():
            by = by_map.get(loc_type.lower())
            if not by:
                continue

            try:
                if single_element:
                    elem = WebDriverWait(driver, timeout).until(
                        EC.presence_of_element_located((by, loc_value))
                    )
                else:
                    elem = WebDriverWait(driver, timeout).until(
                        EC.presence_of_all_elements_located((by, loc_value))
                    )

                # SUCCESS
                print(f"[{dev}] ✅ Element found: {locator_key}")
                return elem

            except Exception:
                print(f"[{dev}] ❌ Locator failed: {locator_key} → trying next")
                take_screenshot(driver, dev, f"{locator_key}_not_found")

        # --------------------------------------
        # 4️⃣ All locators failed → raise
        # --------------------------------------
        raise Exception(f"[{dev}] ❌ Element '{locator_key}' NOT FOUND")


def find_elements(devices, locator_dict, locator_key, timeout=10):
    return find_element(devices, locator_dict, locator_key, timeout, single_element=False)


def load_loctors(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def click_if_visible(devices, locator_dict, locator_key):
    if isinstance(devices, str):
        devices = [devices]

    for device in devices:
        try:
            elem = find_element(device, locator_dict, locator_key, timeout=10)
            if elem.is_displayed():
                elem.click()
                print(f"Clicked '{locator_key}' on {device}")
            else:
                return
        except Exception as e:
            print(f"Click failed for {device}: {e}")
            raise


def swipe_up(device):
    driver = device_manager.get_existing_driver(device)
    size = driver.get_window_size()
    width, height = size["width"], size["height"]

    if height > width:   # Portrait
        driver.swipe(width/2, 4*(height/5), width/2, height/5)
    else:                # Landscape
        driver.swipe(width/4, 4*(height/5), width/4, height/5)

def swipe_multiple(device, count=3):
    for _ in range(count):
        swipe_up(device)

def swipe_till_end(device):
    driver = device_manager.get_existing_driver(device)

    last_page = ""
    same_count = 0

    while True:
        # Take page source before swipe
        page_before = driver.page_source

        # Swipe once
        swipe_up(device)

        time.sleep(1)

        # Take page source after swipe
        page_after = driver.page_source

        # If page did not change → end reached
        if page_before == page_after:
            same_count += 1
        else:
            same_count = 0

        if same_count >= 2:  # two same results = no more scrolling
            print(f"{device}: Reached end of page.")
            break


