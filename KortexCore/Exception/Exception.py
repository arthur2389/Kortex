import abc


class KortexError(Exception):

    @staticmethod
    @abc.abstractmethod
    def message():
        pass


class BadEventName(KortexError):

    @staticmethod
    @abc.abstractmethod
    def message():
        return "Event name cannot contain any of the following [* /, \, :, |]"


class EmptyField(KortexError):

    @staticmethod
    @abc.abstractmethod
    def message():
        return "Please fill all mandatory fields"


class DoubleEventName(KortexError):

    @staticmethod
    @abc.abstractmethod
    def message():
        return "Event with similar name already exists"


class EventNotFound(KortexError):

    @staticmethod
    @abc.abstractmethod
    def message():
        return "Event does not exists in project"


class BadInput(KortexError):

    @staticmethod
    @abc.abstractmethod
    def message():
        return "Input value is not complete"


class BadDateTime(KortexError):

    @staticmethod
    @abc.abstractmethod
    def message():
        return "Invalid date and time values"


class ProjectAlreadyExists(KortexError):

    @staticmethod
    @abc.abstractmethod
    def message():
        return "Project with the same name already exists"


class CashFlowNotInt(KortexError):

    @staticmethod
    @abc.abstractmethod
    def message():
        return "Please insert a valid cash flow value"


class InvalidPath(KortexError):

    @staticmethod
    @abc.abstractmethod
    def message():
        return "Please insert a valid path for project root"
