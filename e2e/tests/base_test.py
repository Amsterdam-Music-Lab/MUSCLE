import configparser
import os
import warnings
import unittest
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


class BaseTest(unittest.TestCase):

    def setUp(self):
        warnings.simplefilter("ignore", ResourceWarning)

        self.config = configparser.ConfigParser()
        self.config.read('config/tests-selenium.ini')
        ini_config_base_url = self.config['url']['root']
        self.base_url = os.getenv('BASE_URL', ini_config_base_url)

        browser = self.config['selenium']['browser']
        headless = self.config['selenium']['headless'] == "yes"

        if browser == "Firefox":
            options = webdriver.FirefoxOptions()
            if headless:
                options.add_argument("-headless")
            self.driver = webdriver.Firefox(options=options)
        elif browser == "Chrome":
            options = webdriver.ChromeOptions()
            options.binary_location = '/usr/bin/chromium'
            if headless:
                options.add_argument("--headless")
            self.driver = webdriver.Chrome(
                options=options,
                executable_path='/usr/bin/chromedriver'
            )
        elif browser == "Chromium":
            options = webdriver.ChromeOptions()
            options.binary_location = '/usr/bin/chromium'
            if headless:
                options.add_argument("--no-sandbox")
                options.add_argument("--headless")
            service = Service('/usr/bin/chromedriver')
            self.driver = webdriver.Chrome(service=service, options=options)
        elif browser == "Safari":
            options = webdriver.safari.options.Options()
            self.driver = webdriver.Safari(options=options)
        elif browser == "Edge":
            options = webdriver.EdgeOptions()
            if headless:
                options.add_argument("--headless=new")
            self.driver = webdriver.Edge(options=options)
        else:
            raise Exception("Unknown browser")

        self.driver.set_window_size(1920, 1080)

    def tearDown(self):
        self.driver.quit()

    def agree_to_consent(self, h4_text='informed consent', button_text='I agree'):
        # If consent present, agree
        informed_consent_heading = WebDriverWait(
            self.driver, 5,
            poll_frequency=1
        ).until(
            lambda x: h4_text in x.find_element(By.TAG_NAME, "h4").text.lower()
        )

        if not informed_consent_heading:
            raise Exception("Informed consent not found")

        WebDriverWait(self.driver, 5,  poll_frequency=1) \
            .until(expected_conditions.element_to_be_clickable((By.XPATH, f'//button[text()="{button_text}"]'))) \
            .click()

        print("I agree button clicked")

    def check_for_error(self, block_name, block_slug='[no slug provided]'):
        if "Error" in self.driver.find_element(By.TAG_NAME, "body").text:
            raise Exception(f"Could not load {block_name} experiment, please check the server logs and make sure the slug ({block_slug}) is correct.")

    def take_screenshot(self, block_name, notes=""):
        current_time = time.strftime("%Y-%m-%d-%H-%M-%S")
        screen_shot_path = f"screenshots/{block_name}-{current_time}.png"
        print('Capturing screenshot to', screen_shot_path, notes)
        self.driver.get_screenshot_as_file(screen_shot_path)

    def handle_error(self, e, block_name):
        self.take_screenshot(block_name, str(e))
        self.fail(e)
