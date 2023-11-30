import sys
import math
from PyQt5.QtWidgets import QApplication, QMainWindow, QGraphicsScene, QGraphicsView,\
	 QGraphicsEllipseItem,QPushButton, QGraphicsRectItem,QGraphicsItem,QLabel, QGraphicsLineItem, QGraphicsTextItem
from PyQt5.QtCore import Qt,QPointF, QRectF
from PyQt5.QtGui import QBrush, QColor, QFont, QPainter, QPen, QPixmap,QPainterPath,QPolygonF,QIcon, QImage

		
class ScatterPlot(QMainWindow):
	def __init__(self):
		super().__init__()
		 #QGraphicsView用于显示QGraphicsScene中的图形元素，可以在QGraphicsScene中添加、删除管理图形项，然后view渲染
		self.view = QGraphicsView(self)
		self.setCentralWidget(self.view)

		self.scene = QGraphicsScene(self) #创建场景，并将主窗口设置为父对象
		self.view.setScene(self.scene) #将scene设置为view的场景，将视图与场景连接起来，在视图中显示场景中的图形项
		
		self.view.setSceneRect(0, 0, 800, 600) #设置了视图的场景矩形

		
		self.reset_button=QPushButton('重置视图',self) 
		# 设置按钮的位置
		self.reset_button.setGeometry(self.width() - 100, 10, 90, 30)

		  # 设置按钮点击事件处理函数
		self.reset_button.clicked.connect(self.reset_view)


		# 创建不规则分布的散点和名称
		scatter_points = [(50, 50), (100, 100), (150, 150), (200, 200), (250, 250),
						  (300, 300), (350, 350), (400, 400), (450, 450), (500, 500),
						  (600, 600), (700, 700), (800, 800), (900, 900), (1000, 1000)]
		
		scatter_buttons_pos=[(100,120),(130,80)]
		buttons_label_pos=[(85,100),(115,60)]
		buttons_label=['KC7505','KZ7909']

		point_names = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J",
					   "K", "L", "M", "N", "O"]

		self.button_items=[]
		for i,(x,y) in enumerate(scatter_buttons_pos):
			label=QLabel()
			label.setFont(QFont("微软雅黑"))
			label.setAlignment(Qt.AlignCenter) #alignment对齐
			label.setText(buttons_label[i])
			label.setGeometry(buttons_label_pos[i][0],buttons_label_pos[i][1],60,20)
			
			
			self.scene.addWidget(label)
			
			button=QPushButton()
			button.setGeometry(x,y,30,30) #按钮位置和大小
			button.setIcon(QIcon('icons/eye_off.ico'))
			button.setIconSize(button.rect().size())
			button.setFlat(True)
			button.setStyleSheet("background-color: transparent; border: none;")  # 设置按钮无背景色和边框
			button.clicked.connect(self.on_button_clicked)
			self.scene.addWidget(button)
			self.button_items.append(button)

		# 添加一个透明的矩形项，用于捕获鼠标事件并拖动场景
		self.drag_rect = QGraphicsRectItem(self.scene.sceneRect())
	
		self.drag_rect.setBrush(QBrush(Qt.NoBrush))
		self.drag_rect.setPen(QPen(Qt.NoPen))

		self.scene.addItem(self.drag_rect)
		self.setMouseTracking(True)
		#self.setInteractive(True)
		self.view.setInteractive(True)
		self.view.setDragMode(QGraphicsView.ScrollHandDrag)
		
		self.scatter_items = []

		for i, (x, y) in enumerate(scatter_points):
			scatter_item = QGraphicsEllipseItem(x - 5, y - 5, 10, 10) #左上角坐标，高和宽
			scatter_item.setBrush(QBrush(Qt.blue))
			scatter_item.setToolTip(point_names[i]) #该图形项的工具题是文本，悬停在图形项时显示
			self.scatter_items.append(scatter_item)
			self.scene.addItem(scatter_item)

		# 创建标记为星星的散点
		for i in range(10, 15):
			x, y = scatter_points[i]
			scatter_item = QGraphicsEllipseItem(x - 5, y - 5, 10, 10)
			scatter_item.setBrush(QBrush(QColor(255, 165, 0)))
			scatter_item.setToolTip(point_names[i])
			self.scatter_items.append(scatter_item)
			self.scene.addItem(scatter_item)


		self.view.setSceneRect(0, 0, 1050, 1050)

		self.view.setRenderHint(QPainter.Antialiasing)  # 抗锯齿渲染
		self.view.setRenderHint(QPainter.SmoothPixmapTransform)  # 平滑缩放
		self.view.setRenderHint(QPainter.HighQualityAntialiasing)  # 高质量抗锯齿
		self.view.setRenderHint(QPainter.TextAntialiasing)  # 文本抗锯齿

		# 连接视图的缩放事件处理函数
		self.view.wheelEvent = self.handle_zoom

		# 创建两个列表用于控制显示和透明度
		self.show_points_list = [1, 3, 5, 7, 9, 11, 13, 15]
		self.transparent_points_list = [0, 2, 4, 6, 8, 10, 12, 14]
 
		# 设置透明度
		for i in self.transparent_points_list:
			self.set_opacity(self.scatter_items[i], 0.5)
		
		# 设置 scene 的边界矩形以包含所有元素
		self.scene.setSceneRect(self.scene.itemsBoundingRect())

	  # 调整窗口大小以适应 scene 的边界矩形
		#self.view.setSceneRect(self.scene.sceneRect())
		# 设置 QGraphicsScene 的范围
		self.scene.setSceneRect(0, 0, 1500, 1200)

		# 获取窗口的大小
		window_width = self.width()
		window_height = self.height()

		# 计算比例因子
		scale_factor = min(window_width / 1500, window_height / 1200)

		# 缩放 QGraphicsScene
		self.view.setRenderHint(QPainter.Antialiasing)
		self.view.setRenderHint(QPainter.SmoothPixmapTransform)
		self.view.setRenderHint(QPainter.HighQualityAntialiasing)
		self.view.setRenderHint(QPainter.TextAntialiasing)
		#self.view.setSceneRect(0, 0, 1500 * scale_factor, 1200 * scale_factor)
		self.view.scale(scale_factor,scale_factor)


		# 自定义四边形的四个顶点坐标
		top_left = QPointF(100, 100)
		top_right = QPointF(400, 100)
		bottom_right = QPointF(400, 300)
		bottom_left = QPointF(100, 300)

		polygon = QPolygonF([top_left, top_right, bottom_right, bottom_left])
		
		# 添加四边形
		background_item = self.scene.addPolygon(polygon)

		# 加载底图
		image = QImage("图片/C7_wells_distrubution.jpg")  # 替换为您的底图文件路径
		pixmap = QPixmap.fromImage(image)
		
		# 创建底图项并设置其坐标
		pixmap_item = self.scene.addPixmap(pixmap)
		pixmap_item.setPos(top_left)

		# 自适应填充四边形
		pixmap_item.setScale(min(polygon.boundingRect().width() / pixmap.width(), 
							   polygon.boundingRect().height() / pixmap.height()))


	def reset_view(self):
		#self.view.resetMatrix()
		self.scale_factor=1.0
		self.view.scale(2 , 2 )
		
	def on_button_clicked(self):
		button=self.sender()
		current_icon=button.icon()
		if current_icon.isNull() or current_icon.name()=='icons/eye_off.ico':
			button.setIcon(QIcon('icons/eye.ico'))


	def create_star_path(self):
		path = QPainterPath()
		path.moveTo(100, 20)

		for i in range(5):
			angle = 2 * math.pi * i / 5
			if i % 2 == 0:
				x = 100 + 50 * math.cos(angle)
				y = 100 + 50 * math.sin(angle)
			else:
				x = 100 + 25 * math.cos(angle)
				y = 100 + 25 * math.sin(angle)
			path.lineTo(x, y)

		path.closeSubpath()
		return path
	
	def set_marker_star(self, item):
		# 设置标记为星星的形状
		path = QPolygonF()
		for i in range(5):
			angle = 2 * math.pi * i / 5
			x = 50 * math.cos(angle)
			y = 50 * math.sin(angle)
			point = QPointF(self.width() / 2 + x, self.height() / 2 + y)
			path.append(point)

		item.setPolygon(path)

	def set_opacity(self, item, opacity):
		# 设置图形项的透明度
		brush = item.brush()
		color = brush.color()
		color.setAlphaF(opacity)
		brush.setColor(color)
		item.setBrush(brush)

	def handle_zoom(self, event):
		# 视图缩放事件处理函数
		delta = event.angleDelta().y()
		zoom_factor = 1.1

		if delta > 0:
			self.view.scale(zoom_factor, zoom_factor)
		else:
			self.view.scale(1 / zoom_factor, 1 / zoom_factor)
			

if __name__ == '__main__':
	app = QApplication(sys.argv)
	window = ScatterPlot()
	window.setGeometry(100, 100, 800, 800)
	window.show()
	sys.exit(app.exec_())
