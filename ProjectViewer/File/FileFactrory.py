from os import path, listdir, makedirs
from ProjectViewer.File.Directory import Directory as Directory
from ProjectViewer.File.FunctionalFile import FuncrionalFile as FunctionalFile
from ProjectViewer.Event.Event import Event as Event
from ProjectViewer.CommonUtils.JsonIO import JsonIO as JsonIO
import ProjectViewer.PVData.PVEnums as PVEnums


class FileFactory(object):

    def __init__(self):
        self._eventAdapter = EventAdapter()

    def GenerateFunctionalFile(self, pathFile, level=0):
        if not pathFile:
            return
        assert path.isfile(pathFile)
        filename, fileDirname = self._getFileAndDirName(pathFile=pathFile)
        return FunctionalFile(filename, fileDirname, level)

    def GenerateDirectory(self, pathFile, level=0):

        filename, fileDirname = self._getFileAndDirName(pathFile=pathFile)

        _dir = Directory(filename, fileDirname, level)
        event = self._eventAdapter.GetEvent(pathFile, _dir)
        _dir.SetEvent(event)
        fileList = listdir(pathFile)
        fileList.remove(PVEnums.ConstantData.projectRepoName)

        for file in fileList:
            fullPath = path.join(pathFile, file)
            if path.isdir(fullPath):
                fileObj = self.GenerateDirectory(fullPath, level + 1)
                _dir.AddDirectory(fileObj)
            else:
                fileObj = self.GenerateFunctionalFile(fullPath, level + 1)
                _dir.AddFunctionalFile(fileObj)
        return _dir

    def _getFileAndDirName(self, pathFile):
        return path.basename(pathFile), path.dirname(pathFile)


class EventAdapter(object):

    def __init__(self):
        self.propertySetters = {PVEnums.EPropertyType.DESCRIPTION: self.AddDescription,
                                PVEnums.EPropertyType.IMAGE: self.AddImage,
                                PVEnums.EPropertyType.IMPORTANCE: self.AddImportance,
                                PVEnums.EPropertyType.DATE_AND_TIME: self.AddDateAndTime}

    def __getitem__(self, propName):
        return self.propertySetters[propName]

    def GetEvent(self, eventPath, directory):
        repoFolder = path.join(eventPath, PVEnums.ConstantData.projectRepoName)
        if not path.exists(repoFolder):
            makedirs(repoFolder)
        eventDataFile = path.join(repoFolder, PVEnums.ConstantData.eventDataFileName)
        if not path.exists(eventDataFile):
            JsonIO.CreateEmptyFile(eventDataFile)
        return Event(directory)

    def AddDescription(self, event, desc, **kwargs):
        if None in [event, desc]:
            raise TypeError
        event.GetProperty(PVEnums.EPropertyType.DESCRIPTION).Assign(desc)

    def AddImage(self, event, picPath, **kwargs):
        if None in [event, picPath]:
            raise TypeError
        event.GetProperty(PVEnums.EPropertyType.IMAGE).Assign(picPath)

    def AddImportance(self, event, importance, **kwargs):
        if None in [event, importance]:
            raise TypeError
        event.GetProperty(PVEnums.EPropertyType.IMPORTANCE).Assign(importance)

    def AddDateAndTime(self, event, date, time, **kwargs):
        if None in [event, date, time]:
            raise TypeError
        event.GetProperty(PVEnums.EPropertyType.DATE_AND_TIME).Assign(date, time)
