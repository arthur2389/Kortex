from shutil import move
from os import path

from ProjectViewer.File.File import File as File


class FuncrionalFile(File):

    def __init__(self, name, dirname, level):
        super(FuncrionalFile, self).__init__(name=name, dirname=dirname, level=level)
        self._suffix = name.split(".")[-1]

    def CopyFile(self, dest, newName=None):
        super(FuncrionalFile, self).CopyFile(dest=dest)
        if not newName:
            return
        assert isinstance(newName, str)
        newName = newName + "." + self._suffix

        move(path.join(dest, self._name), path.join(dest, newName))

        self._dirname = dest
        self._name = newName

    def __str__(self):
        super(FuncrionalFile, self).__str__()
        return self._tabs + self._name + "\n"
