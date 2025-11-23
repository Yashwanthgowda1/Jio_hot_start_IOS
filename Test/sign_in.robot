*** Settings ***
Resource    ../../Jio_hot_start_IOS/Resource/Keywords/Home_page.robot


*** Test Cases ***
Launch Application
    [Tags]    56788
    Launch And Signin Verify Home Page

Tc2: Select fav show from Tv options
    [Tags]    56789
    Launch And Signin Verify Home Page
    Sleep    10
    select fav show from Tv options
    [Teardown]    close all drivers

TC3: lanuh web appliaction jio hotstar
    [Tags]     45679
    lanuh_web_appliaction
    [Teardown]    close all drivers
    

    



