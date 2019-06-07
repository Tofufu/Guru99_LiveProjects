"""
Test Case:
Verify you can save previously placed order as a pdf file

Test Steps:
1. Go to http://live.guru99.com/index.php/
2. Click My Account
3. Login with previous credentials
4. Click My Orders
[ steps 5/6 provided by Guru99 need to be switched - the orders table and status are before pressing view order)
5. Click View Order
6. Verify previously created order - EXPECTED: Order is in Recent Orders Table w/ Status = PENDING
7. Click on Print Order
8. Verify Save as PDF - EXPECTED: Order is saved as PDF <-- This will open up the Print dialog for chrome - but afterwards will open up a system dialog

Test Data:
Password = , email =
Order Number generated:
(From Day6.py)
"""
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pyautogui

class Error(Exception):
    pass
class OrderError(Error):
    pass

class Util():
    def __init__(self):
        cOptions = webdriver.ChromeOptions()
        cOptions.add_argument("--start-maximized")
        cOptions.add_argument("--disable-print-preview")
        driverlocation = ""
        self.driver = webdriver.Chrome(executable_path=driverlocation, options=cOptions)
        self.url = "http://live.guru99.com/index.php/"

def testcase7(driver, url):
    email = ""
    pw = ""
    driver.implicitly_wait(10)
    try:

        # 1. Go to http://live.guru99.com/index.php/
        driver.get(url)
        # 2. Click My Account
        driver.find_element(By.XPATH, "//div[@class='footer-container']//a[@title='My Account']").click()
        # 3. Login with previous credentials
        driver.find_element(By.XPATH, "//input[@id='email']").clear()
        driver.find_element(By.XPATH, "//input[@id='email']").send_keys(email)
        driver.find_element(By.XPATH, "//input[@id='pass']").clear()
        driver.find_element(By.XPATH, "//input[@id='pass']").send_keys(pw)
        driver.find_element(By.XPATH, "//button[@title='Login']").click()
        # 4. Click My Orders
        driver.find_element(By.XPATH, "//a[text()='My Orders']").click()
        # Guru99 provided steps 5/6 are switched here b/c there is no orders table after pressing "view order"
        # 6. Verify previously created order - EXPECTED: Order is in Recent Orders Table w/ Status = PENDING
        expectedOrderNum = ""
        expectedStatus = "pending"
        actualOrderNum = driver.find_element(By.XPATH, "//td[@class='number']").text
        actualStatus = str(driver.find_element(By.XPATH, "//td[@class='status']").text).lower()
        if (expectedOrderNum in actualOrderNum) and (expectedStatus in actualStatus):
            print("PASS: Expected Order #: {} and Status: {}".format(actualOrderNum, actualStatus))
        else:
            raise OrderError
        # 5. Click View Order
        driver.find_element(By.XPATH, "//a[text()='View Order']").click()
        # 7. Click on Print Order
        driver.find_element(By.XPATH, "//a[@class='link-print']").click()
        # 8. Verify Save as PDF - EXPECTED: Order is saved as PDF
        filename = 'test' + str(round(time.time() * 1000))
        time.sleep(5)
        pyautogui.press('enter')
        time.sleep(3)  # wait a bit before typing the rest
        pyautogui.typewrite(filename)
        time.sleep(2)
        pyautogui.press('enter')
        # This sleep is required because microsoft to PDF needs to have the driver open otherwise it will store it at 0 BYTES for the PDF
        time.sleep(10)
    except OrderError:
        print("OrderError")

def main():
    utils = Util()
    testcase7(utils.driver, utils.url)
    utils.driver.quit()

main()


