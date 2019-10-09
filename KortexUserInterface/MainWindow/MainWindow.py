from collections import namedtuple

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from KortexCoreInterface.KortexCoreInterface import KortexCoreInterface
from EnumAndConsts.EnumsAndConsts import EPropertyType


tree_item = namedtuple('tree_item', ('item', 'event'))


class KortexMainWindow(QMainWindow):

    def __init__(self):
        super(KortexMainWindow, self).__init__()

        self.data_moderator =
        self.kortex_project = KortexCoreInterface(project)

        self.setWindowTitle("Kortex")
        self._build_main_menu()
        self._build_tree()
        self.resize(700, 300)
        self.show()

    def _set_font(self, w):
        """
        Set font for caller
        """
        font = QFont()
        font.setPointSize(11)
        w.setFont(font)

    def _build_main_menu(self):
        bar = self.menuBar()
        file = bar.addMenu("&File")
        self._set_font(bar)

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
        self.tree = QTreeWidget()
        table_props = ["Event", "Start time", "End time", "Importance", "Cash flow"]
        self.tree.setHeaderLabels(table_props)
        self.tree.setAlternatingRowColors(True)
        self._set_font(self.tree)

        base_events = self.kortex_project.root.events
        for base_event in base_events.values():
            item = tree_item(item=self._tree_widget_item(base_event),
                             event=base_event)
            nested_exist = self._load_base_event_item(item)
            if nested_exist:
                name = "event_full"
            else:
                name = "event_empty"
            item.item.setIcon(0, QIcon(ExtFiles.get(name)))
            self.tree.addTopLevelItem(item.item)
        self.setCentralWidget(self.tree)
        self.tree.setColumnWidth(0, 200)
        self.tree.setColumnWidth(1, 200)
        self.tree.setColumnWidth(2, 200)

    def _load_base_event_item(self, parent_item):
        events = parent_item.event.events
        for e in events.values():
            item = tree_item(item=self._tree_widget_item(e),
                             event=e)
            nested_exist = self._load_base_event_item(item)
            if nested_exist:
                name = "event_full"
            else:
                name = "event_empty"
            item.item.setIcon(0, QIcon(ExtFiles.get(name)))
            parent_item.item.addChild(item.item)
        return len(events) > 0

    def _tree_widget_item(self, event):
        i = QTreeWidgetItem(["  " + event.get_name(),
                             event.get_property(prop_name=EPropertyType.START_DATE_AND_TIME),
                             event.get_property(prop_name=EPropertyType.END_DATE_AND_TIME),
                             event.get_property(prop_name=EPropertyType.IMPORTANCE),
                             event.get_property(prop_name=EPropertyType.CASH_FLOW)])
        return i

    def _load(self):
        print("Load!!")

    def _new(self):
        print("New!!")
