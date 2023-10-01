from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.webdriver.support.select import Select
import random
import time
import unittest
import configparser
import warnings


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

    [experiment_slugs]
    beat_alignment=bat
    eurovision=ev
    ```

    Run tests:
    python tests-selenium.py
    """
  
    def setUp(self):

        warnings.simplefilter("ignore", ResourceWarning)

        self.config = configparser.ConfigParser()
        self.config.read('tests-selenium.ini')

        browser = self.config['selenium']['browser'] 
        headless = self.config['selenium']['headless'] == "yes"

        if browser == "Firefox":
            options = webdriver.FirefoxOptions()
            if headless: options.add_argument("-headless")
            self.driver = webdriver.Firefox(options=options)
        elif browser == "Chrome":
            options = webdriver.ChromeOptions()
            if headless: options.add_argument("--headless=new")
            driver = webdriver.Chrome(options=options)
        elif browser == "Safari":
            options = webdriver.safari.options.Options()
            driver = webdriver.Safari(options=options)
        elif browser == "Edge":
            options = webdriver.EdgeOptions()
            if headless: options.add_argument("--headless=new")
            driver = webdriver.Edge(options=options)
        else:
            raise Exception("Unknown browser")

        self.driver.set_window_size(1920, 1080)

  
    def tearDown(self):
        self.driver.quit()
        #warnings.simplefilter("default", ResourceWarning)

    def test_beatalignment(self):

        self.driver.get("{}/{}".format(self.config['url']['root'], self.config['experiment_slugs']['beat_alignment']))
        
        # Explainer
        self.driver.find_element(By.XPATH, "//div[text()='Ok']").click()

        # If consent present, agree
        if self.driver.find_element(By.TAG_NAME,"h4").text.lower() == "informed consent":
            self.driver.find_element(By.XPATH, '//div[text()="I agree"]').click()
        
        # Wait for examples to end and click Start
        WebDriverWait(self.driver, 60,  poll_frequency = 1) \
            .until(expected_conditions.element_to_be_clickable((By.XPATH, '//div[text()="Start"]'))) \
            .click()

        btn1 = '//label[text()="ALIGNED TO THE BEAT"]'
        btn2 = '//label[text()="NOT ALIGNED TO THE BEAT"]'
        
        while self.driver.find_element(By.TAG_NAME,"h4").text != "END":
            btn = random.choice([btn1, btn2]) # randomly pick a button to click
            WebDriverWait(self.driver, 30,  poll_frequency = 1) \
                .until(expected_conditions.element_to_be_clickable((By.XPATH, btn))) \
                .click()


    def test_eurovision(self):
    
        self.driver.get("{}/{}".format(self.config['url']['root'], self.config['experiment_slugs']['eurovision']))

        # Explainer
        self.driver.find_element(By.XPATH, "//div[text()=\"Let's go!\"]").click()

        # If consent present, agree
        if self.driver.find_element(By.TAG_NAME,"h4").text.lower() == "informed consent":
            self.driver.find_element(By.XPATH, '//div[text()="I agree"]').click()

        h4_text = None
        bonus_rounds = False

        while True: 

            if h4_text == None: time.sleep(1)
            h4_text = WebDriverWait(self.driver, 1).until(presence_of_element_located((By.TAG_NAME,"h4"))).text

            if "ROUND " in h4_text:

                for i in range(2):
                    ans = random.choices(["Yes", "No", "No response"], weights=(40,40,20))[0]

                    if ans in ("Yes", "No"):
                        WebDriverWait(self.driver, 6) \
                            .until(presence_of_element_located((By.XPATH, '//*[text()="{}"]'.format(ans)))) \
                            .click()
                    if ans in ("No","No response") or bonus_rounds: break


                WebDriverWait(self.driver, 25, poll_frequency = 1) \
                    .until(presence_of_element_located((By.XPATH, '//*[text()="Next"]'))) \
                    .click()
          
            elif h4_text == "QUESTIONNAIRE":

                if self.driver.find_elements(By.CLASS_NAME, "aha__radios"):
                    self.driver.find_element(By.CSS_SELECTOR, ".radio:nth-child(1)").click()
            
                if self.driver.find_elements(By.TAG_NAME, "select"):
                    select = Select(self.driver.find_element(By.TAG_NAME, 'select'))
                    select.select_by_value('nl')
                    #select.select_by_index(1)

                if self.driver.find_elements(By.CLASS_NAME, "aha__text-range"):
                    self.driver.find_element(By.CSS_SELECTOR, ".rangeslider").click()

                els = self.driver.find_elements(By.CSS_SELECTOR, "input[type='text']")
                if els: els[0].send_keys("Trumpet")

                # Click Continue after question answered
                self.driver.find_element(By.XPATH,  '//*[text()="Continue"]').click()
                 
            elif h4_text == "FINAL SCORE":
                break

            elif self.driver.find_element(By.CSS_SELECTOR,"h3").text == "Bonus Rounds":
                self.driver.find_element(By.XPATH,  '//*[text()="Continue"]').click()
                bonus_rounds = True

            else: 
                raise Exception("Unknown view")

        self.driver.find_element(By.XPATH,  '//*[text()="Play again"]')


if __name__ == '__main__':
    unittest.main()
