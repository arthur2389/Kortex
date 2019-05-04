from os import makedirs, path

from Kortex.KortexCore.CommonUtils.Singleton import singleton as singleton
from Kortex.KortexCore.Event.Event import Event as Event
from Kortex.KortexCore.CommonUtils.JsonIO import JsonIO as JsonIO
import Kortex.KortexData.KortexEnums as KortexEnums

@singleton
class EventAdapter(object):

    def __init__(self):
        self.propertySetters = {KortexEnums.EPropertyType.DESCRIPTION: self.AddDescription,
                                KortexEnums.EPropertyType.IMAGE: self.AddImage,
                                KortexEnums.EPropertyType.IMPORTANCE: self.AddImportance,
                                KortexEnums.EPropertyType.DATE_AND_TIME: self.AddDateAndTime,
                                KortexEnums.EPropertyType.MONEY_BALANCE: self.AddMoneyBalance}

    def __getitem__(self, propName):
        return self.propertySetters[propName]

    def GetEvent(self, directory):
        # Create event object
        event = Event(directory)

        # Create directory for metadata
        repoFolder = path.join(directory.path, KortexEnums.ConstantData.projectRepoName)
        if not path.exists(repoFolder):
            makedirs(repoFolder)

        eventDataFile = path.join(repoFolder, KortexEnums.ConstantData.eventDataFileName)

        # In case the event is new, create the metadata file
        if not path.exists(eventDataFile):
            JsonIO.CreateEmptyFile(eventDataFile)
        # In case the event already exists from previous activations
        else:
            event.LoadProperties()
        return event

    def AddDescription(self, event, desc, **kwargs):
        if None in [event, desc]:
            raise TypeError
        event.GetProperty(KortexEnums.EPropertyType.DESCRIPTION).Assign(desc)

    def AddImage(self, event, picPath, **kwargs):
        if None in [event, picPath]:
            raise TypeError
        event.GetProperty(KortexEnums.EPropertyType.IMAGE).Assign(picPath)

    def AddImportance(self, event, importance, **kwargs):
        if None in [event, importance]:
            raise TypeError
        event.GetProperty(KortexEnums.EPropertyType.IMPORTANCE).Assign(importance)

    def AddDateAndTime(self, event, date, time, **kwargs):
        if None in [event, date, time]:
            raise TypeError
        event.GetProperty(KortexEnums.EPropertyType.DATE_AND_TIME).Assign(date, time)

    def AddMoneyBalance(self, event, moneyBalance, **kwargs):
        if None in [event, moneyBalance]:
            raise TypeError
        event.GetProperty(KortexEnums.EPropertyType.MONEY_BALANCE).Assign(moneyBalance)
