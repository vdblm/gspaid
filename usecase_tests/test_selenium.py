from selenium import webdriver

browser = webdriver.Firefox()

browser.get("www.google.com")

browser.close()
