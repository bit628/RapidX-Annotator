import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import os
import win32api
import win32con
from natsort import natsort
from PyQt5.QtWidgets import QFileDialog, QGraphicsItem

from config import Config
from lab.labelFile import LabelFile
from lab.pascal_voc_io import PascalVocReader
from lab.seg_io import SegReader

class Label:
	def __init__(self, mainWin):
		self.mainWin = mainWin
		self.changed_directory = None

		self.mainWin.action_undo.triggered.connect(self.undo)
		self.mainWin.action_hide_box.triggered.connect(self.hide_box)
		self.mainWin.action_change_directory.triggered.connect(self.change_directory)
		self.mainWin.action_save_file.triggered.connect(self.save_file)
		self.mainWin.comboBox_preset_label.addItems(self.mainWin.classWin.classes)
		self.mainWin.button_select_label_file.clicked.connect(self.select_label_file)
		self.mainWin.button_jump_label_file.clicked.connect(self.jump_label_file)

		self.labelFile = LabelFile()

	def undo(self):
		if self.mainWin.scene1.pixmapItem is None:
			return

		child_num = len(self.mainWin.scene1.pixmapItem.childItems())
		if child_num != 0:
			self.mainWin.scene1.removeItem(self.mainWin.scene1.pixmapItem.childItems()[-1])

		self.mainWin.scene1.press_mouse = False
		self.mainWin.scene1.pixmapItem.setFlag(QGraphicsItem.ItemIsMovable, True)

		self.mainWin.scene1.flag_undo = True

	def hide_box(self):
		pixmapItemChildItems = self.mainWin.scene1.pixmapItem.childItems()
		for pixmapItemChildItem in pixmapItemChildItems:
			if self.mainWin.action_hide_box.isChecked():
				pixmapItemChildItem.setVisible(False)
			else:
				pixmapItemChildItem.setVisible(True)

	def change_directory(self):
		self.changed_directory = QFileDialog.getExistingDirectory(None, "选取文件夹", os.getcwd())

	def save_file(self, flag_rotate_overturn=None, flag_scene=None):
		i = 0
		j = 0
		rect_shapes = []
		polygon_shapes = []
		pixmapItemChildItems = self.mainWin.scene1.pixmapItem.childItems()
		for pixmapItemChildItem in pixmapItemChildItems:
			# 判断是否为矩形图元
			if pixmapItemChildItem.type() == 3:
				# 打印矩形图元相对于位图图元的坐标以及长宽
				x = round(pixmapItemChildItem.rect().x() + pixmapItemChildItem.x())
				y = round(pixmapItemChildItem.rect().y() + pixmapItemChildItem.y())
				w = round(pixmapItemChildItem.rect().width())
				h = round(pixmapItemChildItem.rect().height())
				x, y, w, h = self.mainWin.convert_x_y_w_h(flag_rotate_overturn, flag_scene, x, y, w, h)
				shape = {}
				shape['label'] = pixmapItemChildItem.label
				shape['points'] = [(x, y), (x+w, y), (x+w, y+h), (x, y+h)]
				shape['line_color'] = None
				shape['fill_color'] = None
				shape['difficult'] = int(pixmapItemChildItem.difficult)
				rect_shapes.append(shape)
				i+=1

			# 判断是否为多边形图元
			if pixmapItemChildItem.type() == 5:
				points = []
				for m_point in pixmapItemChildItem.m_points:
					x = round(m_point.x() + pixmapItemChildItem.x())
					y = round(m_point.y() + pixmapItemChildItem.y())
					x, y = self.mainWin.convert_x_y_w_h(flag_rotate_overturn, flag_scene, x, y)
					points.append([x, y])
				shape = {}
				shape['label'] = pixmapItemChildItem.label
				shape['points'] = points
				shape['group_id'] = None
				shape['shape_type'] = 'polygon'
				shape['flags'] = {}
				polygon_shapes.append(shape)
				j+=1

		if self.mainWin.show1.fileName:
			# 保存标注结果
			if not self.changed_directory:
				labelNamePascalVoc = os.path.splitext(self.mainWin.show1.fileName)[0] + '.xml'
				labelNameSeg = os.path.splitext(self.mainWin.show1.fileName)[0] + '.json'
			else:
				filename_xml = os.path.splitext(os.path.basename(self.mainWin.show1.fileName))[0] + '.xml'
				filename_json = os.path.splitext(os.path.basename(self.mainWin.show1.fileName))[0] + '.json'
				labelNamePascalVoc = os.path.join(self.changed_directory, filename_xml).replace('\\', '/')
				labelNameSeg = os.path.join(self.changed_directory, filename_json).replace('\\', '/')
			if rect_shapes != [] or os.path.isfile(labelNamePascalVoc):
				self.labelFile.savePascalVocFormat(labelNamePascalVoc, rect_shapes, self.mainWin.show1.fileName)
			if polygon_shapes != [] or os.path.isfile(labelNameSeg):
				self.labelFile.saveSegFormat(
					labelNameSeg,
					polygon_shapes,
					self.mainWin.show1.fileName,
					self.mainWin.checkBox_save_image.isChecked()
				)

	def notice_save_file(self):
		if self.mainWin.show1.fileName and self.mainWin.scene1.pixmapItem is not None:
			labelNamePascalVoc = os.path.splitext(self.mainWin.show1.fileName)[0]+'.xml'
			labelNameSeg = os.path.splitext(self.mainWin.show1.fileName)[0] + '.json'
			pixmapItemChildItems = self.mainWin.scene1.pixmapItem.childItems()
		else:
			return

		self.flag_save_file = True
		if os.path.exists(labelNamePascalVoc) or os.path.exists(labelNameSeg):
			if os.path.exists(labelNamePascalVoc):
				pascalvocReader = PascalVocReader(labelNamePascalVoc)
				shapes = pascalvocReader.getShapes()
				i = 0
				for pixmapItemChildItem in pixmapItemChildItems:
					if pixmapItemChildItem.type() == 3:
						if i < len(shapes):
							x = round(pixmapItemChildItem.rect().x() + pixmapItemChildItem.x())
							y = round(pixmapItemChildItem.rect().y() + pixmapItemChildItem.y())
							w = round(pixmapItemChildItem.rect().width())
							h = round(pixmapItemChildItem.rect().height())
							rect_item = (x, y, x+w, y+h)
							label_item = pixmapItemChildItem.label
							xmin_xml = shapes[i][1][0][0]
							ymin_xml = shapes[i][1][0][1]
							xmax_xml = shapes[i][1][2][0]
							ymax_xml = shapes[i][1][2][1]
							rect_xml = (xmin_xml, ymin_xml, xmax_xml, ymax_xml)
							label_xml = shapes[i][0]
							if rect_item != rect_xml or label_item != label_xml:
								self.flag_save_file = False
								break
						i+=1
				if i != len(shapes):
					self.flag_save_file = False

			if os.path.exists(labelNameSeg):
				segReader = SegReader(labelNameSeg)
				shapes = segReader.getShapes()
				i = 0
				for pixmapItemChildItem in pixmapItemChildItems:
					if pixmapItemChildItem.type() == 5:
						if i < len(shapes):
							points = []
							for m_point in pixmapItemChildItem.m_points:
								x = round(m_point.x() + pixmapItemChildItem.x())
								y = round(m_point.y() + pixmapItemChildItem.y())
								points.append([x, y])
							polygon_item = points
							label_item = pixmapItemChildItem.label
							polygon_json = shapes[i]['points']
							label_json = shapes[i]['label']
							if polygon_item != polygon_json or label_item != label_json:
								self.flag_save_file = False
								break
						i+=1
				if i != len(shapes):
					self.flag_save_file = False

		elif pixmapItemChildItems:
			self.flag_save_file = False

		if not self.flag_save_file:
			result = win32api.MessageBox(0, '是否保存标注文件？', '提示', win32con.MB_YESNO)
			if (result == win32con.IDYES):
				self.save_file()

	def select_label_file(self):
		fileType = "All Files(*);;Files(*.jpg);;Files(*.png);;Files(*.tif);;Files(*.tiff);;Files(*.bmp);;Files(*.dcm)"
		filePath, _ = QFileDialog.getOpenFileName(None, "选取文件", os.getcwd(), fileType)
		self.mainWin.lineEdit_select_label_file.setText(filePath)

	def jump_label_file(self):
		self.notice_save_file()
		self.mainWin.show1.fileName = self.mainWin.lineEdit_select_label_file.text()
		if self.mainWin.show1.fileName:
			filePath = os.path.dirname(self.mainWin.show1.fileName)
			self.mainWin.globalVar.fileNames = []
			self.mainWin.globalVar.fileNames_index = 0
			for root, dirnames, filenames in os.walk(filePath):
				for filename in natsort(filenames):
					fileName = os.path.join(root, filename).replace('\\', '/')
					if os.path.splitext(fileName)[1].lower() in Config.postfix:
						self.mainWin.globalVar.fileNames.append(fileName)
			self.mainWin.globalVar.fileNames_index = self.mainWin.globalVar.fileNames.index(self.mainWin.show1.fileName)

			self.mainWin.refresh_dir_files()
			self.mainWin.listView_dir_files.setCurrentIndex(self.mainWin.listModel.index(self.mainWin.globalVar.fileNames_index))
			self.mainWin.scene1.image = self.mainWin.readImage.read_all(self.mainWin.show1.fileName, dtype='uint16',channels=1)
			self.mainWin.show1.show_image(self.mainWin.scene1.image, True, False)