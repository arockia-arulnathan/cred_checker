import yaml
import os
from util import google, browser_call, twitter, facebook, github, linkedin, instagram, pinterest
from util.common import Configuration


class Cred_Checker:

    def __init__(self, username, password, log_obj):
        self.base_path = os.path.dirname(os.path.abspath(__file__))
        self.username = username
        self.password = password
        self.log_obj = log_obj
        with open(os.path.join(self.base_path,'util/config.yaml')) as f_handle:
            self.config = yaml.load(f_handle.read(), Loader=yaml.FullLoader)
        self.browser = browser_call.Browser()
    
    def site_checker(self, site_name):
        try:
            data = {
                    'username': self.username,
                    'password': self.password,
                    'config': self.config[site_name],
                    'browser': self.browser,
                    'log_obj': self.log_obj
                    }
            site_obj = eval(f"{site_name}.{site_name.capitalize()}()")
            site_obj.setup(**data)
            status, result = site_obj.login()
            return status, result
        except Exception as e:
            self.log_obj.error(f"Error while checking {site_name}. Exception: {str(e)}")
            return False, str(e)