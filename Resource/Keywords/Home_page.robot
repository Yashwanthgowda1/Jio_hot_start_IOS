*** Settings ***
Library    sign_in.py
Library    tv_shows_page.py
Library    ../../Jio_hot_start_IOS/Libraries/device_manager.py
Library    ../../Jio_hot_start_IOS/Libraries/shared_utils.py


*** Keywords ***
Launch And Signin Verify Home Page
    launch_jio_hotstar_application    device=device_1
    click_continue_and_sigin_to_device    device=device_1
    select_required_ott_languages    device=device_1
    swipe_up              device=device_1


select fav show from Tv options
    verify_and_click_on_tv_show_menu_in_homepage    device=device_1
    verify_tv_show_page_opened    device=device_1
    swipe_fav_page_left_to_right    device=device_1

close all drivers
    tear_down_driver

lanuh_web_appliaction
    launch_web_appliaction_verify_login_able_to_sigin_invalid_number    device=device1user
