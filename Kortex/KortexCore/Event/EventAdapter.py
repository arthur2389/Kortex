from os import makedirs, path

from Kortex.KortexCore.CommonUtils.Singleton import singleton as singleton
from Kortex.KortexCore.Event.Event import Event as Event
from Kortex.KortexCore.CommonUtils.JsonIO import JsonIO as JsonIO
import Kortex.KortexData.KortexEnums as KortexEnums


@singleton
class EventAdapter(object):

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
