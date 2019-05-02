from enum import Enum


class ConstantData(object):
    projectRepoName = ".kor"
    eventDataFileName = "eventData.json"


class EFileType(Enum):
    DIRECTORY = 1
    FUNCTIONAL_FILE = 2


class EPropertyType(Enum):
    IMAGE = 1
    DESCRIPTION = 2
    DATE_AND_TIME = 3
    IMPORTANCE = 4
    MONEY_BALANCE = 5

class Importance(Enum):
    VERY_HIGH = 1
    HIGH = 2
    MEDIUM = 3
    LOW = 4
    TRIVIAL = 5
