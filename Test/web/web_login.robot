*** Settings ***
Documentation     Web Browser Login Tests
Library           SeleniumLibrary
Suite Setup       Open Browser To Login Page
Suite Teardown    Close Browser
Test Teardown     Run Keyword If Test Failed    Capture Page Screenshot

*** Variables ***
${URL}              https://the-internet.herokuapp.com/login
${BROWSER}          headlesschrome
${USERNAME}         tomsmith
${PASSWORD}         SuperSecretPassword!

*** Test Cases ***
Web Login - Valid Credentials
    [Documentation]    Test successful login via web browser
    [Tags]    web    smoke    login    positive
    Input Text       id:username    ${USERNAME}
    Input Password   id:password    ${PASSWORD}
    Click Button     css:button[type='submit']
    Wait Until Page Contains    You logged into a secure area!    timeout=5s
    Page Should Contain    Secure Area
    Location Should Contain    /secure

Web Login - Invalid Username
    [Documentation]    Test login failure with invalid username
    [Tags]    web    negative    login
    Go To    ${URL}
    Input Text       id:username    invalid_user
    Input Password   id:password    ${PASSWORD}
    Click Button     css:button[type='submit']
    Wait Until Page Contains    Your username is invalid!    timeout=5s

Web Login - Invalid Password
    [Documentation]    Test login failure with invalid password
    [Tags]    web    negative    login
    Go To    ${URL}
    Input Text       id:username    ${USERNAME}
    Input Password   id:password    wrong_password
    Click Button     css:button[type='submit']
    Wait Until Page Contains    Your password is invalid!    timeout=5s

Web Login - Empty Username
    [Documentation]    Test validation for empty username
    [Tags]    web    validation    negative
    Go To    ${URL}
    Input Password   id:password    ${PASSWORD}
    Click Button     css:button[type='submit']
    Page Should Contain    Your username is invalid!

Web Login - Empty Password
    [Documentation]    Test validation for empty password
    [Tags]    web    validation    negative
    Go To    ${URL}
    Input Text       id:username    ${USERNAME}
    Click Button     css:button[type='submit']
    Page Should Contain    Your password is invalid!

Web Logout - Successful
    [Documentation]    Test successful logout functionality
    [Tags]    web    smoke    logout    positive
    Input Text       id:username    ${USERNAME}
    Input Password   id:password    ${PASSWORD}
    Click Button     css:button[type='submit']
    Wait Until Page Contains    Secure Area    timeout=5s
    Click Link       css:a[href='/logout']
    Wait Until Page Contains    You logged out    timeout=5s
    Page Should Contain    Login Page

Web - Responsive Design Check
    [Documentation]    Test responsive design at different resolutions
    [Tags]    web    ux    responsive
    # Desktop
    Set Window Size    1920    1080
    Page Should Contain Element    id:username
    
    # Tablet
    Set Window Size    768    1024
    Page Should Contain Element    id:username
    
    # Mobile
    Set Window Size    375    667
    Page Should Contain Element    id:username

Web - Page Load Performance
    [Documentation]    Verify page loads within acceptable time
    [Tags]    web    performance
    ${start_time}=    Get Time    epoch
    Go To    ${URL}
    Wait Until Page Contains Element    id:username    timeout=5s
    ${end_time}=    Get Time    epoch
    ${load_time}=    Evaluate    ${end_time} - ${start_time}
    Should Be True    ${load_time} < 5    Page took too long to load

*** Keywords ***
Open Browser To Login Page
    ${chrome_options}=    Evaluate    sys.modules['selenium.webdriver'].ChromeOptions()    sys, selenium.webdriver
    Call Method    ${chrome_options}    add_argument    --headless
    Call Method    ${chrome_options}    add_argument    --no-sandbox
    Call Method    ${chrome_options}    add_argument    --disable-dev-shm-usage
    Call Method    ${chrome_options}    add_argument    --disable-gpu
    Call Method    ${chrome_options}    add_argument    --window-size=1920,1080
    Create Webdriver    Chrome    options=${chrome_options}
    Set Selenium Speed    0.5s
    Set Selenium Timeout    10s
    Go To    ${URL}
    Title Should Be    The Internet