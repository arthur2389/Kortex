from ProjectViewer.File.FileFactrory import FileFactory as FileFactory
from ProjectViewer.File.FileFactrory import EventAdapter as EventAdapter


class PVManager(object):

    def __init__(self, rootdir, projectName):
        self._projectName = projectName
        self._eventAdapter = EventAdapter()
        self._fileFactory = FileFactory()
        self._project = self._fileFactory.GenerateDirectory(rootdir)
        self._writeProjectName(rootdir, projectName)

    def AddPropertyToTheme(self, eventPath, property, picPath=None,
                           desc=None, importance=None, date=None, time=None):
        eventFolder = self._project.GetFile(fileName=eventPath)
        self._eventAdapter[property](event=eventFolder.GetEvent(),
                                     picPath=picPath,
                                     desc=desc,
                                     importance=importance,
                                     date=date,
                                     time=time)

    def GetEvent(self, name):
        return self._project.FindEvent(name)

    def PrintProjectTree(self):
        print("Project : \n\n" + str(self._project))

    def _writeProjectName(self, rootdir, projectName):
        pass
