import storage

import random
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr 

CODE = []

def _password_valid(password):
	''' 密码合法判断
	'''
	return True

def login(mail,password):
	''' 登陆判断
	'''
	print(storage.configure_user(mail,'password'))
	if(password==storage.configure_user(mail,'password')):
		return 100
	else:
		return 403

def regist(mail,password,name):
	''' 增加用户
	'''
	if _password_valid(password)==False:
		return 403
	# 写入用户名与密码
	if storage.add_user(mail,password,name=name) == True:
		return 100
	else:
		return 403

def find_password(mail,code):
	''' 找回密码
	'''
	# 请求找回密码
	if code=="request":
		code_ = random.randint(100000,999999)
		CODE.append([mail,str(code_)])
		sent_message(mail,"【IIA】验证码："+str(code_)+
			"您正在使用找回密码功能, 验证码可能导致IIA账号被盗, 请勿转发或泄漏。")
		return 200
	# 收到验证码
	if [mail,code] in CODE:
		return 100
	else:
		print(CODE)
		return 403

def change_password(mail,password):
	''' 修改密码
	'''
	pass

def sent_message(mail,word):
    ''' sent email 发邮件
    :params mail: Return address 收信人地址
    :params word: Content sent 发送的内容
    '''
    def sentmail():
        ret=True
        try:
	        msg=MIMEText(word,'plain','utf-8')
	        msg['From']=formataddr(["FromRunoob",my_sender])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
	        msg['To']=formataddr(["FK",my_user])              # 括号里的对应收件人邮箱昵称、收件人邮箱账号
	        msg['Subject']="IIA 验证码"                        # 邮件的主题，也可以说是标题
	    
	        server=smtplib.SMTP_SSL("smtp.qq.com", 465)  # 发件人邮箱中的SMTP服务器，端口是25
	        server.login(my_sender, my_pass)  # 括号中对应的是发件人邮箱账号、邮箱密码
	        server.sendmail(my_sender,[my_user,],msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
	        server.quit()  # 关闭连接
        except:  # 如果 try 中的语句没有执行，则会执行下面的 ret=False
        	ret=False
        return ret
    
    my_sender='1742861545@qq.com'    # 发件人邮箱账号
    my_pass = 'ulkgmlgsqbzwhhae'     # 发件人邮箱密码
    my_user=mail                     # 收件人邮箱账号
    if sentmail():print("邮件发送成功")
    else: print("邮件发送失败") 

