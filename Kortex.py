import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from KortexCore.CommonUtils.DataModerator import DataModerator
from KortexUserInterface.MainWindow.MainWindow import KortexMainWindow


def _font():
    """
    Get font object with font properties
    """
    size = DataModerator().get_data(group="main_window_sizes",
                                    parameter="font_size")
    font = QFont()
    font.setPointSize(size)
    return font


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setFont(_font())
    _main = KortexMainWindow()

    sys.exit(app.exec_())
