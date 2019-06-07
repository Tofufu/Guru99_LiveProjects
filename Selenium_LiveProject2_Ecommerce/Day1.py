from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
import time

# User Defined Exceptions
class Error(Exception):
    pass
class WrongTitle(Error):
    pass
class WrongSort(Error):
    pass

class Util():
    def __init__(self):
        driverlocation = ""
        self.driver = webdriver.Chrome(driverlocation)
        self.url = "http://live.guru99.com/index.php/"

def testcase1(driver, url):
    driver.implicitly_wait(3)
    driver.get(url)
    expected_sortedProducts = ["IPHONE", "SAMSUNG GALAXY", "SONY XPERIA"]

    try:
        homepagetitle = driver.find_element(By.XPATH, "//h2")

        # ----------------1. Verify Title Page: "This is demo site"----------------
        if "THIS IS DEMO SITE" in homepagetitle.text:
            print("Correct Homepage Title: " + homepagetitle.text)
            # ----------------2. Click on MOBILE----------------
            time.sleep(2)
            driver.find_element(By.XPATH, "//a[text()='Mobile']").click()
            # ----------------3. Verify Title = MOBILE----------------
            mobiletitle = driver.find_element(By.TAG_NAME, "h1")
            if "MOBILE" in mobiletitle.text:
                print("Correct Mobile Title: " + mobiletitle.text)
                # 4. Select "Sort By Name"----------------
                selectMenu = driver.find_element(By.XPATH, "//div[@class='sort-by']/select[@title='Sort By']")
                selected = Select(selectMenu)
                selected.select_by_index("1")  # [Position, Name, Price]
                time.sleep(2)
                # ----------------5. Verify all 3 products sorted by name----------------
                sortedList = driver.find_elements(By.XPATH, "//h2[@class='product-name']/a")
                print(len(sortedList))
                for i in range(0, 3):
                    if expected_sortedProducts[i] != sortedList[i].text:
                        print("NOT EQUAL: " + expected_sortedProducts[i] + " " + sortedList[i].text)
                        raise WrongSort
                # Everything verified print done
                print("TESTING DONE ALL PASS")
            else:
                raise WrongTitle(mobiletitle.text)
        else:  #error
            raise WrongTitle(homepagetitle.text)
    except WrongTitle as error:
        print("FAIL: Wrong Title. Title: " + str(error))
    except WrongSort:
        print("FAIL: Wrong Sort. ")

def main():
    utils = Util()
    testcase1(utils.driver, utils.url)
    utils.driver.quit()

main()