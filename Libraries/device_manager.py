from threading import Lock
import time
from selenium.webdriver.chrome.options import Options as ChromeOptions
from robot.libraries.BuiltIn import BuiltIn
import os
import subprocess
from Libraries import device_control
from Libraries import shared_utils
import requests
from selenium import webdriver as chrome_webdriver

from appium import webdriver


_logdir_create_lock = Lock()


class DriverManger:
    _driver_store = {}

    @staticmethod
    # ex: pass deviec_1 :user_allaccess
    def initiate_driver(device):
        # the device_1 or browser it will choice
        device_class = shared_utils.getconfig_device_class(device)

        if device_class == "browsers":
            chrome_options = ChromeOptions()
            # Always use incognito/maximized modes:
            chrome_options.add_argument("--incognito")
            chrome_options.add_argument("--start-maximized")

            # No, occasionally leaves "chrome.exe" instances running - blocks pipeline ('logfile in use').
            #   We want all 'chrome.exe' instances to be torn down when the sandbox is torn down:
            #   chrome_options.add_argument("--no-sandbox")

            chrome_options.add_argument("--disable-notifications")
            chrome_options.add_argument("--disable-media-stream")

            prefs = {
                "profile.default_content_setting_values.media_stream_camera": 2,  # using 2 for blocking camera ,Allow camera 1 is not working
                "profile.default_content_setting_values.media_stream_mic": 2,  # Block microphone
                "profile.default_content_setting_values.notifications": 2,  # Block notifications
            }
            chrome_options.add_experimental_option("prefs", prefs)

            # Always capture cromedriver logs, similar to 'appium_logs':
            _logdir = os.path.join(
                BuiltIn().get_variable_value("${OUTPUT DIR}"), "chrome_logs"
            )

            with _logdir_create_lock:
                # directory must exist:
                if not os.path.exists(_logdir):
                    os.makedirs(_logdir)

            # Generate a filename based on the current time
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            _log_file = os.path.join(_logdir, f"{device}_{timestamp}.log")

            # Add, with 'verbose':
            chrome_options.add_argument("--verbose")
            chrome_options.add_argument(f"--log-file={_log_file}")
            print(f"{device}: Chromedriver logging to: {_log_file}")

            # `chrome_webdriver` is the `selenium.webdriver` module alias;
            # instantiate the Chrome WebDriver via its `Chrome` class.
            driver = chrome_webdriver.Chrome(options=chrome_options)

            # The parent directory of 'chromedriver.exe' will suffice for determining the chromedriver version:
            print(f"driver.service.path={driver.service.path}")

        elif device_class == "devices":
            # Load common desired capabilities
            dict_caps_values = shared_utils.config["common_desired_caps"]
            endpoint = shared_utils.appium_endpoint_suffix(device=device_class)

            # You can also merge device-specific caps if needed:
            # dict_caps_values.update(shared_utils.getconfig_device_caps(device))

            print(
                f"Setting up Appium driver for {device} with caps: {dict_caps_values}"
            )
            # port=shared_utils.get_top_level_device_port(device)
            port = shared_utils.config[device_class][device]["port"]

            # Construct Appium server URL
            appium_url = f"http://127.0.0.1:{port}{endpoint}"

            # check_port_running_request_status(appium_process, appium_url, port)

            print(f"Connecting to Appium server at: {appium_url}")

            # Create the Appium WebDriver session
            driver = webdriver.Remote(
                command_executor=appium_url, desired_capabilities=dict_caps_values
            )

            print(f"Driver session started for {device}")
        DriverManger._driver_store[device] = driver
        """
        inside the driver actually store like
        _driver_store={
                    "device_1": <driver_adress>,
                    "device_2": <driver_adress>
                    "browser": <driver>
        }

        """

        return driver


@staticmethod
def get_driver(device=None):
    """
    if only one device is initilized the automatically take the driver and make sure all device is manule make the setup are avilable online

    """
    device_control.collect_and_perform_the_device_status()
    if len(DriverManger._driver_store) == 0:
        """
        driver is not intilized intilize first then take the values"""
        DriverManger.initiate_driver(device)
    if device is not None:
        driver_value = DriverManger._driver_store.get(device)
        return driver_value
    # if it is single deviec using
    if len(DriverManger._driver_store) < 1:
        default_driver_present_single = list(DriverManger._driver_store.values())[0]
        return default_driver_present_single
    raise Exception("Multiple drivers exist; specify device name.")


def lanuch_browser(device):
    _device = []
    if isinstance(device, str):  # the value of the string or what it will check
        _device = [device]
        # using the multipal device in
    for device in _device:
        DriverManger.initiate_driver(device)
        try:
            # Use explicit indexing since config is a dict loaded from JSON.
            # This will raise KeyError for missing keys which we catch to provide
            # a clear error message instead of silently proceeding with None.
            lanuching_website = shared_utils.config["browsers"]["web_site"]
        except KeyError:
            raise RuntimeError(
                "Browser launch URL not configured at config['browsers']['web_site']"
            )

        driver = DriverManger._driver_store.get(device)
        if driver is None:
            raise RuntimeError(
                f"No driver available for device '{device}' after initiate_driver"
            )

        try:
            driver.get(lanuching_website)
            print(f"the browser is launched by device={device}")
        except Exception as e:
            raise RuntimeError(
                f"Failed to open URL '{lanuching_website}' on device={device}: {e}"
            )


@staticmethod
def tear_down_driver(device=None):
    """
    driver quit all and based on specific device
    """

    if device is not None:
        driver = DriverManger._driver_store.pop(device)
        if driver:
            try:
                driver.quit()
                print(f"{device}:  Driver closed successfully.")
            except Exception as e:
                print(f"{device}:  Error closing driver: {e}")
        else:
            print(f"{device}: No active driver found to close.")
    # not specify any driver
    else:
        # close all driver
        for device_name, driver in DriverManger._driver_store.items():
            if driver:
                try:
                    driver.quit()
                    print(f"{device}:  Driver closed successfully.")
                except Exception as e:
                    print(f"{device}:  Error closing driver: {e}")
            else:
                print(f"{device}: No active driver found to close.")


def get_existing_driver(device):
    return DriverManger._driver_store.get(device)
