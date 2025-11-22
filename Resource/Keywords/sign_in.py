from appium.webdriver.common.appiumby import AppiumBy
import time

from Libraries import shared_utils
from Libraries import device_control
from Libraries import device_manager

home_page_dict = shared_utils.load_loctors("Resource\page_object\Home_page.json")

class sign_in:

    def clear_cache_before_launch(func):
        def wrapper(self, device, *args, **kwargs):
            device_control.clear_cache_the_app(device)
            return func(self, device, *args, **kwargs)
        return wrapper

    @clear_cache_before_launch
    def launch_jio_hotstar_application(self, device):
        device_manager.get_driver(device)
        print(f"Launching Jio Hotstar app on {device}...")
        shared_utils.sleep_with_msg(device, 30, "waiting to load the driver application")

    def click_continue_and_sigin_to_device(self, device):
        try:
            element = shared_utils.find_element(device, home_page_dict, "continue")
            element.click()
            shared_utils.sleep_with_msg(device, 2, "Clicked Continue button")
        except Exception as e:
            raise Exception(f"[{device}] Error clicking Continue: {e}")

    def select_required_ott_languages(self, device):
        try:
            element_visible = shared_utils.find_element(device, home_page_dict, "verify_bottom_menu_home")

            if element_visible and element_visible.is_displayed():
                print("Language selection successful and Home screen visible.")
                return
            else:
                raise Exception("Home screen not visible after language selection.")

        except Exception as e:
            print(f"Error in select_required_ott_languages: {str(e)}")
            raise
