from tests.base_test import BaseTest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
import time


class TestTHKids(BaseTest):
    def test_th_kids(self):
        self.driver.get(f"{self.base_url}/thkids")

        dashboard = WebDriverWait(self.driver, 5).until(expected_conditions.presence_of_element_located((By.CLASS_NAME, "dashboard")))
        print("\n✅ The frontend is working and the thkids experiment page is working!")

        # self.driver.find_element(By.TAG_NAME, "h4")

        # click first link in .dashboard
        link = dashboard.find_element(By.TAG_NAME, "a")

        # get link text from h3 in a
        experiment_title = link.find_element(By.TAG_NAME, "h3").text

        # click link
        link.click()

        # wait for page to load
        WebDriverWait(self.driver, 5).until(expected_conditions.presence_of_element_located((By.TAG_NAME, "h3")))

        # assert link text is on the page
        self.assertIn(experiment_title, self.driver.page_source)

        # click the start button
        start_button = self.driver.find_element(By.XPATH, '//button[text()="Start"]')
        start_button.click()

        # wait until .circle is visible
        WebDriverWait(self.driver, 5).until(expected_conditions.visibility_of_element_located((By.CLASS_NAME, "circle")))

        # get circle text and assert it is not empty
        circle_text = self.driver.find_element(By.CLASS_NAME, "circle").text

        # wait 3 seconds and then assert that the circle text has changed (Countdown component)
        time.sleep(2)

        new_circle_text = self.driver.find_element(By.CLASS_NAME, "circle").text

        self.assertNotEqual(circle_text, new_circle_text)

        print(f"\n✅ Countdown text has changed from '{circle_text}' to '{new_circle_text}'")

        print("\n✅ The frontend is working and the thkids experiment page is working!")
