from os import path

from KortexCore.CommonUtils.DataModerator import DataModerator
from KortexCore.Exception.Exception import ProjectAlreadyExists
from KortexCore.CommonUtils.Singleton import singleton


class Project(object):

    class _LoadedData(object):

        def __init__(self, root, events):
            self.root = root
            self.events = events

    def __init__(self, name, _path, root=None, events=[]):
        self._name = name
        self._path = _path
        self._loaded_data = None
        self._root = root
        self._events = events

    @property
    def name(self):
        return self._name

    @property
    def path(self):
        return self._path

    @property
    def root(self):
        return self._root

    @property
    def events(self):
        return self._events

    @root.setter
    def root(self, root):
        self._root = root

    @events.setter
    def events(self, events):
        self._events = events

    def is_not_loaded(self):
        return not self._root

    def __repr__(self):
        return "(" + self.name + " : " + self.path + ") "


@singleton
class ProjectManager(object):

    def __init__(self):
        self._data_moderator = DataModerator()
        self._current = self._data_moderator.get_data(group="projects_local",
                                                      parameter="current_project")
        projects = self._data_moderator.get_data(group="projects_local",
                                                 parameter="projects")

        self._projects = {name: Project(name=name, _path=_path) for name, _path
                          in projects.items()}

        if self._projects and not self._current:
            self._current = self._projects[0]

    def no_projects_crated(self):
        return not self._projects

    def get_current_project(self):
        return self._projects[self._current]

    def set_current_project(self, name):
        self._current = name
        self._data_moderator.write_data(group="projects_local",
                                        parameter="current_project",
                                        new_data=self._current)

    def set_new_project(self, name, pr_path):
        if name in self._projects:
            raise ProjectAlreadyExists
        self._projects.update({name: Project(name=name, _path=path.join(pr_path, name))})
        self._data_moderator.write_data(group="projects_local",
                                        parameter="projects",
                                        new_data={pr.name: pr.path for pr in self._projects.values()})
        self.set_current_project(name)

    @property
    def projectnames(self):
        return self._projects.keys()
