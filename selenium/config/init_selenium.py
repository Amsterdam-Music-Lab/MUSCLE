from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


class InitSelenium():
    """Init Selenium

    attributes: driver    
    """
    driver = None

    def setup_chrome(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument('--verbose')
        self.driver = webdriver.Chrome(service=Service(
            ChromeDriverManager().install()), options=chrome_options)
        return self.driver