import abc
from shutil import copy
from os import path


class File(object):

    """
    Abstract base class for file types.
    """
    __mettaclass__ = abc.ABCMeta

    def __init__(self, name, dirname, level, holdingDir):
        self._name = name
        self._dirname = dirname
        self._level = level
        self._holdingDir = holdingDir
        self._path = None

    @property
    def name(self):
        """
        return: file last name (str)
        """
        return self._name

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
        self._path = path.join(self._dirname, self._name)
        return self._path

    def CopyFile(self, dest):
        """
        Copy file to new destination (old reference to the file remains)
        param: dest: new pull file path (str)
        """
        if not path.isdir(dest):
            raise ValueError
        copy(self.path, dest)

    @abc.abstractmethod
    def Remove(self):
        """
        Abstract method to remove a file
        """
        pass

    @abc.abstractmethod
    def Move(self, targetDir):
        """
        Abstract method to move a file to ew directory (old reference to the file is deleted
        param: targetDir: directory to move the file to (Directory)
        """
        pass

    def __str__(self):
        self._tabs = "\t" * self._level
