import json
import time
import subprocess

def _init_config(file_name: str):
    """
    Returns: parsed configuration object from "config.json"
    """
    return json.loads(open(file_name).read())

config=_init_config("config.json")
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
