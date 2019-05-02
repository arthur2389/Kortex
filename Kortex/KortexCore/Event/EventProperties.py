import abc
from os import path

from Kortex.KortexCore.File.FunctionalFile import FuncrionalFile as FuncrionalFile
from Kortex.KortexCore.CommonUtils.JsonIO import JsonIO as JsonIO
import Kortex.KortexData.KortexEnums as PVEnums


class PropertyBase(object):

    def __init__(self, dirPath):
        self._path = path.join(dirPath, PVEnums.ConstantData.projectRepoName)

    @abc.abstractmethod
    def Assign(self, *args, **kwargs):
        pass

    @abc.abstractmethod
    def Get(self):
        pass


class FileBasedProperty(PropertyBase):

    def __init__(self, dirPath):
        super(FileBasedProperty, self).__init__(dirPath)
        self._file = None

    def Assign(self, filePath):
        self._file = FuncrionalFile(name=path.basename(filePath),
                                    dirname=path.dirname(filePath),
                                    level=0)
        self._file.CopyFile(dest=self._path, newName=self.__class__.__name__)

    def Get(self):
        return self._file.path


class Image(FileBasedProperty):
    pass


class DescriptionProperty(PropertyBase):

    def __init__(self, dirPath):
        super(DescriptionProperty, self).__init__(dirPath)
        self._dataFilePath = path.join(self._path, PVEnums.ConstantData.eventDataFileName)
        self._desc = None

    def Assign(self, desc):
        JsonIO.Write(filePath=self._dataFilePath, field=self.__class__.__name__, data=desc)

    def Get(self):
        return self._desc


class Description(DescriptionProperty):
    pass


class Importance(DescriptionProperty):

    def __init__(self, dirPath):
        super(Importance, self).__init__(dirPath)
        self._importance = None

    def Assign(self, importance):
        if not isinstance(importance, PVEnums.Importance):
            raise TypeError
        self._importance = importance
        super(Importance, self).Assign(importance.name)

    def Get(self):
        return self._importance


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
            return self._year

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
            if value < 0 or  value > 23:
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
        self._date = DateAndTime.Date()
        self._time = DateAndTime.Time()

    def Assign(self, date, time):
        day, month, year = self._parseDate(date)
        self._date.day = day
        self._date.month = month
        self._date.year = year
        hours, minutes = self._parseTime(time)
        self._time.hours = hours
        self._time.minutes = minutes
        super(DateAndTime, self).Assign(str(self))

    def Get(self):
        return str(self)

    def __str__(self):
        return str(self._date) + " " + str(self._time)

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
