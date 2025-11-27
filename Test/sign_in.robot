*** Settings ***
Resource    ../../Jio_hot_start_IOS/Resource/Keywords/Home_page.robot
Library     ../../Jio_hot_start_IOS/Resource/Keywords/web_homepage.py


*** Test Cases ***
Launch Application
    [Tags]    56788
    Launch And Signin Verify Home Page
    [Teardown]    close all drivers

Tc2: Select fav show from Tv options
    [Tags]    56789
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
    [Tags]    45678
    Launch And Signin Verify Home Page
    @{list_of_all_pages_in_studio}=        verfy_user_able_to_select_studio_option    device=device_1
    ${count}=    Get Length    ${list_of_all_pages_in_studio}
    IF    ${count} >= 5
        Log    List of all studio features present: ${list_of_all_pages_in_studio}
    ELSE
        Fail    Studio features missing! Only found ${count}
    END
    [Teardown]    close all drivers



    

    



