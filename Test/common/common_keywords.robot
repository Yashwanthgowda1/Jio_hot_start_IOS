*** Settings ***
Documentation     Common keywords shared across Android and Web tests
Library           BuiltIn
Library           DateTime
Library           OperatingSystem

*** Keywords ***
Generate Timestamp
    [Documentation]    Generate current timestamp
    ${timestamp}=    Get Current Date    result_format=%Y-%m-%d_%H-%M-%S
    [Return]    ${timestamp}

Create Test Data File
    [Documentation]    Create test data file for reporting
    [Arguments]    ${filename}    ${content}
    Create File    ${OUTPUTDIR}/${filename}    ${content}

Log Test Environment
    [Documentation]    Log current test environment details
    ${platform}=    Get Variable Value    ${PLATFORM}    Unknown
    ${timestamp}=    Generate Timestamp
    Log    Platform: ${platform}
    Log    Timestamp: ${timestamp}
    Log    Output Dir: ${OUTPUTDIR}

Wait And Retry
    [Documentation]    Retry a keyword multiple times with wait
    [Arguments]    ${keyword}    ${max_attempts}=3    ${wait_time}=2s
    FOR    ${attempt}    IN RANGE    1    ${max_attempts}+1
        ${status}=    Run Keyword And Return Status    ${keyword}
        Exit For Loop If    ${status}
        Run Keyword If    ${attempt} < ${max_attempts}    Sleep    ${wait_time}
    END
    Run Keyword Unless    ${status}    Fail    Keyword ${keyword} failed after ${max_attempts} attempts

Take Screenshot With Timestamp
    [Documentation]    Capture screenshot with timestamp in filename
    ${timestamp}=    Generate Timestamp
    ${screenshot_name}=    Set Variable    screenshot_${timestamp}.png
    Capture Page Screenshot    ${screenshot_name}
    [Return]    ${screenshot_name}

Verify Element Text Contains
    [Documentation]    Verify element contains expected text (cross-platform)
    [Arguments]    ${locator}    ${expected_text}
    ${actual_text}=    Get Text    ${locator}
    Should Contain    ${actual_text}    ${expected_text}

Compare Images
    [Documentation]    Compare two images (for visual testing)
    [Arguments]    ${baseline_image}    ${current_image}
    # This would require additional image comparison library
    Log    Comparing ${baseline_image} with ${current_image}
    # Placeholder - implement with PIL or opencv

Generate Test Report Summary
    [Documentation]    Generate custom test summary
    ${suite_name}=    Get Variable Value    ${SUITE_NAME}    Unknown Suite
    ${total_tests}=    Get Variable Value    ${SUITE_STATUS}    Unknown
    Log    Suite: ${suite_name}
    Log    Status: ${total_tests}