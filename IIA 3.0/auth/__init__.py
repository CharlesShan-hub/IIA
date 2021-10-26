import storage
import logger

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr 
import random

__all__ = [
	'add_user', #添加用户
	'config_user', #获取全部用户信息
	'config_user', #查改用户信息
	'check_password',#验证用户名与密码匹配 
	'generate_validation_code',#生成验证码
	'check_validation_code',#检查验证码
	'send_find_password',#发送找回密码邮件
	]

""" 初始化
"""

LOG_MODULE = 'Auth'
CODE = [] #验证码

# 构建用户信息仓库
if storage.exist_repository("Auth")==False:
	storage.creat_repository(name='Auth',user_id='System')
	con_table = '''CREATE TABLE AUTH (MAIL TEXT PRIMARY KEY NOT NULL, PASSWORD TEXT, NAME TEXT)'''
	storage.add_info(name='Auth',con=con_table)

""" API
"""
def add_user(mail,password,**kwg):
	''' 添加成员
	*没有写邮箱(ID)重复的情况
	'''
	name=kwg['name']
	if mail=='System': 
		logger.warning("Fail to add user(Auth Not Valid)",LOG_MODULE)
		return False
	con = 'INSERT INTO AUTH (MAIL,PASSWORD,NAME) VALUES (\''+mail+'\',\''+password+'\',\''+name+'\')'
	try:
		storage.add_info(name='Auth',con=con)
		logger.info("Sucessed to add user",LOG_MODULE)
		return True
	except:
		logger.warning("Fail to add user",LOG_MODULE)
		return False

def config_user():
	''' 查改成员信息
	*没有添加各种容错
	'''
	logger.info("Getting all user info!",LOG_MODULE)
	con = '''SELECT mail,password,name from AUTH'''
	info=storage.add_info(name='Auth',con=con)
	return info

def check_password(mail,password):
	''' 验证邮箱与密码
	'''
	logger.info("Start check mail ~ password",LOG_MODULE)
	con = "SELECT mail,password from AUTH where mail=\'"+mail+"\'"
	info=storage.add_info(name='Auth',con=con)
	if info==[]:return False
	return info[0][1]==password


def generate_validation_code(mail):
	''' 生成验证码
	'''
	logger.info("Generate validation code",LOG_MODULE)
	code = str(random.randint(100000,999999))
	CODE.append([mail,code])
	return code


def check_validation_code(mail,code):
	''' 检测验证码
	'''
	logger.info("Check validation code",LOG_MODULE)
	if [mail,code] in CODE:
		CODE.clear()
		return True
	return False


def send_find_password(mail,code):
	''' 发送找回密码验证码
	'''
	logger.info("Constructing mail",LOG_MODULE)
	with open("./auth/resources/mail.html") as f:
		word = f.read()
		word=word.replace("IIA-Flag-Code",code)
		word=word.replace("IIA-Flag-Content","【IIA】您正在使用找回密码功能, 验证码可能导致IIA账号被盗, 请勿转发或泄漏。")
	sent_message(mail,word)


def send_check_mail(mail,code):
	''' 发送验证邮箱验证码
	'''
	logger.info("Constructing mail",LOG_MODULE)
	with open("./auth/resources/mail.html") as f:
		word = f.read()
		word=word.replace("IIA-Flag-Code",code)
		word=word.replace("IIA-Flag-Content","【IIA】您正在注册成为新用户，感谢您的支持！")
	sent_message(mail,word)


def sent_message(mail,word):
    ''' sent email 发邮件
    :params mail: Return address 收信人地址
    :params word: Content sent 发送的内容
    '''
    def sentmail():
        ret=True
        try:
        	msg = MIMEMultipart()
        	html_att = MIMEText(word, 'html', 'utf-8')
	        att=MIMEText(word,'plain','utf-8')
	        msg.attach(html_att)
	        msg.attach(att)
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
    
    my_sender='inforassistant@foxmail.com'    # 发件人邮箱账号
    my_pass = 'bzglhuaizeogdahj'     # 发件人邮箱密码
    my_user=mail                     # 收件人邮箱账号
    if sentmail():print("邮件发送成功")
    else: print("邮件发送失败") 


