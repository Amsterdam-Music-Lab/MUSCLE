import random
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from tests.base_test import BaseTest


class TestBeatAlignment(BaseTest):

    def test_beatalignment(self):
        block_name = "beat_alignment"
        block_slug = self.config['block_slugs'][block_name]
        self.driver.get(f"{self.base_url}/block/{block_slug}")

        self.check_for_error(block_name, block_slug)

        WebDriverWait(self.driver, 5).until(expected_conditions.element_to_be_clickable((By.XPATH, '//button[text()="Ok"]'))).click()

        WebDriverWait(self.driver, 45).until(expected_conditions.element_to_be_clickable((By.XPATH, '//button[text()="Start"]'))).click()

        btn1 = '//label[text()="ALIGNED TO THE BEAT"]'
        btn2 = '//label[text()="NOT ALIGNED TO THE BEAT"]'
        current_round = 1

        while self.driver.find_element(By.TAG_NAME, "h4").text != "END":
            btn = random.choice([btn1, btn2])
            WebDriverWait(self.driver, 45).until(expected_conditions.element_to_be_clickable((By.XPATH, btn))).click()
            print(f"Round {current_round}")
            current_round += 1
            time.sleep(1)

        end_heading = self.driver.find_element(By.TAG_NAME, "h4").text == "END"
        if not end_heading:
            raise Exception("End heading not found")
        print("\n✅ Beat Alignment Test completed!")
