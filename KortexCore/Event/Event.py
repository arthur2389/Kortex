from EnumAndConsts.EnumsAndConsts import EPropertyType as EPropertyType
from EnumAndConsts.EnumsAndConsts import ETimeInterval as ETimeInterval
import KortexCore.Event.EventProperties as EventProperties


class Event(object):

    """
    Interface object for all events in Kortex project. Event consists of a set of properties and
    and a reference to it's holding directory that provides the event the abilities that are
    related to file system.
    """
    minute_to_time_unit = {ETimeInterval.MINUTE: 1,
                           ETimeInterval.HOUR: EventProperties.DateAndTime.Time.minutes_in_hour,
                           ETimeInterval.DAY: EventProperties.DateAndTime.minutes_in_day}

    def __init__(self, directory, file_factory):
        """
        Initialize event object with default properties and a holding directory
        param: directory: the directory of the event (Directory)
        """
        self._dir = directory
        self._prop_objs = {EPropertyType.DESCRIPTION: EventProperties.Description(self._dir.path),
                           EPropertyType.IMAGE: EventProperties.Image(self._dir.path),
                           EPropertyType.IMPORTANCE: EventProperties.Importance(self._dir.path),
                           EPropertyType.START_DATE_AND_TIME: EventProperties.StartDateAndTime(self._dir.path),
                           EPropertyType.END_DATE_AND_TIME: EventProperties.EndDateAndTime(self._dir.path),
                           EPropertyType.MONEY_BALANCE: EventProperties.MoneyBalance(self._dir.path)}
        self._fileFactory = file_factory

    @property
    def files(self):
        return self._dir.functional_files

    @property
    def events(self):
        return self._dir.directories

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

    def get_property(self, prop_name):
        """
        Get a raw property object from the event
        param: propName: property name (KortexEnums.EProperty)
        return: full property object (Property)
        """
        return self._prop_objs[prop_name]

    def get_name(self):
        """
        return: events name (str)
        """
        return self._dir.name

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
        self._prop_objs[prop_name].assign(assign_args=prop_args, event=self)

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
            event_list.sort(key=lambda event: int(event.get_property(sort_by)))
        return event_list

    def get_duration(self, time_unit):
        """
        """
        start_date, end_date =\
            self._prop_objs[EPropertyType.START_DATE_AND_TIME], self._prop_objs[EPropertyType.END_DATE_AND_TIME]
        if not end_date.is_set:
            return float(0)
        time_between_start_and_end = int(end_date) - int(start_date)
        return float(time_between_start_and_end/self.__class__.minute_to_time_unit[time_unit])

    def import_file(self, path=None, new_name=None):
        """
        """
        file = self._fileFactory.generate_functional_file(path_file=path, level=self._dir._level)
        file.copy(target_dir_obj=self._dir, new_name=new_name)

    def move_file(self, file, new_event, erase_current=True, new_name=None):
        """
        """
        if erase_current:
            file.Move(targetDir=new_event.get_directory(), new_name=new_name)
        else:
            file.Copy(targetDir=new_event.get_directory(), new_name=new_name)
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
