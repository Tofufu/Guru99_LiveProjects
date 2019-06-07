"""
Day 3 = More Automated Test Cases with the same scenario: Verifying the Login Page

1. Enter in valid user/valid pw
2. Enter in invalid user/valid pw
3. Enter in valid user/invalid pw
4. Enter in invalid user/invalid pw

- Create generic script that will handle all these inputs
- GURU99 wants us to automate this is putting in the Test Data/Correct Output into Excel and reading from there
- Then handling the input afterwards
"""

# Read in User Data in loop and save to struct
from selenium import webdriver
from selenium.webdriver.common.by import By

import time
from Day3Util import Util

import pandas as pd


class Error(Exception):
    pass
class UnableToVerifyOutput(Error):
    pass

def LoginVerify(driver, url, user, pw):
    try:
        driver.get(url)
        # Enter valid User Id
        userForm = driver.find_element(By.XPATH, "//input[@name='uid']")
        userForm.clear()
        userForm.send_keys(user)
        time.sleep(2)
        # Enter valid PW
        pwForm = driver.find_element(By.XPATH, "//input[@name='password']")
        pwForm.send_keys(pw)
        time.sleep(2)
        # Click Login
        loginButton = driver.find_element(By.XPATH, "//input[@value='LOGIN']")
        loginButton.click()
        time.sleep(2)

        print("Pressed log in")

        if user == "invalid" or pw == "invalid":
            alertpopup = driver.switch_to.alert
            alertpopupTEXT = alertpopup.text

            if "User or Password is not valid" not in alertpopup.text:
                raise UnableToVerifyOutput("FAIL - Wrong Popup Message: " + str(alertpopupTEXT) + " with user: " + user + " password: " + pw)
            else:
                # press okay on the button
                alertpopup.accept()
                # check to make sure we are back in login page
                pageTitle = driver.title
                if "Guru99 Bank Home Page" not in pageTitle: # Else we're at the wrong home page
                    raise UnableToVerifyOutput("FAIL - Redirected to wrong homepage: " + str(pageTitle) + " with user: " + user + " password: " + pw)
                else: # If we're at the right home page than the whole test case is a success
                    print("PASS - Homepage Title: " + str(pageTitle) + " and alert text: " + str(alertpopupTEXT) + " with user: " + user + " password: " + pw)
        else:  # Else it's valid for both so we check title
            # Check Valid Output - if Homepage title doesn't match raise exception (Valid User/Valid PW)
            # <title> Guru99 Bank Manager HomePage </title>
            homepageTitle = driver.title
            if "Guru99 Bank Manager HomePage" not in homepageTitle:
                raise UnableToVerifyOutput("FAIL - Wrong Homepage Title: " + str(homepageTitle) + " with user: " + user + " password: " + pw)
            else:
                print("PASS - Correct Homepage Title: " + str(homepageTitle) + " with user: " + user + " password: " + pw)
    except UnableToVerifyOutput as error1:
        print("Unable to Verify the Output:" + str(error1))
    except Exception as error2:
        print("Error Logging in: " + str(error2))
    finally:
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Test is done~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

def main():
    utils = Util()
    utils.driver.implicitly_wait(3)

    excelSheet = pd.read_excel("DataDay3.xlsx", sheet_name="Sheet1")
    for row in range(0, 4):
        user = excelSheet.iloc[row,0]
        pw = excelSheet.iloc[row,1]
        LoginVerify(utils.driver, utils.url, user, pw)
    utils.driver.quit()

main()