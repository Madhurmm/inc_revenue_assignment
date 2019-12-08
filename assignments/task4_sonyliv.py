import random
import traceback
from time import sleep

from selenium.common.exceptions import TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

from utils.utilities import Utilities

WEBSITE_URL = 'https://www.sonyliv.com/'

# TODO : ADD LOGGER


class TaskFour:

    # ----------------------------------------------------

    @staticmethod
    def select_random_video_on_homepage(driver):

        # click on push notification button

        push_button_no_button = WebDriverWait(driver, 10).until(
            ec.presence_of_element_located((By.CSS_SELECTOR, '#wzrk-cancel')))
        push_button_no_button.click()

        # scroll to video in first row
        scroll_to_element_locator = '#movie-all div:nth-child(1) > .gridRowHeader > .gridRowHeaderInner > h2'
        scroll_to_element = WebDriverWait(driver, 15).until(
            ec.presence_of_element_located((By.CSS_SELECTOR, scroll_to_element_locator)))
        driver.execute_script("arguments[0].scrollIntoView();", scroll_to_element)

        # find list of random videos from 1st row and click on any video
        list_of_video_from_first_row = \
            driver.find_elements_by_css_selector('#movie_4 > ul > data-owl-carousel ul > li')

        if list_of_video_from_first_row:
            random_video_index = random.randrange(0, 5)

            video_element = list_of_video_from_first_row[random_video_index]. \
                find_element_by_css_selector('.Tile-TS-01 > a')

            if video_element:
                video_element.click()
                print('Clicked on video')

    # ----------------------------------------------------

    @staticmethod
    def wait_for_ad_to_complete(driver):
        print('Wait for title section to load')

        title_section_locator = '.main-container div.pull-right.titleSection.left-side-clickable-container'
        WebDriverWait(driver, 5).until(
            ec.presence_of_element_located((By.CSS_SELECTOR, title_section_locator)))

        print('Title section has loaded completed')

        print('Waiting for sharing element to appear and then disappear before the ad is played')

        sharing_icon_xpath_locator = '//*[@class="vjs-control tve-icon share ng-scope"]'

        WebDriverWait(driver, 10).until(
            ec.visibility_of_element_located((By.XPATH, sharing_icon_xpath_locator)))

        WebDriverWait(driver, 10).until(
            ec.invisibility_of_element_located((By.XPATH, sharing_icon_xpath_locator)))

        print('Ad has started to play')

        # Once the ad is completed, share button will appear once again
        print('Waiting for ad to complete and share menu to re-appear')
        share_element = WebDriverWait(driver, 150).until(
            ec.visibility_of_element_located((By.XPATH, sharing_icon_xpath_locator)))

        if share_element:
            print('Share element found. Ad is completed. New video  has started to play')

            WebDriverWait(driver, 10).until(
                ec.presence_of_element_located((By.CSS_SELECTOR, '.vjs-control-bar')))

    # ----------------------------------------------------

    @staticmethod
    def move_progress_bar_to_some_position(driver):
        action_a = ActionChains(driver)

        # First move to the bottom of the video player
        current_time_display_element = WebDriverWait(driver, 10).until(
            ec.presence_of_element_located((By.CSS_SELECTOR, '.vjs-current-time-display')))
        action_a.move_to_element(current_time_display_element).perform()

        # Calculate the width and height of the progress bar
        progress_bar_element = WebDriverWait(driver, 10).until(
            ec.visibility_of_element_located(
                (By.CSS_SELECTOR, '.vjs-progress-holder.vjs-slider.vjs-slider-horizontal')))

        progress_bar_width = progress_bar_element.size['width']
        progress_bar_height = progress_bar_element.size['height']

        print(f'Width of progress bar is : {progress_bar_width}')
        print(f'height of progress bar is : {progress_bar_height}')

        load_progress_bar_element = WebDriverWait(driver, 10).until(
            ec.visibility_of_element_located(
                (By.CSS_SELECTOR, '.vjs-load-progress')))

        # wait for progress bar to load atleast 50 px
        load_progress_bar_width = 0

        while load_progress_bar_width < 50:

            try:
                load_progress_bar_element = WebDriverWait(driver, 10).until(
                    ec.visibility_of_element_located(
                        (By.CSS_SELECTOR, '.vjs-load-progress')))

                load_progress_bar_width = load_progress_bar_element.size['width']
                load_progress_bar_height = load_progress_bar_element.size['height']

                print(f'Width of load progress bar is : {load_progress_bar_width}')
                print(f'height of load progress bar is : {load_progress_bar_height}')

            except TimeoutException:
                action_a.move_to_element(current_time_display_element).perform()

        # Using drag and drop by offset to change the position of progress bar

        action_a.move_to_element(current_time_display_element).perform()
        action_a.drag_and_drop_by_offset(load_progress_bar_element, progress_bar_width / 2,
                                         progress_bar_height / 2).perform()

        print('Moved the cursor to some random position')

        # Added sleep before script is completed so that it will easier to verify the movement
        # of progress bar
        sleep(5)

    # ----------------------------------------------------

    @staticmethod
    def run_script(browser='chrome'):
        try:
            driver = Utilities.create_webdriver_instance(browser=browser)
            driver.get(WEBSITE_URL)

            TaskFour.select_random_video_on_homepage(driver)
            TaskFour.wait_for_ad_to_complete(driver)
            TaskFour.move_progress_bar_to_some_position(driver)

        except Exception:
            # TODO: Remove broad exceptions
            # TODO: Add logging
            # TODO: Take screenshot
            traceback.print_exc()

        finally:
            driver.quit()
            print('Script Complete')

    # ----------------------------------------------------


if __name__ == '__main__':
    TaskFour().run_script()
