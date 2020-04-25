import yaml
import os


class Configuration():

    def __init__(self):
        self.base_path = os.path.dirname(os.path.abspath(__file__))
        self.config_file_name = os.path.join(self.base_path, 'config.yaml')
        status, config = self.read_config()
        if status:
            self.config = config
        else:
            self.config = None
    
    def read_config(self):
        try:
            config = None
            with open(self.config_file_name) as f_config:
                config = yaml.load(f_config.read(), Loader=yaml.FullLoader)
            return True, config
        except Exception as e:
            return False, str(e)
    
    def get_config_section(self,section):
        if self.config:
            if section in self.config:
                return True, self.config[section]
            else:
                return False, 'NA'
        return False, 'Configuration is not available'