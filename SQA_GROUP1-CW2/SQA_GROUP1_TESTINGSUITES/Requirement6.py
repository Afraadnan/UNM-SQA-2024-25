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

class TestRequirement6(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Class-level setup for WebDriver and logging."""
        log_filename = 'RQ6_test_execution.log'
        logging.basicConfig(
            filename=log_filename,
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        logging.info('Test for Requirement6 started.')

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
        time.sleep(5)

    def test_scroll(self):
        """Test scrolling."""
        driver = self.driver

        # Scroll down
        logging.info('Starting scroll down actions.')
        for _ in range(50):
            driver.execute_script("window.scrollBy(0, 100);")
            time.sleep(0.1)

        # Verify scroll down
        current_scroll = driver.execute_script("return window.scrollY;")
        logging.info(f'Current scroll position after scrolling down: {current_scroll}')
        self.assertGreater(current_scroll, 0, "Scroll down did not work.")

        # Scroll up
        logging.info('Starting scroll up actions.')
        for _ in range(50):
            driver.execute_script("window.scrollBy(0, -100);")
            time.sleep(0.1)

        # Verify scroll up
        new_scroll = driver.execute_script("return window.scrollY;")
        logging.info(f'Current scroll position after scrolling up: {new_scroll}')
        self.assertEqual(new_scroll, 0, "Scroll up did not return to the top.")

        logging.info('Scrolling completed.')

    def test_search(self):
        """Test scrolling and search functionality."""
        driver = self.driver

        # Search for "travel"
        logging.info('Entering search term: travel.')
        src = driver.find_element(By.CSS_SELECTOR, '#search-input')
        self.assertIsNotNone(src, "Search input field not found.")
        src.send_keys('travel')
        time.sleep(3)

        btn = driver.find_element(By.CSS_SELECTOR, '#search-button')
        self.assertIsNotNone(btn, "Search button not found.")
        logging.info('Clicking search button.')
        btn.click()
        time.sleep(5)

        # Verify search results for "travel"
        logging.info('Validating search results for "travel".')
        # Add validation of results here (depends on your webpage's behavior).

        # Clear the search field
        logging.info('Clearing search field.')
        src.clear()
        time.sleep(5)

        # Search for "AI"
        logging.info('Entering search term: AI.')
        src.send_keys('AI')
        time.sleep(3)

        logging.info('Clicking search button for "AI".')
        btn.click()
        time.sleep(5)

        # Verify search results for "AI"
        logging.info('Validating search results for "AI".')
        # Add validation of results here (depends on your webpage's behavior).

    @classmethod
    def tearDownClass(cls):
        """Class-level cleanup to close WebDriver."""
        cls.driver.quit()
        logging.info('WebDriver closed, test completed.')

if __name__ == '__main__':
    unittest.main()
