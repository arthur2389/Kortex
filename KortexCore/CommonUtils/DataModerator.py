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

    def get_data(self, group, parameter=None):
        file_data = JsonIO.read(path.join(self._data_files, group))
        if not parameter:
            return file_data
        return file_data[parameter]

    def get_file_path(self, group, name):
        return path.join(self._images, group, name)

    def get_current_project(self):
        name = self.projects["current_project"]
        return self.projects["projects"][name], name

    def set_current_project(self, name):
        self.projects["current_project"] = name
        JsonIO.write(path.join(self._data_files, "projects"),
                     "current_project",
                     name)

    def set_new_project(self, name, pr_path):
        self.projects["projects"].update({name: path.join(pr_path, name)})
        JsonIO.write(path.join(self._data_files, "projects"),
                     "projects",
                     self.projects["projects"])
        self.set_current_project(name)

    @property
    def projectnames(self):
        return self.projects["projects"].keys()
