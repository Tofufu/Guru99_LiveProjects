"""
Refactoring code and adding verification if successful login verify managerID
"""
from selenium.webdriver.common.by import By
import time
from Day5Util import Util
import pandas as pd

class Error(Exception):
    pass
class UnableToVerifyOutput(Error):
    pass


def InvalidLoginVerify(driver, user, pw):
    alert = driver.switch_to.alert
    alertTEXT = alert.text
    if "User or Password is not valid" not in alertTEXT:
        raise UnableToVerifyOutput("FAIL - Wrong Popup Message: " + str(alertTEXT) + " with user: " + user + " password: " + pw)
    else:
        alert.accept()
        pageTitle = driver.title
        if "Guru99 Bank Home Page" not in pageTitle:
            raise UnableToVerifyOutput("FAIL - Redirected to wrong homepage: " + str(pageTitle) + " with user: " + user + " password: " + pw)
        else:
            print("PASS - Homepage Title: " + str(pageTitle) + " and alert text: " + str(alertTEXT) + " with user: " + user + " password: " + pw)


def ValidLoginVerify(driver, user, pw):
    # Check Valid Output - if Homepage title doesn't match raise exception (Valid User/Valid PW)
    # <title> Guru99 Bank Manager HomePage </title>
    homepageTitle = driver.title
    if "Guru99 Bank Manager HomePage" not in homepageTitle:
        raise UnableToVerifyOutput("FAIL - Wrong Homepage Title: " + str(homepageTitle) + " with user: " + user + " password: " + pw)
    else:
        # Check that the userID matches what's displaying on the homepage
        correctManagerString = "Manger Id : " + user  # The correct string - Manager is spelled incorrectly
        actualManagerString = driver.find_element(By.XPATH, "//tr[@class='heading3']/td").text  # String on the page
        if correctManagerString != actualManagerString:
            raise UnableToVerifyOutput("FAIL - Wrong Manager Name: " + str(actualManagerString) + " with user: " + user + " password: " + pw + ".......")
        else:
            print("Correct Homepage Title: " + str(homepageTitle) + " with user: " + user + " password: " + pw)
            print("Correct Manager Name: " + str(actualManagerString))


def LoginVerify(driver, url, user, pw):
    try:
        driver.get(url)
        # Enter valid User Id
        userForm = driver.find_element(By.XPATH, "//input[@name='uid']")
        userForm.clear()  # Best practice to clear before entering in keys
        userForm.send_keys(user)
        time.sleep(2)
        # Enter valid PW
        pwForm = driver.find_element(By.XPATH, "//input[@name='password']")
        pwForm.send_keys(pw)
        time.sleep(2)
        # Click Loogin
        loginButton = driver.find_element(By.XPATH, "//input[@value='LOGIN']")
        loginButton.click()
        time.sleep(2)

        print("Pressed log in")
        # ---------------------VALIDATING OUTPUT--------------------
        if user == "invalid" or pw == "invalid": # If either are invalid pop up with "User or Password is not valid" shows up - press okay - redirected to login screen
            InvalidLoginVerify(driver, user, pw)
        else:
            ValidLoginVerify(driver, user, pw)
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