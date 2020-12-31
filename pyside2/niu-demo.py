from tkinter import *
import tkinter.messagebox as msx

top = Tk()

top.title("注册界面")
top.geometry('300x150')

username_L = Frame(top)
username_L.pack()
userlabel = Label(username_L, text="用户名", width=10)
userlabel.pack(side=LEFT)
Expression1 = Entry(username_L, width=10, bd=4)
Expression1.pack(side=LEFT)

password_L = Frame(top)
password_L.pack()
passlabel = Label(password_L, text="密码", width=10)
passlabel.pack(side=LEFT)
Expression2 = Entry(password_L, width=10, bd=4, show='*')
Expression2.pack(side=LEFT)

mailbox_L = Frame(top)
mailbox_L.pack()
maillabel = Label(mailbox_L, text="邮箱", width=10)
maillabel.pack(side=LEFT)
Expression3 = Entry(mailbox_L, width=10, bd=4)
Expression3.pack(side=LEFT)

mobilenumber_L = Frame(top)
mobilenumber_L.pack()
mobilelabel = Label(mobilenumber_L, text="手机号", width=10)
mobilelabel.pack(side=LEFT)
Expression4 = Entry(mobilenumber_L, width=10, bd=4)
Expression4.pack(side=LEFT)

statuslabel = Label(top, text='')
statuslabel.pack()

users = {}


def submit():
    input1 = Expression1.get()
    input2 = Expression2.get()
    input3 = Expression3.get()
    input4 = Expression4.get()

    if input1 in users:
        msx.showinfo("提示", "该用户名已存在，请换一个名字")
    else:
        if input1 == '' or input2 == '' or input3 == '' or input4 == '':
            statuslabel.config(text='有项目未填写！ ', bg='red')
            top.mainloop()
            return
        else:
            statuslabel.config(text='', bg=top.cget('bg'))

            users[input1] = [input2, input3, input4]
            print("新注册了一个用户:")
            print("用户名是", input1)
            print("密码是", input2)
            print("邮箱是", input3)
            print("电话号码是", input4)
            print("users=", users)

    Expression1.delete(0, END)
    Expression2.delete(0, END)
    Expression3.delete(0, END)
    Expression4.delete(0, END)
    top.mainloop()


Button1 = Button(top, text="提交", command=submit)
Button1.pack()

top.mainloop()