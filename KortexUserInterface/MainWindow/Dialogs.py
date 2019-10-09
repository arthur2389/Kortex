from PyQt5.QtWidgets import *

from KortexCore.CommonUtils.DataModerator import DataModerator


class LoadProjectWindow(QDialog):

    def __init__(self, parent):
        super(LoadProjectWindow, self).__init__(parent=parent)
        self._project_to_load = None
        self._data_moderator = DataModerator()
        self.setLayout(self._build_layout())

    @property
    def project_to_load(self):
        return self._project_to_load

    def _get_dialog_buttons(self):
        button_box = QDialogButtonBox(QDialogButtonBox.Ok|
                                      QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        return button_box

    def _build_layout(self):
        vlayout = QVBoxLayout()

        self.names = QComboBox()
        self.names.addItems(self._data_moderator.projectnames)

        vlayout.addWidget(self.names)
        vlayout.addWidget(self._get_dialog_buttons())

        return vlayout

    def accept(self):
        self._project_to_load = self.names.currentText()
        super(LoadProjectWindow, self).accept()


class NewProjectWindow(QDialog):

    def __init__(self, parent):
        super(NewProjectWindow, self).__init__(parent=parent)
        self._new_project = {"name": None, "path": None}
        self.setLayout(self._build_layout())

    @property
    def new_project(self):
        return self._new_project

    def _get_dialog_buttons(self):
        button_box = QDialogButtonBox(QDialogButtonBox.Ok |
                                      QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        return button_box

    def _build_layout(self):
        vlayout = QVBoxLayout()

        name_layout = QHBoxLayout()
        name_label = QLabel("New project name: ")
        self.name_entry = QLineEdit()
        name_layout.addWidget(name_label)
        name_layout.addWidget(self.name_entry)

        path_layout = QHBoxLayout()
        path_label = QLabel("New project location: ")
        self.path_entry = QLineEdit()
        path_layout.addWidget(path_label)
        path_layout.addWidget(self.path_entry)

        vlayout.addLayout(name_layout)
        vlayout.addLayout(path_layout)
        vlayout.addWidget(self._get_dialog_buttons())

        return vlayout

    def accept(self):
        self._new_project["name"] = self.name_entry.text()
        self._new_project["path"] = self.path_entry.text()
        super(NewProjectWindow, self).accept()


class NewEventWindow(QDialog):

    def __init__(self, parent):
        super(NewEventWindow, self).__init__(parent=parent)
        self.setLayout(self._build_layout())

    def _build_layout(self):
        vlayout = QVBoxLayout()

        name_layout = QHBoxLayout()
        name_label = QLabel("New event name: ")
        self.name_entry = QLineEdit()
        name_layout.addWidget(name_label)
        name_layout.addWidget(self.name_entry)

        path_layout = QHBoxLayout()
        path_label = QLabel("New project location: ")
        self.path_entry = QLineEdit()
        path_layout.addWidget(path_label)
        path_layout.addWidget(self.path_entry)

        vlayout.addLayout(name_layout)
        vlayout.addLayout(path_layout)
        vlayout.addWidget(self._get_dialog_buttons())

        return vlayout