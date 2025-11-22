*** Settings ***
Documentation     Android Mobile Login Tests
Library           AppiumLibrary
Suite Setup       Open Android Application
Suite Teardown    Close Application
Test Teardown     Run Keyword If Test Failed    Capture Page Screenshot

*** Variables ***
${APPIUM_SERVER}         http://localhost:4723
${PLATFORM_NAME}         Android
${PLATFORM_VERSION}      11
${DEVICE_NAME}           test_emulator
${APP_PACKAGE}           com.example.app
${APP_ACTIVITY}          .MainActivity
${AUTOMATION_NAME}       UiAutomator2

*** Test Cases ***
Android Login - Valid Credentials
    [Documentation]    Test successful login on Android app
    [Tags]    android    smoke    login    positive
    Wait Until Page Contains Element    id=com.example.app:id/username    timeout=10s
    Input Text    id=com.example.app:id/username    testuser
    Input Text    id=com.example.app:id/password    testpass123
    Click Element    id=com.example.app:id/login_button
    Wait Until Page Contains    Welcome    timeout=10s
    Page Should Contain Text    Dashboard

Android Login - Invalid Credentials
    [Documentation]    Test login failure with invalid credentials
    [Tags]    android    negative    login
    Wait Until Page Contains Element    id=com.example.app:id/username    timeout=10s
    Input Text    id=com.example.app:id/username    invalid_user
    Input Text    id=com.example.app:id/password    wrong_pass
    Click Element    id=com.example.app:id/login_button
    Wait Until Page Contains    Invalid credentials    timeout=5s

Android Login - Empty Fields
    [Documentation]    Test validation for empty login fields
    [Tags]    android    validation    negative
    Wait Until Page Contains Element    id=com.example.app:id/login_button    timeout=10s
    Click Element    id=com.example.app:id/login_button
    Wait Until Page Contains    Please enter username    timeout=5s

Android - Check App Version
    [Documentation]    Verify app version is displayed
    [Tags]    android    info
    Wait Until Page Contains Element    id=com.example.app:id/version_text    timeout=10s
    ${version}=    Get Text    id=com.example.app:id/version_text
    Should Match Regexp    ${version}    \\d+\\.\\d+\\.\\d+

Android - Orientation Change
    [Documentation]    Test app behavior on orientation change
    [Tags]    android    ux
    Wait Until Page Contains Element    id=com.example.app:id/username    timeout=10s
    ${original_orientation}=    Get Current Context
    Rotate    LANDSCAPE
    Sleep    2s
    Page Should Contain Element    id=com.example.app:id/username
    Rotate    PORTRAIT
    Sleep    2s
    Page Should Contain Element    id=com.example.app:id/username

*** Keywords ***
Open Android Application
    Open Application    ${APPIUM_SERVER}
    ...    platformName=${PLATFORM_NAME}
    ...    platformVersion=${PLATFORM_VERSION}
    ...    deviceName=${DEVICE_NAME}
    ...    appPackage=${APP_PACKAGE}
    ...    appActivity=${APP_ACTIVITY}
    ...    automationName=${AUTOMATION_NAME}
    ...    noReset=true
    Sleep    3s    # Wait for app to load