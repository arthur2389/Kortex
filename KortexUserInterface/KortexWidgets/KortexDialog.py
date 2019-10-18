import abc
import os

from PyQt5.QtWidgets import *

from KortexCore.CommonUtils.DataModerator import DataModerator
from KortexUserInterface.ExceptionHandler import get_handler
from KortexCore.Exception.Exception import EmptyField


class KortexDialog(QDialog):

    def __init__(self, parent):
        super(KortexDialog, self).__init__(parent=parent)
        self._data_moderator = DataModerator()
        self.excs_handler = get_handler()

    def _entry(self, label, mandatory=False):
        layout = QHBoxLayout()
        label = QLabel(label)
        entry = QLineEdit()
        layout.addWidget(label)
        layout.addWidget(entry)
        if mandatory:
            ast = QLabel("*")
            layout.addWidget(ast)
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
        return os.path.isdir(_path)

    def _is_valid_name(self, name):
        return not any((s in name) for s in ["*", "/", "|", "?"])

    def _assert_inserted(self, fields):
        if any(field == "" for field in fields):
            raise EmptyField
