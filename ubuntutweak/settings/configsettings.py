import logging
import ConfigParser


class ConfigSetting(object):
    '''Key: /etc/lightdm/lightdm.conf::UserManager.load-users
    '''

    def __init__(self, key=None, default=None, type=None):
        self.type = type

        self._path = key.split('::')[0]
        self._section = key.split('::')[1].split('.')[0]
        self._option = key.split('::')[1].split('.')[1]

        self._init_configparser()

    def _init_configparser(self):
        self._configparser = ConfigParser.ConfigParser()
        self._configparser.read(self._path)

    def get_value(self):
        if self.type:
            if self.type == int:
                getfunc = getattr(self._configparser, 'getint')
            elif self.type == float:
                getfunc = getattr(self._configparser, 'getfloat')
            elif self.type == bool:
                getfunc = getattr(self._configparser, 'getfboolean')
            else:
                getfunc = getattr(self._configparser, 'get')

            value = getfunc(self._section, self._option)
        else:
            value = self._configparser.get(self._section, self._option)

        if value:
            return value
        else:
            if self.type == int:
                return 0
            elif self.type == float:
                return 0.0
            elif self.type == bool:
                return False
            elif self.type == str:
                return ''
            else:
                return None

    def set_value(self, value):
        self._configparser.set(self._section, self._option, value)
        with open(self._path, 'wb') as configfile:
            self._configparser.write(configfile)

        self._init_configparser()
