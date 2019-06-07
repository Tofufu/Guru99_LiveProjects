"""
Test Case:
Verifying cost of product in LIST PAGE and its DETAIL PAGE are same
1. Go to http://live.guru99.com/index.php/
2. Click on mobile
3. In list of mobile - read Sony Xperia mobile's price
4. Click on Sony Xperia mobile
5. Read Sony Xperia mobile's price in its detail page
6. Compare value from Step 3 / Step 5

Expected Results:
Product Value in list and details = $100 same
"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
import time

# User Defined Exceptions
class Error(Exception):
    pass
class WrongPrice(Error):
    pass

class Util():
    def __init__(self):
        driverlocation = ""
        self.driver = webdriver.Chrome(driverlocation)
        self.url = "http://live.guru99.com/index.php/"

def testcase2(driver, url):
    driver.implicitly_wait(3)

    # 1. Go to http://live.guru99.com/index.php/
    driver.get(url)
    try:
        # 2. Click on mobile
        driver.find_element(By.XPATH, "//a[text()='Mobile']").click()
        time.sleep(1)
        # 3. Read Sony Xperia mobile's list price
        listPrice = driver.find_element(By.XPATH, "//a[@title='Xperia']//following-sibling::div//span[@class='price']").text
        print("This is the List Price: " + listPrice)
        # 4. Click on Sony Xperia Icon
        driver.find_element(By.XPATH, "//a[@title='Xperia']").click()
        time.sleep(1)
        # 5. Read Sony Xperia mobile's detail price
        detailPrice = driver.find_element(By.XPATH, "//span[@class='price']").text
        print("This is the Detail Price: " + detailPrice)

        if detailPrice == listPrice:
            print("TESTING DONE ALL PASS")
        else:
            raise WrongPrice("Detail Price: " + detailPrice + " List Price: " + listPrice)

    except WrongPrice as error1:
        print("They are different prices: " + str(error1))
    except Exception as error2:
        print("Other Exceptions: " + str(error2))

def main():
    utils = Util()
    testcase2(utils.driver, utils.url)
    utils.driver.quit()


main()
