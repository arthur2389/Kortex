from os import makedirs, path
from KortexCore.CommonUtils.DataModerator import DataModerator

from KortexCore.CommonUtils.Singleton import singleton as singleton
from KortexCore.Event.Event import Event as Event
from KortexCore.CommonUtils.JsonIO import JsonIO as JsonIO
import EnumAndConsts.EnumsAndConsts as KortexEnums


@singleton
class EventAdapter(object):
    """
    Adapter between Event and File. Also stand for factory for events
    """
    def __init__(self):
        self._data_moderator = DataModerator()

    def get_event(self, directory, file_factory):
        """
        Creates new event and creates .kor metadata folder, as well as metadata file
        for the event if needed.

        param: directory: holding directory of the event (Directory)
        return: new event (Event)
        """
        load_existing_event = True

        # Create directory for metadata
        repo_folder = path.join(directory.path, self._data_moderator.get_data(group="project_consts",
                                                                              parameter="project_repo_name"))
        if not path.exists(repo_folder):
            makedirs(repo_folder)

        event_data_file = path.join(repo_folder, self._data_moderator.get_data(group="project_consts",
                                                                               parameter="event_data_file_name"))

        # In case the event is new, create the metadata file
        if not path.exists(event_data_file):
            JsonIO.create_empty_file(event_data_file)
            load_existing_event = False

        # Create event object
        event = Event(directory, file_factory)

        # In case the event already exists from previous activations, load the properties
        # Otherwise, set the current date and time to the event
        if load_existing_event:
            event.load_properties()
        else:
            event.set_current_date_time()

        return event
