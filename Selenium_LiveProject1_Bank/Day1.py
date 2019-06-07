"""
Day 1

Test Scenario: Verify the Login Section
Test Case: Enter in valid userid/pw
Test Steps:
1. Go to website
2. Enter valid User id
3. Enter valid PW
4. Click Login
Test Data:
UserId
Password
Expected Result:
Login Successful

Actual Result:

"""
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

class Chrome():
    def __init__(self):
        driverlocation = "location of chrome driver"
        self.driver = webdriver.Chrome(driverlocation)

    def loginTC(self):
        try:
            self.driver.implicitly_wait(3)
            url = "http://www.demo.guru99.com/V4/"
            self.driver.get(url)
            userForm = self.driver.find_element(By.XPATH, "//input[@name='uid']")
            userForm.send_keys("USERNAME FOR LOGIN")
            pwForm = self.driver.find_element(By.XPATH, "//input[@name='password']")
            pwForm.send_keys("PASSWORD FOR LOGIN")
            loginButton = self.driver.find_element(By.XPATH, "//input[@value='LOGIN']")
            loginButton.click()
            time.sleep(2)
            print("Logged in")
            self.driver.quit()

        except Exception as errorMessage:
            print("This is the error: " + str(errorMessage))


chromeBrowser = Chrome()
chromeBrowser.loginTC()