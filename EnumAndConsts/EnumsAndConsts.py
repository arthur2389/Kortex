from enum import Enum


class ConstantData(object):
    ProjectRepoName = ".kor"
    EventDataFileName = "eventData.json"
    DefaultImage = "default.jpg"


class EFileType(Enum):
    DIRECTORY = 1
    FUNCTIONAL_FILE = 2


class EPropertyType(Enum):
    IMAGE = 1
    DESCRIPTION = 2
    START_DATE_AND_TIME = 3
    END_DATE_AND_TIME = 4
    IMPORTANCE = 5
    CASH_FLOW = 6
    DURATION = 7


class Importance(Enum):
    TRIVIAL = 1
    LOW = 2
    MEDIUM = 3
    HIGH = 4
    VERY_HIGH = 5


class ETimeInterval(Enum):
    MINUTE = 1
    HOUR = 2
    DAY = 3
