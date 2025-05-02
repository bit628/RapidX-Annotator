from enum import Enum

from libs.config import Config

from PyQt5.QtCore import Qt, QRectF, QPointF
from PyQt5.QtGui import QBrush, QPen, QColor, QPainterPath, QPainter, QCursor, QPolygonF
from PyQt5.QtWidgets import QGraphicsItem, QGraphicsPathItem, QGraphicsPolygonItem

class GraphicsPathItem(QGraphicsPathItem):
	radius = Config.circle_radius
	circle = QPainterPath()
	circle.addEllipse(QRectF(-radius, -radius, radius*2, radius*2))
	square = QPainterPath()
	square.addRect(QRectF(-radius, -radius, radius*2, radius*2))

	def __init__(self, annotation_item, index):
		super(GraphicsPathItem, self).__init__()
		self.m_annotation_item = annotation_item
		self.m_index = index

		self.setPath(GraphicsPathItem.circle)
		self.setBrush(QColor("red"))
		self.setPen(QPen(QColor("red"), 1, Qt.SolidLine))
		self.setFlag(QGraphicsItem.ItemIsMovable, True)
		self.setFlag(QGraphicsItem.ItemSendsGeometryChanges, True)
		self.setAcceptHoverEvents(True)
		self.setZValue(1)
		self.setCursor(QCursor(Qt.PointingHandCursor))

	def hoverEnterEvent(self, event):
		self.setPath(GraphicsPathItem.square)
		# self.setBrush(QColor("red"))
		super(GraphicsPathItem, self).hoverEnterEvent(event)

	def hoverLeaveEvent(self, event):
		self.setPath(GraphicsPathItem.circle)
		# self.setBrush(QColor("red"))
		super(GraphicsPathItem, self).hoverLeaveEvent(event)

	def mouseReleaseEvent(self, event):
		super(GraphicsPathItem, self).mouseReleaseEvent(event)

	def itemChange(self, change, value):
		if change == QGraphicsItem.ItemPositionChange and self.isEnabled():
			self.m_annotation_item.movePoint(self.m_index, value)
		return super(GraphicsPathItem, self).itemChange(change, value)

class GraphicsPolygonItem(QGraphicsPolygonItem):
	def __init__(self, parent=None):
		super(GraphicsPolygonItem, self).__init__(parent)
		self.m_points = []
		self.setZValue(1)
		self.setPen(QPen(QColor("white"), 1, Qt.SolidLine))
		self.brush_color = QColor(255, 0, 0, 60)
		self.setAcceptHoverEvents(True)

		self.setFlag(QGraphicsItem.ItemIsMovable, True)
		self.setFlag(QGraphicsItem.ItemSendsGeometryChanges, True)

		self.setCursor(QCursor(Qt.PointingHandCursor))

		self.m_items = []

		self.textItem = None

		self.label = None

	def number_of_points(self):
		return len(self.m_items)

	def addPoint(self, p):
		self.m_points.append(p)
		self.setPolygon(QPolygonF(self.m_points))
		item = GraphicsPathItem(self, len(self.m_points) - 1)
		item.setParentItem(self)
		self.m_items.append(item)
		item.setPos(p)

	def movePoint(self, i, p):
		if 0 <= i < len(self.m_points):
			self.m_points[i] = p
			self.setPolygon(QPolygonF(self.m_points))
			if i == 0 and self.textItem:
				self.textItem.setPos(QPointF(p.x(), p.y() - 20))

	def moveItem(self, index, pos):
		if 0 <= index < len(self.m_items):
			item = self.m_items[index]
			item.setEnabled(False)
			item.setPos(pos)
			item.setEnabled(True)

	def removeLastPoint(self):
		if self.m_points:
			self.m_points.pop()
			self.setPolygon(QPolygonF(self.m_points))
			it = self.m_items.pop()
			self.scene().removeItem(it)
			del it

	def itemChange(self, change, value):
		if change == QGraphicsItem.ItemPositionHasChanged:
			for i, point in enumerate(self.m_points):
				self.moveItem(i, point)
		return super(GraphicsPolygonItem, self).itemChange(change, value)

	def hoverEnterEvent(self, event):
		self.setBrush(self.brush_color)
		super(GraphicsPolygonItem, self).hoverEnterEvent(event)

	def hoverLeaveEvent(self, event):
		self.setBrush(QBrush(Qt.NoBrush))
		super(GraphicsPolygonItem, self).hoverLeaveEvent(event)

class Instructions(Enum):
	No_Instruction = 0
	Polygon_Instruction = 1