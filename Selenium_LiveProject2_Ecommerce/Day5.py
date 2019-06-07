"""
Test Case:
Verify that you can create an account and share wishlist to other people using email

Steps:
1. Go to http://live.guru99.com/index.php/
2. Click on My Account link (bottom)
3. Click Create Account and fill in User Information
4. Click Register
5. Verify Registration is done - EXPECTED: Account Registration done
6. Go to TV menu
7. Add product to wish list
8. Click Share Wishlist
9. Enter in email and message and click share wishlist
10. Verify wishlist is shared - EXPECTED: Wishlist Shared Successfully

Test Data:
product = LG LCD

First Name = test, Middle Name = t, Last Name = test, Password = , email =
shareemail =
"""
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

class Error(Exception):
    pass
class RegistrationError(Error):
    pass
class WishlistError(Error):
    pass

class Util():
    def __init__(self):
        driverlocation = ""
        self.driver = webdriver.Chrome(driverlocation)
        self.url = "http://live.guru99.com/index.php/"
# Steps 2. - 5.
def verify_registration(driver):
    # 2. Click on My Account
    driver.find_element(By.XPATH, "//div[@class='footer-container']//a[@title='My Account']").click()
    time.sleep(1)
    # 3. Click Create Account and fill in User Information
    first_name = "test"
    middle_name = "t"
    last_name = "test"
    password = ""
    email = ""
    driver.find_element(By.XPATH, "//a[@title='Create an Account']").click()
    driver.find_element(By.XPATH, "//input[@id='firstname']").send_keys(first_name)
    driver.find_element(By.XPATH, "//input[@id='middlename']").send_keys(middle_name)
    driver.find_element(By.XPATH, "//input[@id='email_address']").send_keys(email)
    driver.find_element(By.XPATH, "//input[@id='lastname']").send_keys(last_name)
    driver.find_element(By.XPATH, "//input[@id='password']").send_keys(password)
    driver.find_element(By.XPATH, "//input[@id='confirmation']").send_keys(password)  # Confirm PW
    time.sleep(3)
    # 4. Click Register
    driver.find_element(By.XPATH, "//button[@title='Register']").click()
    time.sleep(3)
    # 5. Verify Registration is done - EXPECTED: Account Registration done
    expected_regmsg = "thank you for registering with main website store."
    actual_regmsg = str(driver.find_element(By.XPATH,"//li[@class='success-msg']//span").text).lower()
    if expected_regmsg == actual_regmsg:
        print("PASS: Account Registration Successful")
    else:
        raise RegistrationError

# Steps 6. - 10.
def verify_wishlist(driver):
    share_email = ""
    expectedWishlist = "your wishlist has been shared."
    # 6. Go to TV menu
    driver.find_element(By.XPATH, "//a[text()='TV']").click()
    time.sleep(2)
    # 7. Add product to wish list product = LG LCD
    driver.find_element(By.XPATH, "//a[@title='LG LCD']//following-sibling::div//a[@class='link-wishlist']").click()
    time.sleep(2)
    # 8. Click Share Wishlist
    driver.find_element(By.XPATH, "//span[text()='Share Wishlist']").click()
    time.sleep(2)
    # 9. Enter in email and message and click share wishlist
    driver.find_element(By.XPATH, "//textarea[@id='email_address']").send_keys(share_email)
    time.sleep(2)
    driver.find_element(By.XPATH, "//button[@title='Share Wishlist']").click()
    # 10. Verify wishlist is shared - EXPECTED: Wishlist Shared Successfully
    actualWishlist = str(driver.find_element(By.XPATH,"//li[@class='success-msg']//span").text).lower()
    if expectedWishlist == actualWishlist:
        print("PASS: Wishlist shared")
        print("Success Test - END")
    else:
        raise WishlistError

def testcase5(driver, url):
    driver.implicitly_wait(3)
    # 1. Go to http://live.guru99.com/index.php/
    driver.get(url)
    try:
        # Steps 2. - 5.
        verify_registration(driver)
        # Steps 6. - 10.
        verify_wishlist(driver)
    except RegistrationError:
        print("RegistrationError")
    except WishlistError:
        print("WishlistError")

def main():
    utils = Util()
    testcase5(utils.driver, utils.url)
    utils.driver.quit()

main()