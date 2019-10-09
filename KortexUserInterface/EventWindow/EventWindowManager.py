from KortexCore.CommonUtils.Singleton import singleton as singleton
from KortexCore.Event.Event import Event as Event
from KortexUserInterface.EventWindow.EventWindow import EventWindow as EventWindow


@singleton
class EventWindowManager(object):

    active_events = {}

    def activate(self, event, fix_size=True):
        if not isinstance(event, Event):
            raise TypeError

        name = event.get_name()
        self.__class__.active_events[name] = EventWindow(event, self)
        self.__class__.active_events[name].show()

        if fix_size:
            self.__class__.openEvents[name].setFixedSize(self.__class__.active_events[name].size())
        return self.__class__.active_events[name]
