import sys
import matplotlib
import pandas as pd

matplotlib.use('Qt5Agg')

from PyQt5 import QtCore, QtGui, QtWidgets

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure


class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        sc = MplCanvas(self, width=5, height=4, dpi=100)
        date_list, gdp_list = self.load_data('C0301.xls', [0, 3])
        # 绘制人均GDP柱状图
        y_axis_value_list = gdp_list  # 每年人均GDP数值列表
        color = '#FF4500'  # 柱子颜色
        tick_label = date_list  # X轴坐标 每个坐标的字段
        label_name = 'num'  # 图例名称
        label = {  # X轴 和 Y轴 代表的含义
            'x': 'years',
            'y': 'GDP per capita'
        }
        title = 'GDP per capita from 1978 to 2018'
        index = len(tick_label)
        print(dir(sc.axes))# 需要创建多少个 X轴坐标
        sc.axes.bar(range(index), y_axis_value_list, color=color, tick_label=tick_label, label=label_name)
        # sc.axes.set_xticklabels(fontsize=10)
        # sc.axes.set_yticklabels(fontsize=10)
        # 设置横轴标签
        sc.axes.set_xlabel(label['x'])
        # 设置纵轴标签
        sc.axes.set_ylabel(label['y'])
        # 添加标题
        sc.axes.set_title(title)
        for a, b in zip(range(index), y_axis_value_list):
            sc.axes.text(a, b + 0.4, '%.0f' % b, ha='center', va='bottom', fontsize=7)
        # 添加图例
        sc.axes.legend(loc="upper right")

        # Create toolbar, passing canvas as first parament, parent (self, the MainWindow) as second.
        toolbar = NavigationToolbar(sc, self)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(toolbar)
        layout.addWidget(sc)

        # Create a placeholder widget to hold our toolbar and canvas.
        widget = QtWidgets.QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        self.show()

    @staticmethod
    # 加载数据
    def load_data(file_path, aims_column):
        # 读取数据
        fr = pd.read_excel(file_path, usecols=aims_column, index_col=False, header=None)
        res_list = []
        for index in aims_column:
            res_list.append(fr[index].values)
        return res_list


app = QtWidgets.QApplication(sys.argv)
w = MainWindow()
app.exec_()