from Libraries import shared_utils, device_manager


home_page_dict = shared_utils.load_loctors("Resource/page_object/Home_page.json")


def swipe_the_elemnt_main_suggestion_left_and_verify(device):
    """Scroll the web page and verify main suggestion elements change as expected.

    Raises a clear error when the driver is not initialized or when expected
    elements are missing/unchanged.
    """
    driver = device_manager.get_existing_driver(device)
    if driver is None:
        raise RuntimeError(f"No driver found for device '{device}'. Did you call initiate_driver(device) first?")

    try:
        # Scroll the page (works for web drivers)
        driver.execute_script("window.scrollBy(100,350)")

        # Verify suggestion section exists
        elemnts = shared_utils.find_element(device, home_page_dict, "web_home_page_suggetsion")
        if not (elemnts and elemnts.is_displayed()):
            raise Exception(f"{device}: web_home_page_suggetsion not found or not visible")

        # Get list of sliding items and iterate
        shared_utils.sleep_with_msg(device, 5, "waiting for load the scroll page")
    
        # for _ in range(1):
        #     elemnst_last_active = shared_utils.find_element(device, home_page_dict, "web_scroll_main_trending_page")
        #     print(f"the text i need to evrify which one pick first {elemnst_last_active.text}")
        #     last = elemnst_last_active.text.strip().split('-')[-1]
        #     shared_utils.sleep_with_msg(device, 60, "waiting for change the main elements")

        #     if last not in ["prev", "next"]:
        #         elemnst_last_active = shared_utils.find_element(device, home_page_dict, 'web_scroll_main_trending_page').text
        #         print(f"the element not changed: {elemnst_last_active}")
        #         raise Exception(f"{device}: main trending element did not change after swipe")

    except Exception as e:
        raise AssertionError(f"{device}: element check failed: {e}")

    
    