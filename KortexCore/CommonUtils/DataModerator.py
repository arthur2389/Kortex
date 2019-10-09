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
        self.projects = JsonIO.read(path.join(self._data_files, "projects"))

    def get_data(self, group, parameter):
        _file = JsonIO.read(path.join(self._data_files, group))
        return _file[parameter]

    def get_file_path(self, group, name):
        return path.join(self._images, group, name + ".png")

    def get_current_project(self):
        name = self.projects["current_project"]
        return self.projects["projects"][name], name

    def set_current_project(self, name):
        self.projects["current_project"] = name
        JsonIO.write(file_path=path.join(self._data_files, "projects"),
                     field="current_project",
                     data=name)

    @property
    def projectnames(self):
        return self.projects["projects"].keys()
