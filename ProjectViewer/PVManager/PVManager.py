from os import path

from ProjectViewer.File.FileFactrory import FileFactory as FileFactory
from ProjectViewer.File.FileFactrory import EventAdapter as EventAdapter
from ProjectViewer.Event.EventAdapter import EventAdapter as EventAdapter


class PVManager(object):

    def __init__(self, rootdir):
        self._eventAdapter = EventAdapter()
        self._fileFactory = FileFactory()
        self._project = self._fileFactory.GenerateDirectory(rootdir)

    def AddPropertyToEvent(self, eventPath, property, picPath=None,
                           desc=None, importance=None, date=None, time=None):
        eventFolder = self._project.GetFile(filePath=eventPath)
        self._eventAdapter[property](event=eventFolder.GetEvent(),
                                     picPath=picPath,
                                     desc=desc,
                                     importance=importance,
                                     date=date,
                                     time=time)

    def CreateEvent(self, eventName, holdingEvent=None):
        holdingEvent = holdingEvent or self._project.GetEvent()
        _dir = holdingEvent.GetDirectory()
        createdDir = self._fileFactory.GenerateDirectory(path.join(_dir.path, eventName), _dir.level + 1)
        return createdDir.GetEvent()

    def GetEvent(self, name):
        event = self._project.FindDirectory(name=name, getEvent=True)
        if not event:
            raise FileNotFoundError
        return event

    def PrintProjectTree(self):
        print("Project : \n\n" + str(self._project))
