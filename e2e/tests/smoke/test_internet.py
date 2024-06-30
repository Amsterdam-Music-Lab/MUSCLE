from tests.base_test import BaseTest


class TestInternet(BaseTest):
    def test_internet(self):

        # Test if the internet is working by opening Google
        self.driver.get("http://www.google.com")
        self.assertIn("Google", self.driver.title)

        # Test if the internet is working by opening Cloudflare
        self.driver.get("https://www.cloudflare.com")
        self.assertIn("Cloudflare", self.driver.title)

        print("\n✅ Google & Cloudflare are available and thus the internet is working!")
