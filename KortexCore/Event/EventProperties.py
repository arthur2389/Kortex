import abc
from os import path
import datetime

from KortexCore.File.FunctionalFile import FunctionalFile as FunctionalFile
from KortexCore.CommonUtils.JsonIO import JsonIO as JsonIO
import EnumAndConsts.EnumsAndConsts as KortexEnums


class PropertyBase(object):
    """
    Abstract base class for event property. A property is a characterization unit of the event.
    """

    def __init__(self, dir_path):
        """
        param: dirPath: each property is initiated by it's metadata directory path (str)
        """
        self._path = path.join(dir_path, KortexEnums.ConstantData.ProjectRepoName)

    @abc.abstractmethod
    def load_existing(self):
        """
        Load existing property from metadata file.
        """
        pass

    @abc.abstractmethod
    def assign(self, assign_args, **kwargs):
        """
        Assign new value to the property
        """
        pass

    @abc.abstractmethod
    def get(self):
        """
        Get the value of a property
        """
        pass

    def __str__(self):
        """
        Debug method for representing a property
        """
        _repr = self.get()
        if not _repr:
            return self.__class__.__name__ + " : Property does not exists"
        return self.__class__.__name__ + " : " + _repr


class FileBasedProperty(PropertyBase):

    """
    Base class for properties that are represented by functional files in the event's metadata folder.
    Main property variable is FunctionalFile object that stands for the file.
    """
    suffixes = []

    def __init__(self, dir_path):
        super(FileBasedProperty, self).__init__(dir_path)
        self._file = None

    def load_existing(self):
        """
        Load existing property by searching for the specified file
        """
        for suffix in self.__class__.suffixes:
            if path.exists(path.join(self._path, self.__class__.__name__ + suffix)):
                self._file = FunctionalFile(name=self.__class__.__name__ + suffix,
                                            dir_name=self._path,
                                            level=0,
                                            holding_dir=None)
                break

    def assign(self, assign_args, **kwargs):
        """
        param: filePath: assign new file to property by copying and replacing the old file
        """
        self._file = FunctionalFile(name=path.basename(assign_args),
                                    dir_name=path.dirname(assign_args))
        if self._file.suffix not in self.__class__.suffixes:
            raise FileNotFoundError
        self._file.copy(target_dir_path=self._path, new_name=self.__class__.__name__)

    def get(self):
        """
        Returns the full path of the file
        return: file full path (str) or None the is no file
        """
        return self._file.path if self._file else None


class Image(FileBasedProperty):

    """
    Image is a type of file based property
    """
    suffixes = [".jpg", ".png", ".gif", ".svg"]

    def assign(self, assign_args, **kwargs):
        super(Image, self).assign(assign_args=assign_args.img_path)


class DescriptionProperty(PropertyBase):

    """
    Description property stand for a property that can be described by text. The data of the property
    will be held in event's metadata file, that is placed in events metadata folder.
    """
    def __init__(self, dir_path):
        super(DescriptionProperty, self).__init__(dir_path)
        self._data_file_path = path.join(self._path, KortexEnums.ConstantData.EventDataFileName)
        self._desc = None

    def load_existing(self):
        """
        Load existing property from metadata file
        """
        data = JsonIO.read(self._data_file_path)
        if self.__class__.__name__ in data.keys():
            self._set_desc(data[self.__class__.__name__])

    def assign(self, assign_args, **kwargs):
        """
        Write a new description to metadata file
        param: desc: description to write (str)
        """
        JsonIO.write(file_path=self._data_file_path, field=self.__class__.__name__, data=assign_args)

    @abc.abstractmethod
    def _set_desc(self, desc_str):
        """
        Abstract method that is called when loading a description
        param: descStr: description from metadata file
        """
        pass


class Description(DescriptionProperty):

    """
    Event description string. Free description section about the event
    """
    def __init__(self, dir_path):
        super(Description, self).__init__(dir_path)
        self._description = None

    def assign(self, assign_args, **kwargs):
        """
        Assign new description
        param: propArgs: argument object that holds description field (KortexKoreInterface.PropertyArgs)
        """
        self._desc = assign_args.description
        super(Description, self).assign(assign_args=assign_args.description)

    def get(self):
        """
        return: event's description (str)
        """
        return self._description

    def _set_desc(self, desc_str):
        """
        Assign loaded description
        param: descStr: loaded description (str)
        """
        self._desc = desc_str


class QuantifiableProperty(DescriptionProperty):

    """
    Base class of a description that can is countable and comparable.
    """
    @abc.abstractmethod
    def __int__(self):
        """
        QuantifiableProperty object must have an explicit ability to be casted to integer
        """
        pass


class Importance(QuantifiableProperty):

    """
    Event importance. Represented by KortexEnums.Importance enumeration
    """
    def __init__(self, dir_path):
        """
        Default importance is set to trivial
        """
        super(Importance, self).__init__(dir_path)
        self._importance = KortexEnums.Importance.TRIVIAL

    def assign(self, assign_args, **kwargs):
        """
        Assign new importance value
        param: propArgs: argument object that holds importance field (KortexKoreInterface.PropertyArgs)
        """
        if not isinstance(assign_args.importance, KortexEnums.Importance):
            raise TypeError
        self._importance = assign_args.importance
        super(Importance, self).assign(assign_args=assign_args.importance.name)

    def get(self):
        """
        return: event importance (KortexEnums.Importance)
        """
        return self._importance

    def __int__(self):
        """
        Cast to integer by taking the value of the enumeration
        return: importance value (int)
        """
        return self._importance.value

    def __str__(self):
        """
        Debug method to represent the importance
        """
        importance = self.get()
        if not importance:
            return "Importance : Property does not exists"
        return "Importance : " + importance.name

    def _set_desc(self, desc_str):
        """
        Load importance from file to object by convertig string to KortexEnums.Importance enum
        param: descStr: loaded importance from file (str)
        """
        self._importance = getattr(KortexEnums.Importance, desc_str)


class MoneyBalance(QuantifiableProperty):
    """
    Represents money input or output of the event
    """

    def __init__(self, dir_path):
        super(MoneyBalance, self).__init__(dir_path)
        self._money_balance = 0

    def assign(self, assign_args, **kwargs):
        """
        Assign new money balance value
        param: propArgs: argument object that holds moneyBalance field (KortexKoreInterface.PropertyArgs)
        """
        self._money_balance = int(assign_args.money_balance)
        super(MoneyBalance, self).assign(assign_args=assign_args.money_balance)

    def get(self):
        """
        return: money balamce value (int)
        """
        return self._money_balance

    def __str__(self):
        money_balance = self.get()
        if not money_balance:
            return "MoneyBalance : Property does not exists"
        return "MoneyBalance : " + str(money_balance)

    def __int__(self):
        """
        return: money balance value (int)
        """
        return int(self._money_balance)

    def _set_desc(self, desc_str):
        """
        Convent string money balance to integer field
        param: descStr: money balance (str)
        """
        self._money_balance = int(desc_str)


class DateAndTime(QuantifiableProperty):

    """
    Date and time of the event
    """
    class Date(object):
        """
        Class that stands for representing the date
        """

        days_in_month = 30
        days_in_year = 365

        def __init__(self, year, month, day):
            """
            Initiate new date. Default is 1.1.2010
            param: year: year must be > 0 (int)
            param month: month must be 12 > m > 0 (int)
            param day: day must be 31 > d > 0 (int)
            """
            if year < 0 or month < 0 or day < 0 or month > 12 or day > 31:
                raise ValueError
            self._year = year
            self._month = month
            self._day = day

        def __str__(self):
            """
            Debug method to represent date
            """
            return str(self.day) + "/" + str(self.month) + "/" + str(self.year)

        def __int__(self):
            """
            Cast date to srting by summing the number of days
            return: total numver of days (int)
            """
            return self.day + self.month * self.__class__.days_in_month \
                            + self.year * self.__class__.days_in_year

        @property
        def year(self):
            return self._year

        @year.setter
        def year(self, value):
            if value < 0:
                raise ValueError
            self._year = value

        @property
        def month(self):
            return self._month

        @month.setter
        def month(self, value):
            if value < 0 or value > 12:
                raise ValueError
            self._month = value

        @property
        def day(self):
            return self._day

        @day.setter
        def day(self, value):
            if value < 0 or value > 31:
                raise ValueError
            self._day = value

    class Time(object):
        """
        Class that stands for representing the time
        """

        minutes_in_hour = 60

        def __init__(self, hours, minutes):
            """
            Initiate new time. Default is 00:00
            param: hours: hours must be 23 > h > 0 (int)
            param minutes: minutes must be 59 > m > 0 (int)
            """
            if hours < 0 or hours > 23 or minutes < 0 or minutes > 59:
                raise ValueError
            self._hours = hours
            self._minutes = minutes

        def __str__(self):
            """
            Debug method to represent time
            """
            if self.minutes == 0:
                min_str = "00"
            else:
                min_str = str(self.minutes)
            return str(self.hours) + ":" + min_str

        def __int__(self):
            """
            Cast time to integer by summing the total minutes
            return: sum of the minutes (int)
            """
            return self.minutes + self.hours * self.__class__.minutes_in_hour

        @property
        def hours(self):
            return self._hours

        @hours.setter
        def hours(self, value):
            if value < 0 or value > 23:
                raise ValueError
            self._hours = value

        @property
        def minutes(self):
            return self._minutes

        @minutes.setter
        def minutes(self, value):
            if value < 0 or value > 59:
                raise ValueError
            self._minutes = value

    minutes_in_day = 1440

    def __init__(self, dir_path):
        """
        Initialize date and time by default values
        """
        super(DateAndTime, self).__init__(dir_path)
        self._date = None
        self._time = None
        self._date_and_time_set = False

    @property
    def is_set(self):
        """
        return: is the date and time set for the event
        type: Bool
        """
        return self._date_and_time_set

    def get(self):
        """
        Get value of date and time by string
        return: "DD:MM:YYYY HH:MM" date and time (str)
        """
        if None in [self._date, self._time]:
            return None
        return str(self._date) + " " + str(self._time)

    def __int__(self):
        """
        Cast data and time to integer by summing the total number of minutes
        return: total number of minutes (int)
        """
        if not self._date or not self._time:
            return 0
        return int(self._time) + int(self._date) * self.__class__.minutes_in_day

    def _set_desc(self, desc_str):
        """
        Parse date and time input from metadata file and assign in object
        param descStr: data and time from file (str)
        """
        date, time = desc_str.split(" ")
        self._set_date_time(date, time)

    def _parse_date(self, date_str):
        """
        Turns "DD:MM:YYYY" to integers that represent the date
        param dateStr: "DD:MM:YYYY" (str)
        return: day, month, year (tuple (int, int, int))
        """
        data_list = date_str.split("/")
        if len(data_list) != 3:
            raise TypeError
        return int(data_list[0]), int(data_list[1]), int(data_list[2])

    def _parse_time(self, time_str):
        """
        Turns "HH:MM" to integers that represent the time
        param dateStr: "HH:MM" (str)
        return: hours, minutes (tuple (int, int))
        """
        data_list = time_str.split(":")
        if len(data_list) != 2:
            raise TypeError
        return int(data_list[0]), int(data_list[1])

    def _set_date_time(self, date, time):
        """
        Parse data and time to integer form and create the objects
        param: date: "DD:MM:YYYY" (str)
        param: time: "HH:MM" (str)
        """
        day, month, year = self._parse_date(date)
        self._date = DateAndTime.Date(day=day, month=month, year=year)
        hours, minutes = self._parse_time(time)
        self._time = DateAndTime.Time(hours=hours, minutes=minutes)
        self._date_and_time_set = True


class StartDateAndTime(DateAndTime):
    
    def __init__(self, dir_path):
        super(StartDateAndTime, self).__init__(dir_path)
        now = datetime.datetime.now()
        self._set_date_time(date=now.strftime("%d/%m/%Y"), time=now.strftime("%H:%M"))
        super(StartDateAndTime, self).assign(assign_args=self.get())

    def assign(self, assign_args, event, **kwargs):
        """
        Assign new start date and  time value for the event
        param: propArgs: argument object that holds date and time fields (KortexKoreInterface.PropertyArgs)
        """
        end_date_and_time = event.get_property(KortexEnums.EPropertyType.END_DATE_AND_TIME)
        self._set_date_time(assign_args.date, assign_args.time)
        # assert start date and time is not ahead of end data and time
        if end_date_and_time.is_set and int(end_date_and_time) < int(self):
            raise NotImplementedError
        super(StartDateAndTime, self).assign(assign_args=self.get())


class EndDateAndTime(DateAndTime):

    def assign(self, assign_args, event, **kwargs):
        """
        Assign new end date and  time value for the event
        param: propArgs: argument object that holds date and time fields (KortexKoreInterface.PropertyArgs)
        """
        start_date_and_time = event.get_property(KortexEnums.EPropertyType.START_DATE_AND_TIME)
        self._set_date_time(assign_args.date, assign_args.time)
        if int(start_date_and_time) > int(self):
            raise NotImplementedError
        super(EndDateAndTime, self).assign(assign_args=self.get())
