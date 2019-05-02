from os import makedirs, path

from Kortex.KortexCore.Event.Event import Event as Event
from Kortex.KortexCore.CommonUtils.JsonIO import JsonIO as JsonIO
import Kortex.KortexData.KortexEnums as PVEnums


class EventAdapter(object):

    def __init__(self):
        self.propertySetters = {PVEnums.EPropertyType.DESCRIPTION: self.AddDescription,
                                PVEnums.EPropertyType.IMAGE: self.AddImage,
                                PVEnums.EPropertyType.IMPORTANCE: self.AddImportance,
                                PVEnums.EPropertyType.DATE_AND_TIME: self.AddDateAndTime}

    def __getitem__(self, propName):
        return self.propertySetters[propName]

    def GetEvent(self, directory):
        # Create directory for metadata
        repoFolder = path.join(directory.path, PVEnums.ConstantData.projectRepoName)
        if not path.exists(repoFolder):
            makedirs(repoFolder)
        # Create metadata file
        eventDataFile = path.join(repoFolder, PVEnums.ConstantData.eventDataFileName)
        if not path.exists(eventDataFile):
            JsonIO.CreateEmptyFile(eventDataFile)
        return Event(directory)

    def AddDescription(self, event, desc, **kwargs):
        if None in [event, desc]:
            raise TypeError
        event.GetProperty(PVEnums.EPropertyType.DESCRIPTION).Assign(desc)

    def AddImage(self, event, picPath, **kwargs):
        if None in [event, picPath]:
            raise TypeError
        event.GetProperty(PVEnums.EPropertyType.IMAGE).Assign(picPath)

    def AddImportance(self, event, importance, **kwargs):
        if None in [event, importance]:
            raise TypeError
        event.GetProperty(PVEnums.EPropertyType.IMPORTANCE).Assign(importance)

    def AddDateAndTime(self, event, date, time, **kwargs):
        if None in [event, date, time]:
            raise TypeError
        event.GetProperty(PVEnums.EPropertyType.DATE_AND_TIME).Assign(date, time)