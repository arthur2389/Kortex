from Kortex.KortexCore.File.File import File as File
from Kortex.KortexData.KortexEnums import EFileType as EFileType

class Directory(File):

    def __init__(self, name, dirname, level, event=None):
        super(Directory, self).__init__(name=name, dirname=dirname, level=level)
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
