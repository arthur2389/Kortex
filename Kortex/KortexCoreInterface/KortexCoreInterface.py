from os import path
from Kortex.KortexCore.File.FileFactrory import FileFactory as FileFactory
from Kortex.KortexCore.Event.EventAdapter import EventAdapter as EventAdapter


class KortexCoreInterface(object):

    def __init__(self, rootdir):
        def _getName(_dir):
            return _dir.name

        self._eventAdapter = EventAdapter()
        self._fileFactory = FileFactory()
        self._project = self._fileFactory.GenerateDirectory(rootdir)
        allDirs = []
        self._project.GetAllDirectories(dirList=allDirs)
        self._allEvents = list(map(_getName, allDirs))

    def AddPropertyToEvent(self, event, property, picPath=None,
                           desc=None, importance=None, date=None, time=None):
        self._eventAdapter[property](event=event,
                                     picPath=picPath,
                                     desc=desc,
                                     importance=importance,
                                     date=date,
                                     time=time)

    def CreateEvent(self, eventName, holdingEvent=None):
        if eventName in self._allEvents:
            raise NotImplementedError
        holdingEvent = holdingEvent or self._project.GetEvent()
        _dir = holdingEvent.GetDirectory()
        createdDir = self._fileFactory.GenerateDirectory(path.join(_dir.path, eventName), _dir.level + 1)
        # Append the event name to all the event name list
        _dir.AddDirectory(createdDir)
        self._allEvents.append(createdDir.name)

        return createdDir.GetEvent()

    def GetEvent(self, name):
        event = self._project.FindDirectory(name=name, getEvent=True)
        if not event:
            raise FileNotFoundError
        return event

    def PrintProjectTree(self):
        print("Project : \n\n" + str(self._project))


class PropertyArgs(object):

    def __init__(self, imgPath=None,
                 description=None,
                 importance=None,
                 data=None,
                 time=None,
                 moneyBalance=None):
        self.imgPath = imgPath
        self.description = description
        self.importance = importance
        self.data = data
        self.time = time
        self.moneyBalance = moneyBalance
