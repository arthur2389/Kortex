from EnumAndConsts.EnumsAndConsts import EPropertyType
from EnumAndConsts.EnumsAndConsts import ETimeInterval
from KortexCore.Event.DateTimeHandler import DateTimeHandler
import KortexCore.Event.EventProperties as EventProperties


class Event(object):

    """
    Interface object for all events in Kortex project. Event consists of a set of properties and
    and a reference to it's holding directory that provides the event the abilities that are
    related to file system.
    """

    def __init__(self, directory, file_factory):
        """
        Initialize event object with default properties and a holding directory
        param: directory: the directory of the event (Directory)
        """
        self._dir = directory
        self._date_time_handler = DateTimeHandler()
        self._prop_objs = {EPropertyType.DESCRIPTION: EventProperties.Description(self._dir.path, directory.name),
                           EPropertyType.COMPLETION_STATUS: EventProperties.CompletionStatus(self._dir.path),
                           EPropertyType.IMAGE: EventProperties.Image(self._dir.path),
                           EPropertyType.IMPORTANCE: EventProperties.Importance(self._dir.path),
                           EPropertyType.CASH_FLOW: EventProperties.CashFlow(self._dir.path),
                           EPropertyType.START_DATE_AND_TIME: EventProperties.StartDateAndTime(self._dir.path, self._date_time_handler),
                           EPropertyType.END_DATE_AND_TIME: EventProperties.EndDateAndTime(self._dir.path, self._date_time_handler)
                           }
        self._fileFactory = file_factory

    @property
    def files(self):
        return self._dir.functional_files

    @property
    def events(self):
        return {name: _dir.get_event() for name, _dir in self._dir.directories.items()}

    def set_current_date_time(self):
        """
        """
        start_dt, end_dt = self._date_time_handler.get_default_date_time()
        self._prop_objs[EPropertyType.START_DATE_AND_TIME].assign(start_dt)
        self._prop_objs[EPropertyType.END_DATE_AND_TIME].assign(end_dt)

    def load_properties(self):
        """
        Load existing properties from metadata file
        """
        for prop in self._prop_objs.values():
            prop.load_existing()

    def set_directory(self, directory):
        """
        param: directory: new directory to set (Directory)
        """
        self._dir = directory

    def get_directory(self):
        """
        return: reference to event's directory (Directory)
        """
        return self._dir

    def get_property(self, prop_name, cast_type=str):
        """
        Get a raw property object from the event
        param: propName: property name (KortexEnums.EProperty)
        return: full property object (Property)
        """
        return cast_type(self._prop_objs[prop_name])

    def get_name(self):
        """
        return: events name (str)
        """
        return self._dir.name

    def set_date_time(self, start_date_time_args=None, end_date_time_args=None):
        """
        """
        start_dt, end_dt = self._date_time_handler.start_and_end_time(curr_start=self[EPropertyType.START_DATE_AND_TIME],
                                                                      start=start_date_time_args,
                                                                      end=end_date_time_args)
        self._prop_objs[EPropertyType.START_DATE_AND_TIME].assign(date_and_time=start_dt)
        self._prop_objs[EPropertyType.END_DATE_AND_TIME].assign(date_and_time=end_dt)

    def __getitem__(self, prop_name):
        """
        Operator [] - get a property data via Get method
        param: propName: property name (KortexEnums.EProperty)
        return: property data (type varies with property type)
        """
        return self._prop_objs[prop_name].get()

    def __setitem__(self, prop_name, prop_args):
        """
        Operator [] - set a property data via Assign method
        param: propName: property name (KortexEnums.EProperty)
        param propArgs: generic data object for setting a property (KortexKoreInterface.PropertyArgs)
        """
        self._prop_objs[prop_name].assign(assign_args=prop_args)

    def get_event_list(self, sort_by=None):
        """
        Get nested event list of the event. The list may be sorted by a property
        param sortBy: property to sort by or None for not sorted list (KortexEnums.EProperty/None)
        return: sorted event list (list <Event>)
        """
        dir_list = []
        self._dir.get_all_directories(dir_list)
        event_list = list(map(lambda d: d.get_event(),  dir_list))
        if not sort_by:
            return event_list
        if sort_by == EPropertyType.DURATION:
            event_list.sort(key=lambda event: event.get_duration(time_unit=ETimeInterval.MINUTE))
        else:
            event_list.sort(key=lambda event: event.get_property(prop_name=sort_by, cast_type=int))
        return event_list

    def get_duration(self, time_unit):
        """
        """
        return self._date_time_handler.get_duration(start_dt=self[EPropertyType.START_DATE_AND_TIME],
                                                    end_dt=self[EPropertyType.END_DATE_AND_TIME],
                                                    time_unit=time_unit)

    def import_file(self, path=None, new_name=None):
        """
        """
        file = self._fileFactory.generate_functional_file(path_file=path, level=self._dir._level)
        file.copy(target_dir_obj=self._dir, new_name=new_name)

    def move_file(self, file, new_event, erase_current=True, new_name=None):
        """
        """
        if erase_current:
            file.move(targetDir=new_event.get_directory(), new_name=new_name)
        else:
            file.copy(targetDir=new_event.get_directory(), new_name=new_name)
        return file

    def open_file(self, file):
        """
        """
        file.open()

    def open_event_location(self):
        """
        """
        self._dir.open()

    def __repr__(self):
        """
        Debug method that prints the name of the property
        """
        return "Event << " + self.get_name() + " >>"
