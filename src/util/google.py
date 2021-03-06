import time

class Google():

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
            # Open login page
            self.log_obj.debug("Testing in-progress for Google")
            self.browser.open_url(self.config['login_url'])
            # Enter username
            status, _ = self.browser.send_keys(keys=self.username, xpath=self.config['username_xpath'])
            # Click Next
            if status:
                status, _ = self.browser.click_element(xpath=self.config['username_next_xpath'])
                time.sleep(5)
                if status:
                    # Enter Password
                    status, message = self.browser.send_keys(keys=self.password, xpath=self.config['password_xpath'])
                    if status:
                        # Click Next
                        self.browser.click_element(xpath=self.config['password_next_xpath'])
                        if self.config['result_patterns']['failure'][1] in self.browser.browser.page_source:
                            return False, 'Invalid Credentials'
                        return True, 'Valid Credentials'
                    else:
                        return False, 'Invalid Credentials'
                else:
                    self.log_obj.error("Username field is not found in Google.")
                    return False, 'Username field not found'
        except Exception as e:
            return False, str(e)