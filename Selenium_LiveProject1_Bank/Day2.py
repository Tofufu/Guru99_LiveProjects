"""
Excepted output = Able to verify the title of the HomePage
"""
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from Day2Util import Util

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
        # Enter valid PW
        pwForm = driver.find_element(By.XPATH, "//input[@name='password']")
        pwForm.send_keys(pw)
        # Click Login
        loginButton = driver.find_element(By.XPATH, "//input[@value='LOGIN']")
        loginButton.click()
        time.sleep(2)

        print("Logged in")

        # Check Valid Output - if Homepage title doesn't match raise exception
        # <title> Guru99 Bank Manager HomePage </title>
        homepageTitle = driver.title
        if "Guru99 Bank Manager HomePage" not in homepageTitle:
            raise UnableToVerifyOutput("Wrong Output - Homepage Title is this: " + str(homepageTitle))
        else:
            print("Correct Output - Homepage Title is this: " + str(homepageTitle))
    except UnableToVerifyOutput as error1:
        print("Unable to Verify the Output:" + str(error1))
    except Exception as error2:
        print("Error Logging in: " + str(error2))


def main():
    utils = Util()
    utils.driver.implicitly_wait(3)
    LoginVerify(utils.driver, utils.url, utils.username, utils.password)
    utils.driver.quit()

main()