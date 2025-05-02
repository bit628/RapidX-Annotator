from PyQt5.QtCore import Qt, QRectF, QPointF
from PyQt5.QtGui import QBrush, QColor, QPen
from PyQt5.QtWidgets import QGraphicsItem, QGraphicsRectItem, QGraphicsEllipseItem
from libs.config import Config

class GraphicsRectItem(QGraphicsRectItem):

	handleTopLeft = 1
	handleTopMiddle = 2
	handleTopRight = 3
	handleMiddleLeft = 4
	handleMiddleRight = 5
	handleBottomLeft = 6
	handleBottomMiddle = 7
	handleBottomRight = 8

	handleSize = +8.0
	handleSpace = -4.0

	handleCursors = {
		handleTopLeft: Qt.SizeFDiagCursor,
		handleTopMiddle: Qt.SizeVerCursor,
		handleTopRight: Qt.SizeBDiagCursor,
		handleMiddleLeft: Qt.SizeHorCursor,
		handleMiddleRight: Qt.SizeHorCursor,
		handleBottomLeft: Qt.SizeBDiagCursor,
		handleBottomMiddle: Qt.SizeVerCursor,
		handleBottomRight: Qt.SizeFDiagCursor,
	}

	def __init__(self, *args):
		"""
		Initialize the shape.
		"""
		super().__init__(*args)
		self.handles = {}
		self.handleSelected = None
		self.mousePressPos = None
		self.mousePressRect = None
		self.setAcceptHoverEvents(True)
		self.setFlag(QGraphicsItem.ItemIsMovable, True)
		self.setFlag(QGraphicsItem.ItemSendsGeometryChanges, True)

		self.setPen(QPen(QColor("red"), 1, Qt.SolidLine))
		self.brush_color = QColor(255, 0, 0, 60)

		self.circles = []
		radius = Config.circle_radius
		for i in range(8):
			circle = QGraphicsEllipseItem(QRectF(-radius, -radius, radius*2, radius*2))
			circle.setBrush(QColor("red"))
			circle.setPen(QPen(QColor("red"), 1, Qt.SolidLine))
			circle.setParentItem(self)
			circle.setZValue(1)
			self.circles.append(circle)

		self.textItem = None

		self.label = None
		self.difficult = None

		self.mainWin = None

		self.updateHandlesPos()

	def handleAt(self, point):
		"""
		Returns the resize handle below the given point.
		"""
		for k, v, in self.handles.items():
			# 只有创建rectItem_permanent时self.mainWin才不为空，所以只有调整rectItem_permanent大小时，才更容易出现双箭头符号
			if self.mainWin:
				v = QRectF(v.x()-25, v.y()-25, 50, 50)
			if v.contains(point):
				return k
		return None

	def hoverMoveEvent(self, moveEvent):
		"""
		Executed when the mouse moves over the shape (NOT PRESSED).
		"""
		self.setBrush(self.brush_color)
		handle = self.handleAt(moveEvent.pos())
		cursor = Qt.PointingHandCursor if handle is None else self.handleCursors[handle]
		self.setCursor(cursor)
		super().hoverMoveEvent(moveEvent)

	def hoverLeaveEvent(self, moveEvent):
		"""
		Executed when the mouse leaves the shape (NOT PRESSED).
		"""
		self.setBrush(QBrush(Qt.NoBrush))
		self.setCursor(Qt.ArrowCursor)
		super().hoverLeaveEvent(moveEvent)

	def mousePressEvent(self, mouseEvent):
		"""
		Executed when the mouse is pressed on the item.
		"""
		self.handleSelected = self.handleAt(mouseEvent.pos())
		if self.handleSelected:
			self.mousePressPos = mouseEvent.pos()
			self.mousePressRect = self.boundingRect()
		super().mousePressEvent(mouseEvent)

	def mouseMoveEvent(self, mouseEvent):
		"""
		Executed when the mouse is being moved over the item while being pressed.
		"""
		if self.handleSelected is not None:
			self.interactiveResize(mouseEvent.pos())
		else:
			super().mouseMoveEvent(mouseEvent)

	def mouseReleaseEvent(self, mouseEvent):
		"""
		Executed when the mouse is released from the item.
		"""
		super().mouseReleaseEvent(mouseEvent)
		self.handleSelected = None
		self.mousePressPos = None
		self.mousePressRect = None
		self.update()

	def boundingRect(self):
		"""
		Returns the bounding rect of the shape (including the resize handles).
		"""
		o = self.handleSize + self.handleSpace
		return self.rect().adjusted(-o, -o, o, o)

	def updateHandlesPos(self):
		"""
		Update current resize handles according to the shape size and position.
		"""
		s = self.handleSize
		b = self.boundingRect()
		self.handles[self.handleTopLeft] = QRectF(b.left(), b.top(), s, s)
		self.handles[self.handleTopMiddle] = QRectF(b.center().x() - s / 2, b.top(), s, s)
		self.handles[self.handleTopRight] = QRectF(b.right() - s, b.top(), s, s)
		self.handles[self.handleMiddleLeft] = QRectF(b.left(), b.center().y() - s / 2, s, s)
		self.handles[self.handleMiddleRight] = QRectF(b.right() - s, b.center().y() - s / 2, s, s)
		self.handles[self.handleBottomLeft] = QRectF(b.left(), b.bottom() - s, s, s)
		self.handles[self.handleBottomMiddle] = QRectF(b.center().x() - s / 2, b.bottom() - s, s, s)
		self.handles[self.handleBottomRight] = QRectF(b.right() - s, b.bottom() - s, s, s)

		for handle, rect in self.handles.items():
			self.circles[handle-1].setPos(rect.x()+rect.width()/2, rect.y()+rect.height()/2)

		if self.textItem:
			self.textItem.setPos(QPointF(b.x(), b.y() - 20))

		if self.mainWin and self.mainWin.action_continuous_collect.isChecked():
			self.mainWin.lineEdit_collect_roi_width.setText(str(int(self.rect().width())))
			self.mainWin.lineEdit_collect_roi_height.setText(str(int(self.rect().height())))
		if self.mainWin and self.mainWin.action_continuous_scan.isChecked():
			self.mainWin.lineEdit_scan_roi_width.setText(str(int(self.rect().width())))
			self.mainWin.lineEdit_scan_roi_height.setText(str(int(self.rect().height())))

	def interactiveResize(self, mousePos):
		"""
		Perform shape interactive resize.
		"""
		offset = self.handleSize + self.handleSpace
		boundingRect = self.boundingRect()
		rect = self.rect()
		diff = QPointF(0, 0)

		self.prepareGeometryChange()

		if self.handleSelected == self.handleTopLeft:

			fromX = self.mousePressRect.left()
			fromY = self.mousePressRect.top()
			toX = fromX + mousePos.x() - self.mousePressPos.x()
			toY = fromY + mousePos.y() - self.mousePressPos.y()
			diff.setX(toX - fromX)
			diff.setY(toY - fromY)
			boundingRect.setLeft(toX)
			boundingRect.setTop(toY)
			rect.setLeft(boundingRect.left() + offset)
			rect.setTop(boundingRect.top() + offset)
			if rect.width()>=Config.min_width_of_box and rect.height()>=Config.min_height_of_box:
				self.setRect(rect)

		elif self.handleSelected == self.handleTopMiddle:

			fromY = self.mousePressRect.top()
			toY = fromY + mousePos.y() - self.mousePressPos.y()
			diff.setY(toY - fromY)
			boundingRect.setTop(toY)
			rect.setTop(boundingRect.top() + offset)
			if rect.width() >= Config.min_width_of_box and rect.height() >= Config.min_height_of_box:
				self.setRect(rect)

		elif self.handleSelected == self.handleTopRight:

			fromX = self.mousePressRect.right()
			fromY = self.mousePressRect.top()
			toX = fromX + mousePos.x() - self.mousePressPos.x()
			toY = fromY + mousePos.y() - self.mousePressPos.y()
			diff.setX(toX - fromX)
			diff.setY(toY - fromY)
			boundingRect.setRight(toX)
			boundingRect.setTop(toY)
			rect.setRight(boundingRect.right() - offset)
			rect.setTop(boundingRect.top() + offset)
			if rect.width() >= Config.min_width_of_box and rect.height() >= Config.min_height_of_box:
				self.setRect(rect)

		elif self.handleSelected == self.handleMiddleLeft:

			fromX = self.mousePressRect.left()
			toX = fromX + mousePos.x() - self.mousePressPos.x()
			diff.setX(toX - fromX)
			boundingRect.setLeft(toX)
			rect.setLeft(boundingRect.left() + offset)
			if rect.width() >= Config.min_width_of_box and rect.height() >= Config.min_height_of_box:
				self.setRect(rect)

		elif self.handleSelected == self.handleMiddleRight:

			fromX = self.mousePressRect.right()
			toX = fromX + mousePos.x() - self.mousePressPos.x()
			diff.setX(toX - fromX)
			boundingRect.setRight(toX)
			rect.setRight(boundingRect.right() - offset)
			if rect.width() >= Config.min_width_of_box and rect.height() >= Config.min_height_of_box:
				self.setRect(rect)

		elif self.handleSelected == self.handleBottomLeft:

			fromX = self.mousePressRect.left()
			fromY = self.mousePressRect.bottom()
			toX = fromX + mousePos.x() - self.mousePressPos.x()
			toY = fromY + mousePos.y() - self.mousePressPos.y()
			diff.setX(toX - fromX)
			diff.setY(toY - fromY)
			boundingRect.setLeft(toX)
			boundingRect.setBottom(toY)
			rect.setLeft(boundingRect.left() + offset)
			rect.setBottom(boundingRect.bottom() - offset)
			if rect.width() >= Config.min_width_of_box and rect.height() >= Config.min_height_of_box:
				self.setRect(rect)

		elif self.handleSelected == self.handleBottomMiddle:

			fromY = self.mousePressRect.bottom()
			toY = fromY + mousePos.y() - self.mousePressPos.y()
			diff.setY(toY - fromY)
			boundingRect.setBottom(toY)
			rect.setBottom(boundingRect.bottom() - offset)
			if rect.width() >= Config.min_width_of_box and rect.height() >= Config.min_height_of_box:
				self.setRect(rect)

		elif self.handleSelected == self.handleBottomRight:

			fromX = self.mousePressRect.right()
			fromY = self.mousePressRect.bottom()
			toX = fromX + mousePos.x() - self.mousePressPos.x()
			toY = fromY + mousePos.y() - self.mousePressPos.y()
			diff.setX(toX - fromX)
			diff.setY(toY - fromY)
			boundingRect.setRight(toX)
			boundingRect.setBottom(toY)
			rect.setRight(boundingRect.right() - offset)
			rect.setBottom(boundingRect.bottom() - offset)
			if rect.width() >= Config.min_width_of_box and rect.height() >= Config.min_height_of_box:
				self.setRect(rect)

		self.updateHandlesPos()