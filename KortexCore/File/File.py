import abc
from os import path


class File(object):

    """
    Abstract base class for file types.
    """
    __mettaclass__ = abc.ABCMeta

    add_me = ""

    def __init__(self, name, level, holding_dir, dir_name):
        self._name = name
        self._level = level
        self._holding_dir = holding_dir
        self._dir_name = dir_name
        self._path = None

    @property
    def name(self):
        """
        return: file last name (str)
        """
        return self._name

    @name.setter
    def name(self, new_name):
        self._name = new_name

    @property
    def level(self):
        """
        return: File level in project tree hierarchy
        """
        return self._level

    @property
    def path(self):
        """
        Full file path
        """
        if self._holding_dir:
            dir_path = self._holding_dir.path
        elif self._dir_name:
            dir_path = self._dir_name
        else:
            raise NotImplementedError
        self._path = path.join(dir_path, self._name)
        return self._path

    @abc.abstractmethod
    def remove(self):
        """
        Abstract method to remove a file
        """
        pass

    @abc.abstractmethod
    def move(self, target_dir, new_name=None):
        """
        Abstract method to move a file to ew directory (old reference to the file is deleted
        """
        pass

    @abc.abstractmethod
    def copy(self, target_dir_obj=None, target_dir_path=None, new_name=None):
        """
        Copy file to new destination (old reference to the file remains)
        """
        pass

    @abc.abstractmethod
    def open(self):
        """
        Open a file
        """
        pass

    def _update_holding_directory(self, target_dir):
        getattr(target_dir, self.__class__.add_me)(self)
        self._holding_dir = target_dir
        self._level = self._holding_dir._level + 1

    def __str__(self):
        self._tabs = "\t" * self._level
