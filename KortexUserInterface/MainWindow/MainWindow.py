from collections import namedtuple

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from KortexCoreInterface.KortexCoreInterface import KortexCoreInterface
from KortexCore.CommonUtils.DataModerator import DataModerator
from EnumAndConsts.EnumsAndConsts import EPropertyType


tree_item = namedtuple('tree_item', ('item', 'event'))


class KortexMainWindow(QMainWindow):

    class WindowSizes(object):

        def __init__(self, sizes):
            self.font_size = sizes["font_size"]
            self.main_window_width = self.font_size * sizes["main_window_width_ratio"]
            self.main_window_height = self.font_size * sizes["main_window_height_ratio"]
            self.tree_column_width = self.font_size * sizes["tree_column_width_ratio"]

    def __init__(self):
        super(KortexMainWindow, self).__init__()

        self._data_moderator = DataModerator()
        self.window_sizes = \
            KortexMainWindow.WindowSizes(sizes=self._data_moderator.get_data(group="main_window_sizes"))
        prj_path, prj_name = self._data_moderator.get_current_project()
        self.kortex_project = KortexCoreInterface(root_dir=prj_path)

        self.setWindowTitle("Kortex " + "Project : " + prj_name)
        self._build_main_menu()
        self._build_tree()
        self.resize(self.window_sizes.main_window_width, self.window_sizes.main_window_height)
        self.show()

    def _build_main_menu(self):
        bar = self.menuBar()
        file = bar.addMenu("&File")

        _load_project = QAction(QIcon(self._data_moderator.get_file_path(group="main_menu", name="open.png")),
                                "Load project", self)
        _load_project.setShortcut('Ctrl+W')
        _load_project.setStatusTip('Load existing project')
        _load_project.triggered.connect(self._load)
        file.addAction(_load_project)

        _new_project = QAction(QIcon(self._data_moderator.get_file_path(group="main_menu", name="new.png")),
                               "New project", self)
        _new_project.setShortcut('Ctrl+N')
        _new_project.setStatusTip('Create new project')
        _new_project.triggered.connect(self._new)
        file.addAction(_new_project)

        file.addSeparator()

        _exit = QAction(QIcon(self._data_moderator.get_file_path(group="main_menu", name="exit.png")),
                        "Exit", self)
        _exit.setShortcut('Ctrl+Q')
        _exit.setStatusTip('Exit application')
        _exit.triggered.connect(self.close)
        file.addAction(_exit)

    def _build_tree(self):
        self.tree = QTreeWidget()
        table_props = ["Event", "Start time", "End time", "Importance", "Cash flow"]
        self.tree.setHeaderLabels(table_props)
        self.tree.setAlternatingRowColors(True)

        base_events = self.kortex_project.root.events
        for base_event in base_events.values():
            item = tree_item(item=self._tree_widget_item(base_event),
                             event=base_event)
            nested_exist = self._load_base_event_item(item)
            if nested_exist:
                name = "event_full.png"
            else:
                name = "event_empty.png"
            item.item.setIcon(0, QIcon(self._data_moderator.get_file_path(group="main_tree", name=name)))
            self.tree.addTopLevelItem(item.item)
        self.setCentralWidget(self.tree)
        self.tree.setColumnWidth(0, self.window_sizes.tree_column_width)
        self.tree.setColumnWidth(1, self.window_sizes.tree_column_width)
        self.tree.setColumnWidth(2, self.window_sizes.tree_column_width)

    def _load_base_event_item(self, parent_item):
        events = parent_item.event.events
        for e in events.values():
            item = tree_item(item=self._tree_widget_item(e),
                             event=e)
            nested_exist = self._load_base_event_item(item)
            if nested_exist:
                name = "event_full.png"
            else:
                name = "event_empty.png"
            item.item.setIcon(0, QIcon(self._data_moderator.get_file_path(group="main_tree", name=name)))
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
