from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class EventWindow(QWidget):

    def __init__(self, event, builder):
        super(EventWindow, self).__init__()

        self._kortex_event = event
        self._builder = builder

        self.nested_events = self._make_table(name="Events",
                                              connect=self._open_new_event,
                                              iterator=self._kortex_event.events)
        self.files_in_event = self._make_table(name="Files",
                                               connect=self._make_open_file,
                                               iterator=self._kortex_event.files)

        hsplitter = QSplitter(Qt.Horizontal)
        hsplitter.addWidget(self.nested_events)
        hsplitter.addWidget(self.files_in_event)
        right_side = QVBoxLayout()
        right_side.addWidget(hsplitter)

        self.resize(self.sizeHint())

    def _make_open_file(self, file):
        event = self._kortex_event

        def open_file():
            event.open_file(file)
        return open_file

    def _open_new_event(self, dir_to_open):
        builder = self._builder

        def open_event():
            builder.activate(dir_to_open.get_event())
        return open_event
