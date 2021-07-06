from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from config import const


def chrome():
    options = Options()
    options.add_argument('--headless')
    if chrome.driver == None:
        chrome.driver = webdriver.Chrome(const.CHROME_PATH, options=options)
    return chrome.driver
chrome.driver = None

def get_page(url):
    driver = chrome()
    driver.get(url)
    driver.implicitly_wait(10)
    return driver.page_source

def close_chrome():
    if chrome.driver != None:
        chrome.driver.quit()
        chrome.driver = None
