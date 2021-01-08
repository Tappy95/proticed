from tkinter import *
import psutil
import time


def make_gui():
    app = Tk()  # 创建窗口
    app.geometry('300x150')  # 设置窗口大小
    app.config(bg='#303030')  # 设置窗口颜色为灰色
    # 设置第一行显示的内容为“Speed Monitor”,字体为hack，字号25,加粗
    Label(text='Speed Monitor', font=('Hack', 25, 'bold'), bg='#303030', fg='white').pack()
    # 设置第二行显示的内容为"_kb/s",字体为hack，字号为25，加粗
    Label(name='lb2', text='_kb/s', font=('Hack', 20, 'bold'), bg='#303030', fg='white').pack()
    return app


def ui_update(do, app):
    # 获取网卡接口，Linux下为 en0,win下可以使用"WLAN","本地连接"等等
    data = do()
    lb2 = app.children['lb2']
    lb2.config(text=data+'kb/s')
    app.after(1000, lambda: ui_update(do, app))


def do():
    s1 = psutil.net_io_counters(pernic=True)['以太网']
    time.sleep(1)  # 设置睡1秒，防止出现过快获取不到下一次网络速度的问题
    s2 = psutil.net_io_counters(pernic=True)['以太网']
    result = s2.bytes_recv - s1.bytes_recv  # 将两次获得的下载速度相减
    print("此时获得的网速为：" + str(result / 1024) + ' kb/s')  # 注：在测试时打印出来，之后再删掉
    return str(round(result / 1024, 2))  # 将返回的字符串进行拼接


if __name__ == "__main__":  # 当模块被直接运行时，以下代码块将被运行
    app = make_gui()  # 构造一个图形化界面窗口
    app.after(1000, lambda: ui_update(do, app))  # 在1秒钟之后执行（传入网络测速这个动作）
    app.mainloop()  # 将事件循环下去
