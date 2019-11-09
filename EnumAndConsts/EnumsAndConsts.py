from enum import Enum


class EFileType(Enum):
    DIRECTORY = 1
    FUNCTIONAL_FILE = 2


class EPropertyType(Enum):
    IMAGE = 1
    DESCRIPTION = 2
    COMPLETION_STATUS = 3
    START_DATE_AND_TIME = 4
    END_DATE_AND_TIME = 5
    IMPORTANCE = 6
    CASH_FLOW = 7
    DURATION = 8


class ECompletionStatus(Enum):
    NOT_COMPLETED = 1
    COMPLETED = 2


class ETimeInterval(Enum):
    SECOND = 1
    MINUTE = 2
    HOUR = 3
    DAY = 4
