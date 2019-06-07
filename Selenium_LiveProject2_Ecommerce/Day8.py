"""
Test Case:
Verify you are able to change or reorder previously added product

Test Steps:
1. Go to http://live.guru99.com/index.php/
2. Click My Account
3. Login with previous cred
4. Click Reorder - Change QTY = 10 and click UPDATE
5. Verify Grand total is changed - EXPECTED: Price * 10 + $5 shipping = 6150
6. Complete Billing and Shipping information (saved)
7. Verify order is generated - EXPECTED: Order Number

Password = , email =
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.common.exceptions import *

class Error(Exception):
    pass
class OrderError(Error):
    pass

class Util():
    def __init__(self):
        cOptions = webdriver.ChromeOptions()
        cOptions.add_argument("--start-maximized")
        driverlocation = ""
        self.driver = webdriver.Chrome(executable_path=driverlocation, options=cOptions)
        self.url = "http://live.guru99.com/index.php/"

def testcase8(driver, url):
    driver.implicitly_wait(10)
    email = ""
    pw = ""
    try:
        driver.get(url)
        # 2. Click My Account
        driver.find_element(By.XPATH, "//div[@class='footer-container']//a[@title='My Account']").click()
        # 3. Login with previous cred
        driver.find_element(By.XPATH, "//input[@id='email']").clear()
        driver.find_element(By.XPATH, "//input[@id='email']").send_keys(email)
        driver.find_element(By.XPATH, "//input[@id='pass']").clear()
        driver.find_element(By.XPATH, "//input[@id='pass']").send_keys(pw)
        driver.find_element(By.XPATH, "//button[@title='Login']").click()
        # 4. Click Reorder - Change QTY = 10 and click UPDATE
        driver.find_element(By.XPATH, "//a[@class='link-reorder']").click()
        driver.find_element(By.XPATH, "//input[@title='Qty']").clear()
        driver.find_element(By.XPATH, "//input[@title='Qty']").send_keys("10")
        driver.find_element(By.XPATH, "//button[@title='Update']").click()
        time.sleep(2)
        # 5. Verify Grand total is changed - EXPECTED: Price * 10 + $50 shipping = 6200
        expectedTotal = "$6,200.00"
        actualTotal = driver.find_element(By.XPATH, "//table[@id='shopping-cart-totals-table']/tfoot/tr/td[2]/strong/span").text

        if expectedTotal == actualTotal:
            print("PASS: Grand Total = {}".format(actualTotal))
        else:
            raise OrderError("Total is incorrect")
        # Proceed to checkout
        driver.find_element(By.XPATH, "//button[@title='Proceed to Checkout']").click()
        # 6. Complete Billing and Shipping information (saved address - press continue)
        driver.find_element(By.XPATH, "//div[@id='billing-buttons-container']/button[@title='Continue']").click()
        driver.find_element(By.XPATH, "//div[@id='shipping-method-buttons-container']/button").click()
        driver.find_element(By.XPATH, "//input[@value='checkmo']").click()
        driver.find_element(By.XPATH, "//div[@id='payment-buttons-container']/button").click()
        driver.find_element(By.XPATH, "//button[@title='Place Order']").click()
        try:
            actualOrderNumber = driver.find_element(By.XPATH, "//p[contains(text(), 'Your order # is:')]/a").text
            print("PASS: Order Number generated: {}".format(actualOrderNumber))
        except NoSuchElementException as cause:
            print("FAIL: Order Number was not generated")
            raise OrderError(NoSuchElementException) from cause
    except OrderError as error:
        print("FAIL: OrderError")
        print(error)
        print(error.__cause__)

def main():
    utils = Util()
    testcase8(utils.driver, utils.url)
    utils.driver.quit()

main()
