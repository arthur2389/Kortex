import abc
import os

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from KortexCore.CommonUtils.DataModerator import DataModerator
from KortexUserInterface.ExceptionHandler import get_handler
from KortexCore.Exception.Exception import EmptyField


class KortexDialog(QDialog):

    def __init__(self, parent, label_width=150):
        super(KortexDialog, self).__init__(parent=parent)
        self._label_width = label_width
        self._data_moderator = DataModerator()
        self.excs_handler = get_handler()
        self.setWindowIcon(QIcon(self._data_moderator.get_file_path(group="main_tree", name="kortex_tree")))

    def _entry(self, label, mandatory=False):
        layout = QHBoxLayout()
        label = QLabel(label)
        label.setFixedWidth(self._label_width)
        entry = QLineEdit()
        layout.addWidget(label)
        layout.addWidget(entry)
        if mandatory:
            ast = QLabel("*")
            layout.addWidget(ast)
        return layout, entry

    def _get_dialog_buttons(self, _layout):
        button_box = QDialogButtonBox(QDialogButtonBox.Ok|
                                      QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        _layout.addWidget(button_box, alignment=Qt.AlignCenter)

    def accept(self):
        self.excs_handler.try_execute(self._accept)

    def _accept(self):
        pass

    def _is_valid_path(self, _path):
        return os.path.isdir(_path)

    def _is_valid_name(self, name):
        return not any((s in name) for s in ["*", "/", "|", "?"])

    def _assert_inserted(self, fields):
        if any(field == "" for field in fields):
            raise EmptyField


class Verification(KortexDialog):

    def __init__(self, parent, question):
        super(Verification, self).__init__(parent=parent)
        self.setLayout(self._build_layout(question))
        self.setWindowTitle("Kortex")

    def _build_layout(self, question):
        vlayout = QVBoxLayout()
        question_label = QLabel(question)

        vlayout.addWidget(question_label)
        self._get_dialog_buttons(vlayout)

        return vlayout

    def accept(self):
        QDialog.accept(self)
