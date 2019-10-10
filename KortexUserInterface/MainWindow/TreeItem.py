from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from EnumAndConsts.EnumsAndConsts import EPropertyType


class KortexTreeItem(QTreeWidgetItem):

    def __init__(self, data_moderator):
        super(KortexTreeItem, self).__init__()
        self._data_moderator = data_moderator
        

    def _tree_widget_item(self, event):
        cash = event.get_property(prop_name=EPropertyType.CASH_FLOW, cast_type=int)
        if cash >= 0:
            icon_name = "plus"
        else:
            icon_name = "minus"
            cash = abs(cash)
        importance = event.get_property(prop_name=EPropertyType.IMPORTANCE)

        i = QTreeWidgetItem([event.get_name(),
                             event.get_property(prop_name=EPropertyType.START_DATE_AND_TIME),
                             event.get_property(prop_name=EPropertyType.END_DATE_AND_TIME),
                             importance,
                             str(cash)])
        i.setIcon(3, QIcon(self._data_moderator.get_file_path(group="main_tree",
                                                              name=self.importance_icons[importance])))
        i.setIcon(4, QIcon(self._data_moderator.get_file_path(group="main_tree",
                                                              name=icon_name)))