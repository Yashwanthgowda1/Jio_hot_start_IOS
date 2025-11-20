import time
import json
from functools import wraps
from appium.webdriver.common.appiumby import AppiumBy
from selenium.common.exceptions import (
    InvalidSessionIdException,
    NoSuchElementException,
    ElementNotVisibleException
)

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# ---------------- UNIVERSAL DECORATORS ---------------- #

def auto_handle_appium_errors(retry_count=3, retry_delay=3):
    """
    Auto-handles common Appium errors such as:
    - Session expired
    - Element not found
    - Element not ready (NoneType errors)
    """

    def decorator(func):
        @wraps(func)
        def wrapper(device, *args, **kwargs):

            for attempt in range(1, retry_count + 1):
                try:
                    return func(device, *args, **kwargs)

                except InvalidSessionIdException:
                    print(f"[{device}] ⚠ Session expired. Restarting driver...")
                    # Device class handles restart → FIXES circular import
                    device.restart_driver()
                    time.sleep(retry_delay)

                except NoSuchElementException:
                    print(f"[{device}] ⚠ Element not found. Retrying ({attempt}/{retry_count})...")
                    time.sleep(retry_delay)

                except AttributeError as ae:
                    if "'NoneType' object has no attribute" in str(ae):
                        print(f"[{device}] ⚠ Element not ready yet. Retrying ({attempt}/{retry_count})...")
                        time.sleep(retry_delay)
                    else:
                        raise

                except Exception as e:
                    print(f"[{device}] ❌ Unexpected error in {func.__name__}: {e}")
                    break

            print(f"[{device}] ❌ Failed after {retry_count} retries in {func.__name__}")
            return None

        return wrapper
    return decorator


def for_each_device(func):
    """
    Runs a function independently for each device.
    """
    @wraps(func)
    def wrapper(devices, *args, **kwargs):
        if isinstance(devices, str):
            devices = [devices]
        results = []
        for device in devices:
            result = func(device, *args, **kwargs)
            results.append(result)
        return results
    return wrapper


from Libraries.device_manager import DriverManger, tear_down_driver

def restart_driver(device_id):
    print(f"[{device_id}] Restarting driver session...")
    tear_down_driver(device_id)
    DriverManger.initiate_driver(device_id)
    print(f"[{device_id}] Driver restarted successfully.")
