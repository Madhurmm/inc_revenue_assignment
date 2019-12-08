from selenium import webdriver


class Utilities:

    @staticmethod
    def create_webdriver_instance(browser: str = 'firefox'):

        """ Create webdriver instance """

        if browser == 'chrome':
            driver = webdriver.Chrome()
            driver.maximize_window()
            return driver

        elif browser == 'firefox':
            return webdriver.Firefox()
