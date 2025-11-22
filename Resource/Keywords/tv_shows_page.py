from Libraries import shared_utils
import time
tv_shows_dict=shared_utils.load_loctors("Resource/page_object/tv_shows.json")



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
    else:
        raise Exception("TV Show page did not open as expected.")

def swipe_page_to_get_fav_option(device, max_swipes=7):
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

    # If reached here → not found even after swiping
    raise Exception(f"Movie not found after {max_swipes} swipes")

