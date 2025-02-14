import unittest
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.chrome.options import Options


# Set up Chrome options to disable GPU
chrome_options = Options()
chrome_options.add_argument("--disable-gpu")

class TestRequirement5(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Class-level setup for WebDriver and logging."""
        log_filename = 'RQ5_test_execution.log'
        logging.basicConfig(
            filename=log_filename,
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        logging.info('Test for Requirement5 started.')

        # Initialize WebDriver
        cls.driver = webdriver.Chrome(
           service=Service(r'C:/Users/user/Downloads/chromedriver/chromedriver-win64/chromedriver.exe')
        )
        cls.driver.implicitly_wait(10)
        logging.info('WebDriver initialized.')

    def setUp(self):
        """Test-level setup to navigate to the webpage."""
        self.driver = self.__class__.driver
        self.driver.get('C:/Users/user/Desktop/SQA/SQA_GROUP1-CW2/SQATube_Group1/index.html')
        logging.info('Navigated to SQATube webpage.')

    def test_scroll_and_keyword_interaction(self):
        """Test scrolling actions and keyword button interactions."""
        driver = self.driver

        # Scroll down
        logging.info('Starting scroll down actions.')
        for _ in range(50):
            driver.execute_script("window.scrollBy(0, 100);")
            time.sleep(0.1)

        # Verify scroll down
        current_scroll = driver.execute_script("return window.scrollY;")
        self.assertGreater(current_scroll, 0, "Scroll down did not work.")

        # Scroll up
        for _ in range(50):
            driver.execute_script("window.scrollBy(0, -100);")
            time.sleep(0.1)
        new_scroll = driver.execute_script("return window.scrollY;")
        self.assertEqual(new_scroll, 0, "Scroll up did not return to the top.")

        # Keyword interaction
        kw1 = driver.find_element(By.CSS_SELECTOR, 'button.keyword-btn:nth-child(1)')
        self.assertIsNotNone(kw1, "First keyword button not found.")
        driver.execute_script("arguments[0].click();", kw1)

    @classmethod
    def tearDownClass(cls):
        """Class-level cleanup to close WebDriver."""
        cls.driver.quit()
        logging.info('WebDriver closed, test completed.')

if __name__ == '__main__':
    unittest.main()
