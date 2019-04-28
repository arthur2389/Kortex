# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Projectviewermain.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

import sys

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_ProjectViewer(object):
    def setupUi(self, ProjectViewer):
        ProjectViewer.setObjectName(_fromUtf8("ProjectViewer"))
        ProjectViewer.resize(517, 397)
        self.centralwidget = QtGui.QWidget(ProjectViewer)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.timeEdit = QtGui.QTimeEdit(self.centralwidget)
        self.timeEdit.setGeometry(QtCore.QRect(40, 70, 118, 22))
        self.timeEdit.setObjectName(_fromUtf8("timeEdit"))
        self.calendarWidget = QtGui.QCalendarWidget(self.centralwidget)
        self.calendarWidget.setGeometry(QtCore.QRect(180, 50, 280, 155))
        self.calendarWidget.setObjectName(_fromUtf8("calendarWidget"))
        ProjectViewer.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(ProjectViewer)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 517, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuProject = QtGui.QMenu(self.menubar)
        self.menuProject.setObjectName(_fromUtf8("menuProject"))
        ProjectViewer.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(ProjectViewer)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        ProjectViewer.setStatusBar(self.statusbar)
        self.actionNew = QtGui.QAction(ProjectViewer)
        self.actionNew.setObjectName(_fromUtf8("actionNew"))
        self.actionOpen = QtGui.QAction(ProjectViewer)
        self.actionOpen.setObjectName(_fromUtf8("actionOpen"))
        self.actionQuit = QtGui.QAction(ProjectViewer)
        self.actionQuit.setObjectName(_fromUtf8("actionQuit"))
        self.actionQuit_2 = QtGui.QAction(ProjectViewer)
        self.actionQuit_2.setObjectName(_fromUtf8("actionQuit_2"))
        self.menuProject.addSeparator()
        self.menuProject.addAction(self.actionNew)
        self.menuProject.addAction(self.actionOpen)
        self.menuProject.addSeparator()
        self.menuProject.addAction(self.actionQuit_2)
        self.menubar.addAction(self.menuProject.menuAction())

        self.retranslateUi(ProjectViewer)
        QtCore.QMetaObject.connectSlotsByName(ProjectViewer)

    def retranslateUi(self, ProjectViewer):
        ProjectViewer.setWindowTitle(_translate("ProjectViewer", "Project Viewer", None))
        self.menuProject.setTitle(_translate("ProjectViewer", "Project", None))
        self.actionNew.setText(_translate("ProjectViewer", "New", None))
        self.actionOpen.setText(_translate("ProjectViewer", "Open", None))
        self.actionQuit.setText(_translate("ProjectViewer", "Quit", None))
        self.actionQuit_2.setText(_translate("ProjectViewer", "Quit", None))


def run():
    app = QtGui.QApplication(sys.argv)
    ProjectViewer = QtGui.QMainWindow()
    ui = Ui_ProjectViewer()
    ui.setupUi(ProjectViewer)
    ProjectViewer.show()
    sys.exit(app.exec_())

