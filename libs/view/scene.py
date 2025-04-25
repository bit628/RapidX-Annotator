import cv2
import numpy as np
import pyautogui
import matplotlib.pyplot as plt

from PyQt5.QtCore import Qt, QPointF, QLineF
from PyQt5.QtGui import QPen, QBrush, QColor
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsItem
from PyQt5.QtWidgets import QGraphicsRectItem,  QGraphicsSimpleTextItem, QGraphicsLineItem

from libs.config import Config
from libs.view.rect import GraphicsRectItem
from libs.view.polygon import Instructions, GraphicsPolygonItem

class GraphicsScene(QGraphicsScene):
	def __init__(self, mainWin, show, key_is_active, name, parent=None):
		super(GraphicsScene, self).__init__(parent)
		self.mainWin = mainWin
		self.show = show
		self.key_is_active = key_is_active
		self.name = name
		self.press_1 = False
		self.press_2 = False
		self.press_3 = False
		self.press_4 = False
		self.press_5 = False
		self.press_6 = False
		self.press_7 = False
		self.press_mouse = False
		self.image = None
		self.pixmapItem = None
		self.rectItem = None
		self.flag_undo = False

		self.current_instruction = Instructions.No_Instruction

	def keyPressEvent(self, QKeyEvent):
		if QKeyEvent.key() == Qt.Key_1:
			self.press_1 = True

		if QKeyEvent.key() == Qt.Key_2 and self.key_is_active:
			self.press_2 = True

		if QKeyEvent.key() == Qt.Key_3 and self.key_is_active:
			self.press_3 = True

		if QKeyEvent.key() == Qt.Key_4:
			self.press_4 = True

		if QKeyEvent.key() == Qt.Key_5:
			pixmapItemChildItems = self.pixmapItem.childItems()
			for pixmapItemChildItem in pixmapItemChildItems:
				pixmapItemChildItem.setVisible(False)

		if QKeyEvent.key() == Qt.Key_6 and self.key_is_active:
			self.press_6 = True

		if QKeyEvent.key() == Qt.Key_7:
			self.press_7 = True

		return super().keyPressEvent(QKeyEvent)

	def keyReleaseEvent(self, QKeyEvent):
		if QKeyEvent.key() == Qt.Key_1:
			self.press_1 = False

		if QKeyEvent.key() == Qt.Key_2:
			self.press_2 = False

		if QKeyEvent.key() == Qt.Key_3:
			self.press_3 = False

		if QKeyEvent.key() == Qt.Key_4:
			self.press_4 = False

		if QKeyEvent.key() == Qt.Key_5:
			pixmapItemChildItems = self.pixmapItem.childItems()
			for pixmapItemChildItem in pixmapItemChildItems:
				pixmapItemChildItem.setVisible(True)

		if QKeyEvent.key() == Qt.Key_6:
			self.press_6 = False

		if QKeyEvent.key() == Qt.Key_7:
			self.press_7 = False

		return super().keyReleaseEvent(QKeyEvent)

	def setCurrentInstruction(self):
		self.polygon_item = GraphicsPolygonItem()
		self.polygon_item.setParentItem(self.pixmapItem)

	def point_in_item(self, point, item):
		def intersect(p, s, e):
			if s[1] > p.y() and e[1] > p.y(): # 线段在点上方
				return False
			elif s[1] < p.y() and e[1] < p.y(): # 线段在点下方
				return  False
			elif s[1] == e[1] and s[1] != p.y(): # 线段水平且线段与点不重合
				return False
			elif s[1] == e[1] and s[1] == p.y(): # 线段水平且线段与点重合
				return True
			else:
				x = e[0] - (e[0] - s[0]) * (e[1] - p.y()) / (e[1] - s[1]) # 交点x坐标
				if x >= p.x():
					return True
				return False

		if item.type() == 3:
			x = item.rect().x() + item.x()
			y = item.rect().y() + item.y()
			w = item.rect().width()
			h = item.rect().height()
			if x<=point.x()<=x+w and y<=point.y()<=y+h:
				return True

		elif item.type() == 5:
			points = []
			for m_point in item.m_points:
				x = round(m_point.x() + item.x())
				y = round(m_point.y() + item.y())
				points.append([x, y])
			intersect_num = 0
			total_num = len(points)
			for i in range(total_num):
				j = i+1 if i+1<total_num else 0
				if intersect(point, points[i], points[j]):
					intersect_num += 1
			if intersect_num % 2 == 1:
				return True

		return False

	def point_in_m_points(self, point, item):
		for m_point in item.m_points:
			x = round(m_point.x() + item.x())
			y = round(m_point.y() + item.y())
			if x-2 <= round(point.x()) <= x+2 and y-2 <= round(point.y()) <= y+2:
				return True
		return False

	def class_color(self, classWin):
		rgbs = []
		if classWin is None:
			classes = ['defect', 'gray', 'good']
		else:
			classes = classWin.classes
		for i in range(len(classes)):
			np.random.seed(i)
			rgb = [np.random.randint(0,255) for i in range(3)]
			rgbs.append(tuple(rgb))
		return rgbs

	def create_label_and_refresh_color(self, label, pos, item):
		bgrs = self.class_color(self.mainWin.classWin)
		try:
			bgr = bgrs[self.mainWin.classWin.classes_to_ids[label]]
		except KeyError:
			bgr = (0, 0, 255)
		pen_color = QColor(bgr[2], bgr[1], bgr[0], 255)
		brush_color = QColor(bgr[2], bgr[1], bgr[0], 60)
		item.setPen(QPen(pen_color, 1, Qt.SolidLine))
		item.brush_color = brush_color
		item.label = label
		if item.type() == 3:
			item.difficult = self.mainWin.checkBox_difficult.isChecked()
			for circle in item.circles:
				circle.setPen(QPen(pen_color, 1, Qt.SolidLine))
				circle.setBrush(brush_color)
		elif item.type() == 5:
			for m_item in item.m_items:
				m_item.setPen(QPen(pen_color, 1, Qt.SolidLine))
				m_item.setBrush(brush_color)

		if item.type() == 3 and Config.bool_show_length:
			length = max(item.rect().width(), item.rect().height()) * float(self.mainWin.globalVar.pixel_size) / 1000
			label_ = f'{label} {length:.1f}mm'
		else:
			label_ = label

		self.textItem = QGraphicsSimpleTextItem()
		self.textItem.setText(label_)
		self.textItem.setPen(pen_color)
		self.textItem.setPos(QPointF(pos.x(), pos.y() - 20))
		self.textItem.setParentItem(item)
		item.textItem = self.textItem

	def mousePressEvent(self, event: 'QGraphicsSceneMouseEvent') -> None:
		QGraphicsScene.mousePressEvent(self, event)

		if event.buttons() == Qt.RightButton and self.name not in ['scene2']:
			x, y = pyautogui.position()

		if self.flag_undo:
			self.press_1 = False
			self.press_2 = False
			self.press_3 = False
			self.press_4 = False
			self.press_5 = False
			self.press_6 = False
			self.press_7 = False
			self.flag_undo = False

		if self.press_1 or self.press_2 or self.press_7:
			self.pixmapItem.setFlag(QGraphicsItem.ItemIsMovable, False)
			self.press_mouse = True
			self.start_x = event.pos().x()
			self.start_y = event.pos().y()
			self.x0 = event.scenePos().x()
			self.y0 = event.scenePos().y()
			if self.press_1 or self.press_7:
				self.rectItem = QGraphicsRectItem(self.start_x, self.start_y, 0, 0)
				self.rectItem.setBrush(QBrush(QColor(255, 255, 255, 100)))
			if self.press_2:
				self.rectItem = GraphicsRectItem(self.start_x, self.start_y, 0, 0)

		elif self.press_3:
			self.current_instruction = Instructions.Polygon_Instruction
			self.setCurrentInstruction()

		elif self.press_4:
			pixmapItemChildItems = self.pixmapItem.childItems()
			for pixmapItemChildItem in pixmapItemChildItems:
				if self.point_in_item(self.pixmapItem.mapFromScene(event.scenePos()), pixmapItemChildItem):
					self.removeItem(pixmapItemChildItem)

		if self.current_instruction == Instructions.Polygon_Instruction:
			i_in_0 = False
			if self.polygon_item.m_points:
				x0 = self.polygon_item.m_points[0].x()
				y0 = self.polygon_item.m_points[0].y()
				xi = self.polygon_item.mapFromScene(event.scenePos()).x()
				yi = self.polygon_item.mapFromScene(event.scenePos()).y()
				offset_x = abs(xi - x0)
				offset_y = abs(yi - y0)
				i_in_0 = (offset_x < Config.margin_i_in_0 and offset_y < Config.margin_i_in_0)
			if i_in_0 or self.press_6:
				self.press_6 = False
				self.polygon_item.removeLastPoint()
				self.current_instruction = Instructions.No_Instruction

				pos = self.polygon_item.m_points[0]

				if self.mainWin.checkBox_preset.isChecked():
					polygon_label = self.mainWin.comboBox_preset_label.currentText()
					self.create_label_and_refresh_color(polygon_label, pos, self.polygon_item)
				elif self.mainWin.classWin is not None:
					mouse_x, mouse_y = pyautogui.position()
					self.mainWin.classWin.move(mouse_x, mouse_y)
					self.mainWin.classWin.show()
					self.mainWin.classWin.scene = self
					self.mainWin.classWin.create_label_and_refresh_color = self.create_label_and_refresh_color
					self.mainWin.classWin.pos = pos
					self.mainWin.classWin.item = self.polygon_item
			else:
				self.polygon_item.removeLastPoint()
				self.polygon_item.addPoint(self.polygon_item.mapFromScene(event.scenePos()))
				self.polygon_item.addPoint(self.polygon_item.mapFromScene(event.scenePos()))


	def mouseMoveEvent(self, event: 'QGraphicsSceneMouseEvent') -> None:
		QGraphicsScene.mouseMoveEvent(self, event)

		if self.pixmapItem is not None:
			pos = self.pixmapItem.mapFromScene(event.scenePos())
			x = round(pos.x())
			y = round(pos.y())
		else:
			x = 0
			y = 0

		if self.image is not None:
			ih, iw = self.image.shape[:2]
		else:
			return

		if 0<=x<iw and 0<=y<ih:
			if len(self.image.shape) == 3:
				color = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)[y, x]
			else:
				color = [self.image[y,x]]

			'''
			density = [float('%.2f' % (-1.2092e-11 * color[i]**3 + 8.8493e-8 * color[i]**2 - 1.3292e-3 * color[i] + 4.7786))
					   for i in range(len(color))] # 灰度有效范围为0~4000
			'''

			density = [float('%.2f' % (9.880e-5 * (65535 - color[i]) - 5.040e-3))
					   for i in range(len(color))]  # 灰度有效范围为5000~50000

			density = np.array(density)
			density[density > 5] = 5
			density[density < 0.5] = 0.5
			density = list(density)

			if len(color) == 3:
				if color[0] == color[1] and color[1] == color[2]:
					color = color[0]
					density = density[0]
			else:
				color = color[0]
				density = density[0]

		else:
			color = 'None'
			density = 'None'

		message = 'x={}   y={}'.format(x, y)
		message += '   color={}'.format(color)
		message += '   density={}'.format(density)

		self.mainWin.status.showMessage(message, 0)

		if (self.press_1 or self.press_2) and self.press_mouse:
			w = event.scenePos().x()-self.x0
			h = event.scenePos().y()-self.y0
			if w>Config.min_width_of_box and h>Config.min_height_of_box:
				self.rectItem.setRect(self.start_x, self.start_y, w, h)
				self.rectItem.setZValue(1)
				self.rectItem.setParentItem(self.pixmapItem)
				if self.press_2:
					self.rectItem.updateHandlesPos()

		if self.press_7 and self.press_mouse:
			w = event.scenePos().x() - self.x0
			h = event.scenePos().y() - self.y0
			aw = abs(w)
			ah = abs(h)
			if aw > Config.min_width_of_box and ah > Config.min_height_of_box:
				if h > 0:
					self.rectItem.setRect(self.start_x, self.start_y, aw, ah)
				else:
					self.rectItem.setRect(self.start_x, self.start_y - ah, aw, ah)

				self.rectItem.setZValue(1)
				self.rectItem.setParentItem(self.pixmapItem)

			try:
				current_info = self.mainWin.status.currentMessage()
				STD, SNRn = self.snr_measure(int(self.x0), int(self.y0), int(event.scenePos().x()), int(event.scenePos().y()))
				width = int(aw * float(self.mainWin.globalVar.pixel_size) / 1000)
				height = int(ah * float(self.mainWin.globalVar.pixel_size) / 1000)
				add_info = f'   标准差：{STD}   信噪比：{SNRn}   宽度：{width}mm   高度：{height}mm'
				self.mainWin.status.showMessage(f'{current_info}{add_info}')
			except:
				pass

		if self.current_instruction == Instructions.Polygon_Instruction:
			self.polygon_item.movePoint(self.polygon_item.number_of_points() - 1,
										self.polygon_item.mapFromScene(event.scenePos()))

	def mouseReleaseEvent(self, event: 'QGraphicsSceneMouseEvent') -> None:
		QGraphicsScene.mouseReleaseEvent(self, event)

		if self.pixmapItem is not None:
			pos = self.pixmapItem.mapFromScene(event.scenePos())

		if (self.press_1 or self.press_2) and self.press_mouse:
			self.press_mouse = False
			w = event.scenePos().x() - self.x0
			h = event.scenePos().y() - self.y0
			if w>=Config.min_width_of_box and h>=Config.min_height_of_box:
				if self.press_1 and self.rectItem is not None:
					self.removeItem(self.rectItem)
					if self.image is None:
						return
					if self.name in ['scene1', 'scene2']:
						if self.mainWin.scene1.image is not None:
							image = self.adjust_contrast(self.mainWin.scene1.image, round(self.start_x),
														 round(self.start_y), round(w), round(h))
							self.mainWin.show1.show_image(image, False, True)
						if self.mainWin.scene2.image is not None:
							image = self.adjust_contrast(self.mainWin.scene2.image, round(self.start_x),
														 round(self.start_y), round(w), round(h))
							self.mainWin.show2.show_image(image, False, True)
					elif self.name in ['scene_a', 'scene_b', 'scene_c', 'scene_d', 'scene_e']:
						if self.mainWin.scene_a.image is not None:
							image = self.adjust_contrast(self.mainWin.scene_a.image, round(self.start_x),
														 round(self.start_y), round(w), round(h))
							self.mainWin.show_a.show_image(image, False, True)
						if self.mainWin.scene_b.image is not None:
							image = self.adjust_contrast(self.mainWin.scene_b.image, round(self.start_x),
														 round(self.start_y), round(w), round(h))
							self.mainWin.show_b.show_image(image, False, True)
						if self.mainWin.scene_c.image is not None:
							image = self.adjust_contrast(self.mainWin.scene_c.image, round(self.start_x),
														 round(self.start_y), round(w), round(h))
							self.mainWin.show_c.show_image(image, False, True)
						if self.mainWin.scene_d.image is not None:
							image = self.adjust_contrast(self.mainWin.scene_d.image, round(self.start_x),
														 round(self.start_y), round(w), round(h))
							self.mainWin.show_d.show_image(image, False, True)
						if self.mainWin.scene_e.image is not None:
							image = self.adjust_contrast(self.mainWin.scene_e.image, round(self.start_x),
														 round(self.start_y), round(w), round(h))
							self.mainWin.show_e.show_image(image, False, True)

				if self.press_2 and self.rectItem is not None:
					pos = QPointF(self.start_x, self.start_y)
					if self.mainWin.checkBox_preset.isChecked():
						rect_label = self.mainWin.comboBox_preset_label.currentText()
						self.create_label_and_refresh_color(rect_label, pos, self.rectItem)
					elif self.mainWin.classWin is not None:
						mouse_x, mouse_y = pyautogui.position()
						self.mainWin.classWin.move(mouse_x, mouse_y)
						self.mainWin.classWin.show()
						self.mainWin.classWin.scene = self
						self.mainWin.classWin.create_label_and_refresh_color = self.create_label_and_refresh_color
						self.mainWin.classWin.pos = pos
						self.mainWin.classWin.item = self.rectItem

						self.press_2 = False

			self.pixmapItem.setFlag(QGraphicsItem.ItemIsMovable, True)

		if self.press_7 and self.press_mouse:
			self.press_mouse = False
			if self.rectItem is not None:
				self.removeItem(self.rectItem)

	def adjust_contrast(self, image, x, y, w, h):
		if image is None:
			return

		region = image[y: y + h, x: x + w]
		min = np.min(region)
		max = np.max(region)
		image_blank = np.zeros(image.shape, image.dtype)
		if image.dtype == 'uint16':
			max_value = 65535
			dtype = np.uint16
		else:
			max_value = 255
			dtype = np.uint8
		image_min = image_blank + min
		image_max = image_blank + max
		image_max_value = image_blank + max_value
		image = image.astype(np.float)
		image = (image - image_min) / (image_max - image_min) * image_max_value
		image[image < 0] = 0
		image[image > max_value] = max_value
		image = image.astype(dtype)
		return image

	def snr_measure(self, x0, y0, x1, y1):
		x0 = x0 if x0 > 0 else 0
		y0 = y0 if y0 > 0 else 0
		roi_area = self.image[y0:y1, x0:x1]
		roi_line = roi_area[roi_area.shape[0]//2,:]

		STD = int(np.std(roi_area))

		mean = np.mean(roi_line)
		std = np.std(roi_line)
		std = std if std != 0 else 1e-6
		SNR = mean / std
		SNRn = int(SNR * 88.6 / self.mainWin.globalVar.pixel_size)

		return STD, SNRn