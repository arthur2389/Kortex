from os import path

from KortexCore.CommonUtils.JsonIO import JsonIO
from KortexCore.CommonUtils.Singleton import singleton


@singleton
class DataModerator(object):

    def __init__(self):
        self._data_files = self._from_base("Metadata//DataFiles")
        self._images = self._from_base("Metadata//Images")
        self.projects = JsonIO.read(path.join(self._data_files, "projects"))

    def get_data(self, group, parameter):
        _file = JsonIO.read(path.join(self._data_files, group))
        return _file[parameter]

    def get_file_path(self, group, name):
        return path.join(self._images, group, name)

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

    def _from_base(self, rel):
        return path.join(path.dirname(path.abspath(__file__)), rel)
