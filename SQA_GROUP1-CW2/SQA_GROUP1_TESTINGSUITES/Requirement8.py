import unittest
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
import time

# Set up Chrome options to disable GPU
chrome_options = Options()
chrome_options.add_argument("--disable-gpu")

class TestRequirement8(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Class-level setup for WebDriver and logging."""
        log_filename = 'RQ8_test_execution.log'
        logging.basicConfig(
            filename=log_filename,
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        logging.info('Test for Requirement8 started.')

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

    def test_sorting_and_scrolling(self):
        """Test the sorting dropdown and scrolling actions."""
        driver = self.driver

        # Locate the sorting dropdown
        select = Select(driver.find_element(By.ID, "sortOptions"))
        self.assertIsNotNone(select, "Sorting dropdown not found.")
        logging.info('Sorting dropdown element found.')

        # Options to test in the dropdown
        options = ['date', 'relevance', 'rating', 'duration']

        for option in options:
            # Select the sorting option
            logging.info(f'Selecting sorting option: {option}.')
            select.select_by_value(option)
            time.sleep(3)

            # Verify that the correct option is selected
            selected_option = select.first_selected_option.get_attribute("value")
            self.assertEqual(selected_option, option, f"Failed to select sorting option {option}.")
            logging.info(f'Successfully selected option: {option}.')

            # Perform scroll down actions
            logging.info(f'Starting scroll down actions for "{option}" option.')
            for _ in range(50):
                driver.execute_script("window.scrollBy(0, 100);")
                time.sleep(0.1)

            # Verify scroll position (should be greater than 0)
            current_scroll = driver.execute_script("return window.scrollY;")
            self.assertGreater(current_scroll, 0, f"Scroll down did not work for option {option}.")
            logging.info(f'Scroll position after scrolling down for "{option}": {current_scroll}.')

            # Perform scroll up actions
            logging.info(f'Starting scroll up actions for "{option}" option.')
            for _ in range(50):
                driver.execute_script("window.scrollBy(0, -100);")
                time.sleep(0.1)

            # Verify scroll position (should return to the top)
            new_scroll = driver.execute_script("return window.scrollY;")
            self.assertEqual(new_scroll, 0, f"Scroll up did not return to the top for option {option}.")
            logging.info(f'Scroll position after scrolling up for "{option}": {new_scroll}.')

        logging.info('All sorting options tested successfully.')

    @classmethod
    def tearDownClass(cls):
        """Class-level cleanup to close WebDriver."""
        cls.driver.quit()
        logging.info('WebDriver closed, test completed.')


if __name__ == '__main__':
    unittest.main()
