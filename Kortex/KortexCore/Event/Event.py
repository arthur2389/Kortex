from Kortex.KortexData.KortexEnums import EPropertyType as EPropertyType
import Kortex.KortexCore.Event.EventProperties as EventProperties


class Event(object):

    def __init__(self, directory):
        self._dir = directory
        self._propObjs = {EPropertyType.DESCRIPTION: EventProperties.Description(self._dir.path),
                          EPropertyType.IMAGE: EventProperties.Image(self._dir.path),
                          EPropertyType.IMPORTANCE: EventProperties.Importance(self._dir.path),
                          EPropertyType.DATE_AND_TIME: EventProperties.DateAndTime(self._dir.path),
                          EPropertyType.MONEY_BALANCE: EventProperties.MoneyBalance(self._dir.path)}

    def LoadProperties(self):
        for prop in self._propObjs.values():
            prop.LoadExisting()

    def SetDirectory(self, directory):
        self._dir = directory

    def GetDirectory(self):
        return self._dir

    def GetProperty(self, propName):
        return self._propObjs[propName]

    def GetName(self):
        return self._dir.name

    def __getitem__(self, propName):
        return self._propObjs[propName].Get()

    def __setitem__(self, propName, propArgs):
        self._propObjs[propName].Assign(propArgs)

    def GetEventList(self, sortBy=None):
        def _sort(event, sortProperty):
            return int(event.GetProperty(sortProperty))

        dirList = []
        self._dir.GetAllDirectories(dirList)
        eventList = [_dir.GetEvent() for _dir in dirList]
        if sortBy:
            eventList.sort(key=lambda event: _sort(event, sortBy))
        return eventList

    def __repr__(self):
        return "Event << " + self.GetName() + " >>"
