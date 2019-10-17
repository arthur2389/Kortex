from PyQt5.QtWidgets import *


class ExceptionHandler(object):

    def __init__(self, excs):
        self.excs = excs

    def try_execute(self, procedure, *args, **kwargs):
        try:
            return procedure(*args, **kwargs)
        except self.excs as e:
            exc_msg = QMessageBox()
            exc_msg.setIcon(QMessageBox.Warning)
            exc_msg.setText(e.message())
            exc_msg.setStandardButtons(QMessageBox.Ok)
            exc_msg.exec_()
