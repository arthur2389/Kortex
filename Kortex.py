import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from KortexUserInterface.MainWindow.MainWindow import KortexMainWindow


def _font():
    """
    Set font for caller
    """
    font = QFont()
    font.setPointSize(11)
    return font


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setFont(_font())
    _main = KortexMainWindow()

    sys.exit(app.exec_())
