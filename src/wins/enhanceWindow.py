import os
import time
import win32api
import win32con

from PyQt5.QtWidgets import QDialog

from wins.ui.ui_enhanceWindow import Ui_EnhanceWindow
from libs.enhance import enhance1, enhance2, enhance3

class EnhanceWindow(QDialog, Ui_EnhanceWindow):
	def __init__(self, mainWin, parent=None):
		super(EnhanceWindow, self).__init__(parent)
		self.setupUi(self)
		self.setFixedSize(500, 400)

		self.mainWin = mainWin

		self.button_set_e1.clicked.connect(self.set_e1_paras)
		self.button_set_e2.clicked.connect(self.set_e2_paras)
		self.button_set_e3.clicked.connect(self.set_e3_paras)

		# 屏蔽点击回车响应
		self.button_set_e1.setAutoDefault(False)
		self.button_set_e2.setAutoDefault(False)
		self.button_set_e3.setAutoDefault(False)

		self.lineEdit_e1_blur_size.returnPressed.connect(self.return_pressed1)
		self.lineEdit_e1_gamma.returnPressed.connect(self.return_pressed1)
		self.lineEdit_e1_gamma_times.returnPressed.connect(self.return_pressed1)
		self.lineEdit_e1_center_value.returnPressed.connect(self.return_pressed1)
		self.lineEdit_e1_times.returnPressed.connect(self.return_pressed1)

		self.lineEdit_e2_blur_size.returnPressed.connect(self.return_pressed2)
		self.lineEdit_e2_gamma.returnPressed.connect(self.return_pressed2)
		self.lineEdit_e2_gamma_times.returnPressed.connect(self.return_pressed2)
		self.lineEdit_e2_block_size.returnPressed.connect(self.return_pressed2)
		self.lineEdit_e2_bias.returnPressed.connect(self.return_pressed2)
		self.lineEdit_e2_d.returnPressed.connect(self.return_pressed2)
		self.lineEdit_e2_sigmaColor.returnPressed.connect(self.return_pressed2)
		self.lineEdit_e2_sigmaSpace.returnPressed.connect(self.return_pressed2)
		self.lineEdit_e2_clipLimit.returnPressed.connect(self.return_pressed2)
		self.lineEdit_e2_k1.returnPressed.connect(self.return_pressed2)
		self.lineEdit_e2_dde.returnPressed.connect(self.return_pressed2)

		self.lineEdit_e3_sigma.returnPressed.connect(self.return_pressed3)
		self.lineEdit_e3_alpha.returnPressed.connect(self.return_pressed3)

	def set_e1_paras(self):
		self.lineEdit_e1_blur_size.setText('3')
		self.lineEdit_e1_gamma.setText('0.4')
		self.lineEdit_e1_gamma_times.setText('1.0')
		self.lineEdit_e1_center_value.setText('4.2')
		self.lineEdit_e1_times.setText('8.0')

	def set_e2_paras(self):
		self.lineEdit_e2_blur_size.setText('3')
		self.lineEdit_e2_gamma.setText('0.5')
		self.lineEdit_e2_gamma_times.setText('1.0')
		self.lineEdit_e2_block_size.setText('3')
		self.lineEdit_e2_bias.setText('600.0')
		self.lineEdit_e2_d.setText('20')
		self.lineEdit_e2_sigmaColor.setText('75')
		self.lineEdit_e2_sigmaSpace.setText('75')
		self.lineEdit_e2_clipLimit.setText('5')
		self.lineEdit_e2_k1.setText('0.2')
		self.lineEdit_e2_dde.setText('2.0')

	def set_e3_paras(self):
		self.lineEdit_e3_sigma.setText('4.0')
		self.lineEdit_e3_alpha.setText('6.0')

	def get_e1_paras(self):
		self.e1_blur_size = int(self.lineEdit_e1_blur_size.text())
		self.e1_gamma = float(self.lineEdit_e1_gamma.text())
		self.e1_gamma_times = float(self.lineEdit_e1_gamma_times.text())
		self.e1_center_value = float(self.lineEdit_e1_center_value.text())
		self.e1_times = float(self.lineEdit_e1_times.text())

	def get_e2_paras(self):
		self.e2_blur_size = int(self.lineEdit_e2_blur_size.text())
		self.e2_gamma = float(self.lineEdit_e2_gamma.text())
		self.e2_gamma_times = float(self.lineEdit_e2_gamma_times.text())
		self.e2_block_size = int(self.lineEdit_e2_block_size.text())
		self.e2_bias = float(self.lineEdit_e2_bias.text())
		self.e2_d = int(self.lineEdit_e2_d.text())
		self.e2_sigmaColor = int(self.lineEdit_e2_sigmaColor.text())
		self.e2_sigmaSpace = int(self.lineEdit_e2_sigmaSpace.text())
		self.e2_clipLimit = int(self.lineEdit_e2_clipLimit.text())
		self.e2_k1 = float(self.lineEdit_e2_k1.text())
		self.e2_dde = float(self.lineEdit_e2_dde.text())

	def get_e3_paras(self):
		self.e3_sigma = float(self.lineEdit_e3_sigma.text())
		self.e3_alpha = float(self.lineEdit_e3_alpha.text())

	def execute_enhance1(self, image):
		self.get_e1_paras()

		if not (self.e1_blur_size >= 3 and self.e1_blur_size % 2 != 0):
			win32api.MessageBox(0, '层1必须是大于等于3的奇数！', '提示', win32con.MB_ICONWARNING)
			return image

		image = enhance1(image, self.e1_blur_size, self.e1_gamma, self.e1_gamma_times, self.e1_center_value, self.e1_times)
		return image

	def execute_enhance2(self, image):
		self.get_e2_paras()

		if not (self.e2_blur_size >= 3 and self.e2_blur_size % 2 != 0):
			win32api.MessageBox(0, '层1必须是大于等于3的奇数！', '提示', win32con.MB_ICONWARNING)
			return image

		if not (self.e2_block_size >= 3 and self.e2_block_size % 2 != 0):
			win32api.MessageBox(0, '层4必须是大于等于3的奇数！', '提示', win32con.MB_ICONWARNING)
			return image

		image = enhance2(image, self.e2_blur_size, self.e2_gamma, self.e2_gamma_times, self.e2_block_size, self.e2_bias,
						 self.e2_d, self.e2_sigmaColor, self.e2_sigmaSpace, self.e2_clipLimit, self.e2_k1, self.e2_dde)
		return image

	def execute_enhance3(self, image):
		self.get_e3_paras()

		image = enhance3(image, self.e3_sigma, self.e3_alpha)
		image = enhance3(image, self.e3_sigma, self.e3_alpha)
		return image

	def return_pressed1(self):
		if self.mainWin.show1.fileName is not None:
			image = self.mainWin.readImage.read_all(self.mainWin.show1.fileName, dtype='uint16', channels=1)
			self.mainWin.scene1.image = self.execute_enhance1(image)
			self.mainWin.show1.show_image(self.mainWin.scene1.image, False, True)

		# if self.mainWin.show2.fileName is not None:
		# 	image = self.mainWin.readImage.read_all(self.mainWin.show2.fileName, dtype='uint16', channels=1)
		# 	self.mainWin.scene2.image = self.execute_enhance1(image)
		# 	self.mainWin.show2.show_image(self.mainWin.scene2.image, False, True)

	def return_pressed2(self):
		if self.mainWin.show1.fileName is not None:
			image = self.mainWin.readImage.read_all(self.mainWin.show1.fileName, dtype='uint16', channels=1)
			self.mainWin.scene1.image = self.execute_enhance2(image)
			self.mainWin.show1.show_image(self.mainWin.scene1.image, False, True)

		# if self.mainWin.show2.fileName is not None:
		# 	image = self.mainWin.readImage.read_all(self.mainWin.show2.fileName, dtype='uint16', channels=1)
		# 	self.mainWin.scene2.image = self.execute_enhance2(image)
		# 	self.mainWin.show2.show_image(self.mainWin.scene2.image, False, True)

	def return_pressed3(self):
		if self.mainWin.show1.fileName is not None:
			image = self.mainWin.readImage.read_all(self.mainWin.show1.fileName, dtype='uint16', channels=1)
			self.mainWin.scene1.image = self.execute_enhance3(image)
			self.mainWin.show1.show_image(self.mainWin.scene1.image, False, True)

		# if self.mainWin.show2.fileName is not None:
		# 	image = self.mainWin.readImage.read_all(self.mainWin.show2.fileName, dtype='uint16', channels=1)
		# 	self.mainWin.scene2.image = self.execute_enhance3(image)
		# 	self.mainWin.show2.show_image(self.mainWin.scene2.image, False, True)