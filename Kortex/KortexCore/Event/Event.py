from Kortex.KortexData.KortexEnums import EPropertyType as EPropertyType
import Kortex.KortexCore.Event.EventProperties as EventProperties


class Event(object):

    """
    Interface object for all events in Kortex project. Event consists of a set of properties and
    and a reference to it's holding directory that provides the event the abilities that are
    related to file system.
    """
    def __init__(self, directory):
        """
        Initialize event object with default properties and a holding directory
        param: directory: the directory of the event (Directory)
        """
        self._dir = directory
        self._propObjs = {EPropertyType.DESCRIPTION: EventProperties.Description(self._dir.path),
                          EPropertyType.IMAGE: EventProperties.Image(self._dir.path),
                          EPropertyType.IMPORTANCE: EventProperties.Importance(self._dir.path),
                          EPropertyType.DATE_AND_TIME: EventProperties.DateAndTime(self._dir.path),
                          EPropertyType.MONEY_BALANCE: EventProperties.MoneyBalance(self._dir.path)}

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
        self._propObjs[propName].Assign(propArgs)

    def GetEventList(self, sortBy=None):
        """
        Get nested event list of the event. The list may be sorted by a property
        param sortBy: property to sort by or None for not sorted list (KortexEnums.EProperty/None)
        return: sorted event list (list <Event>)
        """
        def _sort(event, sortProperty):
            return int(event.GetProperty(sortProperty))

        dirList = []
        self._dir.GetAllDirectories(dirList)
        eventList = [_dir.GetEvent() for _dir in dirList]
        if sortBy:
            eventList.sort(key=lambda event: _sort(event, sortBy))
        return eventList

    def __repr__(self):
        """
        Debug method that prints thet name of the property
        """
        return "Event << " + self.GetName() + " >>"
