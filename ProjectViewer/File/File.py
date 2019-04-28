import abc
from shutil import copy
from os import path



class File(object):

    __mettaclass__ = abc.ABCMeta

    def __init__(self, name, dirname, level):
        self._name = name
        self._dirname = dirname
        self._level = level
        self._path = None

    @property
    def path(self):
        self._path = path.join(self._dirname, self._name)
        return self._path

    @path.setter
    def path(self, value):
        raise NotImplementedError

    def CopyFile(self, dest):
        if not path.isdir(dest):
            raise ValueError
        copy(self.path, dest)

    def __str__(self):
        self._tabs = "\t" * self._level
