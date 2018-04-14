from selenium import webdriver
import unittest
import time


unit_test = unittest.TestCase


browser = webdriver.Chrome('C:\\Users\\vahid\\Desktop\\chromedriver.exe')
browser.get("file:///D:/Sharif/Term/SAD/gspaid/documents/design/wireframe/general/home.html")

time.sleep(3)
name = browser.find_element_by_id("name")
email = browser.find_element_by_id("email")
description = browser.find_element_by_id("description")
name.send_keys("vahid")
email.send_keys("1")
description.send_keys("slala")

# time.sleep(10)
submit_attempt = browser.find_element_by_xpath("//*[@type='submit']")
submit_attempt.submit()

