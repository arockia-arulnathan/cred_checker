import os
import platform
import time
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Browser:

    def __init__(self):
        self.base_path = os.path.dirname(os.path.abspath(__file__))
        if platform.system().lower() == 'windows':
            self.os = 'win'
            self.filetype = '.exe'
        elif platform.system().lower() == 'linux':
            self.os = 'linux'
            self.filetype = ''
        else:
            self.os = 'mac'
            self.filetype = ''

        if 'PROCESSOR_ARCHITEW6432' in os.environ:
            self.arch = '64'
        else:
            self.arch = '32'
        self.webdriver_path = os.path.join(self.base_path, f'assets/{self.os}_geckodriver_{self.arch}{self.filetype}')
        options = Options()
        options.headless = True
        # self.browser = webdriver.Firefox(executable_path=self.webdriver_path, options=options)
        self.browser = webdriver.Firefox(executable_path=self.webdriver_path)

    def __del__(self):
        if self.browser:
            self.browser.close()

    def open_url(self, url):
        try:
            if self.browser:
                self.browser.get(url)
                return True, self.browser.page_source
        except Exception as e:
            return False, str(e)

    def send_keys(self, xpath, keys):
        try:
            element = WebDriverWait(self.browser, 10).until(
                    EC.presence_of_element_located((By.XPATH, xpath)))
            # element = self.browser.find_element_by_xpath(xpath)
            if element:
                element.send_keys(keys)
                return True, 'Keys sent'
            else:
                return False, f'Element not found in xpath: {xpath}'
        except Exception as e:
            return False, str(e)

    def click_element(self, xpath):
        try:
            element = WebDriverWait(self.browser, 10).until(
                    EC.presence_of_element_located((By.XPATH, xpath)))
            # element = self.browser.find_element_by_xpath(xpath)
            if element:
                element.click()
                return True, f'Element {xpath} clicked successfully'
            else:
                return False, f'Element not found in xpath: {xpath}'
        except Exception as e:
            return False, str(e)

    def check_visible_element(self, xpath):
        try:
            element = WebDriverWait(self.browser, 10).until(
                    EC.visibility_of_element_located((By.XPATH, xpath)))
            # element = self.browser.find_element_by_xpath(xpath)
            if element:
                return True, f'Element {xpath} is visible'
            else:
                return False, f'Element is not visible in xpath: {xpath}'
        except Exception as e:
            return False, str(e)
            


if __name__ == '__main__':
    obj = Browser()
    status, resp_content = obj.open_url(url='https://eazytutor.in')
    if status:
        obj.click_element(xpath=r'//*[@id="primary-menu"]/li[2]/a/span[1]/span')
        time.sleep(10)