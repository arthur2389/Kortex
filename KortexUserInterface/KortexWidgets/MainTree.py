from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from EnumAndConsts.EnumsAndConsts import EPropertyType
from EnumAndConsts.EnumsAndConsts import ECompletionStatus as CompStatus
from KortexCoreInterface.KortexCoreInterface import PropertyArgs
from KortexUserInterface.MainWindow.Dialogs import NewEventWindow
from KortexUserInterface.KortexWidgets.KortexDialog import Verification, KortexDialog


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
        self._set_icon_for_item(parent_item, len(events) > 0)

        for e in events.values():
            item = KortexTreeItem(data_moderator=self._data_moderator, event=e)

            self._load_tree_node(item)
            parent_item.addChild(item)

    def _set_icon_for_item(self, item, is_children):
        if item.event[EPropertyType.COMPLETION_STATUS] == CompStatus.COMPLETED:
            icon_name = "completed"
        else:
            if is_children:
                icon_name = "event_full"
            else:
                icon_name = "event_empty"
        item.setIcon(0, QIcon(self._data_moderator.get_file_path(group="main_tree", name=icon_name)))

    def mousePressEvent(self, QMouseEvent):
        if QMouseEvent.button() == Qt.RightButton:
            try:
                self._picked_item = self.itemAt(QMouseEvent.pos().y(), QMouseEvent.pos().y())
                self.rc_menu = self._drop_menu()
                self.rc_menu.popup(QCursor.pos() + QPoint(self._window_sizes.rc_menu_dst, 0))
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

        if self._picked_item.event[EPropertyType.COMPLETION_STATUS] == CompStatus.NOT_COMPLETED:
            set_completion = QAction("Set '{}' completed".format(event_name), self)
            set_completion.triggered.connect(self._toggle_completion)
        else:
            set_completion = QAction("Set '{}' not completed".format(event_name), self)
            set_completion.triggered.connect(self._toggle_completion)

        remove_event = QAction("Remove '{}'".format(event_name), self)
        remove_event.triggered.connect(self._remove_event)

        move_event = QAction("Move '{}'".format(event_name), self)
        move_event.triggered.connect(self._move_event)

        rc_menu.addAction(add_event)
        rc_menu.addAction(open_in_location)
        rc_menu.addAction(set_completion)
        rc_menu.addSeparator()
        rc_menu.addAction(remove_event)
        rc_menu.addAction(move_event)

        font = QFont()
        font.setPointSize(self._window_sizes.rc_menu_font)
        rc_menu.setFont(font)
        return rc_menu

    def _move_event(self):
        move = MoveEvent(parent=self, prj=self._kortex_project, event=self._picked_item.event)
        if move.exec_():
            self.fill(self._kortex_project)

    def _remove_event(self):
        verification = Verification(parent=self, question="Remove {} ?".format(self._picked_item.event.get_name()))
        if verification.exec_():
            self._kortex_project.remove_event(self._picked_item.event)
            self.fill(self._kortex_project)

    def _toggle_completion(self):
        event = self._picked_item.event
        if event[EPropertyType.COMPLETION_STATUS] == CompStatus.NOT_COMPLETED:
            args = PropertyArgs(completion_status=CompStatus.COMPLETED)
        else:
            args = PropertyArgs(completion_status=CompStatus.NOT_COMPLETED)
        event[EPropertyType.COMPLETION_STATUS] = args
        self._set_icon_for_item(self._picked_item, len(event.events) > 0)

    def _open_in_location(self):
        self._picked_item.event.open_event_location()

    def _add_event(self):
        new = NewEventWindow(parent=self,
                             kortex_project=self._kortex_project,
                             window_width=self._window_sizes.new_dlg_size,
                             holding_event=self._picked_item.event)
        if new.exec_():
            item = KortexTreeItem(data_moderator=self._data_moderator, event=new.new_event)
            self._load_tree_node(item)
            self._picked_item.addChild(item)
            self._picked_item.setExpanded(True)
            self._set_icon_for_item(self._picked_item, True)


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


class MoveEvent(KortexDialog):

    def __init__(self, parent, prj, event):
        super(MoveEvent, self).__init__(parent=parent)
        self._move_to = None
        self._prj = prj
        self._event = event
        self.setMaximumHeight(100)
        self.setLayout(self._build_layout())

    @property
    def move_to(self):
        return self._move_to

    def _build_layout(self):
        vlayout = QVBoxLayout()
        self.event_list = QListWidget()

        for e_name in self._prj.all_events:
            self.event_list.addItem(QListWidgetItem(e_name))
        self.event_list.setCurrentRow(0)
        vlayout.addWidget(self.event_list)
        self._get_dialog_buttons(vlayout)

        return vlayout

    def _accept(self):
        self._prj.move_event(event=self._event,
                             target_holding_event=self._prj.get_event(self.event_list.currentItem().text()))
        QDialog.accept(self)
