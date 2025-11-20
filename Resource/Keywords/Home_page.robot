*** Settings ***
Library    sign_in.py
Library    ../../Libraries//shared_utils.py


*** Test Cases ***
Launch Application
    [Tags]    56788
    Launch And Signin Verify Home Page


*** Keywords ***
Launch And Signin Verify Home Page
    launch_jio_hotstar_application    device=device_1
    click_continue_and_sigin_to_device    device=device_1
    select_required_ott_languages    device=device_1
    swipe_up              device=device_1

