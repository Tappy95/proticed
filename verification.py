import smtplib
from email.mime.text import MIMEText
from email.header import Header
import random


def generate_verification_code(len=4):
    ''' 随机生成6位的验证码 '''
    # 注意： 这里我们生成的是0-9A-Za-z的列表，当然你也可以指定这个list，这里很灵活
    # 比如： code_list = ['P','y','t','h','o','n','T','a','b'] # PythonTab的字母
    code_list = []
    for i in range(10):  # 0-9数字
        code_list.append(str(i))
    for i in range(65, 91):  # 对应从“A”到“Z”的ASCII码
        code_list.append(chr(i))
    for i in range(97, 123):  # 对应从“a”到“z”的ASCII码
        code_list.append(chr(i))
    myslice = random.sample(code_list, len)  # 从list中随机获取6个元素，作为一个片断返回
    verification_code = ''.join(myslice)  # list to string
    return verification_code


def Verification(useremail):
    # 获取smtp对象
    smtp = smtplib.SMTP()
    # 连接邮件服务器
    smtp.connect(host="smtp.qq.com")
    f_user = "wyhui0419@foxmail.com"
    # 登陆邮箱，密码指的是邮件的登陆密码/授权码(部分邮件运行商只支持授权码，例如QQ)
    smtp.login(f_user, "kheyplxzecipeaha")
    # 准备开始进行邮件发送的 准备工作
    """
        content:邮件的正文
        subtype:默认是plain, 代表内容是一个字符串
                html ：支持html网页格式
        charset: 设置发送邮件的字符集编码格式，常用UTF-8
    """
    code = generate_verification_code()

    message = MIMEText(f"您正在密码找回验证，验证码{code}，切勿将验证码泄露与他人。", "plain","utf-8")
    # 设置发件人
    message["From"] = Header("【BLT大数据】", charset="utf-8")
    # 设置收件人，是一个列表或者元组
    message["To"] = Header(useremail, charset="utf-8")

    # 设置邮件标题
    message["Subject"] = Header("【BLT大数据注册验证码】", charset="utf-8")
    # 发送邮件
    smtp.sendmail(f_user, useremail, message.as_string())
    return code


if __name__ == "__main__":
    user_email = "495088732@qq.com"
    code = Verification(user_email)
