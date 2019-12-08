import random
import traceback

from selenium.common.exceptions import WebDriverException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

from utils.utilities import Utilities

WEBSITE_URL = 'https://www.wego.co.in/'

# TODO :  ADD LOGGER


class TaskTwo:

    # ----------------------------------------------------

    # https://stackoverflow.com/questions/36141681/does-anybody-know-how-to-identify-shadow-dom-web-elements-using-selenium-webdriv
    @staticmethod
    def expand_shadow_element(driver, element):
        shadow_root = driver.execute_script('return arguments[0].shadowRoot', element)
        return shadow_root

    # ----------------------------------------------------

    # TODO: MOVE THIS METHOD TO utils PACKAGE
    @staticmethod
    def switch_to_window(driver, number_of_windows):
        # Waiting for new window to open
        try:
            WebDriverWait(driver, 10).until(ec.number_of_windows_to_be(number_of_windows))

            child = driver.window_handles[1]
            print(f'Found {number_of_windows} windows. Switching to new window')
            driver.switch_to.window(child)

        except TimeoutException as e:
            print('Script is executing in current window')
            pass

    # ----------------------------------------------------

    @staticmethod
    def search_for_flights(driver):

        driver.get(WEBSITE_URL)

        shawdow_root_selector = '#app'
        shadow_root_element = driver.find_element_by_css_selector(shawdow_root_selector)
        shadow_root_section = TaskTwo.expand_shadow_element(driver, shadow_root_element)

        flights_app_shadow_l2_locator = '[app-name="flights"]'
        flights_app_shadow_l2_element = shadow_root_section.find_element_by_css_selector(flights_app_shadow_l2_locator)
        flights_app_shadow_l2_section = TaskTwo.expand_shadow_element(driver, flights_app_shadow_l2_element)

        wego_flight_search_shadow_l3_locator = 'wego-flight-search-form.flightSearchForm'
        wego_flight_search_shadow_l3_element = flights_app_shadow_l2_section.find_element_by_css_selector(
            wego_flight_search_shadow_l3_locator)
        wego_flight_search_shadow_l3_section = TaskTwo.expand_shadow_element(driver,
                                                                             wego_flight_search_shadow_l3_element)

        ############################################
        ####### SELECT RANDOM DEPARTURE CITY #######
        ############################################

        dept_shadow_l4_locator = '#dep'
        dept_shadow_l4_element = wego_flight_search_shadow_l3_section.find_element_by_css_selector(
            dept_shadow_l4_locator)
        dept_shadow_l4_section = TaskTwo.expand_shadow_element(driver, dept_shadow_l4_element)

        dept_shadow_l4_section.find_element_by_css_selector('.container').click()

        dept_result_box_shadow_l5_locator = 'result-box'
        dept_result_box_shadow_l5_element = WebDriverWait(dept_shadow_l4_section, 10).until(
            ec.presence_of_element_located((By.CSS_SELECTOR, dept_result_box_shadow_l5_locator)))

        dept_result_box_shadow_l5_section = TaskTwo.expand_shadow_element(driver, dept_result_box_shadow_l5_element)

        list_of_dept_location_element = WebDriverWait(dept_result_box_shadow_l5_section, 10).until(
            ec.presence_of_all_elements_located((By.CSS_SELECTOR, '.content .location')))

        random_dept_location_element = list_of_dept_location_element[random.randrange(0, len(list_of_dept_location_element))]

        random_dept_location_element.click()

        ##########################################
        ####### SELECT RANDOM ARRIVAL CITY #######
        ##########################################

        arr_shadow_l4_locator = '#arr'
        arr_shadow_l4_element = wego_flight_search_shadow_l3_section.find_element_by_css_selector(arr_shadow_l4_locator)
        arr_shadow_l4_section = TaskTwo.expand_shadow_element(driver, arr_shadow_l4_element)

        arr_shadow_l4_section.find_element_by_css_selector('.container').click()

        arr_result_box_shadow_l5_locator = 'result-box'
        arr_result_box_shadow_l5_element = arr_shadow_l4_section.find_element_by_css_selector(
            arr_result_box_shadow_l5_locator)
        arr_result_box_shadow_l5_section = TaskTwo.expand_shadow_element(driver, arr_result_box_shadow_l5_element)

        list_of_arr_location_element = WebDriverWait(arr_result_box_shadow_l5_section, 10).until(
            ec.presence_of_all_elements_located((By.CSS_SELECTOR, '.content .location')))

        random_arr_location_element = list_of_arr_location_element[
            random.randrange(0, len(list_of_arr_location_element))]

        random_arr_location_element.click()

        ###########################################
        ####### SELECT RANDOM DEPARURE DATE #######
        ###########################################

        dept_date_picker_shadow_l4_locator = 'date-picker#dates'
        dept_date_picker_shadow_l4_element = wego_flight_search_shadow_l3_section.find_element_by_css_selector(
            dept_date_picker_shadow_l4_locator)
        dept_date_picker_shadow_l4_section = TaskTwo.expand_shadow_element(driver, dept_date_picker_shadow_l4_element)

        dept_date_field_shadow_l5_locator = 'date-field#depart'
        dept_date_field_shadow_l5_element = dept_date_picker_shadow_l4_section.find_element_by_css_selector(
            dept_date_field_shadow_l5_locator)
        dept_date_field_shadow_l5_section = TaskTwo.expand_shadow_element(driver, dept_date_field_shadow_l5_element)

        dept_date_field_shadow_l5_section.find_element_by_css_selector('#btn').click()

        dept_calendar_popup_shadow_l5_locator = 'calendar-popup'
        dept_calendar_popup_shadow_l5_element = dept_date_picker_shadow_l4_section.find_element_by_css_selector(
            dept_calendar_popup_shadow_l5_locator)
        dept_calendar_popup_shadow_l5_section = TaskTwo.expand_shadow_element(driver,
                                                                              dept_calendar_popup_shadow_l5_element)

        list_of_departure_days_element = dept_calendar_popup_shadow_l5_section.find_elements_by_css_selector(
            '.calendars .day')
        valid_list_of_departure_days_element = [e for e in list_of_departure_days_element if e.text != '']

        while True:
            try:
                random_departure_date_element = valid_list_of_departure_days_element[
                    random.randrange(0, len(valid_list_of_departure_days_element))]

                random_departure_date_element.click()

                break

            except WebDriverException:
                continue

        ######################################
        ####### CLICK ON SEARCH BUTTON #######
        ######################################

        parent = driver.current_window_handle

        search_button_element = wego_flight_search_shadow_l3_section.find_element_by_css_selector('#search.search.round-right')
        search_button_element.click()

        print('Clicked on Search Button')

    # ----------------------------------------------------

    @staticmethod
    def wait_for_flight_results_page_to_load(driver):

        TaskTwo.switch_to_window(driver, 2)

        shawdow_root_selector = '#app'
        shadow_root_element = WebDriverWait(driver, 10).until(
            ec.presence_of_element_located((By.CSS_SELECTOR, shawdow_root_selector)))
        shadow_root_section = TaskTwo.expand_shadow_element(driver, shadow_root_element)

        flights_search_shadow_l2_locator = '#flights-search'
        flights_search_shadow_l2_element = WebDriverWait(shadow_root_section, 10).until(
            ec.presence_of_element_located((By.CSS_SELECTOR, flights_search_shadow_l2_locator)))
        flights_search_shadow_l2_section = TaskTwo.expand_shadow_element(driver, flights_search_shadow_l2_element)

        print('Waiting for Spinner to appear')
        wego_spinner_wrapper_shadow_l2_locator = '#interstitial'
        wego_spinner_wrapper_shadow_l2_element = WebDriverWait(flights_search_shadow_l2_section, 10).until(
            ec.presence_of_element_located((By.CSS_SELECTOR, wego_spinner_wrapper_shadow_l2_locator)))
        wego_spinner_wrapper_shadow_l2_section = TaskTwo.expand_shadow_element(driver,
                                                                               wego_spinner_wrapper_shadow_l2_element)

        print('Waiting for spinner to hide')

        WebDriverWait(wego_spinner_wrapper_shadow_l2_section, 10).until(
            ec.presence_of_element_located((By.CSS_SELECTOR, 'wego-spinner[hidden=""]')))

        print('Page loaded completely')

    # ----------------------------------------------------

    @staticmethod
    def select_first_view_deal(driver):

        shawdow_root_selector = '#app'
        shadow_root_element = WebDriverWait(driver, 10).until(
            ec.presence_of_element_located((By.CSS_SELECTOR, shawdow_root_selector)))
        shadow_root_section = TaskTwo.expand_shadow_element(driver, shadow_root_element)

        flights_search_shadow_l2_locator = '#flights-search'
        flights_search_shadow_l2_element = WebDriverWait(shadow_root_section, 10).until(
            ec.presence_of_element_located((By.CSS_SELECTOR, flights_search_shadow_l2_locator)))
        flights_search_shadow_l2_section = TaskTwo.expand_shadow_element(driver, flights_search_shadow_l2_element)

        flights_result_list_shadow_l3_locator = '#flightResultList'
        flights_result_list_shadow_l3_element = WebDriverWait(flights_search_shadow_l2_section, 10).until(
            ec.presence_of_element_located((By.CSS_SELECTOR, flights_result_list_shadow_l3_locator)))
        flights_result_list_shadow_l3_section = TaskTwo.expand_shadow_element(driver, flights_result_list_shadow_l3_element)

        flight_card_shadow_l4_element = WebDriverWait(flights_result_list_shadow_l3_section, 10).until(
            ec.presence_of_element_located((By.CSS_SELECTOR, 'flight-card')))
        flight_card_shadow_l4_section = TaskTwo.expand_shadow_element(driver, flight_card_shadow_l4_element)

        view_deal_shadow_l5_element = WebDriverWait(flight_card_shadow_l4_section, 10).until(
            ec.presence_of_element_located((By.CSS_SELECTOR, '.view-deal')))

        # Click on view deal button
        print('Clicking on 1st view deal button')
        view_deal_shadow_l5_element.click()

    # ----------------------------------------------------

    @staticmethod
    def select_second_view_deal(driver):

        shawdow_root_selector = '#app'
        shadow_root_element = WebDriverWait(driver, 10).until(
            ec.presence_of_element_located((By.CSS_SELECTOR, shawdow_root_selector)))
        shadow_root_section = TaskTwo.expand_shadow_element(driver, shadow_root_element)

        flights_search_shadow_l2_locator = '#flights-search'
        flights_search_shadow_l2_element = WebDriverWait(shadow_root_section, 10).until(
            ec.presence_of_element_located((By.CSS_SELECTOR, flights_search_shadow_l2_locator)))
        flights_search_shadow_l2_section = TaskTwo.expand_shadow_element(driver, flights_search_shadow_l2_element)

        flights_detail_shadow_l3_locator = 'flight-detail#detail'
        flights_detail_shadow_l3_element = WebDriverWait(flights_search_shadow_l2_section, 10).until(
            ec.presence_of_element_located((By.CSS_SELECTOR, flights_detail_shadow_l3_locator)))
        flights_detail_shadow_l3_section = TaskTwo.expand_shadow_element(driver, flights_detail_shadow_l3_element)

        # Fetch list of all buttons and filter only those which has 'VIEW DEAL' in its text
        view_deals_element_list = WebDriverWait(flights_detail_shadow_l3_section, 10).until(
            ec.presence_of_all_elements_located((By.CSS_SELECTOR, 'flight-detail-fare')))

        filtered_view_deals_element_list = [e for e in view_deals_element_list if 'view deal' in e.text.lower()]

        if filtered_view_deals_element_list:

            print('View Deal buttons found')

            # Select the first view deal button
            view_deal_element = filtered_view_deals_element_list[0]
            view_deal_section_l4_section = TaskTwo.expand_shadow_element(driver, view_deal_element)

            view_deal_button = WebDriverWait(view_deal_section_l4_section, 10).until(
                ec.presence_of_element_located((By.CSS_SELECTOR, 'wego-button')))

            print('Clicking on 2nd view deal button')

            view_deal_button.click()

            TaskTwo.switch_to_window(driver, 3)

    # ----------------------------------------------------

    @staticmethod
    def run_script(browser='chrome'):
        try:
            driver = Utilities.create_webdriver_instance(browser=browser)

            TaskTwo.search_for_flights(driver)
            TaskTwo.wait_for_flight_results_page_to_load(driver)
            TaskTwo.select_first_view_deal(driver)
            TaskTwo.select_second_view_deal(driver)

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
    TaskTwo().run_script()
