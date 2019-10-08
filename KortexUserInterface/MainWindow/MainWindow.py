from collections import namedtuple

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import ExtFiles
from KortexCoreInterface.KortexCoreInterface import KortexCoreInterface


# ToDo - REMOVE !!!!
project = "C://Users//USER//Documents//arthur//Project"


tree_item = namedtuple('tree_item', ('item', 'event'))


class KortexMainWindow(QMainWindow):

    def __init__(self):
        # ToDo - REMOVE !!!!
        global project
        super(KortexMainWindow, self).__init__()
        self._build_main_menu()
        self.kortex_project = KortexCoreInterface(project)
        self._build_tree()
        self.show()

    def _build_main_menu(self):
        bar = self.menuBar()
        file = bar.addMenu("&File")

        _load_project = QAction(QIcon(ExtFiles.get("open")), "Load project", self)
        _load_project.setShortcut('Ctrl+W')
        _load_project.setStatusTip('Load existing project')
        _load_project.triggered.connect(self._load)
        file.addAction(_load_project)

        _new_project = QAction(QIcon(ExtFiles.get("new")), "New project", self)
        _new_project.setShortcut('Ctrl+N')
        _new_project.setStatusTip('Create new project')
        _new_project.triggered.connect(self._new)
        file.addAction(_new_project)

        file.addSeparator()

        _exit = QAction(QIcon(ExtFiles.get("exit")), "Exit", self)
        _exit.setShortcut('Ctrl+Q')
        _exit.setStatusTip('Exit application')
        _exit.triggered.connect(self.close)
        file.addAction(_exit)

    def _build_tree(self):
        self.tree = QTreeWidget(self)
        self.tree.setColumnCount(1)
        self.tree.setHeaderLabels(["Event"])
        base_events = self.kortex_project.root.events
        for base_event in base_events.values():
            item = tree_item(item=QTreeWidgetItem([base_event.get_name()]),
                             event=base_event)
            self._load_base_event_item(item)
            self.tree.addTopLevelItem(item.item)
        self.setCentralWidget(self.tree)

    def _load_base_event_item(self, parent_item):
        events = parent_item.event.events
        for e in events.values():
            item = tree_item(item=QTreeWidgetItem([e.get_name()]),
                             event=e)
            self._load_base_event_item(item)
            parent_item.item.addChild(item.item)

    def _load(self):
        print("Load!!")

    def _new(self):
        print("New!!")
