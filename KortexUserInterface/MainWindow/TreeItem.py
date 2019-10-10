from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from EnumAndConsts.EnumsAndConsts import EPropertyType


class KortexTreeItem(QTreeWidgetItem):

    def __init__(self, data_moderator, event):
        self._data_moderator = data_moderator
        self.importance_icons = self._data_moderator.get_data(group="event_properties",
                                                              parameter="importance_names_and_icons")
        self._event = event
        cash = event.get_property(prop_name=EPropertyType.CASH_FLOW, cast_type=int)
        if cash >= 0:
            icon_name = "plus"
        else:
            icon_name = "minus"
            cash = abs(cash)
        importance = event.get_property(prop_name=EPropertyType.IMPORTANCE)

        super(KortexTreeItem, self).__init__([event.get_name(),
                                              event.get_property(prop_name=EPropertyType.START_DATE_AND_TIME),
                                              event.get_property(prop_name=EPropertyType.END_DATE_AND_TIME),
                                              importance,
                                              str(cash)])
        self.setIcon(3, QIcon(self._data_moderator.get_file_path(group="main_tree",
                                                                 name=self.importance_icons[importance])))
        self.setIcon(4, QIcon(self._data_moderator.get_file_path(group="main_tree",
                                                                 name=icon_name)))

    @property
    def event(self):
        return self._event

