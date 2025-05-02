import os
import time
import win32api
import win32con
from wins.ui.ui_classWindow import Ui_ClassWindow
from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import QStringListModel, Qt

class ClassWindow(QDialog, Ui_ClassWindow):
	def __init__(self, parent=None):
		super(ClassWindow, self).__init__(parent)
		self.setupUi(self)
		self.setFixedSize(300, 300)

		# 定义按钮关联函数
		self.ok_button.clicked.connect(self.ok)
		self.cancel_button.clicked.connect(self.cancel)

		self.lineEdit_class.setFocusPolicy(Qt.NoFocus)

		self.classes = []
		self.classes_to_ids = {}
		self.flag_ok = False

		self.scene = None

		self.create_label_and_refresh_color = None
		self.pos = None
		self.item = None

		path = 'classes.txt'
		if os.path.exists(path):
			with open(path, 'r', encoding='utf-8') as f:
				self.classes=f.read().split('\n')
				self.classes[:] = [s for s in self.classes if s != '']
				self.classes_to_ids = dict(zip(self.classes, range(len(self.classes))))
			listModel=QStringListModel()
			listModel.setStringList(self.classes)
			self.listView_classes.setModel(listModel)
			self.listView_classes.clicked.connect(self.click)

	def closeEvent(self, event):
		if self.flag_ok:
			self.flag_ok = False
		else:
			self.scene.removeItem(self.item)

	def click(self, qModelIndex):
		self.lineEdit_class.setFocusPolicy(Qt.StrongFocus)
		self.lineEdit_class.setText(self.classes[qModelIndex.row()])

	def ok(self):
		if self.lineEdit_class.text():
			self.create_label_and_refresh_color(self.lineEdit_class.text(), self.pos, self.item)
			self.flag_ok = True
			self.close()
		else:
			win32api.MessageBox(0, '请选择类别！', '提示', win32con.MB_ICONWARNING)

	def cancel(self):
		self.close()