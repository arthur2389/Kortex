from shutil import rmtree, move
from os import path

from Kortex.KortexCore.File.File import File as File
from Kortex.KortexData.KortexEnums import EFileType as EFileType


class Directory(File):

    def __init__(self, name, dirname, level, holdingDir, event=None):
        super(Directory, self).__init__(name=name, dirname=dirname, level=level, holdingDir=holdingDir)
        self._fileList = {EFileType.DIRECTORY: [],
                          EFileType.FUNCTIONAL_FILE: []}
        self._event = event

    @property
    def allfiles(self):
        return self._fileList[EFileType.FUNCTIONAL_FILE] + self._fileList[EFileType.DIRECTORY]

    def AddFunctionalFile(self, file):
        self._fileList[EFileType.FUNCTIONAL_FILE].append(file)

    def AddDirectory(self, file):
        self._fileList[EFileType.DIRECTORY].append(file)

    def RemoveFunctionalFile(self, file):
        self._fileList[EFileType.FUNCTIONAL_FILE].remove(file)

    def RemoveDirectory(self, file):
        self._fileList[EFileType.DIRECTORY].remove(file)

    def Remove(self):
        if self._holdingDir:
            self._holdingDir.RemoveDirectory(self)
        rmtree(self.path)
        del self

    def Move(self, targetDir):
        foundDir = self.FindDirectory(targetDir.name)
        if foundDir != None:
            raise NotImplementedError
        if self._holdingDir:
            self._holdingDir.RemoveDirectory(self)
        move(self.path, path.join(targetDir.path, self.name))
        targetDir.AddDirectory(self)
        self._holdingDir = targetDir

    def GetFile(self, filePath):
        if self.path == filePath:
            return self
        for file in self._fileList[EFileType.DIRECTORY]:
            file = file.GetFile(filePath)
            if file != None:
                return file
        return None

    def FindDirectory(self, name, getEvent=False):
        if self._name == name:
            return self._event if getEvent else self
        for file in self._fileList[EFileType.DIRECTORY]:
            foundObj =  file.FindDirectory(name, getEvent)
            if foundObj is not None:
                return foundObj
        return None

    def GetAllDirectories(self, dirList):
        for file in self._fileList[EFileType.DIRECTORY]:
            dirList.append(file)
            file.GetAllDirectories(dirList)

    def GetEvent(self):
        return self._event

    def SetEvent(self, event):
        self._event = event

    def __str__(self):
        super(Directory, self).__str__()
        name = self._tabs + "<< " + self._name + " >>\n"
        for file in self.allfiles:
            name += str(file)
        return name
