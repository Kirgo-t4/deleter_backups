# -*- coding: utf-8 -*-


from configparser import ConfigParser

class Deleter_config:
    def __init__(self, way):
        self.__dirs = {}
        self.__err = False
        config = ConfigParser()
        config.optionxform = str
        config.read(way)
        for section in config.sections():
            if section == "directories":
                try:
                    for option in config.options(section):
                        self.__dirs[option] = int(config.get(section, option))
                except ValueError as verr:
                    self.__err = True
                    self.__err_description = ("i", option, config.get(section, option))
    def isError(self):
        return self.__err
    def get_err_description(self):
        return self.__err_description


    def get_dirs(self):
            return self.__dirs

if __name__ == '__main__':
    delter_config = Deleter_config(CONF_WAY)
    print(delter_config.get_dirs())
