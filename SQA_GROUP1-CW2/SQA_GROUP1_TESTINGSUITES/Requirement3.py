import unittest
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from time import sleep

from selenium.webdriver.chrome.options import Options


# Set up Chrome options to disable GPU
chrome_options = Options()
chrome_options.add_argument("--disable-gpu")
class TestRequirement3(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Class-level setup for WebDriver and logging."""
        log_filename = 'RQ3_test_execution.log'
        logging.basicConfig(
            filename=log_filename,
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        logging.info('Test for Requirement3 started.')

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

    def test_video_playback(self):
        """Test to verify video playback functionality."""
        # Locate the iframe containing the video
        video = self.driver.find_element(By.CSS_SELECTOR, 'div.video:nth-child(1)>iframe')
        logging.info('Found iframe containing video.')
        self.assertIsNotNone(video, "Iframe containing video was not found.")

        # Switch to iframe
        self.driver.switch_to.frame(video)
        logging.info('Switched to iframe.')

        # Find the video player
        fstvideo = self.driver.find_element(By.CSS_SELECTOR, '#movie_player')
        logging.info('Found the video player element.')
        self.assertIsNotNone(fstvideo, "Video player element was not found.")

        # Click on the video player to start playback
        fstvideo.click()
        logging.info('Clicked on the video player to start playback.')
        sleep(7)

        # Verify playback started (by checking if the player is not paused)
        is_playing = self.driver.execute_script("return document.querySelector('#movie_player').getPlayerState() === 1;")
        self.assertTrue(is_playing, "Video did not start playback.")
        logging.info('Video playback verified.')

    @classmethod
    def tearDownClass(cls):
        """Class-level cleanup to close WebDriver."""
        cls.driver.quit()
        logging.info('WebDriver closed, test completed.')

if __name__ == '__main__':
    unittest.main()
