# -*- coding: utf-8 -*-
import sys
import os
import re
import cv2
import time
import math
import array
import hashlib
import logging
import win32api
import win32con
import pydicom
import threading
import numpy as np
from scipy import signal
from natsort import natsort

from PyQt5.QtGui import QTransform
from PyQt5.QtCore import Qt, QRectF, QTimer, QDateTime
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QFileDialog
from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QMessageBox

from wins.ui.ui_loginWindow import Ui_LoginWindow
from wins.ui.ui_mainWindow import Ui_MainWindow
from wins.userWindow import UserWindow
from wins.classWindow import ClassWindow
from wins.enhanceWindow import EnhanceWindow

from libs.config import Config
from libs.globalvar import GlobalVar
from libs.log import Log
from libs.readimage import ReadImage
from libs.label import Label

if Config.bool_predict_on:
	from libs.predict import Predict

from libs.view.scene import GraphicsScene
from libs.view.show import Show
from libs.view.abstractlist import MyItemDelegate, MyAbstractListModel

import warnings
warnings.filterwarnings('ignore', category=DeprecationWarning)

class MainWindow(QMainWindow, Ui_MainWindow):
	def __init__(self, user_id, parent=None):
		super(MainWindow, self).__init__(parent)
		self.setupUi(self)

		self.setWindowTitle(Config.company_name)

		self.splitter.setSizes([1, 0])

		self.globalVar = GlobalVar()

		self.memory_path = ''

		log = Log()
		self.logger = log.logger

		# 定义按钮关联函数
		self.action_user.triggered.connect(self.open_userWin)
		self.action_enhance_para.triggered.connect(self.open_enhanceWin)
		self.action_open_image.triggered.connect(self.open_image)
		self.action_open_directory.triggered.connect(self.open_directory)
		self.action_prev_image.triggered.connect(self.prev_image)
		self.action_next_image.triggered.connect(self.next_image)
		self.action_other_image.triggered.connect(self.other_image)
		self.action_fit_window.triggered.connect(self.fit_window)
		self.action_init_size.triggered.connect(self.init_size)
		self.action_black_white_convert.triggered.connect(self.black_white_convert)
		self.action_relief_image.triggered.connect(self.relief_image)
		self.action_sharpen_image.triggered.connect(self.sharpen_image)
		self.action_blur_image.triggered.connect(self.blur_image)
		self.action_false_color_image.triggered.connect(self.false_color_image)
		self.action_image_enhance1.triggered.connect(self.image_enhance1)
		self.action_image_enhance2.triggered.connect(self.image_enhance2)
		self.action_image_enhance3.triggered.connect(self.image_enhance3)
		self.action_source_image.triggered.connect(self.source_image)
		self.action_rotate_left.triggered.connect(self.cv2_rotate_left)
		self.action_rotate_right.triggered.connect(self.cv2_rotate_right)
		self.action_overturn_x.triggered.connect(self.cv2_overturn_x)
		self.action_overturn_y.triggered.connect(self.cv2_overturn_y)

		self.listView_dir_files.clicked.connect(self.click_dir_files)

		# 调用状态栏类
		self.status = self.statusBar()
		# 创建self.currentTimeLabel，用于显示当前时间
		self.currentTimeLabel = QLabel()
		# 状态栏显示当前时间（默认位于状态栏右侧）
		self.status.addPermanentWidget(self.currentTimeLabel, stretch=0)

		self.readImage = ReadImage()

		self.userWin = UserWindow(user_id)
		self.enhanceWin = EnhanceWindow(self)
		self.classWin = ClassWindow()
		self.scene1 = GraphicsScene(self, None, True, 'scene1')
		self.scene2 = GraphicsScene(self, None, False, 'scene2')
		self.show1 = Show(self, self.scene1, self.graphicsView_1, True, True)
		self.show2 = Show(self, self.scene2, self.graphicsView_2, True, True)
		self.scene1.show = self.show1
		self.scene2.show = self.show2

		self.label = Label(self)

		if Config.bool_predict_on:
			self.predict = Predict(self)

		self.timer1 = QTimer()
		self.timer1.timeout.connect(self.timer_update_currentTimeLabel)
		self.timer1.start(1000)

		self.msgBox = None

		# 获取当前进程的ID
		process_id = os.getpid()
		self.logger.info(f'MainWindow ID: {process_id}')

	def timer_update_currentTimeLabel(self):
		# 获取当前时间
		currentTime = QDateTime.currentDateTime()
		# 格式化当前时间
		currentTime = currentTime.toString("yyyy-MM-dd hh:mm:ss dddd")
		# 更新self.currentTimeLabel
		self.currentTimeLabel.setText(currentTime)

	# 捕获窗口关闭事件
	def closeEvent(self, event):
		result = win32api.MessageBox(0, '确定退出吗？', '提示', win32con.MB_YESNO)
		if (result == win32con.IDYES):
			event.accept()

			self.userWin.close()

		else:
			event.ignore()

	def wheelEvent(self, event):
		scaleFactor = math.pow(2.0, event.angleDelta().y() / 240.0)

		factor = self.graphicsView_1.transform().scale(scaleFactor, scaleFactor).mapRect(
			QRectF(0, 0, 1, 1)).width()
		if factor < 0.07 or factor > 100:
			return

		factor = self.graphicsView_2.transform().scale(scaleFactor, scaleFactor).mapRect(
			QRectF(0, 0, 1, 1)).width()
		if factor < 0.07 or factor > 100:
			return

		self.graphicsView_1.scale(scaleFactor, scaleFactor)
		self.graphicsView_2.scale(scaleFactor, scaleFactor)

	def eventFilter(self, watched, event):
		if watched == self.graphicsView_1.verticalScrollBar():
			return True

		if watched == self.graphicsView_2.verticalScrollBar():
			return True

		return False

	def keyPressEvent(self, event):
		if Config.bool_predict_on and event.key() == Qt.Key_A:
			self.predict.prev_image()
		elif Config.bool_predict_on and event.key() == Qt.Key_D:
			self.predict.next_image()
		else:
			super().keyPressEvent(event)

	def open_userWin(self):
		self.userWin.show()

	def open_enhanceWin(self):
		self.enhanceWin.show()

	def read_image(self, read_scene, read_show):
		read_scene.image = self.readImage.read_all(read_show.fileName, dtype='uint16', channels=1)

		if Config.bool_check_and_process_image:
			read_scene.image = self.check_and_process_image(read_scene.image)

		if read_scene.image is not None:
			read_show.show_image(read_scene.image, True, False)

			# 自动旋转确保图像长边水平
			h, w = read_scene.image.shape[:2]
			if h > w and self.checkBox_auto_rotate.isChecked():
				self.cv2_rotate_left()

		else:
			read_show.fileName = None
			return

	def open_image(self):
		self.label.notice_save_file()
		fileType = "All Files(*);;Files(*.jpg);;Files(*.png);;Files(*.tif);;Files(*.tiff);;Files(*.bmp);;Files(*.dcm)"
		self.show1.fileName, _ = QFileDialog.getOpenFileName(self, "选取文件", os.getcwd(), fileType)
		if self.show1.fileName:
			self.read_image(self.scene1, self.show1)

	def click_dir_files(self, qModelIndex):
		self.label.notice_save_file()
		if self.globalVar.fileNames:
			self.globalVar.fileNames_index = qModelIndex.row()
			self.show1.fileName = self.globalVar.fileNames[self.globalVar.fileNames_index]
			self.read_image(self.scene1, self.show1)

	def refresh_dir_files(self):
		self.listModel = MyAbstractListModel(self.globalVar.fileNames, self)
		itemDelegate = MyItemDelegate(self)
		self.listView_dir_files.setModel(self.listModel)
		self.listView_dir_files.setItemDelegate(itemDelegate)

	def open_directory(self):
		if self.memory_path == '':
			self.memory_path = os.getcwd()
		self.filePath = QFileDialog.getExistingDirectory(None, "选取文件夹", self.memory_path)
		self.memory_path = self.filePath
		self.label.notice_save_file()
		self.globalVar.fileNames = []
		self.globalVar.fileNames_index = 0
		if self.filePath:
			for root, dirnames, filenames in os.walk(self.filePath):
				for filename in natsort(filenames):
					fileName = os.path.join(root, filename).replace('\\', '/')
					# 判断文件是否为图像
					if os.path.splitext(fileName)[1].lower() in Config.postfix:
						self.globalVar.fileNames.append(fileName)
			if self.globalVar.fileNames != []:
				self.refresh_dir_files()
				self.listView_dir_files.setCurrentIndex(self.listModel.index(self.globalVar.fileNames_index))
				self.show1.fileName = self.globalVar.fileNames[self.globalVar.fileNames_index]
				self.read_image(self.scene1, self.show1)

	def prev_image(self):
		self.label.notice_save_file()
		if self.globalVar.fileNames != [] and self.globalVar.fileNames_index > 0:
			self.globalVar.fileNames_index -= 1
			self.listView_dir_files.setCurrentIndex(self.listModel.index(self.globalVar.fileNames_index))
			self.show1.fileName = self.globalVar.fileNames[self.globalVar.fileNames_index]
			self.read_image(self.scene1, self.show1)

	def next_image(self):
		self.label.notice_save_file()
		if self.globalVar.fileNames != [] and \
				self.globalVar.fileNames_index < len(self.globalVar.fileNames) - 1:
			self.globalVar.fileNames_index += 1
			self.listView_dir_files.setCurrentIndex(self.listModel.index(self.globalVar.fileNames_index))
			self.show1.fileName = self.globalVar.fileNames[self.globalVar.fileNames_index]
			self.read_image(self.scene1, self.show1)

	def other_image(self):
		if self.action_other_image.isChecked():
			vh2 = self.graphicsView_1.height()
			vh3 = self.graphicsView_2.height()
			vh = (vh2 + vh3) // 2
			self.splitter.setSizes([vh, vh])

			fileType = "All Files(*);;Files(*.jpg);;Files(*.png);;Files(*.tif);;Files(*.tiff);;Files(*.bmp);;Files(*.dcm)"
			self.show2.fileName, _ = QFileDialog.getOpenFileName(self, "选取文件", os.getcwd(), fileType)
			if self.show2.fileName:
				self.read_image(self.scene2, self.show2)

		else:
			self.splitter.setSizes([1, 0])

			self.show2.fileName = None
			self.scene2.image = None

			# 清除对比图像
			if self.show2.pixmapItem is not None:
				self.scene2.removeItem(self.show2.pixmapItem)

	def reset_view(self):
		self.graphicsView_1.resetTransform()
		self.graphicsView_2.resetTransform()

	def fit_window(self):
		self.reset_view()

		if self.scene1.image is not None:
			vw2 = self.graphicsView_1.width()
			vh2 = self.graphicsView_1.height()
			ih2, iw2 = self.scene1.image.shape[:2]
			scaleFactor2 = min(vh2/ih2, vw2/iw2)
			self.graphicsView_1.scale(scaleFactor2, scaleFactor2)

		if self.scene2.image is not None:
			vw3 = self.graphicsView_2.width()
			vh3 = self.graphicsView_2.height()
			ih3, iw3 = self.scene2.image.shape[:2]
			scaleFactor3 = min(vh3 / ih3, vw3 / iw3)
			self.graphicsView_2.scale(scaleFactor3, scaleFactor3)

	def init_size(self):
		self.reset_view()

	def scene1_scene2_read_image(self):
		if self.scene1.image is not None:
			self.read_image(self.scene1, self.show1)

		if self.scene2.image is not None:
			self.read_image(self.scene2, self.show2)

	def scene1_scene2_read_source_image(self):
		self.action_sharpen_image.setChecked(False)
		self.action_relief_image.setChecked(False)
		self.action_blur_image.setChecked(False)
		self.action_false_color_image.setChecked(False)
		self.action_black_white_convert.setChecked(False)
		self.action_image_enhance1.setChecked(False)
		self.action_image_enhance2.setChecked(False)
		self.action_image_enhance3.setChecked(False)

		self.scene1_scene2_read_image()

	def check_and_process_image(self, image):
		if image is None:
			return None

		if self.action_sharpen_image.isChecked():
			image = self.sharpen_image_execute(image)
		if self.action_relief_image.isChecked():
			image = self.relief_image_execute(image)
		if self.action_blur_image.isChecked():
			image = cv2.GaussianBlur(image, (5, 5), 1.5)
		if self.action_false_color_image.isChecked():
			if image.dtype == 'uint16':
				image = (image / 257).astype(np.uint8)
			image = cv2.applyColorMap(image, cv2.COLORMAP_COOL) # 只能用于8位图像
		if self.action_black_white_convert.isChecked():
			if image.dtype == 'uint8':
				image = 255 - image
			elif image.dtype == 'uint16':
				image = 65535 - image
		if self.action_image_enhance1.isChecked():
			image = self.enhanceWin.execute_enhance1(image)
		if self.action_image_enhance2.isChecked():
			image = self.enhanceWin.execute_enhance2(image)
		if self.action_image_enhance3.isChecked():
			image = self.enhanceWin.execute_enhance3(image)

		return image

	def sharpen_image_execute(self, image):
		if len(image.shape) == 3:
			image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
		image_dtype = image.dtype
		image = signal.convolve2d(image, Config.kernel_sharpen, 'same', boundary='fill', fillvalue=0) # dtype为int32
		if image_dtype == 'uint8':
			max_value = 255
			dtype = np.uint8
		elif image_dtype == 'uint16':
			max_value = 65535
			dtype = np.uint16
		image[image > max_value] = max_value
		image[image < 0] = 0
		image = image.astype(dtype)
		return image

	def sharpen_image(self):
		if self.action_sharpen_image.isChecked():
			if self.scene1.image is not None:
				self.scene1.image = self.sharpen_image_execute(self.scene1.image)
				self.show1.show_image(self.scene1.image, False, True)
			if self.scene2.image is not None:
				self.scene2.image = self.sharpen_image_execute(self.scene2.image)
				self.show2.show_image(self.scene2.image, False, True)
		else:
			self.scene1_scene2_read_image()

	def relief_image_execute(self, image):
		if len(image.shape) == 3:
			image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
		image_dtype = image.dtype
		image = signal.convolve2d(image, Config.kernel_relief, 'same', boundary='fill', fillvalue=0)  # dtype为int32
		if image_dtype == 'uint8':
			max_value = 255
			dtype = np.uint8
		elif image_dtype == 'uint16':
			max_value = 65535
			dtype = np.uint16
		image = image + max_value // 2
		image[image > max_value] = max_value
		image[image < 0] = 0
		image = image.astype(dtype)
		return image

	def relief_image(self):
		if self.action_relief_image.isChecked():
			if self.scene1.image is not None:
				self.scene1.image = self.relief_image_execute(self.scene1.image)
				self.show1.show_image(self.scene1.image, False, True)
			if self.scene2.image is not None:
				self.scene2.image = self.relief_image_execute(self.scene2.image)
				self.show2.show_image(self.scene2.image, False, True)
		else:
			self.scene1_scene2_read_image()

	def blur_image(self):
		if self.action_blur_image.isChecked():
			if self.scene1.image is not None:
				self.scene1.image = cv2.GaussianBlur(self.scene1.image, (5, 5), 1.5)
				self.show1.show_image(self.scene1.image, False, True)
			if self.scene2.image is not None:
				self.scene2.image = cv2.GaussianBlur(self.scene2.image, (5, 5), 1.5)
				self.show2.show_image(self.scene2.image, False, True)
		else:
			self.scene1_scene2_read_image()

	def false_color_image(self):
		if self.action_false_color_image.isChecked():
			if self.scene1.image is not None:
				if self.scene1.image.dtype == 'uint16':
					self.scene1.image = self.scene1.image / 257
					self.scene1.image = self.scene1.image.astype(np.uint8)
				self.scene1.image = cv2.applyColorMap(self.scene1.image, cv2.COLORMAP_COOL)
				self.show1.show_image(self.scene1.image, False, True)
			if self.scene2.image is not None:
				if self.scene2.image.dtype == 'uint16':
					self.scene2.image = self.scene2.image / 257
					self.scene2.image = self.scene2.image.astype(np.uint8)
				self.scene2.image = cv2.applyColorMap(self.scene2.image, cv2.COLORMAP_COOL)
				self.show2.show_image(self.scene2.image, False, True)
		else:
			self.scene1_scene2_read_image()

	def black_white_convert(self):
		if self.action_black_white_convert.isChecked():
			if self.scene1.image is not None:
				if self.scene1.image.dtype == 'uint8':
					self.scene1.image = 255 - self.scene1.image
				elif self.scene1.image.dtype == 'uint16':
					self.scene1.image = 65535 - self.scene1.image
				self.show1.show_image(self.scene1.image, False, True)

			if self.scene2.image is not None:
				if self.scene2.image.dtype == 'uint8':
					self.scene2.image = 255 - self.scene2.image
				elif self.scene2.image.dtype == 'uint16':
					self.scene2.image = 65535 - self.scene2.image
				self.show2.show_image(self.scene2.image, False, True)
		else:
			self.scene1_scene2_read_image()

	def image_enhance1(self):
		if self.action_image_enhance1.isChecked():
			if self.scene1.image is not None:
				self.scene1.image = self.enhanceWin.execute_enhance1(self.scene1.image)
				self.show1.show_image(self.scene1.image, False, True)
			# if self.scene2.image is not None:
			# 	self.scene2.image = self.enhanceWin.execute_enhance1(self.scene2.image)
			# 	self.show2.show_image(self.scene2.image, False, True)
		else:
			self.scene1_scene2_read_image()

	def image_enhance2(self):
		if self.action_image_enhance2.isChecked():
			if self.scene1.image is not None:
				self.scene1.image = self.enhanceWin.execute_enhance2(self.scene1.image)
				self.show1.show_image(self.scene1.image, False, True)
			# if self.scene2.image is not None:
			# 	self.scene2.image = self.enhanceWin.execute_enhance2(self.scene2.image)
			# 	self.show2.show_image(self.scene2.image, False, True)
		else:
			self.scene1_scene2_read_image()

	def image_enhance3(self):
		if self.action_image_enhance3.isChecked():
			if self.scene1.image is not None:
				self.scene1.image = self.enhanceWin.execute_enhance3(self.scene1.image)
				self.show1.show_image(self.scene1.image, False, True)
			# if self.scene2.image is not None:
			# 	self.scene2.image = self.enhanceWin.execute_enhance3(self.scene2.image)
			# 	self.show2.show_image(self.scene2.image, False, True)
		else:
			self.scene1_scene2_read_image()

	def source_image(self):
		self.scene1_scene2_read_source_image()

	def adjust_global_contrast_execute(self, img, value):
		image = img.copy()

		if image is None:
			return

		min = value
		max = np.max(image)

		if image.dtype == 'uint8':
			max_value = 255
			dtype = np.uint8
		elif image.dtype == 'uint16':
			max_value = 65535
			dtype = np.uint16

		# 调节对比度
		image[image < min] = min
		image = image.astype(np.float64)
		image = (image - min) / (max - min) * max_value
		image = image.astype(dtype)

		return image

	def convert_x_y_w_h(self, flag, scene, x, y, w=None, h=None):
		if scene == 'scene1':
			# 注意：这是旋转之后图像的长宽
			ih, iw = self.scene1.image.shape[:2]

		elif scene == 'scene2':
			# 注意：这是旋转之后图像的长宽
			ih, iw = self.scene2.image.shape[:2]

		if flag == 'cv2_rotate_left':
			if w and h:
				return y, ih-w-x, h, w
			else:
				return y, ih-x

		elif flag == 'cv2_rotate_right':
			if w and h:
				return iw-h-y, x, h, w
			else:
				return iw-y, x

		elif flag == 'cv2_overturn_x':
			if w and h:
				return x, ih-h-y, w, h
			else:
				return x, ih-y

		elif flag == 'cv2_overturn_y':
			if w and h:
				return iw-w-x, y, w, h
			else:
				return iw-x, y

		elif flag == 'cv2_overturn_xy':
			if w and h:
				return iw-w-x, ih-h-y, w, h
			else:
				return iw-x, ih-y

		else:
			if w and h:
				return x, y, w, h
			else:
				return x, y

	def imencode_wo_compression(self, path, image):
		if path is None or image is None:
			return

		if os.path.splitext(path)[1].lower() == '.dcm':
			ds = pydicom.dcmread(path)
			ds.PixelData = image.tobytes()
			ds.Rows = image.shape[0]
			ds.Columns = image.shape[1]
			ds.save_as(path)
			return

		ext = os.path.splitext(path)[1]
		if ext in ['.tif', '.TIF', '.tiff', '.TIFF']:
			compression = [cv2.IMWRITE_TIFF_COMPRESSION, 1]
		elif ext in ['.jpg', '.JPG']:
			compression = [cv2.IMWRITE_JPEG_QUALITY, 100]
		elif ext in ['.png', '.PNG']:
			compression = [cv2.IMWRITE_PNG_COMPRESSION, 1]
		else:
			compression = []
		if compression:
			cv2.imencode(ext, image, compression)[1].tofile(path)
		else:
			cv2.imencode(ext, image)[1].tofile(path)

	def cv2_rotate_execute(self, angle, flag):
		if self.scene1.image is not None:
			self.scene1.image = cv2.rotate(self.scene1.image, angle)
			imencode_image = cv2.rotate(self.readImage.read_all(self.show1.fileName, dtype='uint16', channels=1), angle)
			self.imencode_wo_compression(self.show1.fileName, imencode_image)
			self.label.save_file(flag, 'scene1')
			self.show1.show_image(self.scene1.image, True, False)

		if self.scene2.image is not None:
			self.scene2.image = cv2.rotate(self.scene2.image, angle)
			imencode_image = cv2.rotate(self.readImage.read_all(self.show2.fileName, dtype='uint16', channels=1), angle)
			self.imencode_wo_compression(self.show2.fileName, imencode_image)
			self.label.save_file(flag, 'scene2')
			self.show2.show_image(self.scene2.image, True, False)

	def cv2_rotate_left(self):
		self.cv2_rotate_execute(cv2.ROTATE_90_COUNTERCLOCKWISE, 'cv2_rotate_left')

	def cv2_rotate_right(self):
		self.cv2_rotate_execute(cv2.ROTATE_90_CLOCKWISE, 'cv2_rotate_right')

	def cv2_overturn_execute(self, direction, flag):
		if self.scene1.image is not None:
			self.scene1.image = cv2.flip(self.scene1.image, direction)
			imencode_image = cv2.flip(self.readImage.read_all(self.show1.fileName, dtype='uint16', channels=1), direction)
			self.imencode_wo_compression(self.show1.fileName, imencode_image)
			self.label.save_file(flag, 'scene1')
			self.show1.show_image(self.scene1.image, True, False)

		if self.scene2.image is not None:
			self.scene2.image = cv2.flip(self.scene2.image, direction)
			imencode_image = cv2.flip(self.readImage.read_all(self.show2.fileName, dtype='uint16', channels=1), direction)
			self.imencode_wo_compression(self.show2.fileName, imencode_image)
			self.label.save_file(flag, 'scene2')
			self.show2.show_image(self.scene2.image, True, False)

	def cv2_overturn_x(self):
		self.cv2_overturn_execute(0, 'cv2_overturn_x') # 0表示上下翻转

	def cv2_overturn_y(self):
		self.cv2_overturn_execute(1, 'cv2_overturn_y') # 1表示左右翻转

	# 附带对比度调节
	def uintx_to_uint8(self, image):
		min_val = image.min()
		max_val = image.max()
		image = (image - min_val) / (max_val - min_val)
		image = np.uint8(image * 255)
		return image

	# 附带对比度调节
	def uintx_to_uint16(self, image):
		min_val = image.min()
		max_val = image.max()
		image = (image - min_val) / (max_val - min_val)
		image = np.uint16(image * 65535)
		return image

	def showMessageBox(self, flag_icon, title, text):
		if flag_icon == 'Information':
			icon = QMessageBox.Information
			style = "QWidget {color: rgb(0, 0, 0);} QPushButton {color: rgb(0,0,0);}"
		elif flag_icon == 'Warning':
			icon = QMessageBox.Warning
			style = "QWidget {color: rgb(0, 0, 0);} QPushButton {color: rgb(0,0,0);}"

		self.msgBox = QMessageBox()
		self.msgBox.setIcon(icon)
		self.msgBox.setStyleSheet(style)
		self.msgBox.setWindowTitle(title)
		self.msgBox.setText(text)
		self.msgBox.setWindowFlag(Qt.WindowStaysOnTopHint)
		self.msgBox.show()

# QMainWindow表示该窗口为主窗口，QDialog表示该窗口为子窗口
class LoginWindow(QMainWindow, Ui_LoginWindow):
	def __init__(self, parent=None):
		super(LoginWindow, self).__init__(parent)
		self.setupUi(self)

		self.setWindowTitle(Config.company_name)

		self.app = None

		self.setFixedSize(450, 300)

		self.file_users = 'users.txt'

		self.lineEdit_password.setEchoMode(QLineEdit.Password)

		self.login_button.clicked.connect(self.login)

	def login_execute(self, user_id):
		self.mainWin = MainWindow(user_id)

		self.mainWin.showMaximized()

		self.app.installEventFilter(self.mainWin)

		self.close()

	def login(self):
		my_id = self.lineEdit_id.text()
		my_password = self.lineEdit_password.text()
		flag_login = False

		# 验证用户管理文件是否存在
		if os.path.exists(self.file_users):
			my_password = hashlib.sha256(my_password.encode('utf-8')).hexdigest()
			with open(self.file_users, 'r') as f:
				users = f.readlines()
				for user in users:
					assert len(user.split(' ')) == 2, '用户管理文件内容错误！'
					id, password = user.split(' ')
					# 验证账号和密码是否输入正确
					if my_id == id and my_password == password[:-1]:
						self.login_execute(my_id)
						flag_login = True
						break
				if not flag_login:
					win32api.MessageBox(0, '账号或密码输入错误！', '提示', win32con.MB_ICONWARNING)
		else:
			win32api.MessageBox(0, '用户管理文件丢失！', '提示', win32con.MB_ICONWARNING)

if __name__ == '__main__':
	app = QApplication(sys.argv)
	loginWin = LoginWindow()
	loginWin.app = app
	loginWin.show()
	sys.exit(app.exec_())
