import os
import cv2
import sys
import time
import win32api
import win32con
import numpy as np
from PyQt5.QtCore import Qt, QPointF
from PyQt5.QtGui import QImage, QPixmap, QPen, QBrush, QColor
from PyQt5.QtWidgets import QGraphicsItem, QGraphicsPixmapItem, QGraphicsSimpleTextItem, QGraphicsView

from libs.config import Config

from libs.view.rect import GraphicsRectItem
from libs.view.polygon import GraphicsPolygonItem

from libs.lab.pascal_voc_io import PascalVocReader
from libs.lab.seg_io import SegReader

class Show:
	def __init__(self, mainWin, scene, view, flag_set_center, flag_show_label):
		self.mainWin = mainWin
		self.scene = scene
		self.view = view
		self.flag_set_center = flag_set_center
		self.flag_show_label = flag_show_label

		self.fileName = None
		self.pixmapItem = None

	def array2qt(self, image):
		rows, cols = image.shape[:2]
		if len(image.shape) == 3:
			image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
		if image.dtype == 'uint8':
			if len(image.shape) == 2:
				qimage = QImage(image.data.tobytes(), cols, rows, cols, QImage.Format_Grayscale8)
			elif len(image.shape) == 3:
				qimage = QImage(image.data.tobytes(), cols, rows, cols*3, QImage.Format_RGB888)
		elif image.dtype == 'uint16':
			if len(image.shape) == 2:
				qimage = QImage(image.data.tobytes(), cols, rows, cols*2, QImage.Format_Grayscale16)
			elif len(image.shape) == 3:
				qimage = QImage(image.data.tobytes(), cols, rows, cols*6, QImage.Format_RGB16)
		# qimage转换为qpixmap
		qpixmap = QPixmap(qimage)
		return rows, cols, qpixmap

	def enhance_brightness_contrast(self, image, coef):
		if coef == 1.0:
			return image

		if image.dtype == 'uint16':
			image_max = 65535
			image_dtype = np.uint16
		else:
			image_max = 255
			image_dtype = np.uint8
		image = image.astype(np.float64)
		image = image * coef
		image[image > image_max] = image_max
		image = image.astype(image_dtype)
		return image

	def show_image(self, image, flag_open_image, flag_adjust_contrast, result=[], coef=1.0):
		# 设置标题栏信息
		if self.fileName:
			self.mainWin.setWindowTitle(Config.company_name + self.fileName)
		else:
			self.mainWin.setWindowTitle(Config.company_name)

		# 图像类型转换
		if image is not None:
			image = self.enhance_brightness_contrast(image, coef)
			ih, iw, self.qpixmap = self.array2qt(image)
		else:
			win32api.MessageBox(0, '图像不能为空！', '提示', win32con.MB_ICONASTERISK)
			return

		if flag_open_image and self.pixmapItem:
			self.scene.removeItem(self.pixmapItem)

		if flag_adjust_contrast:
			self.oldPixmapItem = self.pixmapItem
			self.oldPixmapItemScenePos = self.pixmapItem.scenePos()
			self.oldPixmapItemChildItems = self.pixmapItem.childItems()
			self.oldGraphicsViewRect = self.view.sceneRect()

		# 创建位图图元
		self.pixmapItem = QGraphicsPixmapItem(self.qpixmap)
		# 设置位图图元可以移动
		self.pixmapItem.setFlag(QGraphicsItem.ItemIsMovable, True)
		# 设置位图图元层叠顺序，数值大的图元位于数值小的图元之上，默认为0
		self.pixmapItem.setZValue(0)

		# 用于将位图图元设置为矩形图元的父图元
		self.scene.pixmapItem = self.pixmapItem
		# 将位图图元添加至场景
		self.scene.addItem(self.pixmapItem)

		# 设置视图所在场景
		self.view.setScene(self.scene)
		# 确保位图图元位于视图中心
		if self.flag_set_center:
			vw = self.view.width()
			vh = self.view.height()
			self.view.setSceneRect(-(vw-iw)/2, -(vh-ih)/2, vw, vh)

		# 设置GraphicsView的缓存模式为CacheBackground
		self.view.setCacheMode(QGraphicsView.CacheBackground)

		def show_object_detection_label(label, difficult, xmin, ymin, xmax, ymax, score):
			# 通过predefined_classes.txt设置区块颜色
			bgrs = self.scene.class_color(self.mainWin.classWin)
			try:
				bgr = bgrs[self.mainWin.classWin.classes_to_ids[label]]
			except KeyError:
				bgr = (0, 0, 255)
			pen_color = QColor(bgr[2], bgr[1], bgr[0], 255)
			brush_color = QColor(bgr[2], bgr[1], bgr[0], 60)

			w = xmax - xmin
			h = ymax - ymin
			self.rectItem = GraphicsRectItem(xmin, ymin, w, h)
			# 设置矩形图元位于位图图元上方
			self.rectItem.setZValue(1)
			# 设置位图图元为矩形图元的父图元
			self.rectItem.setParentItem(self.pixmapItem)
			# 设置矩形图元pen_color和brush_color
			self.rectItem.setPen(QPen(pen_color, 1, Qt.SolidLine))
			self.rectItem.brush_color = brush_color

			for circle in self.rectItem.circles:
				circle.setPen(QPen(pen_color, 1, Qt.SolidLine))
				circle.setBrush(brush_color)

			if Config.bool_show_length:
				length = max(w, h) * float(self.mainWin.globalVar.pixel_size) / 1000
				if label == '气孔':
					convert_points = self.mainWin.predict.NBT47013.get_convert_points([length])
					label_ = f'{label} {convert_points}'
				else:
					label_ = f'{label} {length:.2f}mm'
			elif Config.bool_show_score_w_h:
				score_w_h = f'{score:.2f} {int(w)} {int(h)}'
				label_ = f'{label} {score_w_h}'
			else:
				label_ = label

			# 创建标签，并设置内容、设置颜色、设置位置、设置父图元
			self.textItem = QGraphicsSimpleTextItem()
			self.textItem.setText(label_)
			self.textItem.setPen(pen_color)
			self.textItem.setPos(QPointF(xmin, ymin - 20))
			self.textItem.setParentItem(self.rectItem)
			# 用于更新文本图元位置，确保文本图元与矩形图元相对位置不变
			self.rectItem.textItem = self.textItem

			self.rectItem.label = label
			self.rectItem.difficult = difficult

		def show_semantic_segmentation_label(label, points):
			# 通过predefined_classes.txt设置区块颜色
			bgrs = self.scene.class_color(self.mainWin.classWin)
			try:
				bgr = bgrs[self.mainWin.classWin.classes_to_ids[label]]
			except KeyError:
				bgr = (0, 0, 255)
			pen_color = QColor(bgr[2], bgr[1], bgr[0], 255)
			brush_color = QColor(bgr[2], bgr[1], bgr[0], 60)

			self.polygon_item = GraphicsPolygonItem()
			for point in points:
				self.polygon_item.addPoint(QPointF(point[0], point[1]))
			# 设置矩形图元位于位图图元上方
			self.polygon_item.setZValue(1)
			# 设置位图图元为矩形图元的父图元
			self.polygon_item.setParentItem(self.pixmapItem)
			# 设置多边形图元pen_color和brush_color
			self.polygon_item.setPen(QPen(pen_color, 1, Qt.SolidLine))
			self.polygon_item.brush_color = brush_color

			for m_item in self.polygon_item.m_items:
				m_item.setPen(QPen(pen_color, 1, Qt.SolidLine))
				m_item.setBrush(brush_color)

			self.textItem = QGraphicsSimpleTextItem()
			self.textItem.setText(label)
			self.textItem.setPen(pen_color)
			self.textItem.setPos(QPointF(points[0][0], points[0][1] - 20))
			self.textItem.setParentItem(self.polygon_item)
			self.polygon_item.textItem = self.textItem

			self.polygon_item.label = label

		if flag_open_image and self.flag_show_label:
			if self.fileName:
				labelNamePascalVoc = os.path.splitext(self.fileName)[0] + '.xml'
				labelNameSeg = os.path.splitext(self.fileName)[0] + '.json'
			else:
				labelNamePascalVoc = ''
				labelNameSeg = ''

			if Config.label_file != '':
				labelNamePascalVoc = os.path.dirname(os.path.dirname(labelNamePascalVoc)) + f'/{Config.label_file}/' + \
									 os.path.basename(labelNamePascalVoc)
				labelNameSeg = os.path.dirname(os.path.dirname(labelNameSeg)) + f'/{Config.label_file}/' + \
									 os.path.basename(labelNameSeg)

			if os.path.exists(labelNamePascalVoc) or os.path.exists(labelNameSeg):
				if os.path.exists(labelNamePascalVoc):
					pascalvocReader = PascalVocReader(labelNamePascalVoc)
					shapes = pascalvocReader.getShapes()
					for shape in shapes:
						label = shape[0]
						if Config.bool_cut_weld and label in ['weld', '焊缝']:
							continue
						difficult = shape[4]
						xmin = shape[1][0][0]
						ymin = shape[1][0][1]
						xmax = shape[1][2][0]
						ymax = shape[1][2][1]
						try:
							score = shape[5]
						except:
							score = 1.0
						show_object_detection_label(label, difficult, xmin, ymin, xmax, ymax, score)

				if os.path.exists(labelNameSeg):
					segReader = SegReader(labelNameSeg)
					shapes = segReader.getShapes()
					for shape in shapes:
						label = shape['label']
						points = shape['points']
						show_semantic_segmentation_label(label, points)

			else:
				if self.mainWin.globalVar.model == 'object_detection':
					for subresult in result:
						label = subresult['category']
						try:
							score = subresult['score']
						except:
							score = 1.0
						difficult = 0
						xmin, ymin, w, h = subresult['bbox']
						xmax = xmin + w
						ymax = ymin + h
						show_object_detection_label(label, difficult, xmin, ymin, xmax, ymax, score)

				elif self.mainWin.globalVar.model == 'semantic_segmentation':
					for subresult in result:
						label = subresult['category']
						points = subresult['point']
						show_semantic_segmentation_label(label, points)

		if flag_adjust_contrast:
			self.scene.removeItem(self.oldPixmapItem)
			self.pixmapItem.setPos(self.oldPixmapItemScenePos)
			for oldPixmapItemChildItem in self.oldPixmapItemChildItems:
				oldPixmapItemChildItem.setParentItem(self.pixmapItem)
			self.view.setSceneRect(self.oldGraphicsViewRect)