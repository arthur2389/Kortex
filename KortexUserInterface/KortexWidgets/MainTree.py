from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from EnumAndConsts.EnumsAndConsts import EPropertyType
from KortexUserInterface.MainWindow.Dialogs import NewEventWindow


class MainTree(QTreeWidget):

    def __init__(self, parent, window_sizes, kortex_project, data_moderator):
        super(MainTree, self).__init__(parent=parent)
        self._picked_item = None
        self.rc_menu = None
        self._data_moderator = data_moderator
        self._window_sizes = window_sizes
        table_props = ["Event", "Start time", "End time", "Importance", "Cash flow"]
        self.setHeaderLabels(table_props)
        self.setAlternatingRowColors(True)

        self.fill(kortex_project)

    def fill(self, project):
        self._kortex_project = project
        self.clear()
        base_events = self._kortex_project.root.events
        for base_event in base_events.values():
            item = KortexTreeItem(data_moderator=self._data_moderator,
                                  event=base_event)
            self._load_tree_node(item)
            self.addTopLevelItem(item)
        self.setColumnWidth(0, self._window_sizes.tree_column_width)
        self.setColumnWidth(1, self._window_sizes.tree_column_width)
        self.setColumnWidth(2, self._window_sizes.tree_column_width)

    def _load_tree_node(self, parent_item):
        events = parent_item.event.events
        if len(events) > 0:
            icon_name = "event_full.png"
        else:
            icon_name = "event_empty.png"
        parent_item.setIcon(0, QIcon(self._data_moderator.get_file_path(group="main_tree", name=icon_name)))

        for e in events.values():
            item = KortexTreeItem(data_moderator=self._data_moderator, event=e)

            self._load_tree_node(item)
            parent_item.addChild(item)

    def mousePressEvent(self, QMouseEvent):
        if QMouseEvent.button() == Qt.RightButton:
            try:
                self._picked_item = self.itemAt(QMouseEvent.pos().y(), QMouseEvent.pos().y())
                self.rc_menu = self._drop_menu()
                self.rc_menu.popup(QCursor.pos() + QPoint(15, 0))
            # Catch exception in case user right clicked the tree in place with no item
            except Exception:
                pass
        super(MainTree, self).mousePressEvent(QMouseEvent)

    def _drop_menu(self):
        rc_menu = QMenu(self)
        event_name = self._picked_item.event.get_name()
        open_in_location = QAction("Open location of '{}'".format(event_name), self)
        open_in_location.triggered.connect(self._open_in_location)
        add_event = QAction("Add event to '{}'".format(event_name), self)
        add_event.triggered.connect(self._add_event)
        rc_menu.addAction(add_event)
        rc_menu.addAction(open_in_location)
        font = QFont()
        font.setPointSize(8)
        rc_menu.setFont(font)
        return rc_menu

    def _open_in_location(self):
        self._picked_item.event.open_event_location()

    def _add_event(self):
        new = NewEventWindow(parent=self,
                             kortex_project=self._kortex_project,
                             holding_event=self._picked_item.event)
        if new.exec_():
            item = KortexTreeItem(data_moderator=self._data_moderator, event=new.new_event)
            self._load_tree_node(item)
            self._picked_item.addChild(item)
            self._picked_item.setExpanded(True)


class KortexTreeItem(QTreeWidgetItem):

    def __init__(self, data_moderator, event):
        self._data_moderator = data_moderator
        self.importance_icons = self._data_moderator.get_data(group="event_properties",
                                                              parameter="importance_names_and_icons")
        self._event = event
        cash = event.get_property(prop_name=EPropertyType.CASH_FLOW, cast_type=int)
        if cash >= 0:
            icon_name = "plus"
        else:
            icon_name = "minus"
            cash = abs(cash)
        importance = event.get_property(prop_name=EPropertyType.IMPORTANCE)

        super(KortexTreeItem, self).__init__([event.get_name(),
                                              event.get_property(prop_name=EPropertyType.START_DATE_AND_TIME),
                                              event.get_property(prop_name=EPropertyType.END_DATE_AND_TIME),
                                              importance,
                                              str(cash)])
        self.setIcon(3, QIcon(self._data_moderator.get_file_path(group="main_tree",
                                                                 name=self.importance_icons[importance])))
        self.setIcon(4, QIcon(self._data_moderator.get_file_path(group="main_tree",
                                                                 name=icon_name)))

    @property
    def event(self):
        return self._event
