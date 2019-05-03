import abc
from os import path

from Kortex.KortexCore.File.FunctionalFile import FuncrionalFile as FuncrionalFile
from Kortex.KortexCore.CommonUtils.JsonIO import JsonIO as JsonIO
import Kortex.KortexData.KortexEnums as KortexEnums


class PropertyBase(object):

    def __init__(self, dirPath):
        self._path = path.join(dirPath, KortexEnums.ConstantData.projectRepoName)

    @abc.abstractmethod
    def LoadExisting(self):
        pass

    @abc.abstractmethod
    def Assign(self, *args, **kwargs):
        pass

    @abc.abstractmethod
    def Get(self):
        pass

    def __str__(self):
        _repr = self.Get()
        if not _repr:
            return self.__class__.__name__ + " : Property does not exists"
        return self.__class__.__name__ + " : " + _repr


class FileBasedProperty(PropertyBase):

    suffixes = []

    def __init__(self, dirPath):
        super(FileBasedProperty, self).__init__(dirPath)
        self._file = None

    def LoadExisting(self):
        for suffix in self.__class__.suffixes:
            if path.exists(path.join(self._path, self.__class__.__name__ + suffix)):
                self._file = FuncrionalFile(name=self.__class__.__name__ + suffix,
                                            dirname=self._path,
                                            level=0)
                break

    def Assign(self, filePath):
        self._file = FuncrionalFile(name=path.basename(filePath),
                                    dirname=path.dirname(filePath),
                                    level=0)
        if self._file.suffix not in self.__class__.suffixes:
            raise FileNotFoundError
        self._file.CopyFile(dest=self._path, newName=self.__class__.__name__)

    def Get(self):
        return self._file.path if self._file else None


class Image(FileBasedProperty):

    suffixes = [".jpg", ".png", ".gif", ".svg"]


class DescriptionProperty(PropertyBase):

    def __init__(self, dirPath):
        super(DescriptionProperty, self).__init__(dirPath)
        self._dataFilePath = path.join(self._path, KortexEnums.ConstantData.eventDataFileName)
        self._desc = None

    def LoadExisting(self):
        data = JsonIO.Read(self._dataFilePath)
        if self.__class__.__name__ in data.keys():
            self._setDesc(data[self.__class__.__name__])

    def Assign(self, desc):
        JsonIO.Write(filePath=self._dataFilePath, field=self.__class__.__name__, data=desc)

    @abc.abstractmethod
    def _setDesc(self, descStr):
        pass


class Description(DescriptionProperty):

    def __init__(self, dirPath):
        super(Description, self).__init__(dirPath)
        self._description = None

    def Assign(self, desc):
        self._desc = desc
        super(Description, self).Assign(desc)

    def Get(self):
        return self._description

    def _setDesc(self, descStr):
        self._desc = descStr


class Importance(DescriptionProperty):

    def __init__(self, dirPath):
        super(Importance, self).__init__(dirPath)
        self._importance = None

    def Assign(self, importance):
        if not isinstance(importance, KortexEnums.Importance):
            raise TypeError
        self._importance = importance
        super(Importance, self).Assign(importance.name)

    def Get(self):
        return self._importance

    def __str__(self):
        importance = self.Get()
        if not importance:
            return "Importance : Property does not exists"
        return "Importance : " + importance.name

    def _setDesc(self, descStr):
        self._importance = getattr(KortexEnums.Importance, descStr)


class MoneyBalance(DescriptionProperty):

    def __init__(self, dirPath):
        super(MoneyBalance, self).__init__(dirPath)
        self._moneyBalance = None

    def Assign(self, moneyBalance):
        self._moneyBalance = int(moneyBalance)
        super(MoneyBalance, self).Assign(moneyBalance)

    def Get(self):
        return self._moneyBalance

    def __str__(self):
        moneyBalance = self.Get()
        if not moneyBalance:
            return "MoneyBalance : Property does not exists"
        return "MoneyBalance : " + str(moneyBalance)

    def _setDesc(self, descStr):
        self._moneyBalance = int(descStr)


class DateAndTime(DescriptionProperty):

    class Date(object):

        def __init__(self, year=0, month=0, day=0):
            if year < 0 or month < 0 or day < 0 or month > 12 or day > 31:
                raise ValueError
            self._year = year
            self._month = month
            self._day = day

        def __str__(self):
            return str(self.day) + "/" + str(self.month) + "/" + str(self.year)

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

        def __init__(self, hours=0, minutes=0):
            if hours < 0 or hours > 23 or minutes < 0 or minutes > 59:
                raise ValueError
            self._hours = hours
            self._minutes = minutes

        def __str__(self):
            return str(self.hours) + ":" + str(self.minutes)

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

    def __init__(self, dirPath):
        super(DateAndTime, self).__init__(dirPath)
        self._date = None
        self._time = None

    def Assign(self, date, time):
        self._setDateTime(date, time)
        super(DateAndTime, self).Assign(self.Get())

    def Get(self):
        if None in [self._date, self._time]:
            return None
        return str(self._date) + " " + str(self._time)

    def _setDesc(self, descStr):
        date, time = descStr.split(" ")
        self._setDateTime(date, time)

    def _parseDate(self, dateStr):
        if not isinstance(dateStr, str):
            raise TypeError
        dataList = dateStr.split("/")
        if len(dataList) != 3:
            raise TypeError
        return int(dataList[0]), int(dataList[1]), int(dataList[2])

    def _parseTime(self, timeStr):
        if not isinstance(timeStr, str):
            raise TypeError
        dataList = timeStr.split(":")
        if len(dataList) != 2:
            raise TypeError
        return int(dataList[0]), int(dataList[1])

    def _setDateTime(self, date, time):
        day, month, year = self._parseDate(date)
        self._date = DateAndTime.Date(day=day, month=month, year=year)
        hours, minutes = self._parseTime(time)
        self._time = DateAndTime.Time(hours=hours, minutes=minutes)
