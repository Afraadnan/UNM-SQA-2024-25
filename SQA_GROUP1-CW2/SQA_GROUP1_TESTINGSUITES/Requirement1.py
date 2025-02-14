from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import logging
import unittest
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException, NoSuchElementException

class TestSQATube(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Set up logging configuration
        cls.log_filename = 'RQ1_test_execution.log'
        logging.basicConfig(filename=cls.log_filename, 
                          level=logging.INFO, 
                          format='%(asctime)s - %(levelname)s - %(message)s')
        logging.info('Test for Requirement1 started.')

    def setUp(self):
        # Set up the WebDriver and configure implicit wait
        logging.info('Starting WebDriver.')
        self.wd = webdriver.Chrome(service=Service(r'C:/Users/user/Downloads/chromedriver/chromedriver-win64/chromedriver.exe'))
        self.wd.maximize_window()
        self.wd.implicitly_wait(10)

    def wait_and_find_element(self, by, value, timeout=10):
        """Helper method to wait for and find an element"""
        try:
            element = WebDriverWait(self.wd, timeout).until(
                EC.presence_of_element_located((by, value))
            )
            return element
        except TimeoutException as e:
            logging.error(f"Timeout waiting for element {value}")
            raise e

    def scroll_page(self):
        """Scroll the page slightly to load more content"""
        self.wd.execute_script("window.scrollBy(0, 300);")  # Scrolls down by 300 pixels
        time.sleep(2)  # Wait for content to load after scrolling

    def test_youtube_search(self):
        try:
            search_query = 'AI DevOps Tools'

            # 1. Navigate to the SQATube page
            logging.info('Navigating to SQATube webpage.')
            self.wd.get('file:///C:/Users/user/Desktop/SQA/SQA_GROUP1-CW2/SQATube_Group1/index.html')

            # Verify page load and title
            self.assertIn("YouTubeCloneForSQA", self.wd.title, "Page title does not contain YouTubeCloneForSQA.")
            logging.info('Page title verified.')

            # Wait for and find search elements
            search_input = self.wait_and_find_element(By.ID, 'search-input')
            search_button = self.wait_and_find_element(By.ID, 'search-button')

            # Perform search
            search_input.clear()
            search_input.send_keys(search_query)
            logging.info(f'Entered search query: {search_query}')

            search_button.click()
            logging.info(f'Clicked search button for "{search_query}"')

            # Wait for video grid container
            video_grid_container = self.wait_and_find_element(By.ID, 'video-grid', timeout=20)
            
            # Wait for dynamic content using JavaScript
            try:
                WebDriverWait(self.wd, 20).until(
                    lambda driver: driver.execute_script(
                        'return document.getElementById("video-grid").children.length > 0'
                    )
                )
            except TimeoutException:
                logging.error("Timeout waiting for video grid to populate")
                # Log the current state
                logging.info(f"Video grid HTML: {video_grid_container.get_attribute('innerHTML')}")
                raise

            # Get video items
            video_grid = self.wd.find_elements(By.CSS_SELECTOR, '#video-grid > *')
            logging.info(f'Found {len(video_grid)} video items in the grid.')

            # Assert search results
            self.assertGreater(len(video_grid), 0, "No search results found on SQATube.")
            logging.info(f"Test passed for SQATube, {len(video_grid)} videos found.")

            # Scroll the page after fetching search results
            self.scroll_page()

            time.sleep(7)

            # 2. Navigate to YouTube and perform the same search
            logging.info('Navigating to YouTube website.')
            self.wd.get('https://www.youtube.com/')

            # Wait for and verify YouTube page load
            self.wait_and_find_element(By.NAME, 'search_query')
            self.assertIn("YouTube", self.wd.title, "YouTube homepage title not found.")
            logging.info('YouTube homepage title verified.')

            # Perform YouTube search
            search_input_youtube = self.wait_and_find_element(By.NAME, 'search_query')
            search_input_youtube.send_keys(search_query)
            logging.info(f'Entered search query: {search_query} on YouTube.')

            search_button_youtube = self.wait_and_find_element(By.ID, 'search-icon-legacy')
            search_button_youtube.click()
            logging.info(f'Searched for "{search_query}" on YouTube.')

            # Wait for and verify YouTube search results
            contents = self.wait_and_find_element(By.CSS_SELECTOR, '#contents', timeout=20)
            video_grid_youtube = self.wd.find_elements(By.CSS_SELECTOR, '#contents ytd-video-renderer')
            logging.info(f'Found {len(video_grid_youtube)} video items on YouTube.')

            self.assertGreater(len(video_grid_youtube), 0, "No search results found on YouTube.")
            logging.info(f"Test passed for YouTube, {len(video_grid_youtube)} videos found.")

            # Scroll the page after fetching YouTube search results
            self.scroll_page()

            time.sleep(5)

        except Exception as e:
            logging.error(f"Test failed with error: {str(e)}")
            # Log the page source in case of failure
            logging.error(f"Page source at failure: {self.wd.page_source}")
            raise

    def tearDown(self):
        # Close the WebDriver
        logging.info('Closing WebDriver.')
        self.wd.quit()
        logging.info('WebDriver closed, test completed.')

    @classmethod
    def tearDownClass(cls):
        # Finish logging
        logging.info('Test execution finished, logging completed.')

if __name__ == '__main__':
    unittest.main()
