# encoding:utf-8
import json
import os
import logging
from datetime import datetime

class DictAsClass(dict):
    ATTRIBUTE = []

    def __init__(self, **kwargs):
        if self.ATTRIBUTE:
            for key in kwargs.keys():
                if key not in self.ATTRIBUTE:
                    raise AttributeError(f'Illegal attributes {key}, not in ATTRIBUTE: {self.ATTRIBUTE}')

        for k, v in kwargs.items():
            if isinstance(v, dict):
                kwargs[k] = DictAsClass(**v)
            elif isinstance(v, list):
                kwargs[k] = self.handle_list(v)
            else:
                pass

        super(DictAsClass, self).__init__(**kwargs)

    def handle_list(self, l):
        new_list = []
        for item in l:
            if isinstance(item, dict):
                new_list.append(DictAsClass(**item))
            elif isinstance(item, list):
                new_list.append(self.handle_list(item))
            else:
                new_list.append(item)
        return new_list

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(f'Attribute {key} not exist.')

    def __setattr__(self, key, value):
        if self.ATTRIBUTE:
            if key not in self.ATTRIBUTE:
                raise AttributeError(f'Illegal attributes {key}, not in ATTRIBUTE: {self.ATTRIBUTE}')
        self[key] = value

    def __str__(self):
        return json.dumps(self, sort_keys=False, indent=2)

    __repr__ = __str__

class ClassToDict:
    def __iter__(self):
        return iter(self.__dict__.items())

    def __str__(self):
        return json.dumps(dict(self), sort_keys=False, indent=2)

    __repr__ = __str__

def get_json_config_from_file(file_path):
    config = None

    with open(file_path, 'r') as f:
        config_obj = json.load(f)
        config = DictAsClass(**config_obj)

    return config

def load_config(CONFIG_FILE_NAME):
    config_file_path = os.path.join(os.path.dirname(__file__), CONFIG_FILE_NAME)
    config = get_json_config_from_file(config_file_path)
    return config

def Logger_Model():
    logger = logging.getLogger('atp_log')
    logger.setLevel(logging.DEBUG)
    # create a handler, write the log info into it
    dir = os.getcwd()
    time = datetime.now().strftime("%Y-%m-%d")
    fh = logging.FileHandler(dir+'/log/'+time+'.log',encoding='utf-8')
    fh.setLevel(logging.DEBUG)
    # create another handler output the log though console
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    logger.addHandler(fh)
    logger.addHandler(ch)
    return logger