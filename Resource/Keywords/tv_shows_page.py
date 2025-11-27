from Libraries import shared_utils
import time
from Libraries import device_manager

tv_shows_dict=shared_utils.load_loctors("Resource/page_object/tv_shows.json")
home_page_dict = shared_utils.load_loctors("Resource\page_object\Home_page.json")



def verify_and_click_on_tv_show_menu_in_homepage(device):
    try:
        
        all_favorites_short_cut_section=shared_utils.find_element(device, tv_shows_dict,"main_tv_shows_menu_home_page")
        if all_favorites_short_cut_section and all_favorites_short_cut_section.is_displayed():
            element = shared_utils.find_element(device, tv_shows_dict, "tv_shows_first_item")
            element.click()
            shared_utils.sleep_with_msg(device, 2, "Clicked TV Show menu")
    except Exception as e:
        raise Exception(f"[{device}] Error clicking TV Show menu: {e}")

def verify_tv_show_page_opened(device):
    shared_utils.swipe_up(device)
    shared_utils.sleep_with_msg(device, 2, "Swiped up to verify TV Show page so the load the wrong button")
    element_visible = shared_utils.find_element(device, tv_shows_dict, "clsoe_filter_button")
    if element_visible and element_visible.is_displayed():
        print("TV Show page is opened successfully.")
        shared_utils.swipe_down(device)
    else:
        raise Exception("TV Show page did not open as expected.")

def swipe_page_to_get_fav_option(device, max_swipes=10):
    for attempt in range(max_swipes):
        element = shared_utils.find_element(device, tv_shows_dict, "select_the_show_favritos")
        if element and element.is_displayed():
            print("Successfully found the favorite option.")
            time.sleep(3)
            return  # Return the visible element
        shared_utils.swipe_up(device)
        shared_utils.sleep_with_msg(device, 2, f"Swipe {attempt+1} to get favorite option")

    raise Exception("Favorite option not found even after swiping {} times".format(max_swipes))


def swipe_fav_page_left_to_right(device, max_swipes=5):

    element=shared_utils.find_element(device, tv_shows_dict, "scroll_the_favriout_section_left_right")
    for attempt in range(max_swipes):

        # Try to find the movie after each swipe
        # target_movie = shared_utils.find_element(device, tv_shows_dict, "select_home_drame_required_movie_click")

        # if target_movie and target_movie.is_displayed():
        #     target_movie.click()
        #     shared_utils.sleep_with_msg(device, 2, "Movie found after swiping")
        #     print(f"Movie found after {attempt} swipes")
        #     return

        # If not found → swipe
        shared_utils.swipe_left_to_right_fav_shows(device, element)
        shared_utils.sleep_with_msg(device, 1, f"Swipe left {attempt+1}")


def launch_web_appliaction_verify_login_able_to_sigin_invalid_number(device):
    device_manager.lanuch_browser(device)


def verfy_user_able_to_select_studio_option(device) -> list:
    all_favorites_short_cut_section=shared_utils.find_element(device, tv_shows_dict,"main_tv_shows_menu_home_page")
    if all_favorites_short_cut_section and all_favorites_short_cut_section.is_displayed():
            more_option=shared_utils.find_element(device, home_page_dict, "more_option")
            more_option.click()
            el_info_page=shared_utils.find_element(device, home_page_dict, "more_option_dilouge_box_popups")
            if el_info_page and el_info_page.is_displayed():
                shared_utils.find_element(device, home_page_dict, "studio_option").click()
                el_studi=shared_utils.find_element(device, home_page_dict, "studio_option")
                if el_studi and el_studi.is_displayed():
                    shared_utils.sleep_with_msg(device, 2, f"waiting to load the {el_studi}")
                    list_all_options=shared_utils.find_elements(device, tv_shows_dict, "studio_page_options")
                    el_ments=[]
                    for all_options_one_by in list_all_options:
                            each_starting_elemnt=all_options_one_by.get_attribute("content-desc")
                            el_ments.append(each_starting_elemnt.split(',')[0])
                    return  el_ments





            

