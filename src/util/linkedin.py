import time

class Linkedin():

    def __init__(self):
        pass

    def setup(self, username, password, config, browser, log_obj):
        self.username = username
        self.password = password
        self.config = config
        self.log_obj = log_obj
        if browser:
            self.browser = browser

    def login(self):
        try:
            self.log_obj.debug("Testing in-progress for Linkedin")
            # Open login page
            self.browser.open_url(self.config['login_url'])
            # Enter username
            self.browser.send_keys(keys=self.username, xpath=self.config['username_xpath'])
            # Enter Password
            self.browser.send_keys(keys=self.password, xpath=self.config['password_xpath'])
            # Click Next
            self.browser.click_element(xpath=self.config['login_button_xpath'])
            time.sleep(5)
            for xpath in self.config['result_patterns']['failure_xpaths']:
                status, message = self.browser.check_visible_element(xpath=xpath)
                if status:
                    return False, 'Invalid Credentials'
            return True, 'Valid Credentials'
        except Exception as e:
            return False, str(e)
