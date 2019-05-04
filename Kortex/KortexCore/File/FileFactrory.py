from os import path, listdir, makedirs

from Kortex.KortexCore.File.Directory import Directory as Directory
from Kortex.KortexCore.File.FunctionalFile import FuncrionalFile as FunctionalFile
from Kortex.KortexCore.Event.EventAdapter import EventAdapter as EventAdapter
import Kortex.KortexData.KortexEnums as KortexEnums


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

        # Create the directory in file system if it doesn't exists
        if not path.exists(pathFile):
            makedirs(pathFile)

        filename, fileDirname = self._getFileAndDirName(pathFile=pathFile)
        _dir = Directory(filename, fileDirname, level)
        event = self._eventAdapter.GetEvent(_dir)
        _dir.SetEvent(event)
        fileList = listdir(pathFile)
        fileList.remove(KortexEnums.ConstantData.projectRepoName)

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
