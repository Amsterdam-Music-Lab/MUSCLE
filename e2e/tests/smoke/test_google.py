from tests.base_test import BaseTest


class TestGoogle(BaseTest):
    def test_google(self):
        self.driver.get("http://www.google.com")
        self.assertIn("Google", self.driver.title)
        print("Google (and thus the internet) is working!")