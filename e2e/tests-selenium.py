from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.webdriver.support.select import Select
import random
import time
import unittest
import configparser
import warnings
import os


class TestsSelenium(unittest.TestCase):
    """
    Install selenium on your system
    pip install selenium

    Create tests-selenium.ini file in the same directory as this file describing your setup:

    ```
    [selenium]
    browser=Firefox
    ; Firefox | Chrome | Safari | Edge

    headless=no
    ; yes | no  (headless does not work on Safari)

    [url]
    root=http://localhost:3000
    ; root url of the server, used as fallback if BASE_URL is not set

    [experiment_slugs]
    beat_alignment=bat
    eurovision=ev
    ```

    Run tests:
    python tests-selenium.py

    To skip individual tests, add `@unittest.skip` before the test
    """

    def setUp(self):

        warnings.simplefilter("ignore", ResourceWarning)

        self.config = configparser.ConfigParser()
        self.config.read('tests-selenium.ini')
        ini_config_base_url = self.config['url']['root']
        self.base_url = os.getenv('BASE_URL', ini_config_base_url)

        # Check if config is set
        if not self.config.sections():
            raise Exception("Config file not found or empty")

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

            self.driver = webdriver.Chrome(options=options, executable_path='/usr/bin/chromedriver')

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

    # This is a simple test to check if the e2e setup and the internet connection is working
    def test_google(self):
        self.driver.get("http://www.google.com")
        self.assertIn("Google", self.driver.title)

    def test_beatalignment(self):

        experiment_name = "beat_alignment"

        experiment_slug = self.config['experiment_slugs'][experiment_name]
        self.driver.get(f"{self.base_url}/{experiment_slug}")

        # if page body contains the word "Error", raise an exception
        self.check_for_error(experiment_name, experiment_slug)

        # Explainer
        ok_button = self.driver.find_element(By.XPATH, "//div[text()='Ok']")

        if not ok_button:
            raise Exception("Ok button not found")

        ok_button.click()

        heading = self.driver.find_element(By.TAG_NAME,"h4").text.lower() == "informed consent"

        if not heading:
            raise Exception("Informed consent not found")

        # If consent present, agree
        agree_button = self.driver.find_element(By.XPATH, '//div[text()="I agree"]')
        agree_button.click()

        # Wait for examples to end and click Start
        WebDriverWait(self.driver, 5,  poll_frequency = 1) \
            .until(expected_conditions.element_to_be_clickable((By.XPATH, '//div[text()="Start"]'))) \
            .click()

        btn1 = '//label[text()="ALIGNED TO THE BEAT"]'
        btn2 = '//label[text()="NOT ALIGNED TO THE BEAT"]'

        while self.driver.find_element(By.TAG_NAME,"h4").text != "END":
            btn = random.choice([btn1, btn2]) # randomly pick a button to click
            WebDriverWait(self.driver, 30,  poll_frequency = 1) \
                .until(expected_conditions.element_to_be_clickable((By.XPATH, btn))) \
                .click()

    def test_eurovision(self):

        experiment_name = "eurovision"

        experiment_slug = self.config['experiment_slugs'][experiment_name]
        self.driver.get(f"{self.base_url}/{experiment_slug}")

        # if page body contains the word "Error", raise an exception
        self.check_for_error(experiment_name, experiment_slug)

        # Explainer
        self.driver.find_element(By.XPATH, "//button[text()=\"Let's go!\"]").click()

        # If consent present, agree
        informed_consent_heading = self.driver.find_element(By.TAG_NAME,"h4").text.lower() == "informed consent"

        if not informed_consent_heading:
            raise Exception("Informed consent not found")

        i_agree_button = self.driver.find_element(By.XPATH, '//button[text()="I agree"]')
        i_agree_button.click()

        h4_text = None
        bonus_rounds = False

        while True:

            if h4_text is None:
                time.sleep(1)

            h4_text = WebDriverWait(self.driver, 1).until(presence_of_element_located((By.TAG_NAME,"h4"))).text

            if "ROUND " in h4_text:

                for i in range(2):
                    ans = random.choices(["Yes", "No", "No response"], weights=(40, 40, 20))[0]

                    if ans in ("Yes", "No"):
                        WebDriverWait(self.driver, 6) \
                            .until(presence_of_element_located((By.XPATH, '//*[text()="{}"]'.format(ans)))) \
                            .click()
                    if ans in ("No", "No response") or bonus_rounds:
                        break

                WebDriverWait(self.driver, 25, poll_frequency=1) \
                    .until(presence_of_element_located((By.XPATH, '//*[text()="Next"]'))) \
                    .click()

            elif h4_text == "QUESTIONNAIRE":

                if self.driver.find_elements(By.CLASS_NAME, "aha__radios"):
                    self.driver.find_element(By.CSS_SELECTOR, ".radio:nth-child(1)").click()

                if self.driver.find_elements(By.TAG_NAME, "select"):
                    select = Select(self.driver.find_element(By.TAG_NAME, 'select'))
                    select.select_by_value('nl')
                    #select.select_by_index(1)

                if self.driver.find_elements(By.CLASS_NAME, "aha__text-range"):
                    self.driver.find_element(By.CSS_SELECTOR, ".rangeslider").click()

                els = self.driver.find_elements(By.CSS_SELECTOR, "input[type='text']")
                if els: els[0].send_keys("Trumpet")

                # Click Continue after question answered
                self.driver.find_element(By.XPATH,  '//*[text()="Continue"]').click()

            elif h4_text == "FINAL SCORE":
                break

            elif self.driver.find_element(By.CSS_SELECTOR,"h3").text == "Bonus Rounds":
                self.driver.find_element(By.XPATH,  '//*[text()="Continue"]').click()
                bonus_rounds = True

            else:
                raise Exception("Unknown view")

        self.driver.find_element(By.XPATH,  '//*[text()="Play again"]')

    def test_categorization(self):

        experiment_name = "categorization"

        experiment_slug = self.config['experiment_slugs'][experiment_name]
        self.driver.get(f"{self.base_url}/{experiment_slug}")

        # if page body contains the word "Error", raise an exception
        self.check_for_error(experiment_name, experiment_slug)

        # Explainer 1
        self.driver.find_element(By.XPATH, "//button[text()=\"Ok\"]").click()

        # If consent present, agree
        informed_consent_heading = self.driver.find_element(By.TAG_NAME,"h4").text.lower() == "informed consent"

        if not informed_consent_heading:
            raise Exception("Informed consent not found")

        i_agree_button = self.driver.find_element(By.XPATH, '//button[text()="I agree"]')
        i_agree_button.click()

        # What is your age?
        el = WebDriverWait(self.driver, 3).until(presence_of_element_located((By.CSS_SELECTOR,"input[type='number']")))
        el.send_keys(18)
        self.driver.find_element(By.XPATH,  '//*[text()="Continue"]').click()

        # What is your gender
        self.driver.find_element(By.CSS_SELECTOR, ".radio:nth-child(1)").click()
        self.driver.find_element(By.XPATH,  '//*[text()="Continue"]').click()

        # What is your native language
        select = Select(self.driver.find_element(By.TAG_NAME, 'select'))
        select.select_by_value('nl')
        self.driver.find_element(By.XPATH,  '//*[text()="Continue"]').click()

        # Please select your level of musical experience
        self.driver.find_element(By.CSS_SELECTOR, ".radio:nth-child(1)").click()
        self.driver.find_element(By.XPATH,  '//*[text()="Continue"]').click()

        # Explainer 2
        WebDriverWait(self.driver, 10) \
            .until(presence_of_element_located((By.XPATH, "//div[text()=\"Ok\"]"))) \
            .click()

        training_rounds = 20
        testing_rounds = 80
        training = True
        for n in (training_rounds, testing_rounds):
            for i in range(n):

                WebDriverWait(self.driver, 5) \
                    .until(presence_of_element_located((By.CSS_SELECTOR, ".aha__play-button"))) \
                    .click()

                expected_response = self.driver.execute_script('return document.querySelector(".expected-response").textContent')
                button_to_click = self.driver.execute_script(f'return document.querySelector(\'input[value="{expected_response}"]\').parentElement')
                WebDriverWait(self.driver, 5) \
                    .until(lambda x: False if "disabled" in button_to_click.get_attribute("class") else button_to_click) \
                    .click()

            if training:
                WebDriverWait(self.driver, 5) \
                    .until(presence_of_element_located((By.XPATH, "//div[text()=\"Ok\"]"))) \
                    .click()
                training = False

    def check_for_error(self, experiment_name, experiment_slug='[no slug provided]'):
        if "Error" in self.driver.find_element(By.TAG_NAME, "body").text:
            raise Exception(f"Could not load {experiment_name} experiment, please check the server logs and make sure the slug ({experiment_slug}) is correct.")


if __name__ == '__main__':
    unittest.main()
