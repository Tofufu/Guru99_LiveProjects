from selenium import webdriver

class Util():
    def __init__(self):
        driverlocation = ""
        self.driver = webdriver.Chrome(driverlocation)
        self.username = ""
        self.password = ""
        self.url = "http://www.demo.guru99.com/V4/"