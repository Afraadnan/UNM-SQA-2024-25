import unittest
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from time import sleep
import time
from selenium.webdriver.chrome.options import Options


# Set up Chrome options to disable GPU
chrome_options = Options()
chrome_options.add_argument("--disable-gpu")

class TestRequirement2(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Class-level setup for WebDriver and logging."""
        log_filename = 'RQ2_test_execution.log'
        logging.basicConfig(
            filename=log_filename,
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        logging.info('Test For Requirement2 started.')

        # Initialize WebDriver
        cls.driver = webdriver.Chrome(
            service=Service(r'C:/Users/user/Downloads/chromedriver/chromedriver-win64/chromedriver.exe')
        )
        cls.driver.implicitly_wait(10)
        logging.info('WebDriver initialized.')

    def setUp(self):
        """Test-level setup to navigate to the page."""
        self.driver = self.__class__.driver
        self.driver.get('C:/Users/user/Desktop/SQA/SQA_GROUP1-CW2/SQATube_Group1/index.html')
        logging.info('Navigated to the webpage.')
        sleep(5)

    def test_scroll_action(self):
        """Test to verify the scrolling action."""
        logging.info('Starting scrolling action.')
        initial_scroll_position = self.driver.execute_script("return window.pageYOffset;")
        logging.info(f"Initial scroll position: {initial_scroll_position}")

        for _ in range(50):
            self.driver.execute_script("window.scrollBy(0, 100);")
            time.sleep(0.1)
            logging.info('Scrolled by 100px.')

        final_scroll_position = self.driver.execute_script("return window.pageYOffset;")
        logging.info(f"Final scroll position: {final_scroll_position}")

        # Assert that the page has scrolled down
        self.assertGreater(final_scroll_position, initial_scroll_position, "Scrolling action did not move the page down.")
        logging.info('Scrolling action verified.')

    @classmethod
    def tearDownClass(cls):
        """Class-level cleanup to close WebDriver."""
        cls.driver.quit()
        logging.info('WebDriver closed, test completed.')

if __name__ == '__main__':
    unittest.main()
