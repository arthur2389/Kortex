import abc
from os import path


class File(object):

    """
    Abstract base class for file types.
    """
    __mettaclass__ = abc.ABCMeta

    def __init__(self, name, level, holdingDir, dirname):
        self._name = name
        self._level = level
        self._holdingDir = holdingDir
        self._dirname = dirname
        self._path = None

    @property
    def name(self):
        """
        return: file last name (str)
        """
        return self._name

    @name.setter
    def name(self, newName):
        self._name = newName

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
        if self._holdingDir:
            dirPath = self._holdingDir.path
        elif self._dirname:
            dirPath = self._dirname
        else:
            raise NotImplementedError
        self._path = path.join(dirPath, self._name)
        return self._path

    @abc.abstractmethod
    def Remove(self):
        """
        Abstract method to remove a file
        """
        pass

    @abc.abstractmethod
    def Move(self, targetDir, newName=None):
        """
        Abstract method to move a file to ew directory (old reference to the file is deleted
        """
        pass

    @abc.abstractmethod
    def Copy(self, targetDirObj=None, targetDirPath=None, newName=None):
        """
        Copy file to new destination (old reference to the file remains)
        """
        pass

    def __str__(self):
        self._tabs = "\t" * self._level
