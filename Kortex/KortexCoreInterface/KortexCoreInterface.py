from os import path
from Kortex.KortexCore.File.FileFactrory import FileFactory as FileFactory
from Kortex.KortexCore.Event.EventAdapter import EventAdapter as EventAdapter


class KortexCoreInterface(object):

    """
    Interface class for Kortex core (engine) operations.
    """
    def __init__(self, rootdir):
        """
        Create interface instance as well as a new project
        param: rootdir: The root directory of the project. If the direcory doesn't
        exist it will be created (str)
        """

        # Create main utils and initialize the project
        self._eventAdapter = EventAdapter()
        self._fileFactory = FileFactory()
        self._project = self._fileFactory.GenerateDirectory(rootdir)

        # Map and store all the event names
        allDirs = []
        self._project.GetAllDirectories(dirList=allDirs)
        self._allEvents = list(map(lambda _dir: _dir.name, allDirs))

    def CreateEvent(self, eventName, holdingEvent=None):
        """
        Create new event. The new event cannot have the same name the other event in the project
        param: eventName: The name of the new event (str)
        param: holdingEvent: The holding event of the created event (Event)
        return: created event (Event)
        """

        # Check if event name already exists
        if eventName in self._allEvents:
            raise NotImplementedError

        # Assign holding event. Default is the root event
        holdingEvent = holdingEvent or self._project.GetEvent()

        # Create directory (and the event) inside the holding event
        _dir = holdingEvent.GetDirectory()
        createdDir = self._fileFactory.GenerateDirectory(path.join(_dir.path, eventName), _dir.level + 1)

        # Append the event name to all the event name list
        _dir.AddDirectory(createdDir)
        self._allEvents.append(createdDir.name)

        # From the created directory return the created event
        return createdDir.GetEvent()

    def RemoveEvent(self, event):
        """
        Remove existing event
        param: event: The event to remove (Event)
        """

        # Extract the event directory from the event, use it to remove itself (and the event)
        directory = event.GetDirectory()
        dirName = directory.name
        directory.Remove()
        self._allEvents.remove(dirName)

    def MoveEvent(self, event, targetHoldingEvent):
        """
        Move event from it's holding event to a new holding event
        param: event: The event to be moved (Event)
        param: targetHoldingEvent: The new holding event. The holding event cannot be held in
        the moved event (Event)
        """

        # Extract the event directory from the event
        directory = event.GetDirectory()

        # Extract the target event directory and move the directories
        targetDirectory = targetHoldingEvent.GetDirectory()
        directory.Move(targetDirectory)

    def GetEvent(self, name):
        """
        Get event by name.
        param: name: The name of the event to return (str)
        return: The found event (Event)
        """
        event = self._project.FindDirectory(name=name, getEvent=True)
        if not event:
            raise FileNotFoundError
        return event

    def PrintProjectTree(self):
        """
        Debug procedure, print all project to command line
        """
        print("Project : \n\n" + str(self._project))


class PropertyArgs(object):

    """
    Input class for assigning new property to an event
    """
    def __init__(self, imgPath=None,
                 description=None,
                 importance=None,
                 date=None,
                 time=None,
                 moneyBalance=None):
        """
        param: imgPath: full path of image [".jpg", ".png", ".gif", ".svg"] file (str)
        param description: event description (str)
        param importance: event importance (KortexEnums.Importance)
        param date: event date (DD/MM/YYYY str)
        param: time: event time (HH:MM str)
        param: moneyBalance: event money in/out (int)
        """
        self.imgPath = imgPath
        self.description = description
        self.importance = importance
        self.date = date
        self.time = time
        self.moneyBalance = moneyBalance
