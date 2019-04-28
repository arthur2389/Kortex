from ProjectViewer.File.File import File as File
from ProjectViewer.PVData.PVEnums import EFileType as EFileType

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

    def GetFile(self, fileName):
        if self.path == fileName:
            return self
        for file in self._fileList[EFileType.DIRECTORY]:
            file = file.GetFile(fileName)
            if file != None:
                return file
        return None

    def FindEvent(self, name):
        if self._name == name:
            return self._event
        for file in self._fileList[EFileType.DIRECTORY]:
            event =  file.FindEvent(name)
            if event != None:
                return event
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
