from ssl import Options
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

class TestRequirement7(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Class-level setup for WebDriver and logging."""
        log_filename = 'RQ7_test_execution.log'
        logging.basicConfig(
            filename=log_filename,
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        logging.info('Test for Requirement7 started.')

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
        time.sleep(3)

    def test_keyword_and_interact(self):
        """Test adding a keyword, interacting with it, and scrolling functionality."""
        driver = self.driver

        # Step 1: Add a new keyword
        logging.info('Testing adding a new keyword.')
        nk = driver.find_element(By.CSS_SELECTOR, '#newKeyword')
        self.assertIsNotNone(nk, "New keyword input field not found.")
        nk.send_keys('Best AI coding Tools')
        logging.info('Entered "Best AI coding Tools" in the newKeyword input field.')
        time.sleep(2)

        ak = driver.find_element(By.CSS_SELECTOR, '#addKeywordButton')
        self.assertIsNotNone(ak, "Add Keyword button not found.")
        ak.click()
        logging.info('Clicked the "Add Keyword" button.')
        time.sleep(3)

        # Verify that the keyword button is added
        kw6 = driver.find_element(By.CSS_SELECTOR, 'button.keyword-btn:nth-child(6)')
        self.assertIsNotNone(kw6, "6th keyword button was not added.")
        logging.info('Verified that the 6th keyword button is present.')

        # Step 2: Click the new keyword button
        kw6.click()
        logging.info('Clicked the 6th keyword button.')
        time.sleep(5)

        # Step 3: Scroll down the page
        logging.info('Testing scroll down actions.')
        for _ in range(50):
            driver.execute_script("window.scrollBy(0, 100);")
            time.sleep(0.1)

        current_scroll = driver.execute_script("return window.scrollY;")
        logging.info(f'Current scroll position after scrolling down: {current_scroll}')
        self.assertGreater(current_scroll, 0, "Scroll down did not work.")

        # Step 4: Scroll up the page
        logging.info('Testing scroll up actions.')
        for _ in range(50):
            driver.execute_script("window.scrollBy(0, -100);")
            time.sleep(0.1)

        new_scroll = driver.execute_script("return window.scrollY;")
        logging.info(f'Current scroll position after scrolling up: {new_scroll}')
        self.assertEqual(new_scroll, 0, "Scroll up did not return to the top.")

        logging.info('Test completed successfully.')

    @classmethod
    def tearDownClass(cls):
        """Class-level cleanup to close WebDriver."""
        cls.driver.quit()
        logging.info('WebDriver closed, test completed.')


if __name__ == '__main__':
    unittest.main()
