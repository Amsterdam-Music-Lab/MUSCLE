from config.init_selenium import InitSelenium
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import sys
import time

# Run this script from the terminal:
# docker-compose run selenium bash -c "python example_script.py"

# initialize webdriver
driver = InitSelenium().setup_chrome()

try:
    driver.get('http://client:3000/cat')

    for entry in driver.get_log('browser'):
        print(entry)
    time.sleep(1)
    element = driver.find_element(By.TAG_NAME, "body")
    print(element.text)
    driver.close()
except:  # pylint: disable=bare-except
    sys.exit('Something went wrong')
