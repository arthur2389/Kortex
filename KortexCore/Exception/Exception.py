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
        return "Event name is not suitable"


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
