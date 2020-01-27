import yaml

class Settings: 
    def __init__(self):
        self._config = self.load_config()

    def load_config(self):
        config = None
        with open('settings.yaml') as f:
            config = yaml.load(f.read(), Loader=yaml.FullLoader)
        return config
    
    def get_property(self, property_name):
        if property_name not in self._config.keys():
            return None
        return self._config[property_name]

    @property
    def InputFolder(self):
        return self.get_property('input_folder')

    @property
    def SegmentLen(self):
        return self.get_property('segment_length')

settings = Settings()