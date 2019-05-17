from shutil import rmtree, move
from os import path

from Kortex.KortexCore.File.File import File as File
from Kortex.KortexData.KortexEnums import EFileType as EFileType


class Directory(File):

    """
    Directory object stand for one directory in Kortex project file system. Holds reference to an
    event that is placed in it. Directory is made to supply the held event the functionality of
    the file system - holding and looking up other directories and files, as well as move and
    remove procedures.
    """
    def __init__(self, name, dirname, level, holdingDir, event=None):
        """
        Initialize Directory object
        param: name: last name of directory (str)
        param dirname: holding directory full path (str)
        param: level: directory level in project tree (int)
        param: holdingDir: Holding directory object (Directory)
        param event: event held in the directory (Event)
        """
        super(Directory, self).__init__(name=name, dirname=dirname, level=level, holdingDir=holdingDir)
        self._fileList = {EFileType.DIRECTORY: [],
                          EFileType.FUNCTIONAL_FILE: []}
        self._event = event

    @property
    def allfiles(self):
        """
        return: All files that are directly under the directory (list <File>)
        """
        return self._fileList[EFileType.FUNCTIONAL_FILE] + self._fileList[EFileType.DIRECTORY]

    def AddFunctionalFile(self, file):
        """
        Add file to the list of files that are directly under the directory
        param: file: file to add (FunctionalFile)
        """
        self._fileList[EFileType.FUNCTIONAL_FILE].append(file)

    def AddDirectory(self, file):
        """
        Add directory to the list of directories that are directly under the directory
        param: file: directory to add (Directory)
        """
        self._fileList[EFileType.DIRECTORY].append(file)

    def RemoveFunctionalFile(self, file):
        """
        Remove file from the list of files that are directly under the directory
        param: file: file to remove (FunctionalFile)
        """
        self._fileList[EFileType.FUNCTIONAL_FILE].remove(file)

    def RemoveDirectory(self, file):
        """
        Remove directory from the list of directories that are directly under the directory
        param: file: directory to remove (Directory)
        """
        self._fileList[EFileType.DIRECTORY].remove(file)

    def Remove(self):
        """
        Remove the current directory from the project. This will practically remove the
        event held by it.
        """
        # Remove the object from the list of directories in the holding directory
        if self._holdingDir:
            self._holdingDir.RemoveDirectory(self)

        # Remove the directory from the file system and delete the object
        rmtree(self.path)
        del self

    def Move(self, targetDir):
        """
        Move the current directory to a new directory in the project. This will practically move
        the event held by it to new holding event. The target directory cannot be nested in the
        moved directory
        param: targetDir: directory to move to (Directory)
        """

        # Assert that target directory is not nested insode moved directory
        foundDir = self.FindDirectory(targetDir.name)
        if foundDir != None:
            raise NotImplementedError

        # Remove the object from the list of directories in the holding directory
        if self._holdingDir:
            self._holdingDir.RemoveDirectory(self)

        # Move the directory to new directory in file system
        move(self.path, path.join(targetDir.path, self.name))

        # Update the directory and the holding directory
        targetDir.AddDirectory(self)
        self._holdingDir = targetDir

    def GetFile(self, filePath):
        """
        Find file by full path
        param: filePath: full path to the file (str)
        return: file (File) if found otherwise None
        """
        if self.path == filePath:
            return self
        for file in self._fileList[EFileType.DIRECTORY]:
            file = file.GetFile(filePath)
            if file != None:
                return file
        return None

    def FindDirectory(self, name, getEvent=False):
        """
        Find directory by name
        param: name:  the last name of the directory (str)
        param getEvent: return the event inside the directory (bool)
        return: If found, directory (Directory) or the held event (Event), otherwise None
        """
        if self._name == name:
            return self._event if getEvent else self
        for file in self._fileList[EFileType.DIRECTORY]:
            foundObj =  file.FindDirectory(name, getEvent)
            if foundObj is not None:
                return foundObj
        return None

    def GetAllDirectories(self, dirList):
        """
        Fills the given list with all the nested directories (not only the once that are directly
        held) in the directory
        param: dirList: the list to be filled with directories (list <Directory>)
        """
        for file in self._fileList[EFileType.DIRECTORY]:
            dirList.append(file)
            file.GetAllDirectories(dirList)

    def GetEvent(self):
        """
        return: reference to the held event (Event)
        """
        return self._event

    def SetEvent(self, event):
        """
        param: event: Event to be set (Event)
        """
        self._event = event

    def __str__(self):
        """
        Debug procedure - print the directory tree
        """
        super(Directory, self).__str__()
        name = self._tabs + "<< " + self._name + " >>\n"
        for file in self.allfiles:
            name += str(file)
        return name
