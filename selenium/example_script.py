from config.init_selenium import InitSelenium
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import sys
import time

# Run this script from the terminal:
# docker-compose run selenium bash -c "python example_script.py"

# slug of the experiment to run this script on
SLUG = 'cat'

# Initialize selenium
selenium = InitSelenium()
# Get current server host name
HOST = selenium.host
# Get the webdriver (defaults to chrome)
driver = selenium.driver

# Example code to test selenium setup
try:
    driver.get(HOST + '/' + SLUG)
    time.sleep(1)
    element = driver.find_element(By.TAG_NAME, "body")
    print(element.text)
    driver.close()
except:  # pylint: disable=bare-except
    sys.exit('Something went wrong')
