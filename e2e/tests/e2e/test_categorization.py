import random
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.webdriver.support.select import Select
from tests.base_test import BaseTest


class TestCategorization(BaseTest):

    def test_categorization(self):

        block_name = "categorization"

        try:
            self.driver.delete_all_cookies()

            block_slug = self.config['block_slugs'][block_name]
            self.driver.get(f"{self.base_url}/block/{block_slug}")

            # if page body contains the word "Error", raise an exception
            self.check_for_error(block_name, block_slug)

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
            self.handle_error(e, block_name)
