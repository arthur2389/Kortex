import abc
from os import path
import datetime

from Kortex.KortexCore.File.FunctionalFile import FuncrionalFile as FuncrionalFile
from Kortex.KortexCore.CommonUtils.JsonIO import JsonIO as JsonIO
import Kortex.KortexData.KortexEnums as KortexEnums


class PropertyBase(object):
    """
    Abstract base class for event property. A property is a characterization unit of the event.
    """

    def __init__(self, dirPath):
        """
        param: dirPath: each property is initiated by it's metadata directory path (str)
        """
        self._path = path.join(dirPath, KortexEnums.ConstantData.projectRepoName)

    @abc.abstractmethod
    def LoadExisting(self):
        """
        Load existing property from metadata file.
        """
        pass

    @abc.abstractmethod
    def Assign(self, assignArgs, **kwargs):
        """
        Assign new value to the property
        """
        pass

    @abc.abstractmethod
    def Get(self):
        """
        Get the value of a property
        """
        pass

    def __str__(self):
        """
        Debug method for representing a property
        """
        _repr = self.Get()
        if not _repr:
            return self.__class__.__name__ + " : Property does not exists"
        return self.__class__.__name__ + " : " + _repr


class FileBasedProperty(PropertyBase):

    """
    Base class for properties that are represented by functional files in the event's metadata folder.
    Main property variable is FunctionalFile object that stands for the file.
    """
    suffixes = []

    def __init__(self, dirPath):
        super(FileBasedProperty, self).__init__(dirPath)
        self._file = None

    def LoadExisting(self):
        """
        Load existing property by searching for the specified file
        """
        for suffix in self.__class__.suffixes:
            if path.exists(path.join(self._path, self.__class__.__name__ + suffix)):
                self._file = FuncrionalFile(name=self.__class__.__name__ + suffix,
                                            dirname=self._path,
                                            level=0,
                                            holdingDir=None)
                break

    def Assign(self, assignArgs, **kwargs):
        """
        param: filePath: assign new file to property by copying and replacing the old file
        """
        self._file = FuncrionalFile(name=path.basename(assignArgs),
                                    dirname=path.dirname(assignArgs))
        if self._file.suffix not in self.__class__.suffixes:
            raise FileNotFoundError
        self._file.Copy(targetDirPath=self._path, newName=self.__class__.__name__)

    def Get(self):
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

    def Assign(self, assignArgs, **kwargs):
        super(Image, self).Assign(assignArgs=assignArgs.imgPath)


class DescriptionProperty(PropertyBase):

    """
    Description property stand for a property that can be described by text. The data of the property
    will be held in event's metadata file, that is placed in events metadata folder.
    """
    def __init__(self, dirPath):
        super(DescriptionProperty, self).__init__(dirPath)
        self._dataFilePath = path.join(self._path, KortexEnums.ConstantData.eventDataFileName)
        self._desc = None

    def LoadExisting(self):
        """
        Load existing property from metadata file
        """
        data = JsonIO.Read(self._dataFilePath)
        if self.__class__.__name__ in data.keys():
            self._setDesc(data[self.__class__.__name__])

    def Assign(self, assignArgs, **kwargs):
        """
        Write a new description to metadata file
        param: desc: description to write (str)
        """
        JsonIO.Write(filePath=self._dataFilePath, field=self.__class__.__name__, data=assignArgs)

    @abc.abstractmethod
    def _setDesc(self, descStr):
        """
        Abstract method that is called when loading a description
        param: descStr: description from metadata file
        """
        pass


class Description(DescriptionProperty):

    """
    Event description string. Free description section about the event
    """
    def __init__(self, dirPath):
        super(Description, self).__init__(dirPath)
        self._description = None

    def Assign(self, assignArgs, **kwargs):
        """
        Assign new description
        param: propArgs: argument object that holds description field (KortexKoreInterface.PropertyArgs)
        """
        self._desc = assignArgs.description
        super(Description, self).Assign(assignArgs=assignArgs.description)

    def Get(self):
        """
        return: event's description (str)
        """
        return self._description

    def _setDesc(self, descStr):
        """
        Assign loaded description
        param: descStr: loaded description (str)
        """
        self._desc = descStr


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
    def __init__(self, dirPath):
        """
        Default importance is set to trivial
        """
        super(Importance, self).__init__(dirPath)
        self._importance = KortexEnums.Importance.TRIVIAL

    def Assign(self, assignArgs, **kwargs):
        """
        Assign new importance value
        param: propArgs: argument object that holds importance field (KortexKoreInterface.PropertyArgs)
        """
        if not isinstance(assignArgs.importance, KortexEnums.Importance):
            raise TypeError
        self._importance = assignArgs.importance
        super(Importance, self).Assign(assignArgs=assignArgs.importance.name)

    def Get(self):
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
        importance = self.Get()
        if not importance:
            return "Importance : Property does not exists"
        return "Importance : " + importance.name

    def _setDesc(self, descStr):
        """
        Load importance from file to object by convertig string to KortexEnums.Importance enum
        param: descStr: loaded importance from file (str)
        """
        self._importance = getattr(KortexEnums.Importance, descStr)


class MoneyBalance(QuantifiableProperty):
    """
    Represents money input or output of the event
    """

    def __init__(self, dirPath):
        super(MoneyBalance, self).__init__(dirPath)
        self._moneyBalance = 0

    def Assign(self, assignArgs, **kwargs):
        """
        Assign new money balance value
        param: propArgs: argument object that holds moneyBalance field (KortexKoreInterface.PropertyArgs)
        """
        self._moneyBalance = int(assignArgs.moneyBalance)
        super(MoneyBalance, self).Assign(assignArgs=assignArgs.moneyBalance)

    def Get(self):
        """
        return: money balamce value (int)
        """
        return self._moneyBalance

    def __str__(self):
        moneyBalance = self.Get()
        if not moneyBalance:
            return "MoneyBalance : Property does not exists"
        return "MoneyBalance : " + str(moneyBalance)

    def __int__(self):
        """
        return: money balance value (int)
        """
        return int(self._moneyBalance)

    def _setDesc(self, descStr):
        """
        Convent string money balance to integer field
        param: descStr: money balance (str)
        """
        self._moneyBalance = int(descStr)


class DateAndTime(QuantifiableProperty):

    """
    Date and time of the event
    """
    class Date(object):
        """
        Class that stands for representing the date
        """

        daysInMonth = 30
        daysInYear = 365

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
            return self.day + self.month * self.__class__.daysInMonth + self.year * self.__class__.daysInYear

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

        minutesInHours = 60

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
                minStr = "00"
            else:
                minStr = str(self.minutes)
            return str(self.hours) + ":" + minStr

        def __int__(self):
            """
            Cast time to integer by summing the total minutes
            return: sum of the minutes (int)
            """
            return self.minutes + self.hours * self.__class__.minutesInHours

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

    minutesInDay = 1440

    def __init__(self, dirPath):
        """
        Initialize date and time by default values
        """
        super(DateAndTime, self).__init__(dirPath)
        self._date = None
        self._time = None
        self._dateAndTimeSet = False

    @property
    def isset(self):
        """
        return: is the date and time set for the event
        type: Bool
        """
        return self._dateAndTimeSet

    @isset.setter
    def isset(self, value):
        raise NotImplementedError

    def Get(self):
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
        return int(self._time) + int(self._date) * self.__class__.minutesInDay

    def _setDesc(self, descStr):
        """
        Parse date and time input from metadata file and assign in object
        param descStr: data and time from file (str)
        """
        date, time = descStr.split(" ")
        self._setDateTime(date, time)

    def _parseDate(self, dateStr):
        """
        Turns "DD:MM:YYYY" to integers that represent the date
        param dateStr: "DD:MM:YYYY" (str)
        return: day, month, year (tuple (int, int, int))
        """
        dataList = dateStr.split("/")
        if len(dataList) != 3:
            raise TypeError
        return int(dataList[0]), int(dataList[1]), int(dataList[2])

    def _parseTime(self, timeStr):
        """
        Turns "HH:MM" to integers that represent the time
        param dateStr: "HH:MM" (str)
        return: hours, minutes (tuple (int, int))
        """
        dataList = timeStr.split(":")
        if len(dataList) != 2:
            raise TypeError
        return int(dataList[0]), int(dataList[1])

    def _setDateTime(self, date, time):
        """
        Parse data and time to integer form and create the objects
        param: date: "DD:MM:YYYY" (str)
        param: time: "HH:MM" (str)
        """
        day, month, year = self._parseDate(date)
        self._date = DateAndTime.Date(day=day, month=month, year=year)
        hours, minutes = self._parseTime(time)
        self._time = DateAndTime.Time(hours=hours, minutes=minutes)
        self._dateAndTimeSet = True


class StartDateAndTime(DateAndTime):
    
    def __init__(self, dirPath):
        super(StartDateAndTime, self).__init__(dirPath)
        now = datetime.datetime.now()
        self._setDateTime(date=now.strftime("%d/%m/%Y"), time=now.strftime("%H:%M"))
        super(StartDateAndTime, self).Assign(assignArgs=self.Get())


    def Assign(self, assignArgs, event, **kwargs):
        """
        Assign new start date and  time value for the event
        param: propArgs: argument object that holds date and time fields (KortexKoreInterface.PropertyArgs)
        """
        endDateAndTime = event.GetProperty(KortexEnums.EPropertyType.END_DATE_AND_TIME)
        self._setDateTime(assignArgs.date, assignArgs.time)
        if endDateAndTime.isset and int(endDateAndTime) < int(self):
            raise NotImplementedError
        super(StartDateAndTime, self).Assign(assignArgs=self.Get())


class EndDateAndTime(DateAndTime):

    def Assign(self, assignArgs, event, **kwargs):
        """
        Assign new end date and  time value for the event
        param: propArgs: argument object that holds date and time fields (KortexKoreInterface.PropertyArgs)
        """
        startDateAndTime = event.GetProperty(KortexEnums.EPropertyType.START_DATE_AND_TIME)
        self._setDateTime(assignArgs.date, assignArgs.time)
        if int(startDateAndTime) > int(self):
            raise NotImplementedError
        super(EndDateAndTime, self).Assign(assignArgs=self.Get())
