from os import path, listdir, makedirs
from Kortex.KortexCore.CommonUtils.Singleton import singleton as singleton

from Kortex.KortexCore.File.Directory import Directory as Directory
from Kortex.KortexCore.File.FunctionalFile import FuncrionalFile as FunctionalFile
from Kortex.KortexCore.Event.EventAdapter import EventAdapter as EventAdapter
import Kortex.KortexData.KortexEnums as KortexEnums

@singleton
class FileFactory(object):

    """
    FileFactory is used to initiate (create or map) the Kortex project file system tree. It created
    functional files, it creates and maps the directories, and gets pair Directory and Event objects
    one the another.
    """
    def __init__(self):
        self._eventAdapter = EventAdapter()

    def GenerateFunctionalFile(self, pathFile, level=0, holdingDir=None):
        """
        Create functional file object
        param: pathFile: full path to functional file (str)
        param: level: file level in project tree (int)
        param: holdingDir: holding directory object of the file (Directory)
        return: created functional file object (FunctionalFile)
        """
        assert path.isfile(pathFile)
        return FunctionalFile(name=path.basename(pathFile),
                              level=level,
                              holdingDir=holdingDir,
                              dirname=path.dirname(pathFile))

    def GenerateDirectory(self, pathFile, level=0, holdingDir=None):
        """
        Recursive procedure that maps directories of file system to Directory objects.
        Also creates event for each directory and maps event to it's directory.
        param: pathFile: full path to directory
        param: level: directory level in file system (int)
        param holdingDir: holding directory for the directory (Directory/None)
        return: created directory (Directory)
        """

        # Create the directory in file system if it doesn't exists
        if not path.exists(pathFile):
            makedirs(pathFile)

        # Create directory object, create an event and pair them
        _dir = Directory(name=path.basename(pathFile), dirname=path.dirname(pathFile), level=level, holdingDir=holdingDir)
        event = self._eventAdapter.GetEvent(_dir, self)
        _dir.SetEvent(event)

        # Map all nested directories in the created directory, and remove metadata directory
        # from it as it will not be represented in the tree
        fileList = listdir(pathFile)
        fileList.remove(KortexEnums.ConstantData.projectRepoName)

        # Go over the nested files and map them into objects (FunctionalFile/Directory)
        for file in fileList:
            fullPath = path.join(pathFile, file)
            if path.isdir(fullPath):
                fileObj = self.GenerateDirectory(fullPath, level + 1, _dir)
                _dir.AddDirectory(fileObj)
            else:
                fileObj = self.GenerateFunctionalFile(fullPath, level + 1, _dir)
                _dir.AddFunctionalFile(fileObj)
        return _dir
