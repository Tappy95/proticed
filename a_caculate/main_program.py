import pandas as pd
from tkinter import *
import matplotlib.pyplot as plt


# 加载数据
def load_data(file_path, aims_column):
    # 读取数据
    fr = pd.read_excel(file_path, usecols=aims_column, index_col=False, header=None)
    res_list = []
    for index in aims_column:
        res_list.append(fr[index].values)
    return res_list


# 绘制柱状图
def draw_histogram(figsize, y_axis_value_list, color, tick_label, label, title, label_name):
    plt.figure(figsize=figsize, dpi=80)
    index = len(tick_label)  # 需要创建多少个 X轴坐标
    plt.bar(range(index), y_axis_value_list, width=0.8, color=color, tick_label=tick_label, label=label_name, align='center')
    # 设置x轴的刻度，将构建的tick_label代入, 由于年份较多，在一块会比较拥挤和重叠，因此设置字体和对齐方式
    plt.xticks(range(index), tick_label, size='small', rotation=30)
    # 设置横轴标签
    plt.xlabel(label['x'])
    # 设置纵轴标签
    plt.ylabel(label['y'])
    # 添加标题
    plt.title(title)
    # 设置数字标签
    for a, b in zip(range(index), y_axis_value_list):
        plt.text(a, b + 0.4, '%.0f' % b, ha='center', va='bottom', fontsize=9)
    # 添加图例
    plt.legend(loc="upper right")
    # 展示
    plt.show()


def CallOn(event):
    root1 = Tk()
    Label(root1, text='你的选择是' + listbox.get(listbox.curselection()) + "年").pack()
    Button(root1, text='退出', command=root1.destroy).pack()


if __name__ == '__main__':
    # 加载绘制人均GDP柱状图所需数据
    date_list, gdp_list = load_data('C0301.xls', [0, 3])
    # 绘制人均GDP柱状图
    figsize = (18, 10)  # 创建大小为 18 x 10 的画布
    y_axis_value_list = gdp_list  # 每年人均GDP数值列表
    color = '#FF4500'  # 柱子颜色
    tick_label = date_list  # X轴坐标 每个坐标的字段
    label_name = 'num'  # 图例名称
    label = {  # X轴 和 Y轴 代表的含义
        'x': 'years',
        'y': 'GDP per capita'
    }
    title = 'GDP per capita from 1978 to 2018'
    draw_histogram(figsize, y_axis_value_list, color, tick_label, label, title, label_name)

    # 加载绘制工业污染治理完成投资柱状图所需数据
    date_list, investment_list = load_data('C0837.xls', [0, 1])
    # 绘制工业污染治理完成投资柱状图
    figsize = (10, 10)  # 创建大小为 10 x 10 的画布
    y_axis_value_list = investment_list  # 每年工业污染治理投资数值列表
    color = '#87CEFA'  # 柱子颜色
    tick_label = date_list  # X轴坐标 每个坐标的字段
    label_name = 'num'  # 图例名称
    label = {  # X轴 和 Y轴 代表的含义
        'x': 'years',
        'y': 'Complete the investment'
    }
    title = 'Industrial pollution control investment from 2000 to 2017'
    draw_histogram(figsize, y_axis_value_list, color, tick_label, label, title, label_name)

    # 绘制 人均GDP 和 工业治理投资 相关散点图(2005-2017)
    plt.figure(figsize=(10, 10), dpi=100)
    plt.grid(c='#DDA0DD', axis='y')  # 为画布添加网格线
    GDP_list = gdp_list[27:-1]
    governance_investment_list = investment_list
    plt.scatter(GDP_list, governance_investment_list, s=200, c='r', marker='.', alpha=1, label="none")
    plt.xlabel('GDP per capita')
    plt.ylabel('industrial governance investment')
    plt.title('2005-2017 GDP per capita and industrial governance investment')
    plt.legend(loc='upper right')
    plt.show()

    # GUI 交互部分
    top = Tk()
    # top.geometry('600x300')
    label = Label(top, text='')
    listbox = Listbox(top)
    # 双击命令
    listbox.bind('<Double-Button-1>', CallOn)
    listbox.insert(END, '双击下列年份即可查看详细治理投资')
    for i in range(2010, 2018):
        listbox.insert(END, str(i))

    listbox.pack()
    mainloop()