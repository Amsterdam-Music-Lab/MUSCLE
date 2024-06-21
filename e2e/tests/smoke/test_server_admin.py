from tests.base_test import BaseTest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


class TestServerAdmin(BaseTest):
    def test_server_admin(self):
        self.driver.get(f"{self.base_url}/server/admin")

        # assert it shows the login form
        WebDriverWait(self.driver, 5).until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR, "form")))

        # assert it shows the username input
        self.driver.find_element(By.NAME, "username")

        # assert it shows the password input
        self.driver.find_element(By.NAME, "password")

        print("\n✅ The server is running and the admin (login) page is working!")
