import device_manager
from appium.webdriver.common.appiumby import AppiumBy
import time

def launch_jio_hotstar_application(device):
    """
    Launches the Jio Hotstar (Disney+ Hotstar) app on the given connected device
    using the driver instance managed by device_manager.
    """

    # Get driver from device manager
    driver = device_manager.get_driver(device)

    print(f"Launching Jio Hotstar app on {device}...")

    # Optional: Wait for app to fully load
    time.sleep(5)

    try:
        # Verify app is launched by checking for a key UI element
        # (Example: The "Search" or "Home" icon — update locator as per your app)
        home_element = driver.find_element(AppiumBy.ACCESSIBILITY_ID, "Home")

        if home_element.is_displayed():
            print("✅ Jio Hotstar app launched successfully.")
        else:
            print("⚠️ App launched, but home element not visible yet.")

    except Exception as e:
        print(f"❌ Failed to verify app launch: {e}")

    return driver


if __name__ == "__main__":
    launch_jio_hotstar_application("device_1")