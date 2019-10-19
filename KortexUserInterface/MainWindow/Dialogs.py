from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


from KortexUserInterface.KortexWidgets.KortexDialog import KortexDialog
from KortexCoreInterface.KortexCoreInterface import PropertyArgs, DateTimeArgs
from EnumAndConsts.EnumsAndConsts import EPropertyType as PrType
from KortexCore.Event.DateTimeHandler import DateTimeHandler
from KortexCore.Exception.Exception import *


class NewEventWindow(KortexDialog):

    class _DateTimeUserInput(object):

        def __init__(self, user_input=None):
            self._user_selected = user_input

        def set(self, user_input):
            self._user_selected = user_input

        def __str__(self):
            return self._user_selected["date"].toString() + " " \
                   + self._user_selected["hour"] + ":" + self._user_selected["minute"]

        def __call__(self):
            if not self._user_selected:
                return None
            return DateTimeArgs(day=self._user_selected["date"].day(),
                                month=self._user_selected["date"].month(),
                                year=self._user_selected["date"].year(),
                                hour=int(self._user_selected["hour"]),
                                minute=int(self._user_selected["minute"]))

    def __init__(self, parent, kortex_project, window_width, holding_event=None):
        super(NewEventWindow, self).__init__(parent=parent, label_width=150)

        self._new_event = None
        self._name_entry = self._priorities = None
        self.dt_start_txt = self.dt_end_txt = None
        self.dt_user_input = {PrType.START_DATE_AND_TIME: self._DateTimeUserInput(),
                              PrType.END_DATE_AND_TIME: self._DateTimeUserInput()}

        self._prj = kortex_project
        self._holding_event = holding_event

        self.setLayout(self._build_layout())
        self.setWindowTitle("Insert new event")
        self.setMinimumWidth(window_width)

    @property
    def new_event(self):
        return self._new_event

    def _build_layout(self):
        vlayout = QVBoxLayout()

        name_layout, self._name_entry = self._entry(label="Event name: ", mandatory=True)
        cashflow_layout, self._cashflow_entry = self._entry(label="Event cash flow: ")

        dt_start_layout, self.dt_start_txt = self._entry("Event start time: ")
        dt_start_layout.addWidget(self._open_calendar(PrType.START_DATE_AND_TIME))
        dt_end_layout, self.dt_end_txt = self._entry("Event end time: ")
        dt_end_layout.addWidget(self._open_calendar(PrType.END_DATE_AND_TIME))

        self._cashflow_entry.setText("0")
        importance_layout = self._importance_entry()

        vlayout.addLayout(name_layout)
        vlayout.addLayout(dt_start_layout)
        vlayout.addLayout(dt_end_layout)
        vlayout.addLayout(importance_layout)
        vlayout.addLayout(cashflow_layout)

        self._get_dialog_buttons(vlayout)
        return vlayout

    def _open_calendar(self, time):
        open_calendar = QPushButton()
        open_calendar.setIcon(QIcon(self._data_moderator.get_file_path(group="main_dialogs", name="calendar")))
        open_calendar.clicked.connect(lambda: self._calendar(time))

        return open_calendar

    def _calendar(self, time):
        self.cal = KortexCalendar(self)
        if self.cal.exec_():
            if time == PrType.START_DATE_AND_TIME:
                ent = self.dt_start_txt
            else:
                ent = self.dt_end_txt
            p = QPalette()
            p.setColor(QPalette.Base, Qt.cyan)
            ent.setPalette(p)

            self.dt_user_input[time].set(self.cal.selected_date_time)
            ent.setText(str(self.dt_user_input[time]))

    def _accept(self):
        # Check input
        cash_flow = self._cashflow_entry.text()
        name = self._name_entry.text()
        priority = self._priorities.currentText()
        start_time = self.dt_user_input[PrType.START_DATE_AND_TIME]()
        end_time = self.dt_user_input[PrType.END_DATE_AND_TIME]()

        # Filter user input
        self._assert_inserted([name])
        if not self._is_valid_name(name):
            raise BadEventName
        try:
            cash_flow = int(cash_flow)
        except Exception:
            raise CashFlowNotInt
        DateTimeHandler.validate(start_time, end_time)

        # Build new event
        self._new_event = self._prj.create_event(event_name=name, holding_event=self._holding_event)

        if end_time or start_time:
            self._new_event.set_date_time(start_date_time_args=start_time, end_date_time_args=end_time)

        args = PropertyArgs(importance=priority, cash_flow=cash_flow)
        self._new_event[PrType.IMPORTANCE] = args
        self._new_event[PrType.CASH_FLOW] = args
        QDialog.accept(self)

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


class KortexCalendar(KortexDialog):

    def __init__(self, parent):
        super(KortexCalendar, self).__init__(parent=parent)
        self.calendar = self.h = self.ampm = self.m = None
        self._date_and_time = {"date": None, "hour": "", "minute": ""}
        self.setLayout(self._build_layout())

    @property
    def selected_date_time(self):
        return self._date_and_time

    def _build_layout(self):

        vlayout = QVBoxLayout()
        self.calendar = QCalendarWidget()

        time_set = QHBoxLayout()
        self.h = self._time_input(12)
        i = QLabel(":")
        self.m = self._time_input(60, 15)
        self.ampm = QComboBox()
        self.ampm.addItems(["AM", "PM"])

        time_set.addWidget(self.h)
        time_set.addWidget(i)
        time_set.addWidget(self.m)
        time_set.addWidget(self.ampm)

        time_set.setAlignment(Qt.AlignCenter)
        vlayout.addWidget(self.calendar)
        vlayout.addLayout(time_set)
        self._get_dialog_buttons(vlayout)

        return vlayout

    def _time_input(self, _max, i=1):
        def _to_str(num):
            if num < 10:
                return "0" + str(num)
            return str(num)
        items = list(range(0, _max, i))
        items = map(_to_str, items)

        box = QComboBox()
        box.addItems(items)
        return box

    def _accept(self):
        self._date_and_time["date"] = self.calendar.selectedDate()
        if self.ampm.currentText() == "PM":
            self._date_and_time["hour"] = str(int(self.h.currentText()) + 12)
        else:
            self._date_and_time["hour"] = self.h.currentText()
        self._date_and_time["minute"] = self.m.currentText()
        QDialog.accept(self)


class LoadProjectWindow(KortexDialog):

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
        self._get_dialog_buttons(vlayout)

        return vlayout

    def accept(self):
        self._project_to_load = self._names.currentText()
        QDialog.accept(self)


class NewProjectWindow(KortexDialog):

    def __init__(self, parent):
        super(NewProjectWindow, self).__init__(parent=parent)
        self._name_entry = self._path_entry = None
        self.setLayout(self._build_layout())
        self.setWindowTitle("Create new project")

    def _build_layout(self):
        vlayout = QVBoxLayout()

        name_layout, self._name_entry = self._entry(label="New project name: ", mandatory=True)
        path_layout, self._path_entry = self._entry(label="Location: ", mandatory=True)
        path_input = QPushButton()
        path_input.setIcon(QIcon(self._data_moderator.get_file_path(group="main_dialogs", name="open")))
        path_input.clicked.connect(self._path_input)
        path_layout.addWidget(path_input)

        vlayout.addLayout(name_layout)
        vlayout.addLayout(path_layout)
        self._get_dialog_buttons(vlayout)

        return vlayout

    def _path_input(self):
        self._path = QFileDialog.getExistingDirectory(parent=self,
                                                      caption="Select location for new project")
        if self._path:
            self._path_entry.setText(self._path)

    def _accept(self):
        name = self._name_entry.text()
        _path = self._path_entry.text()
        self._assert_inserted([name, _path])

        if not self._is_valid_name(name):
            raise BadEventName
        if not self._is_valid_path(_path):
            raise InvalidPath
        self._data_moderator.set_new_project(name=name,
                                             pr_path=_path)
        QDialog.accept(self)
