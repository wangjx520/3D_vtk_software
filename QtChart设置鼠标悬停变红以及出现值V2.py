# -*- coding: utf-8 -*-
"""
Created on Sun Oct 29 20:50:25 2023
@author: WJX
"""

import sys
from PyQt5.QtWidgets import QApplication, QGraphicsRectItem  , QSplitter,QMainWindow,QFrame,QHBoxLayout
from PyQt5.QtChart import QChart, QChartView, QBarSet, QBarSeries
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QBrush, QColor, QCursor, QFont
from PyQt5.Qt import Qt as QtEnum
from PyQt5.QtGui import QPen
from PyQt5.QtWidgets import QGraphicsSimpleTextItem

app = QApplication(sys.argv)  # 创建一个应用程序实例

# 创建第一个 QChartView 窗口
chart_view = QChartView()

# 创建一个 QBarSet 对象，用于存储柱状图的数据
set0 = QBarSet("bar1")
set0 << 1 << 4 << 3 << 7 << 2 << 5 << 1 << 3 << 3 << 2
set1 = QBarSet("bar2")
set1 << 1 << 10 << 3 << 7 << 5 << 5 << 5 << 3 << 3 << 2

# 创建第一个 QBarSeries 对象，并将 QBarSet 添加到其中
series = QBarSeries()
series.append(set0)
series.append(set1)

# 创建第一个 QChart 对象，将第一个 QBarSeries 添加到其中
chart = chart_view.chart()
chart.addSeries(series)

# 设置第一个图表的标题
chart.setTitle("First horizontal barchart example")

# 设置图表的背景颜色为透明
background_brush = QBrush(QColor(0, 0, 0, 0))
chart.setBackgroundBrush(background_brush)

# 启用动画效果
chart.setAnimationOptions(QChart.SeriesAnimations)

# 显示图例并设置位置
chart.legend().setVisible(True)
chart.legend().setAlignment(Qt.AlignBottom)

# 创建第一个红色的矩形框
transparent_pen = QPen(QtEnum.NoPen)
hover_item = QGraphicsRectItem()
hover_item.setBrush(QBrush(QColor("red")))
hover_item.setPen(transparent_pen)

# 定义第一个悬停事件处理函数
def on_hover(status, index, chart):
    chart = chart_view
    if status:
        p = chart_view.mapFromGlobal(QCursor.pos())
        it = chart_view.itemAt(p)
        print('p', p)
        print('it.pos', it.boundingRect().x())
        print('b;', it.brush().color() == set0.color())
        print('b1;', it.brush().color() == set1.color())
        print(it)
        if it:
            hover_item.setParentItem(it)
            hover_item.setRect(it.boundingRect())
            hover_item.show()
            item_width = it.boundingRect().width()
            if it.brush().color() == set0.color():
                value = set0.at(index)
            else:
                value = set1.at(index)
            font = QFont()
            font.setPointSize(12)
            font.setPointSize(int(item_width / 2))
            value_text = f"Value: {value:.2f}"
            label = chart_view.scene().addSimpleText(value_text)
            label.setFont(font)
            label.setBrush(QBrush(QColor("red")))
            x = it.boundingRect().x()
            y = it.boundingRect().y()
            print('宽度', it.boundingRect().width())
            label.setPos(p.x() + 10, p.y() - 20)
            print('x, y', x, y)
            label.setPos(x + 10, y - 20)
            label.setPos(x + it.boundingRect().width() * 2 + 10, p.y() - 20)
    else:
        hover_item.setParentItem(None)
        hover_item.hide()
        for item in chart_view.scene().items():
            if isinstance(item, QGraphicsSimpleTextItem):
                chart_view.scene().removeItem(item)

# 连接第一个 QBarSet 的 hovered 信号到第一个悬停事件处理函数
#series.hovered.connect(on_hover)
series.hovered.connect(lambda status, index, chart=chart_view: on_hover(status, index, chart))

# 创建第二个 QChartView 窗口
chart_view2 = QChartView()

# 创建第二个 QBarSet 对象，用于存储第二个画布的数据
set2 = QBarSet("bar3")
set2 << 1 << 2 << 1 << 4 << 6 << 3 << 2 << 1 << 2 << 1
set3 = QBarSet("bar4")
set3 << 2 << 3 << 4 << 1 << 2 << 3 << 2 << 5 << 2 << 1

# 创建第二个 QBarSeries 对象，并将第二个 QBarSet 添加到其中
series2 = QBarSeries()
series2.append(set2)
series2.append(set3)

# 创建第二个 QChart 对象，将第二个 QBarSeries 添加到其中
chart2 = chart_view2.chart()
chart2.addSeries(series2)

# 设置第二个图表的标题
chart2.setTitle("Second horizontal barchart example")

# 设置图表的背景颜色为透明
chart2.setBackgroundBrush(background_brush)

# 启用动画效果
chart2.setAnimationOptions(QChart.SeriesAnimations)

# 显示图例并设置位置
chart2.legend().setVisible(True)
chart2.legend().setAlignment(Qt.AlignBottom)

# 创建第二个红色的矩形框
hover_item2 = QGraphicsRectItem()
hover_item2.setBrush(QBrush(QColor("red")))
hover_item2.setPen(transparent_pen)

# 定义第二个悬停事件处理函数
def on_hover2(status, index, chart):
    chart = chart_view2
    if status:
        p = chart_view2.mapFromGlobal(QCursor.pos())
        it = chart_view2.itemAt(p)
        print('p', p)
        print('it.pos', it.boundingRect().x())
        print('b;', it.brush().color() == set2.color())
        print('b1;', it.brush().color() == set3.color())
        print(it)
        if it:
            hover_item2.setParentItem(it)
            hover_item2.setRect(it.boundingRect())
            hover_item2.show()
            item_width = it.boundingRect().width()
            if it.brush().color() == set2.color():
                value = set2.at(index)
            else:
                value = set3.at(index)
            font = QFont()
            font.setPointSize(12)
            font.setPointSize(int(item_width / 2))
            value_text = f"Value: {value:.2f}"
            label = chart_view2.scene().addSimpleText(value_text)
            label.setFont(font)
            label.setBrush(QBrush(QColor("red")))
            x = it.boundingRect().x()
            y = it.boundingRect().y()
            print('宽度', it.boundingRect().width())
            label.setPos(p.x() + 10, p.y() - 20)
            print('x, y', x, y)
            label.setPos(x + 10, y - 20)
            label.setPos(x + it.boundingRect().width() * 2 + 10, p.y() - 20)
    else:
        hover_item2.setParentItem(None)
        hover_item2.hide()
        for item in chart_view2.scene().items():
            if isinstance(item, QGraphicsSimpleTextItem):
                chart_view2.scene().removeItem(item)

# 连接第二个 QBarSet 的 hovered 信号到第二个悬停事件处理函数
#series2.hovered.connect(on_hover2)
series2.hovered.connect(lambda status, index, chart=chart_view2: on_hover2(status, index, chart))

# 显示窗口
chart_view.show()
chart_view2.show()

main_window = QMainWindow()
main_window.setGeometry(100, 100, 800, 600)
main_window.setWindowTitle("Bar Chart Example")
splitter = QSplitter(main_window)

frame1=QFrame()
frame2=QFrame()
layout1=QHBoxLayout(frame1)
layout2=QHBoxLayout(frame2)

layout1.addWidget(chart_view)
layout2.addWidget(chart_view2)
splitter.addWidget(frame1)
splitter.addWidget(frame2)
# splitter.addWidget(chart_view)
# splitter.addWidget(chart_view2)
main_window.setCentralWidget(splitter)
main_window.show()
# 启动应用程序事件循环
sys.exit(app.exec_())
