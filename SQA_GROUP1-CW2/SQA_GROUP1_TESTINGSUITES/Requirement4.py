import unittest
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep
from selenium.webdriver.chrome.options import Options

# Set up Chrome options to disable GPU
chrome_options = Options()
chrome_options.add_argument("--disable-gpu")

class TestRequirement4(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Class-level setup for WebDriver and logging."""
        log_filename = 'RQ4_test_execution.log'
        logging.basicConfig(
            filename=log_filename,
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        logging.info('Test for Requirement4 started.')

        # Initialize WebDriver
        cls.driver = webdriver.Chrome(
            service=Service(r'C:/Users/user/Downloads/chromedriver/chromedriver-win64/chromedriver.exe')
        )
        cls.driver.implicitly_wait(10)  # Implicit wait for WebDriver
        logging.info('WebDriver initialized.')

    def setUp(self):
        """Test-level setup to navigate to the webpage."""
        self.driver = self.__class__.driver
        self.driver.get('C:/Users/user/Desktop/SQA/SQA_GROUP1-CW2/SQATube_Group1/index.html')
        logging.info('Navigated to SQATube webpage.')

    def test_video_interaction(self):
        """Test video interactions like play/pause, fullscreen, and seeking."""
        driver = self.driver

        # Switch to iframe containing the video
        video = driver.find_element(By.CSS_SELECTOR, 'div.video:nth-child(1)>iframe')
        logging.info('Found iframe containing video.')
        self.assertIsNotNone(video, "Video iframe was not found.")

        driver.switch_to.frame(video)
        logging.info('Switched to iframe.')

        # Play the video
        fstvideo = driver.find_element(By.CSS_SELECTOR, '#movie_player')
        logging.info('Found video player element.')
        self.assertIsNotNone(fstvideo, "Video player element was not found.")

        fstvideo.click()  # Start playback
        logging.info('Clicked on the video player to start playback.')
        sleep(7)  # Wait for video to play

        # Verify video is playing
        is_playing = driver.execute_script("return document.querySelector('#movie_player').getPlayerState() === 1;")
        self.assertTrue(is_playing, "Video did not start playback.")
        logging.info('Video playback verified.')

        # Click fullscreen button
        fs_button = driver.find_element(By.CSS_SELECTOR, 'button.ytp-fullscreen-button')
        logging.info('Found fullscreen button.')
        self.assertIsNotNone(fs_button, "Fullscreen button was not found.")

        fs_button.click()  # Activate fullscreen
        logging.info('Clicked fullscreen button.')
        sleep(5)  # Wait to observe fullscreen

        # Play/Pause the video
        play_button = driver.find_element(By.CSS_SELECTOR, '.ytp-play-button.ytp-button')
        logging.info('Found play button.')
        self.assertIsNotNone(play_button, "Play button was not found.")

        play_button.click()  # Pause the video
        logging.info('Clicked play button to pause the video.')
        sleep(5)

        # Verify video is paused
        is_paused = driver.execute_script("return document.querySelector('#movie_player').getPlayerState() === 2;")
        self.assertTrue(is_paused, "Video did not pause.")
        logging.info('Video paused verified.')

        play_button.click()  # Resume video
        logging.info('Clicked play button again to resume video playback.')
        sleep(5)

        # Verify video is playing again
        is_playing = driver.execute_script("return document.querySelector('#movie_player').getPlayerState() === 1;")
        self.assertTrue(is_playing, "Video did not resume playback.")
        logging.info('Video resumed playback verified.')

        # Seeking forward
        current_time = driver.execute_script("return document.querySelector('#movie_player').getCurrentTime();")
        logging.info(f'Current time before seeking forward: {current_time}')

        driver.execute_script("document.querySelector('#movie_player').seekTo(arguments[0], true);", current_time + 10)
        logging.info('Sought forward by 10 seconds using JavaScript.')
        sleep(5)  # Wait to observe seeking forward

        forward_time = driver.execute_script("return document.querySelector('#movie_player').getCurrentTime();")
        logging.info(f'Current time after seeking forward: {forward_time}')
        self.assertGreater(forward_time, current_time, "Seeking forward did not work.")

        # Seeking backward
        driver.execute_script("document.querySelector('#movie_player').seekTo(arguments[0], true);", forward_time - 5)
        logging.info('Sought backward by 5 seconds using JavaScript.')
        sleep(5)  # Wait to observe seeking backward

        backward_time = driver.execute_script("return document.querySelector('#movie_player').getCurrentTime();")
        logging.info(f'Current time after seeking backward: {backward_time}')
        self.assertLess(backward_time, forward_time, "Seeking backward did not work.")

    @classmethod
    def tearDownClass(cls):
        """Class-level cleanup to close WebDriver."""
        cls.driver.quit()
        logging.info('WebDriver closed, test completed.')

if __name__ == '__main__':
    unittest.main()