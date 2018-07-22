import os
import os.path
from datetime import datetime
from config_parse import Deleter_config

CONF_WAY = "./bc_deleter.conf"

DIR_WATCHERS = []

class ConfigDirError(Exception):
    pass

class NonPositiveCountError(ValueError):
    pass

class Dir_watcher:
    def __init__(self, dir, num):
        if not os.path.exists(dir):
            raise ConfigDirError("Неверный параметр, папки %s не существует " % dir)
        if num < 0:
            raise NonPositiveCountError("Вы указали отрицательное количество файлов в папке %s" % dir)
        self.__dir = dir
        self.__num = num
    def getfilelist(self):
        lst_f = []
        for f in os.listdir(self.__dir):
            f = os.path.join(self.__dir,f)
            if os.path.isfile(f):
                lst_f.append((f,os.path.getctime(f)))
        lst_f.sort(key=lambda x: x[1], reverse=True)
        return lst_f
    def files_for_delete(self):
        return [f[0] for f in self.getfilelist()[self.__num:]]




class Deleter:
    def __init__(self):
        self.__DIR_WATCHERS = []
        deleter_config = Deleter_config(CONF_WAY)
        if deleter_config.isError():
            raise ConfigDirError("Неверное значение параметра папки :" + \
            deleter_config.get_err_description()[1] + " : " + deleter_config.get_err_description()[2])
        deleter_config_dirs = deleter_config.get_dirs()
        for d in deleter_config_dirs:
            self.__DIR_WATCHERS.append(Dir_watcher(d,deleter_config_dirs[d]))
    def get_list_dir_watches(self):
        return self.__DIR_WATCHERS
    def get_list_files_for_delete(self):
        files = []
        for dw in self.__DIR_WATCHERS:
            files +=  dw.files_for_delete()
        return files
    def delete_old_files(self):
        for f in self.get_list_files_for_delete():
            os.remove(f)


if __name__ == '__main__':
    try:
        deleter = Deleter()
        dlst = deleter.get_list_dir_watches()
        for d in dlst:
            d.getfilelist()
            print(d.files_for_delete())
    except ConfigDirError as cerr:
        print(cerr)
    #deleter.delete_old_files()
