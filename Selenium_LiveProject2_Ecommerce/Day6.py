"""
Test Case:
Verify user is able to purchase product using registered email id

Steps:
1. Go to http://live.guru99.com/index.php/
2. Click My Account
3. Login with user cred
4. Click My Wishlist (Wishlist will have LG LCD Product already $615.00)
5. Click Add to cart
6. Click Proceed to checkout
7. Enter shipping information
8. Check Estimate
9. Verify Shipping Cost generated - EXPECTED: Flat Rate Shipping of $5
10. Select Shipping Cost

(These steps provided by Guru99 DO NOT match up with the website)
11. Verify shipping cost is added to total - EXPECTED: $5 + Total of Item ($620)
12. Click Proceed to Checkout
13. Enter Billing Information
14. In Shipping Method click Continue
15. In Payment Information select "Check/Money Order" Radio Button - Click Continue
16. Click Place Order
17. Verify Order is generated (Order Number) - EXPECTED: Order Number Generated

Test Data:
- Password = , email =  (Created in Day5.py)
- Shipping Information: USA, New York, 542896, ABC, New York, 12345678
"""
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import *

class Error(Exception):
    pass
class ShippingError(Error):
    pass
class OrderError(Error):
    pass

class Util():
    def __init__(self):
        driverlocation = ""
        self.driver = webdriver.Chrome(driverlocation)
        self.url = "http://live.guru99.com/index.php/"

# Steps 4 - 10
def shippingcost(driver):
    # 4. Click My Wishlist (Wishlist will have LG LCD Product already)
    driver.find_element(By.XPATH, "//div[@class='block-content']//a[text()='My Wishlist']").click()
    # 5. Click Add to cart
    driver.find_element(By.XPATH, "//span[text()='Add to Cart']").click()
    # 6. Click Proceed to checkout
    driver.find_element(By.XPATH, "//ul[contains(@class,'top')]//button[@title='Proceed to Checkout']").click()
    # 7. Enter shipping information
    address = "ABC"
    city = "New York"
    state = "New York"
    zip = "542896"
    country = "United States"
    telephone = "12345678"
    driver.find_element(By.XPATH, "//input[@id='billing:street1']").send_keys(address)
    driver.find_element(By.XPATH, "//input[@id='billing:city']").send_keys(city)
    selectingState = Select(driver.find_element(By.XPATH, "//select[@id='billing:region_id']"))
    selectingState.select_by_visible_text(state)
    driver.find_element(By.XPATH, "//input[@id='billing:postcode']").send_keys(zip)
    selectingCountry = Select(driver.find_element(By.XPATH, "//select[@id='billing:country_id']"))
    selectingCountry.select_by_visible_text(country)
    driver.find_element(By.XPATH, "//input[@id='billing:telephone']").send_keys(telephone)
    driver.find_element(By.XPATH, "//div[@id='billing-buttons-container']/button[@title='Continue']").click()
    time.sleep(5)
    # 8. Check Estimate
    # 9. Verify Shipping Cost generated - EXPECTED: Flat Rate Shipping of $5
    expectedShipping = "$5.00"
    actualShipping = driver.find_element(By.XPATH, "//div[@id='checkout-shipping-method-load']//span[@class='price']").text
    if expectedShipping == actualShipping:
        print("PASS: Shipping = $5.00")
    else:
        raise ShippingError
    # 10. Select Shipping Cost (This is just pressing Continue)
    driver.find_element(By.XPATH, "//div[@id='shipping-method-buttons-container']/button").click()

# Steps 11 - 17
def order(driver):
    """
    !!!!!!!!!!!!!!!Steps provided by Guru99 do not match with the flow of the website after step 10 - starting from STEP 15!!!!!!!!!!!!!!!
11. Verify shipping cost is added to total - EXPECTED: $5 + Total of Item ($620)
12. Click Proceed to Checkout
13. Enter Billing Information
14. In Shipping Method click Continue
15. In Payment Information select "Check/Money Order" Radio Button - Click Continue
16. Click Place Order
17. Verify Order is generated (Order Number) - EXPECTED: Order Number Generated
    """
    # 15. In Payment Information select "Check/Money Order" Radio Button - Click Continue
    driver.find_element(By.XPATH, "//input[@value='checkmo']").click()
    # Press Continue
    driver.find_element(By.XPATH, "//div[@id='payment-buttons-container']/button").click()
    # 11. Verify shipping cost is added to total - EXPECTED: $5 + Total of Item ($620)
    expectedTotal = "$620.00"
    actualTotal = driver.find_element(By.XPATH, "//tr[@class='last']//span[@class='price']").text
    if expectedTotal == actualTotal:
        print("PASS: Total is $620.00 ($5 Shipping + $615.00 Item")
    else:
        raise ShippingError

    # 16. Click Place Order
    driver.find_element(By.XPATH, "//button[@title='Place Order']").click()
    # 17. Verify Order is generated (Order Number) - EXPECTED: Order Number Generated
    try:
        actualOrderNumber = driver.find_element(By.XPATH, "//p[contains(text(), 'Your order # is:')]/a").text
        print("PASS: Order Number generated: {}".format(actualOrderNumber))
    except NoSuchElementException as cause:
        print("FAIL: Order Number was not generated")
        raise OrderError(NoSuchElementException) from cause
    """ Will print:
    fail...
    OrderError NoSuchElemen...
    no such element....
    """

def testcase6(driver, url):
    email = ""
    pw = ""
    driver.implicitly_wait(3)
    try:
        # 1. Go to http://live.guru99.com/index.php/
        driver.get(url)
        # 2. Click My Account
        driver.find_element(By.XPATH, "//div[@class='footer-container']//a[@title='My Account']").click()
        # 3. Login with user cred
        driver.find_element(By.XPATH, "//input[@id='email']").send_keys(email)
        driver.find_element(By.XPATH, "//input[@id='pass']").send_keys(pw)
        driver.find_element(By.XPATH, "//button[@title='Login']").click()

        # Steps 4 - 10
        shippingcost(driver)
        # Steps 11 - 17
        order(driver)
    except ShippingError:
        print("ShippingError")
    except OrderError as exp:
        print("Order Error", exp)
        print(exp.__cause__)

def main():
    utils = Util()
    testcase6(utils.driver, utils.url)
    utils.driver.quit()

main()