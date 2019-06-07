"""
Test Case:
Verify that product can't be added in cart if no more stock
Test Steps:
1. Go to http://live.guru99.com/index.php/
2. Click on MOBILE
3. Click Add to cart for Sony Xperia (Should be in cart page now)
4. Change QTY to 1000 and press UPDATE
5. Verify if if there is error message: "The requested quantity for Sony Xperia is not available"
6. Click Empty Cart
7. Verify cart is empty - "Shopping Cart is Empty"
"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
import time

# User Defined Exceptions
class Error(Exception):
    pass
class NoErrorQTYCart(Error):
    pass
class NoEmptyCart(Error):
    pass

class Util():
    def __init__(self):
        driverlocation = ""
        self.driver = webdriver.Chrome(driverlocation)
        self.url = "http://live.guru99.com/index.php/"

def testcase3(driver, url):
    phone = "Xperia"
    expectedErrorQTY1 = "Some of the products cannot be ordered in requested quantity."
    expectedErrorQTY2 = "The maximum quantity allowed for purchase is 500."
    expectedEmpty1 = "SHOPPING CART IS EMPTY"
    expectedEmpty2 = "You have no items in your shopping cart."
    driver.implicitly_wait(3)
    # 1. Go to http://live.guru99.com/index.php/
    driver.get(url)
    try:
        # 2. Click on MOBILE
        driver.find_element(By.XPATH, "//a[text()='Mobile']").click()
        time.sleep(1)
        # 3. Click Add to cart for Sony Xperia (Should be in cart page now)
        dynamicButtonXPATH = "//a[@title='"+phone+"']//following-sibling::div/div[@class='actions']/button"
        driver.find_element(By.XPATH, dynamicButtonXPATH).click()
        time.sleep(1)
        qtyTextBox = driver.find_element(By.XPATH, "//input[@title='Qty']")
        qtyTextBox.click()
        time.sleep(1)
        updateButton = driver.find_element(By.XPATH, "//button[@title='Update']")
        # Wait until it's displayed
        while updateButton.is_displayed() != True:
            qtyTextBox.click()
        # 4. Change QTY to 1000 and press UPDATE
        if updateButton.is_displayed():
            qtyTextBox.send_keys("1000")
            updateButton.click()
        time.sleep(2)
        # 5. Verify if if there is error message: "The requested quantity for Sony Xperia is not available"
        actualErrorQTY1 = driver.find_element(By.XPATH, "//li[@class='error-msg']//span").text
        actualErrorQTY2 = driver.find_element(By.XPATH, "//p[contains(@class,'item-msg') and contains(@class,'error')]").text
        if (expectedErrorQTY1 in actualErrorQTY1) and (expectedErrorQTY2 in actualErrorQTY2):
            print("Expected Error Message ------ PASSED for QTY")
        else:
            raise NoErrorQTYCart
        # 6. Click Empty Cart
        driver.find_element(By.XPATH, "//button[@value='empty_cart']").click()
        # 7. Verify cart is empty - "Shopping Cart is Empty"
        actualEmpty1 = driver.find_element(By.TAG_NAME, "h1").text
        actualEmpty2 = driver.find_element(By.XPATH, "//div[@class='cart-empty']/p[1]").text
        if (expectedEmpty1 in actualEmpty1) and (expectedEmpty2 in actualEmpty2):
            print("Successful Test - Passed")
        else:
            raise NoEmptyCart
    except NoErrorQTYCart:
        print("No error when updating over quantity.")
    except NoEmptyCart:
        print("Cart is not empty")
    except Exception as error:
        print("Other Exception: " + str(error))

def main():
    utils = Util()
    testcase3(utils.driver, utils.url)
    utils.driver.quit()

main()