from KortexCore.Exception.Exception import KortexError
from KortexCore.CommonUtils.DataModerator import DataModerator

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *


class ExceptionHandler(object):

    def __init__(self):
        self._data_moderator = DataModerator()
        self.excs = tuple(KortexError.__subclasses__())

    def try_execute(self, procedure, *args, **kwargs):
        try:
            return procedure(*args, **kwargs)
        except self.excs as e:
            self._error_msg(e).exec_()
            return e

    def _error_msg(self, e):
        exc_msg = QMessageBox()
        exc_msg.setIcon(QMessageBox.Warning)
        exc_msg.setText(e.message())
        exc_msg.setStandardButtons(QMessageBox.Ok)
        exc_msg.setWindowIcon(QIcon(self._data_moderator.get_file_path(group="main_tree", name="kortex_tree")))
        exc_msg.setWindowTitle("Error")
        return exc_msg


excs_handler = ExceptionHandler()


def get_handler():
    global excs_handler
    return excs_handler
