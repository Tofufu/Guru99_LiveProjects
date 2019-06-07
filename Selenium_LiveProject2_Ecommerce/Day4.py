"""
Test Case:
- Verify whether able to compare 2 products
Steps:
1. Go to http://live.guru99.com/index.php/
2. Click MOBILE
3. Click "add to compare" for 2 mobile phones
4. Click COMPARE
5. Verify popup window comes up and that the correct products show up w/ heading "compared products"
6. Verify that the selected products are present
7. Close popup window

Phones: Sony Xperia / Iphone
"""
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# User Defined Exceptions
class Error(Exception):
    pass
class PopUpWindowError(Error):
    pass

class Util():
    def __init__(self):
        driverlocation = ""
        self.driver = webdriver.Chrome(driverlocation)
        self.url = "http://live.guru99.com/index.php/"

def testcase4(driver, url):
    try:
        phone1 = "Xperia"
        phone2 = "IPhone"
        # 1. Go to http://live.guru99.com/index.php/
        driver.get(url)
        driver.maximize_window()
        # 2. Click MOBILE
        driver.find_element(By.XPATH, "//a[text()='Mobile']").click()
        # 3. Click "add to compare" for 2 mobile phones
        # This will "refresh the page" and on the top right will say "Xperia" for the list of compare
        phone1XPATH = "//a[@title='" + phone1 + "']//following-sibling::div/div[@class='actions']//a[@class='link-compare']"
        driver.find_element(By.XPATH, phone1XPATH).click()
        time.sleep(2)
        phone2XPATH = "//a[@title='" + phone2 + "']//following-sibling::div/div[@class='actions']//a[@class='link-compare']"
        driver.find_element(By.XPATH, phone2XPATH).click()
        time.sleep(2)
        # 4. Click COMPARE and save product names (used for step 6 to verify popup window)
        driver.find_element(By.XPATH, "//button[@title='Compare']").click()
        expectedPhone1 = str(driver.find_elements(By.XPATH, "//p[@class='product-name']/a")[0].text).lower() # Sony xperia
        expectedPhone2 = str(driver.find_elements(By.XPATH, "//p[@class='product-name']/a")[1].text).lower() # iphone

        # 5. Verify popup window comes up and that the correct products show up w/ heading "compared products"
        parentWindow = driver.current_window_handle  # parent handle = parent window = current window
        allWindows = driver.window_handles
        # if the window did indeed open up there should be 2 windows
        if len(allWindows) == 2:
            for window in allWindows:
                if window != parentWindow:
                    driver.switch_to.window(window)
                    expectedTitle = "compare products"
                    actualTitle = str(driver.find_element(By.TAG_NAME, "h1").text).lower()
                    time.sleep(1)
                    # verifying title of popup
                    if expectedTitle == actualTitle:
                        # 6. Verify that the selected products are present from step 4
                        actualPhone1 = str(driver.find_elements(By.XPATH, "//h2/a")[0].text).lower()
                        actualPhone2 = str(driver.find_elements(By.XPATH, "//h2/a")[1].text).lower()
                        if (actualPhone1 == expectedPhone1) and (actualPhone2 == expectedPhone2):
                            print("PASS: Pop up window title = compare products and products are selected properly")
                            # 7. Close popup window
                            driver.close()
                            break
                        else:
                            raise PopUpWindowError("Fail: Different Items in Pop Up Window: {} and {}".format(actualPhone1, actualPhone2))
                    else:
                        raise PopUpWindowError("Fail: Pop up window title wrong: " + actualTitle)
        else:
            raise PopUpWindowError("FAIL: No pop up window opened")
        time.sleep(1)
        # After closing popup go back to parent window and then it will go to driver.quit()
        driver.switch_to.window(parentWindow)
    except PopUpWindowError as error:
        print("PopUpWindowError: " + str(error))

def main():
    utils = Util()
    testcase4(utils.driver, utils.url)
    utils.driver.quit()

main()