import sys
import PyQt5.QtWidgets as QtWidgets
import Kortex.KortexData.KortexEnums as KortexEnums
from Kortex.KortexCore.Event.Event import Event as Event


class EventUI(QtWidgets.QWidget):

    def __init__(self, event):
        QtWidgets.QWidget.__init__(self)
        if not isinstance(event, Event):
            raise TypeError
        self._kortexEvent = event
        self.resize(200, 200)
        self._eventLayout = QtWidgets.QGridLayout()
        self.setLayout(self._eventLayout)
        self._eventLayout.sizeHint()
        self.setWindowTitle(self._kortexEvent.GetName())

        self._ConfigureEvents()
        self._ConfigureFiles()

    def _ConfigureEvents(self):
        pos = 1
        label = QtWidgets.QLabel("Events : ")
        self._eventLayout.addWidget(label, 0, 0)
        for eventName in self._kortexEvent.events.keys():
            button = QtWidgets.QPushButton(eventName)
            button.resize(10, 50)
            self._eventLayout.addWidget(button, pos, 0)
            pos += 1

    def _ConfigureFiles(self):
        pos = 1
        label = QtWidgets.QLabel("Files : ")
        self._eventLayout.addWidget(label, 0, 1)
        for fileName, file in self._kortexEvent.files.items():
            button = QtWidgets.QPushButton(fileName)
            button.resize(10, 50)
            button.clicked.connect(self._makeOpenFile(self._kortexEvent, file))
            self._eventLayout.addWidget(button, pos, 1)
            pos += 1

    def _makeOpenFile(self, event, file):
        def openFile():
            event.OpenFile(file)
        return openFile
