from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from KortexCoreInterface.KortexCoreInterface import KortexCoreInterface
from KortexCore.CommonUtils.DataModerator import DataModerator
from KortexUserInterface.MainWindow.Dialogs import LoadProjectWindow, NewProjectWindow, NewEventWindow
from KortexUserInterface.KortexWidgets.MainTree import MainTree


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

        self._load_project()
        self._build_main_menu()
        self._main_frame()

        self.resize(self.window_sizes.main_window_width, self.window_sizes.main_window_height)
        self.statusBar()
        self.show()

    def _main_frame(self):
        self._frame = QWidget()
        self._layout = QVBoxLayout()
        self._frame.setLayout(self._layout)
        self.setCentralWidget(self._frame)
        self.tree = MainTree(parent=self,
                             window_sizes=self.window_sizes,
                             kortex_project=self.kortex_project,
                             data_moderator=self._data_moderator)
        self._layout.addWidget(self.tree)

    def _load_project(self):
        prj_path, prj_name = self._data_moderator.get_current_project()
        self.kortex_project = KortexCoreInterface(root_dir=prj_path)
        self.setWindowTitle("Kortex " + "Project : " + prj_name)

    def _build_main_menu(self):
        bar = self.menuBar()
        file = bar.addMenu("&File")

        file.addActions([self._action(name="New project",
                                      icon="new.png",
                                      shortcut="Ctrl+N",
                                      status_tip="Create new project",
                                      connect_action=self._new),
                         self._action(name="Load project",
                                      icon="open.png",
                                      shortcut="Ctrl+W",
                                      status_tip="Load existing project",
                                      connect_action=self._load)])
        file.addSeparator()
        file.addActions([self._action(name="Exit",
                                      icon="exit.png",
                                      shortcut="Ctrl+Q",
                                      status_tip="Exit application",
                                      connect_action=self.close)])

        event = bar.addMenu("Event")
        event.addActions([self._action(name="New event",
                                       icon="new_event.png",
                                       shortcut="Ctrl+E+N",
                                       status_tip="Create new event",
                                       connect_action=self._new_event),
                          self._action(name="Open event",
                                       icon="open_event.png",
                                       shortcut="Ctrl+E+O",
                                       status_tip="Open existing event",
                                       connect_action=self._open_event),
                          self._action(name="Remove event",
                                       icon="remove_event.png",
                                       shortcut="Ctrl+E+W",
                                       status_tip="Delete event",
                                       connect_action=self._remove_event)])

    def _action(self, name, icon, shortcut, status_tip, connect_action):
        _action = QAction(QIcon(self._data_moderator.get_file_path(group="main_menu", name=icon)),
                          name, self)
        _action.setShortcut(shortcut)
        _action.setStatusTip(status_tip)
        _action.triggered.connect(connect_action)
        return _action

    def _load(self):
        load_ui = LoadProjectWindow(self)
        if load_ui.exec_():
            self._data_moderator.set_current_project(load_ui.project_to_load)
            self._load_project()
            self.tree.fill(self.kortex_project)

    def _new(self):
        new_ui = NewProjectWindow(self)
        if new_ui.exec_():
            self._load_project()
            self.tree.fill(self.kortex_project)

    def _new_event(self):
        new_event = NewEventWindow(self, self.kortex_project)
        if new_event.exec_():
            self.tree.fill(self.kortex_project)

    def _open_event(self):
        print("Open event")

    def _remove_event(self):
        print("Remove event")
