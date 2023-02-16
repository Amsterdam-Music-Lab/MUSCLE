from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import os

debug = bool(os.getenv("AML_DEBUG"))
api_root = os.getenv("API_ROOT")


class InitSelenium():
    """Init Selenium

    attributes: driver, host
    """

    driver = None
    host = None

    def setup_chrome(self):
        """Initialize chrome driver        
        """
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument('--verbose')
        self.driver = webdriver.Chrome(service=Service(
            ChromeDriverManager().install()), options=chrome_options)
        return self.driver

    def get_host(self):
        """Determine server host name for selenium
        """
        if debug is True:
            # use docker service host when running locally
            self.host = 'http://client:3000'
        else:
            self.host = api_root
        return self.host
