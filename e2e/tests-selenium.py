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

        print(f"Running tests on {self.base_url}")

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

        print("Google (and thus the internet) is working!")

    def test_beatalignment(self):

        experiment_name = "beat_alignment"

        try:

            experiment_slug = self.config['experiment_slugs'][experiment_name]
            self.driver.get(f"{self.base_url}/{experiment_slug}")

            # if page body contains the word "Error", raise an exception
            self.check_for_error(experiment_name, experiment_slug)

            # Wait for ok button to appear and click it
            WebDriverWait(self.driver, 5,  poll_frequency=1) \
                .until(expected_conditions.element_to_be_clickable((By.XPATH, '//button[text()="Ok"]'))) \

            # Explainer
            ok_button = self.driver.find_element(By.XPATH, "//button[text()='Ok']")

            if not ok_button:
                raise Exception("Ok button not found")

            ok_button.click()

            # Wait for examples to end and click Start
            WebDriverWait(self.driver, 45,  poll_frequency=1) \
                .until(expected_conditions.element_to_be_clickable((By.XPATH, '//button[text()="Start"]'))) \
                .click()

            btn1 = '//label[text()="ALIGNED TO THE BEAT"]'
            btn2 = '//label[text()="NOT ALIGNED TO THE BEAT"]'

            print("Starting BAT rounds...")

            current_round = 1

            while self.driver.find_element(By.TAG_NAME, "h4").text != "END":
                # randomly pick a button to click
                btn = random.choice([btn1, btn2])
                WebDriverWait(self.driver, 45,  poll_frequency=3) \
                    .until(expected_conditions.element_to_be_clickable((By.XPATH, btn))) \

                btn_element = self.driver.find_element(By.XPATH, btn)

                # click the button if it exists and is clickable
                if btn_element and "disabled" not in btn_element.get_attribute("class"):
                    print(f"Round {current_round}")
                    btn_element.click()
                    current_round += 1

                # wait 1 second
                time.sleep(1)

            print("BAT rounds completed")

            # Check if the final score is displayed
            end_heading = self.driver.find_element(By.TAG_NAME, "h4").text == "END"

            if not end_heading:
                raise Exception("End heading not found")

            print("Beat Alignment Test completed!")

        except Exception as e:
            self.handle_error(e, experiment_name)

    def test_eurovision(self):

        experiment_name = "eurovision"

        try:

            experiment_slug = self.config['experiment_slugs'][experiment_name]
            self.driver.get(f"{self.base_url}/{experiment_slug}")

            # if page body contains the word "Error", raise an exception
            self.check_for_error(experiment_name, experiment_slug)

            # Check & Agree to Informed Consent
            self.agree_to_consent()

            # Explainer
            WebDriverWait(self.driver, 5,  poll_frequency=1) \
                .until(expected_conditions.element_to_be_clickable((By.XPATH, '//button[text()="Let\'s go!"]'))) \
                .click()

            print("Let's go! button clicked")

            h4_text = None
            bonus_rounds = False

            while True:

                if h4_text is None:
                    time.sleep(1)

                h4_text = WebDriverWait(self.driver, 5).until(expected_conditions.presence_of_element_located((By.TAG_NAME,"h4"))).text

                print(f"Round {h4_text} started...")
                
                if "ROUND " in h4_text:

                    for i in range(2):
                        ans = random.choices(["Yes", "No", "No response"], weights=(40, 40, 20))[0]

                        if ans in ("Yes", "No"):
                            WebDriverWait(self.driver, 6) \
                                .until(presence_of_element_located((By.XPATH, '//*[text()="{}"]'.format(ans)))) \
                                .click()

                            print(f"Round {h4_text} - {ans}")

                        if ans in ("No", "No response") or bonus_rounds:
                            print(f"Round {h4_text} - Continue")
                            break

                        # wait for next page to load
                        time.sleep(1)

                    WebDriverWait(self.driver, 25, poll_frequency=1) \
                        .until(presence_of_element_located((By.XPATH, '//*[text()="Next"]'))) \
                        .click()

                    print(f"Round {h4_text} - Next")

                    # wait for next page to load
                    time.sleep(1)

                elif h4_text == "QUESTIONNAIRE":

                    # get .aha__question h3 text
                    h3_text = self.driver.find_element(By.CSS_SELECTOR, ".aha__question h3").text
                    print(f"Questionnaire - {h3_text}")

                    if self.driver.find_elements(By.CLASS_NAME, "aha__radios"):
                        self.driver.find_element(By.CSS_SELECTOR, ".radio:nth-child(1)").click()
                        print("Radio button picked (1)")

                    if self.driver.find_elements(By.TAG_NAME, "select"):
                        select = Select(self.driver.find_element(By.TAG_NAME, 'select'))
                        select.select_by_value('nl')
                        print("Select option 'nl' picked")

                    if self.driver.find_elements(By.CLASS_NAME, "aha__text-range"):
                        self.driver.find_element(By.CSS_SELECTOR, ".rangeslider").click()
                        print("Range slider clicked")

                    other_input = self.driver.find_elements(By.CSS_SELECTOR, "input[type='text']")

                    if other_input:
                        other_input[0].send_keys("Trumpet")
                        print("Text input filled with 'Trumpet'")

                    # Click Continue after question answered
                    WebDriverWait(self.driver, 5,  poll_frequency=1) \
                        .until(expected_conditions.element_to_be_clickable((By.XPATH, '//button[text()="Continue"]'))) \
                        .click()

                    print("Continue button clicked")

                    # wait for next page to load
                    time.sleep(1)

                elif h4_text == "FINAL SCORE":
                    break

                elif self.driver.find_element(By.CSS_SELECTOR, "h3").text == "Bonus Rounds":
                    WebDriverWait(self.driver, 5,  poll_frequency=1) \
                        .until(expected_conditions.element_to_be_clickable((By.XPATH, '//button[text()="Continue"]'))) \
                        .click()

                    bonus_rounds = True

                    print("Bonus Rounds - Continue")

                    # wait for next page to load
                    time.sleep(1)

                else:
                    raise Exception("Unknown view")

            self.driver.find_element(By.XPATH,  '//*[text()="Play again"]')

            print("Eurovision Test completed!")

        except Exception as e:
            self.handle_error(e, experiment_name)

    def test_categorization(self):

        experiment_name = "categorization"

        try:
            self.driver.delete_all_cookies()

            experiment_slug = self.config['experiment_slugs'][experiment_name]
            self.driver.get(f"{self.base_url}/{experiment_slug}")

            # if page body contains the word "Error", raise an exception
            self.check_for_error(experiment_name, experiment_slug)

            # wait until h4 element is present and contains "INFORMED CONSENT" text (case-insensitive)
            WebDriverWait(self.driver, 5) \
                .until(lambda x: "informed consent" in x.find_element(By.TAG_NAME, "h4").text.lower())

            # click "I agree" button
            i_agree_button = self.driver.find_element(By.XPATH, '//button[text()="I agree"]')
            i_agree_button.click()

            # Explainer 1
            WebDriverWait(self.driver, 5) \
                .until(presence_of_element_located((By.XPATH, "//button[text()=\"Ok\"]"))) \
                .click()

            # What is your age?
            age_input = WebDriverWait(self.driver, 3).until(presence_of_element_located((By.CSS_SELECTOR,"input[type='number']")))
            age_input.send_keys(18)
            self.driver.find_element(By.XPATH,  '//*[text()="Continue"]').click()

            # What is your gender
            WebDriverWait(self.driver, 3).until(presence_of_element_located((By.CSS_SELECTOR,".radio:nth-child(1)"))).click()
            self.driver.find_element(By.XPATH,  '//*[text()="Continue"]').click()

            # What is your native language
            WebDriverWait(self.driver, 3).until(presence_of_element_located((By.TAG_NAME, 'select')))
            select = Select(self.driver.find_element(By.TAG_NAME, 'select'))
            select.select_by_value('nl')

            # Wait for the Continue button to appear and click it
            WebDriverWait(self.driver, 5) \
                .until(presence_of_element_located((By.XPATH,  '//*[text()="Continue"]'))) \
                .click()

            # Please select your level of musical experience
            WebDriverWait(self.driver, 5) \
                .until(presence_of_element_located((By.CSS_SELECTOR, ".radio:nth-child(1)"))).click()

            WebDriverWait(self.driver, 5) \
                .until(presence_of_element_located((By.XPATH,  '//button[text()="Continue"]'))) \
                .click()

            # Explainer 2
            WebDriverWait(self.driver, 5) \
                .until(presence_of_element_located((By.XPATH, "//button[text()=\"Ok\"]"))) \
                .click()

            training_rounds = 20
            testing_rounds = 80
            training = True
            for n in (training_rounds, testing_rounds):

                round_type = "training" if n == training_rounds else "testing"

                print(f"Starting {round_type} rounds...")

                for i in range(n):

                    # wait .5 second
                    time.sleep(.5)

                    WebDriverWait(self.driver, 5) \
                        .until(
                            presence_of_element_located((By.CSS_SELECTOR, ".aha__play-button")) and
                            expected_conditions.element_to_be_clickable((By.CSS_SELECTOR, ".aha__play-button"))) \
                        .click()

                    print('Round', i + 1, "Play button clicked")

                    round_heading = WebDriverWait(self.driver, 10) \
                        .until(presence_of_element_located((By.TAG_NAME, "h4"))).text

                    print(f"{round_type.capitalize()} round {i + 1} - {round_heading}")

                    expected_response = self.driver.execute_script('return document.querySelector(".expected-response").textContent')
                    input_element = self.driver.execute_script(f'return document.querySelector(\'input[value="{expected_response}"]\')')
                    button_to_click = self.driver.execute_script(f'return document.querySelector(\'input[value="{expected_response}"]\').parentElement')

                    # wait for label + input to not be disabled
                    WebDriverWait(self.driver, 5) \
                        .until(lambda x: False if input_element.get_attribute("disabled") else input_element) \

                    WebDriverWait(self.driver, 5) \
                        .until(lambda x: False if "disabled" in button_to_click.get_attribute("class") else button_to_click) \
                        .click()

                    print(f"{round_type.capitalize()} round {i + 1} - Answer {expected_response} clicked")

                    # The score is only consistently shown during training rounds
                    if training:

                        print("Waiting for score...")

                        # wait for Score to appear
                        WebDriverWait(self.driver, 5) \
                            .until(presence_of_element_located((By.CSS_SELECTOR, ".aha__score")))

                        # wait for Score to disappear (next round)
                        WebDriverWait(self.driver, 5) \
                            .until(lambda x: False if x.find_elements(By.CSS_SELECTOR, ".aha__score") else True)

                if training:
                    WebDriverWait(self.driver, 5) \
                        .until(presence_of_element_located((By.XPATH, "//button[text()=\"Ok\"]"))) \
                        .click()
                    training = False

        except Exception as e:
            self.handle_error(e, experiment_name)

    def agree_to_consent(self, h4_text='informed consent', button_text='I agree'):
        # If consent present, agree
        informed_consent_heading = WebDriverWait(self.driver, 5,  poll_frequency=1) \
            .until(lambda x: h4_text in x.find_element(By.TAG_NAME, "h4").text.lower())

        if not informed_consent_heading:
            raise Exception("Informed consent not found")

        WebDriverWait(self.driver, 5,  poll_frequency=1) \
            .until(expected_conditions.element_to_be_clickable((By.XPATH, f'//button[text()="{button_text}"]'))) \
            .click()

        print("I agree button clicked")

    def check_for_error(self, experiment_name, experiment_slug='[no slug provided]'):
        if "Error" in self.driver.find_element(By.TAG_NAME, "body").text:
            raise Exception(f"Could not load {experiment_name} experiment, please check the server logs and make sure the slug ({experiment_slug}) is correct.")

    def take_screenshot(self, experiment_name, notes=""):
        current_time = time.strftime("%Y-%m-%d-%H-%M-%S")
        screen_shot_path = f"screenshots/{experiment_name}-{current_time}.png"
        print('Capturing screenshot to', screen_shot_path, notes)
        self.driver.get_screenshot_as_file(screen_shot_path)

    def handle_error(self, e, experiment_name):
        self.take_screenshot(experiment_name, str(e))
        self.fail(e)


if __name__ == '__main__':
    unittest.main()