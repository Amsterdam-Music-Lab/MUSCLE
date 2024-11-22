import random
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.webdriver.support.select import Select
from tests.base_test import BaseTest


class TestEurovision(BaseTest):

    def test_eurovision(self):

        block_name = "eurovision"

        try:

            block_slug = self.config['block_slugs'][block_name]
            self.driver.get(f"{self.base_url}/block/{block_slug}")

            # if page body contains the word "Error", raise an exception
            self.check_for_error(block_name, block_slug)

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
            self.handle_error(e, block_name)
