# Tkinter是Python的标准GUI(图形用户界面)库 ，Python使用Tkinter可以快速的创建GUI应用程序
import random
from tkinter import *
from tkinter import messagebox


def closeWindow():
    messagebox.showinfo(title="警告", message="不许关闭，好好回答")
    # messagebox.showerror(title="警告",message="不许关闭，好好回答")
    return


# 点击喜欢触发的方法
def Love():
    # 顶级窗口
    love = Toplevel(window)
    love.geometry("300x100+520+260")
    love.title("结工资")
    label = Label(love, text="不结工资等仲裁吧!", font=("微软雅黑", 20))
    label.pack()
    btn = Button(love, text="同意发钱", width=10, height=2, command=closeAllWindow)
    btn.pack()
    love.protocol("WM_DELETE_WINDOW", closeLove)


def closeLove():
    return


# 关闭所有的窗口
def closeAllWindow():
    # destroy  销毁
    window.destroy()


def noLove():
    no_love = Toplevel(window)
    no_love.geometry("300x100+520+260")
    no_love.title("再考虑考虑")
    label = Label(no_love, text="再考虑考虑呗", font=("微软雅黑", 25))
    label.pack()
    btn = Button(no_love, text="好的", width=10, height=2, command=no_love.destroy)
    btn.pack()
    no_love.protocol("WM_DELETE_WINDOW", closeNoLove)


def closeNoLove():
    noLove()


# 创建父级窗口
window = Tk()  # Tk 是一个类
# 窗口标题
window.title("江湖再见")
# 窗口大小
window.geometry('500x500')
# 窗口位置   geometry:几何
window.geometry('+500+200')

# protocol()  用户关闭窗口触发的事件
window.protocol("WM_DELETE_WINDOW", closeWindow)

# 标签控件
label = Label(window, text="狗贼资本家", font=("微软雅黑", 15), fg='red')
# 定位   网格式布局   pack也可以
label.grid(row=0, column=0, sticky=W)

label1 = Label(window, text="老子要辞职", font=("微软雅黑", 30))
# sticky 对齐方式   E W S N 东西南北
label1.grid(row=1, column=1, sticky=E)

# 显示图片
photo = PhotoImage(file="123.png")
imageLable = Label(window, image=photo)
# columnspan 组件所跨越的列数
imageLable.grid(row=2, columnspan=2)

# 按钮控件
# command 按钮点击触发的事件
btn = Button(window, text="同意", width=15, height=2, command=Love)
btn.grid(row=3, column=0, sticky=W)

btn1 = Button(window, text="不同意", command=noLove)
btn1.grid(row=3, column=1, sticky=E)


def change(event):
    # 为了防止窗口随机移动超出屏幕范围，留出随机移动的边距
    width = window.winfo_screenwidth() - 500
    height = window.winfo_screenheight() - 500
    # 用random.choice实现随机移动
    window.geometry("500x500+{}+{}".format(random.choice(range(0, width)), random.choice(range(0, height))))
    # 改变标签内容
    # text_var.set('不同意，想都别想')


def quit(event):  # 快捷键退出
    window.destroy()


def yes():
    messagebox.showinfo('', '江湖再见')
    # 你还可以做一些其他的事情，比如运用cmd命令关机等等


btn1.bind('<Enter>', change)
window.bind_all('<Alt-o>', quit)
# 显示窗口，也叫消息循环
window.mainloop()
# input("please input any key to exit!")