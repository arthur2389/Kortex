from os import path
from Kortex.KortexCore.File.FileFactrory import FileFactory as FileFactory


class KortexCoreInterface(object):

    """
    Interface class for Kortex core (engine) operations.
    """
    def __init__(self, root_dir):
        """
        Create interface instance as well as a new project
        param: rootdir: The root directory of the project. If the direcory doesn't
        exist it will be created (str)
        """

        # Create main utils and initialize the project
        self._file_factory = FileFactory()
        self._project = self._file_factory.generate_directory(root_dir)

        # Map and store all the event names
        all_dirs = []
        self._project.get_all_directories(dir_list=all_dirs)
        self._all_events = list(map(lambda _dir: _dir.name, all_dirs))

    def create_event(self, event_name, holding_event=None):
        """
        Create new event. The new event cannot have the same name the other event in the project
        param: eventName: The name of the new event (str)
        param: holdingEvent: The holding event of the created event (Event)
        return: created event (Event)
        """

        # Check if event name already exists
        if event_name in self._all_events:
            raise NotImplementedError

        # Assign holding event. Default is the root event
        holding_event = holding_event or self._project.get_event()

        # Create directory (and the event) inside the holding event
        _dir = holding_event.get_directory()
        created_dir = self._file_factory.generate_directory(path.join(_dir.path, event_name), _dir.level + 1)

        # Append the event name to all the event name list
        _dir.add_directory(created_dir)
        self._all_events.append(created_dir.name)

        # From the created directory return the created event
        return created_dir.get_event()

    def remove_event(self, event):
        """
        Remove existing event
        param: event: The event to remove (Event)
        """

        # Extract the event directory from the event, use it to remove itself (and the event)
        directory = event.get_directory()
        dir_name = directory.name
        directory.remove()
        self._all_events.remove(dir_name)

    def move_event(self, event, target_holding_event):
        """
        Move event from it's holding event to a new holding event
        param: event: The event to be moved (Event)
        param: targetHoldingEvent: The new holding event. The holding event cannot be held in
        the moved event (Event)
        """

        # Extract the event directory from the event
        directory = event.get_directory()

        # Extract the target event directory and move the directories
        target_directory = target_holding_event.get_directory()
        directory.move(target_directory)

    def get_event(self, name):
        """
        Get event by name.
        param: name: The name of the event to return (str)
        return: The found event (Event)
        """
        event = self._project.find_directory(name=name, get_event=True)
        if not event:
            raise FileNotFoundError
        return event

    def print_project_tree(self):
        """
        Debug procedure, print all project to command line
        """
        print("Project : \n\n" + str(self._project))


class PropertyArgs(object):

    """
    Input class for assigning new property to an event
    """
    def __init__(self, img_path=None,
                 description=None,
                 importance=None,
                 date=None,
                 time=None,
                 money_balance=None):
        """
        param: imgPath: full path of image [".jpg", ".png", ".gif", ".svg"] file (str)
        param description: event description (str)
        param importance: event importance (KortexEnums.Importance)
        param date: event date (DD/MM/YYYY str)
        param: time: event time (HH:MM str)
        param: moneyBalance: event money in/out (int)
        """
        self.img_path = img_path
        self.description = description
        self.importance = importance
        self.date = date
        self.time = time
        self.money_balance = money_balance
