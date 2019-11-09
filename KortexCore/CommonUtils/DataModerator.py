from os import path
import root

from KortexCore.CommonUtils.JsonIO import JsonIO
from KortexCore.CommonUtils.Singleton import singleton


@singleton
class DataModerator(object):

    def __init__(self):
        self._main_path = root.get_root()
        self._data_files = path.join(self._main_path, "Metadata//DataFiles")
        self._images = path.join(self._main_path, "Metadata//Images")

    def get_data(self, group, parameter=None):
        file_data = JsonIO.read(path.join(self._data_files, group))
        if not parameter:
            return file_data
        return file_data[parameter]

    def write_data(self, group, parameter, new_data):
        full_path = path.join(self._data_files, group)
        JsonIO.write(full_path, parameter, new_data)

    def get_file_path(self, group, name):
        return path.join(self._images, group, name)
