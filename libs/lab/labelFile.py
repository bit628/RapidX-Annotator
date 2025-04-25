import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import time
import xml.dom.minidom

from base64 import b64encode
from json import dump

from readimage import ReadImage

try:
	from PyQt5.QtGui import QImage
	from PyQt5.QtCore import Qt, QTimer
	from PyQt5.QtWidgets import QMessageBox
except ImportError:
	from PyQt4.QtGui import QImage
	from PyQt4.QtCore import Qt, QTimer
	from PyQt4.QtWidgets import QMessageBox

class LabelFile(object):
	def __init__(self, filename=None):
		self.shapes = ()
		self.imagePath = None
		self.imageData = None
		self.verified = False

		self.readImage = ReadImage()

		self.flag_top_window = False
		self.timer2 = QTimer()
		self.timer2.timeout.connect(self.timer_top_window)
		self.timer2.start(200)

	def timer_top_window(self):
		if self.flag_top_window:
			time.sleep(0.2)
			self.flag_top_window = False

			self.showMessageBox(self.top_window_icon, '提示', self.top_window_text)

	def showMessageBox(self, flag_icon, title, text):
		if flag_icon == 'Information':
			icon = QMessageBox.Information
			style = "QWidget {color: rgb(0, 0, 0);} QPushButton {color: rgb(0,0,0);}"
		elif flag_icon == 'Warning':
			icon = QMessageBox.Warning
			style = "QWidget {color: rgb(0, 0, 0);} QPushButton {color: rgb(0,0,0);}"

		msgBox = QMessageBox()
		msgBox.setIcon(icon)
		msgBox.setStyleSheet(style)
		msgBox.setWindowTitle(title)
		msgBox.setText(text)
		msgBox.setWindowFlag(Qt.WindowStaysOnTopHint)
		msgBox.exec_()

	def savePascalVocFormat(self, path_xml, shapes, path_img):
		img = self.readImage.read_all(path_img)
		if len(img.shape) == 2:
			h, w = img.shape
			d = 1
		else:
			h, w, d = img.shape[:3]

		# 创建 XML Document 对象
		doc = xml.dom.minidom.Document()

		# 创建根节点
		annotation = doc.createElement("annotation")
		doc.appendChild(annotation)

		# 创建子节点
		folder = doc.createElement("folder")
		folder.appendChild(doc.createTextNode(os.path.basename(os.path.dirname(path_img))))
		annotation.appendChild(folder)

		# 创建子节点
		filename = doc.createElement("filename")
		filename.appendChild(doc.createTextNode(os.path.basename(path_img)))
		annotation.appendChild(filename)

		# 创建子节点
		path = doc.createElement("path")
		path.appendChild(doc.createTextNode(path_img))
		annotation.appendChild(path)

		# 创建子节点
		source = doc.createElement("source")
		annotation.appendChild(source)

		# 创建孙节点
		database = doc.createElement("database")
		database.appendChild(doc.createTextNode('Unknown'))
		source.appendChild(database)

		# 创建子节点
		size = doc.createElement("size")
		annotation.appendChild(size)

		# 创建孙节点
		width = doc.createElement("width")
		width.appendChild(doc.createTextNode(str(w)))
		size.appendChild(width)

		# 创建孙节点
		height = doc.createElement("height")
		height.appendChild(doc.createTextNode(str(h)))
		size.appendChild(height)

		# 创建孙节点
		depth = doc.createElement("depth")
		depth.appendChild(doc.createTextNode(str(h)))
		size.appendChild(depth)

		# 创建子节点
		segmented = doc.createElement("segmented")
		segmented.appendChild(doc.createTextNode(str(0)))
		annotation.appendChild(segmented)

		for shape in shapes:
			label = shape['label']
			try:
				score_ = shape['score']
			except:
				score_ = 1.0
			x0, y0 = shape['points'][0]
			x2, y2 = shape['points'][2]
			difficult_ = shape['difficult']

			# 创建子节点
			object = doc.createElement("object")
			annotation.appendChild(object)

			# 创建孙节点
			name = doc.createElement("name")
			name.appendChild(doc.createTextNode(str(label)))
			object.appendChild(name)

			# 创建孙节点
			score = doc.createElement("score")
			score.appendChild(doc.createTextNode(str(score_)))
			object.appendChild(score)

			# 创建孙节点
			pose = doc.createElement("pose")
			pose.appendChild(doc.createTextNode('Unspecified'))
			object.appendChild(pose)

			# 创建孙节点
			truncated = doc.createElement("truncated")
			truncated.appendChild(doc.createTextNode('0'))
			object.appendChild(truncated)

			# 创建孙节点
			difficult = doc.createElement("difficult")
			difficult.appendChild(doc.createTextNode(str(difficult_)))
			object.appendChild(difficult)

			# 创建孙节点
			bndbox = doc.createElement("bndbox")
			object.appendChild(bndbox)

			# 创建重孙节点
			xmin = doc.createElement("xmin")
			xmin.appendChild(doc.createTextNode(str(x0)))
			bndbox.appendChild(xmin)

			# 创建重孙节点
			ymin = doc.createElement("ymin")
			ymin.appendChild(doc.createTextNode(str(y0)))
			bndbox.appendChild(ymin)

			# 创建重孙节点
			xmax = doc.createElement("xmax")
			xmax.appendChild(doc.createTextNode(str(x2)))
			bndbox.appendChild(xmax)

			# 创建重孙节点
			ymax = doc.createElement("ymax")
			ymax.appendChild(doc.createTextNode(str(y2)))
			bndbox.appendChild(ymax)

		with open(path_xml, "w", encoding="utf-8") as f:
			doc.writexml(f, indent='', addindent='\t', newl='\n', encoding="utf-8")

	def saveSegFormat(self, filename, shapes, imagePath, bool_save_image):
		imageData = None
		with open(imagePath, 'rb') as f:
			source_bytes = f.read()
			base64_bytes = b64encode(source_bytes)
			imageData = base64_bytes.decode('utf-8')
		image = self.readImage.read_all(imagePath, dtype='uint16', channels=1)
		imageHeight, imageWidth = image.shape[:2]

		if not bool_save_image:
			imageData = None

		annotation = {
			"version": "1.0.0",
			"flags": {},
			"shapes": shapes,
			"imagePath": os.path.basename(imagePath),
			"imageData": imageData,
			"imageHeight": imageHeight,
			"imageWidth": imageWidth
		}

		for shape in shapes:
			for point in shape['points']:
				if point[0] < 0 or point[0] > imageWidth or point[1] < 0 or point[1] > imageHeight:
					self.top_window_icon = 'Warning'
					self.top_window_text = '坐标越界，保存失败！'
					self.flag_top_window = True
					return

		# 写入json数据
		with open(filename, 'w', encoding='utf-8') as f:
			dump(annotation, f, ensure_ascii=False, indent = 4)
