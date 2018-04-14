from selenium import webdriver

import time

browser = webdriver.Chrome('C:\\Users\\vahid\\Desktop\\chromedriver.exe')

browser.get("https://cw.sharif.edu/login/index.php")

time.sleep(10)
username = browser.find_element_by_id("username")
password = browser.find_element_by_id("password")
username.send_keys("94105503")
password.send_keys("1")
login_attempt = browser.find_element_by_xpath("//*[@type='submit']")
login_attempt.submit()
