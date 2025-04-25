import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

####################################################################
class MyItemDelegate(QItemDelegate):
    def __init__(self, mainWin):
        QItemDelegate.__init__(self, None)

        self.mainWin = mainWin

    def paint(self, painter, option, index):
        painter.save()

        painter.setPen(QPen(Qt.NoPen))
        if option.state & QStyle.State_Selected:
            painter.setBrush(QBrush(QColor(0, 0, 255, 60)))
        else:
            painter.setBrush(QBrush(QColor(0, 0, 255, 0)))
        painter.drawRect(option.rect)

        # set text color
        value = index.data(Qt.DisplayRole)
        if value.endswith(' with defect'):
            painter.setPen(QPen(QColor(255, 255, 0, 255)))
            # painter.setPen(QPen(QColor(180, 180, 180, 255)))

            try:
                index = self.mainWin.predict.weld.weld_image_files.index(value[:-12])
                qualified = self.mainWin.predict.weld.weld_image_qualifieds[index]
                if qualified == '0':
                    painter.setPen(QPen(QColor(255, 0, 0, 255)))
                    # painter.setPen(QPen(QColor(100, 100, 100, 255)))
            except:
                pass

        else:
            painter.setPen(QPen(QColor(255, 255, 255, 255)))
        painter.drawText(option.rect, Qt.AlignLeft, value)

        painter.restore()

####################################################################
class MyAbstractListModel(QAbstractListModel):
    def __init__(self, listdata, parent=None, *args):
        """ listdata: a list where each item is a row
        """
        QAbstractTableModel.__init__(self, parent, *args)
        self.listdata = listdata

    def rowCount(self, parent=QModelIndex()):
        return len(self.listdata)

    def data(self, index, role):
        if index.isValid() and role == Qt.DisplayRole:
            return QVariant(self.listdata[index.row()])
        else:
            return QVariant()
