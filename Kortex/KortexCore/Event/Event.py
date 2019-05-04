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

    def __str__(self):
        _str = "Event Name : " +  self.GetName() + "\n"
        for prop in self._propObjs.values():
            _str += str(prop) + "\n"
        return _str
