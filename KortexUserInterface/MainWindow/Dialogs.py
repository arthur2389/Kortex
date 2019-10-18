import abc
import os

from PyQt5.QtWidgets import *

from KortexCore.CommonUtils.DataModerator import DataModerator
from KortexCoreInterface.KortexCoreInterface import PropertyArgs
from EnumAndConsts.EnumsAndConsts import EPropertyType
from KortexUserInterface.ExceptionHandler import get_handler
from KortexCore.Exception.Exception import *


class MainWindowDialog(QDialog):

    def __init__(self, parent):
        super(MainWindowDialog, self).__init__(parent=parent)
        self._data_moderator = DataModerator()
        self.excs_handler = get_handler()

    def _entry(self, label):
        layout = QHBoxLayout()
        label = QLabel(label)
        entry = QLineEdit()
        layout.addWidget(label)
        layout.addWidget(entry)
        return layout, entry

    def _get_dialog_buttons(self):
        button_box = QDialogButtonBox(QDialogButtonBox.Ok|
                                      QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        return button_box

    def accept(self):
        self.excs_handler.try_execute(self._accept)

    @abc.abstractmethod
    def _accept(self):
        pass

    def _is_valid_path(self, _path):
        return os.path.exists(_path) or os.access(os.path.dirname(_path), os.W_OK)

    def _is_valid_name(self, name):
        return not any((s in name) for s in ["*", "/", "|", "?"])

    def _inserted(self, field):
        return field != ""


class LoadProjectWindow(MainWindowDialog):

    def __init__(self, parent):
        super(LoadProjectWindow, self).__init__(parent=parent)
        self._project_to_load = None
        self._names = None
        self.setLayout(self._build_layout())

    @property
    def project_to_load(self):
        return self._project_to_load

    def _build_layout(self):
        vlayout = QVBoxLayout()

        self._names = QComboBox()
        self._names.addItems(self._data_moderator.projectnames)

        vlayout.addWidget(self._names)
        vlayout.addWidget(self._get_dialog_buttons())

        return vlayout

    def accept(self):
        self._project_to_load = self._names.currentText()
        QDialog.accept(self)

    def _accept(self):
        pass


class NewProjectWindow(MainWindowDialog):

    def __init__(self, parent):
        super(NewProjectWindow, self).__init__(parent=parent)
        self._name_entry = self._path_entry = None
        self.setLayout(self._build_layout())

    def _build_layout(self):
        vlayout = QVBoxLayout()

        name_layout, self._name_entry = self._entry(label="New project name: ")
        path_layout, self._path_entry = self._entry(label="New project location: ")

        vlayout.addLayout(name_layout)
        vlayout.addLayout(path_layout)
        vlayout.addWidget(self._get_dialog_buttons())

        return vlayout

    def _accept(self):
        name = self._name_entry.text()
        _path = self._path_entry.text()
        if not self._inserted(name):
            raise EmptyEventName
        if not self._inserted(_path):
            raise EmptyEventName
        if not self._is_valid_name(name):
            raise BadEventName
        if not self._is_valid_path(_path):
            raise InvalidPath
        self._data_moderator.set_new_project(name=name,
                                             pr_path=_path)
        QDialog.accept(self)


class NewEventWindow(MainWindowDialog):

    def __init__(self, parent, kortex_project, holding_event=None):
        super(NewEventWindow, self).__init__(parent=parent)
        self._new_event = None
        self._name_entry = self._priorities = None
        self._prj = kortex_project
        self._holding_event = holding_event
        self.setLayout(self._build_layout())

    @property
    def new_event(self):
        return self._new_event

    def _importance_items(self):
        importance_dict = self._data_moderator.get_data(group="event_properties",
                                                        parameter="importance_metrics")
        importance_names = list(importance_dict.keys())
        importance_names.sort(key=lambda i: importance_dict[i])
        return importance_names

    def _importance_entry(self):
        priority_layout = QHBoxLayout()
        names_label = QLabel("Event importance: ")
        self._priorities = QComboBox()
        self._priorities.addItems(self._importance_items())
        priority_layout.addWidget(names_label)
        priority_layout.addWidget(self._priorities)
        return priority_layout

    def _build_layout(self):
        vlayout = QVBoxLayout()

        name_layout, self._name_entry = self._entry(label="Event name: ")
        cashflow_layout, self._cashflow_entry = self._entry(label="Cash flow: ")
        self._cashflow_entry.setText("0")
        importance_layout = self._importance_entry()

        vlayout.addLayout(name_layout)
        vlayout.addLayout(importance_layout)
        vlayout.addLayout(cashflow_layout)

        vlayout.addWidget(self._get_dialog_buttons())

        return vlayout

    def _accept(self):
        # Check input
        cash_flow = self._cashflow_entry.text()
        name = self._name_entry.text()
        priority = self._priorities.currentText()
        if not self._inserted(name):
            raise EmptyEventName
        if not self._is_valid_name(name):
            raise BadEventName
        try:
            cash_flow = int(cash_flow)
        except Exception:
            raise CashFlowNotInt

        # Build new event
        self._new_event = self._prj.create_event(event_name=name, holding_event=self._holding_event)
        args = PropertyArgs(importance=priority, cash_flow=cash_flow)
        self._new_event[EPropertyType.IMPORTANCE] = args
        self._new_event[EPropertyType.CASH_FLOW] = args
        QDialog.accept(self)
