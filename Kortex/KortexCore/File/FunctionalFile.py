from shutil import move, copyfile
from os import path, remove

from Kortex.KortexCore.File.File import File as File


class FuncrionalFile(File):

    """
    FuncrionalFile object stand for one functional file in Kortex project file system. Functional file can
    the text, presentation, image file etc.
    """
    def __init__(self, name, level=0, holdingDir=None, dirname=None):
        """
        Initialize FunctionalFile object
        param: name: last name of directory (str)
        param dirname: holding directory full path (str)
        param: level: directory level in project tree (int)
        param: holdingDir: Holding directory object (Directory)
        """
        super(FuncrionalFile, self).__init__(name=name, dirname=dirname, level=level, holdingDir=holdingDir)
        self._suffix = "." + name.split(".")[-1]

    @property
    def suffix(self):
        """
        Return the file suffix, that implies its functionality.
        return: fie suffix (str)
        """
        return self._suffix

    def Remove(self):
        """
        Remove functional file from the Kortex project
        """

        # Update the holding directory by removing the file object
        if self._holdingDir:
            self._holdingDir.RemoveFunctionalFile(self)

        # remove file from file system and delete the object
        remove(self.path)
        del self

    def Move(self, targetDir, newName=None):
        """
        Move the current file to a new directory in the project.
        param: targetDir: directory to move to (Directory)
        """
        # Remove the object from the list of functional files in the holding directory
        if self._holdingDir:
            self._holdingDir.RemoveFunctionalFile(self)

        self._changeNameAndReplace(method=copyfile, newName=newName, targetDirPath=targetDir.path)

        # Update the file and the holding directory
        targetDir.AddFunctionalFile(self)
        self._holdingDir = targetDir

    def Copy(self, targetDirObj=None, targetDirPath=None, newName=None):
        """
        Copy functional file, possibly assign new name for it.
        param: targetDir: Full path destination for the file (str)
        param: newName: new name for the file (None/str)
        """
        if not targetDirObj and not targetDirPath:
            raise NotImplementedError

        if targetDirObj:
            self._changeNameAndReplace(method=copyfile, newName=newName, targetDirPath=targetDirObj.path)

            # Update the file and the holding directory
            targetDirObj.AddFunctionalFile(self)
            self._holdingDir = targetDirObj
        else:
            self._changeNameAndReplace(method=copyfile, newName=newName, targetDirPath=targetDirPath)

    def _changeNameAndReplace(self, method, newName, targetDirPath):
        oldPath = self.path
        if newName:
            self.name = newName + self._suffix
        method(oldPath, path.join(targetDirPath, self.name))

    def __str__(self):
        """
        Debug procedure that prints the file name
        """
        super(FuncrionalFile, self).__str__()
        return self._tabs + self._name + "\n"

