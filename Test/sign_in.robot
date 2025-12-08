*** Settings ***
Resource    ../../Jio_hot_start_IOS/Resource/Keywords/Home_page.robot
Library     ../../Jio_hot_start_IOS/Resource/Keywords/web_homepage.py


*** Test Cases ***
Launch Application
    [Tags]    56788
    Launch And Signin Verify Home Page
    [Teardown]    close all drivers

Tc2: Select fav show from Tv options
    [Tags]    56789    @SANITY
    Launch And Signin Verify Home Page
    Sleep    10
    select fav show from Tv options
    [Teardown]    close all drivers

TC3: lanuh web appliaction jio hotstar
    [Tags]     45679     
    lanuh_web_appliaction
    Sleep    10s
    [Teardown]    close all drivers


TC4: verfy all avilable options in studio
    [Tags]    45678     @SOMKE    @SANITY
    Launch And Signin Verify Home Page
    @{list_of_all_pages_in_studio}=        verfy_user_able_to_select_studio_option    device=device_1
    ${count}=    Get Length    ${list_of_all_pages_in_studio}
    IF    ${count} >= 5
        Log    List of all studio features present: ${list_of_all_pages_in_studio}
    ELSE
        Fail    Studio features missing! Only found ${count}
    END
    click_selected_content_page_on_studio    device=device_1
    [Teardown]    close all drivers



TC5: verify top treanding movies today
    [Tags]   45709   @SMOKE   @SANITY
    Launch And Signin Verify Home Page
    select_top_trading_movies_list_and_verify_able_to_see_indiffrent_languages    device=device_1
    verify_top_trending_diffrent_language        device=device_1
    [Teardown]    close all drivers

    

TC6: lanuh web appliaction jio hotstar
    [Tags]    78789   
    lanuh_web_appliaction
    swipe_the_elemnt_main_suggestion_left_and_verify    device=device1user
    [Teardown]    close all drivers


Tc5: Verify user bale to see the main tray option when drag up the more option    
    [Tags]    34574       @smoke     @sanity
    Launch And Signin Verify Home Page
    open_verify_more_option    device=device_1
    verfiy_user_able_to_see_the_main_try_opton_when_scroll    device=device_1
    [Teardown]    close all drivers

