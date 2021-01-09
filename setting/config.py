import configparser
import os
import errno

file_path = './file'
config_file = 'config.ini'

class Config():
    def __init__(self):
        path_to_config_file = '{}/{}'.format(file_path, config_file)
        if not os.path.exists(path_to_config_file):
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), path_to_config_file)
        self._parser = configparser.ConfigParser()
        self._parser.read(path_to_config_file, encoding='utf_8')
    
    def output_path(self):
        section = 'DEFAULT'
        key = 'OutputDir'
        return self._parser.get(section, key)
