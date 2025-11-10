
import device_manager
from appium.webdriver.common.appiumby import AppiumBy
import time
import  shared_utils
import device_control
from Libraries.shared_utils import sleep_with_msg

home_page_dict=shared_utils.load_loctors("C:\\New folder\\JIO__hotstar_apllication\\Jio_hot_start_IOS\\Resource\\page_object\\Home_page.json")


def clear_cache_before_launch(func):
    def wrapper(device, *args, **kwargs):
        device_control.clear_cache_the_app(device)  # clear cache first
        # this fun (launch_jio_hotstar_application) run over here
        return func(device, *args, **kwargs)
    return wrapper

@clear_cache_before_launch
def launch_jio_hotstar_application(device):
    """
    Launches the Jio Hotstar (Disney+ Hotstar) app on the given connected device
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
    try:
        webelement = shared_utils.find_element(device, home_page_dict, "continue")
        webelement.click()
        sleep_with_msg(device, 20, "Continue button clicked — waiting for Sign-In page to load")
    except Exception as e:
        print(f"[{device}] Error while clicking 'Continue' button: {str(e)}")

def select_required_ott_languages(device):
    try:
        # Select Hindi
        shared_utils.click_if_visible(device, home_page_dict, "hind_language")

        # Select Kannada
        shared_utils.click_if_visible(device, home_page_dict, "kannada_language_select")

        # Click Continue button
        shared_utils.click_if_visible(device, home_page_dict, "continue_button")

        # Verify Home menu is visible
        element_visible = shared_utils.find_element(device, home_page_dict, "verify_bottom_menu_home")

        if element_visible and element_visible.is_displayed():
            print("✅ Language selection successful and Home screen visible.")
            return True
        else:
            raise Exception("❌ Home screen not visible after language selection.")

    except Exception as e:
        print(f"⚠️ Error in select_required_ott_languages: {str(e)}")
        raise


if __name__ == "__main__":
    launch_jio_hotstar_application("device_1")
    click_continue_and_sigin_to_device("device_1")
    select_required_ott_languages("device_1")