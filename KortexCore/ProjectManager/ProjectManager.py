from KortexCore.CommonUtils.DataModerator import DataModerator
from KortexCore.Exception.Exception import ProjectAlreadyExists
from KortexCore.CommonUtils.Singleton import singleton


class Project(object):

    class _LoadedData(object):

        def __init__(self, root, events):
            self.root = root
            self.events = events

    def __init__(self, name, _path):
        self._name = name
        self._path = _path
        self._loaded_data = None

    @property
    def loaded_data(self):
        return self._loaded_data

    @property
    def name(self):
        return self._name

    @property
    def path(self):
        return self._path

    def set_loaded_data(self, root, events):
        self._loaded_data = self._LoadedData(root=root, events=events)

    def __repr__(self):
        return "(" + self.name + " : " + self._path + ") "


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
        self._projects.update({name: Project(name=name, _path=pr_path)})
        self._data_moderator.write_data(group="projects_local",
                                        parameter="projects",
                                        new_data={pr.name: pr.path for pr in self._projects.values()})
        self.set_current_project(name)

    @property
    def projectnames(self):
        return self._projects.keys()
