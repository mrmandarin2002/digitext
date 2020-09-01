import time

from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium import webdriver

opts = Options()
opts.add_argument("--disable-notifications")
browser = Chrome(executable_path=r'C:\chromedriver.exe', options=opts)
browser.get("https://www.ruggedtabletpc.com/barcode-generator")
browser.get("https://www.ruggedtabletpc.com/barcode-generator")
time.sleep(1)


selection_dot = browser.find_element_by_css_selector("input[type='radio'][value='CODE_128']").click()

time.sleep(20)