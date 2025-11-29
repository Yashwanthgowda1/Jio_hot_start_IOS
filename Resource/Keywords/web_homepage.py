from Libraries import shared_utils, device_manager


home_page_dict = shared_utils.load_loctors("Resource\page_object\Home_page.json")


def swipe_the_elemnt_main_suggestion_left_and_verify(device):
    driver = device_manager.get_existing_driver(device)
    element_auto_appear_in_home_page = shared_utils.find_elements(
        device, home_page_dict, "web_home_main_suggestion_swipping_content"
    )
    driver.execute_script(
        "arguments[0].scrollIntoView(true)", element_auto_appear_in_home_page
    )
    for eachPindex_values in element_auto_appear_in_home_page:
        attribute_values_pre = eachPindex_values.get_attribute(
            "data-swiper-slide-index"
        )
        attribute_values_pre.click()
        shared_utils.sleep_with_msg(device, 3, "waiting for next elemnt get changes")
        attribute_values_active = eachPindex_values.get_attribute(
            "data-swiper-slide-index"
        )
        if attribute_values_active == attribute_values_pre:
            raise Exception(
                f"sliding is not happend the index is matching prev-> {attribute_values_pre} and current ->{attribute_values_active}"
            )
