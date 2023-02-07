from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import sys

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument('--verbose')
chrome_options.add_argument("--disable-web-security")
chrome_options.add_argument("--disable-site-isolation-trials")
chrome_options.add_argument("--disable-xss-auditor")
chrome_options.add_argument("--disable-web-security")
chrome_options.add_argument("--allow-running-insecure-content")
chrome_options.add_argument("--disable-setuid-sandbox")
chrome_options.add_argument("--disable-webgl")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument('--log-level=3')
chrome_options.add_argument("no-default-browser-check")
chrome_options.add_argument(
    'user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36')
chrome_options.binary_location = '/usr/bin/google-chrome-stable'

driver = webdriver.Chrome(service=Service(
    ChromeDriverManager().install()), options=chrome_options)
try:
    driver.get('http://client:3000/cat')
    # driver.get('https://acc.amsterdammusiclab.nl/cat')
    element = driver.find_element(By.TAG_NAME, "body")
    print(element.text)
    driver.close()
except:  # pylint: disable=bare-except
    sys.exit('Something went wrong')
