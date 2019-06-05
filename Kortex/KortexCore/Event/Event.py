from Kortex.KortexData.KortexEnums import EPropertyType as EPropertyType
from Kortex.KortexData.KortexEnums import ETimeInterval as ETimeInterval
import Kortex.KortexCore.Event.EventProperties as EventProperties


class Event(object):

    """
    Interface object for all events in Kortex project. Event consists of a set of properties and
    and a reference to it's holding directory that provides the event the abilities that are
    related to file system.
    """
    minuteToTimeUnit = {ETimeInterval.MINUTE: 1,
                        ETimeInterval.HOUR: EventProperties.DateAndTime.Time.minutesInHours,
                        ETimeInterval.DAY: EventProperties.DateAndTime.minutesInDay}

    def __init__(self, directory, fileFactory):
        """
        Initialize event object with default properties and a holding directory
        param: directory: the directory of the event (Directory)
        """
        self._dir = directory
        self._propObjs = {EPropertyType.DESCRIPTION: EventProperties.Description(self._dir.path),
                          EPropertyType.IMAGE: EventProperties.Image(self._dir.path),
                          EPropertyType.IMPORTANCE: EventProperties.Importance(self._dir.path),
                          EPropertyType.START_DATE_AND_TIME: EventProperties.StartDateAndTime(self._dir.path),
                          EPropertyType.END_DATE_AND_TIME: EventProperties.EndDateAndTime(self._dir.path),
                          EPropertyType.MONEY_BALANCE: EventProperties.MoneyBalance(self._dir.path)}
        self._fileFactory = fileFactory

    @property
    def files(self):
        return self._dir.functionalfiles

    def LoadProperties(self):
        """
        Load existing properties from metadata file
        """
        for prop in self._propObjs.values():
            prop.LoadExisting()

    def SetDirectory(self, directory):
        """
        param: directory: new directory to set (Directory)
        """
        self._dir = directory

    def GetDirectory(self):
        """
        return: reference to event's directory (Directory)
        """
        return self._dir

    def GetProperty(self, propName):
        """
        Get a raw property object from the event
        param: propName: property name (KortexEnums.EProperty)
        return: full property object (Property)
        """
        return self._propObjs[propName]

    def GetName(self):
        """
        return: events name (str)
        """
        return self._dir.name

    def __getitem__(self, propName):
        """
        Operator [] - get a property data via Get method
        param: propName: property name (KortexEnums.EProperty)
        return: property data (type varies with property type)
        """
        return self._propObjs[propName].Get()

    def __setitem__(self, propName, propArgs):
        """
        Operator [] - set a property data via Assign method
        param: propName: property name (KortexEnums.EProperty)
        param propArgs: generic data object for setting a property (KortexKoreInterface.PropertyArgs)
        """
        self._propObjs[propName].Assign(assignArgs=propArgs, event=self)

    def GetEventList(self, sortBy=None):
        """
        Get nested event list of the event. The list may be sorted by a property
        param sortBy: property to sort by or None for not sorted list (KortexEnums.EProperty/None)
        return: sorted event list (list <Event>)
        """
        dirList = []
        self._dir.GetAllDirectories(dirList)
        eventList = [_dir.GetEvent() for _dir in dirList]
        if not sortBy:
            return eventList
        if sortBy == EPropertyType.DURATION:
            eventList.sort(key=lambda event: event.GetDuration(timeUnit=ETimeInterval.MINUTE))
        else:
            eventList.sort(key=lambda event: int(event.GetProperty(sortBy)))
        return eventList

    def GetDuration(self, timeUnit):
        """
        """
        startDate, endDate =\
            self._propObjs[EPropertyType.START_DATE_AND_TIME], self._propObjs[EPropertyType.END_DATE_AND_TIME]
        if not endDate.isset:
            return float(0)
        timeBetweenStartAndEnd = int(endDate) - int(startDate)
        return float(timeBetweenStartAndEnd/self.__class__.minuteToTimeUnit[timeUnit])

    def ImportFile(self, path=None, newName=None):
        """
        """
        file = self._fileFactory.GenerateFunctionalFile(pathFile=path, level=self._dir._level)
        file.Copy(targetDirObj=self._dir, newName=newName)

    def MoveFile(self, file, newEvent, eraseCurrent=True, newName=None):
        """
        """
        if eraseCurrent:
            file.Move(targetDir=newEvent.GetDirectory(), newName=newName)
        else:
            file.Copy(targetDir=newEvent.GetDirectory(), newName=newName)
        return file

    def __repr__(self):
        """
        Debug method that prints the name of the property
        """
        return "Event << " + self.GetName() + " >>"
