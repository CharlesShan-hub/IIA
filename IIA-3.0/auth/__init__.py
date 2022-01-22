import storage
import logger

import random

__all__ = [
	# 构建表
	'add_user',                #添加用户
	'change_info',             #修改信息
	# 验证
	'check_password',          #验证用户名与密码匹配 
	'check_validation_code',   #检查验证码
	# 邮件
	'send_check_mail',         #发送验证邮箱验证码邮件
	'send_find_password',      #发送找回密码邮件
	'send_change_password',    #发送修改密码邮件
	# 服务
	'remember_user',           #记住账户(邮箱)
	# 测试
	'config_user',             #获取全部用户信息（测试用）
	]

""" Init
"""

LOG_MODULE = 'Auth'
AUTH_MAIL_PATH = "./auth/resources/mail.html"

CODE = [] #验证码
INVALID_MAIL = ['System'] #邮箱保留字


# 构建用户信息仓库
if storage.exist_repository("Auth")==False:
	storage.creat_repository(name='Auth',user_id='System')
	con_table = '''
		CREATE TABLE AUTH (
			MAIL     TEXT PRIMARY KEY NOT NULL, 
			PASSWORD TEXT, 
			NAME     TEXT
		)'''
	storage.add_info(name='Auth',con=con_table)


""" API
"""

def add_user(mail,password,**kwg):
	''' 添加成员
	*没有写邮箱(ID)重复的情况
	'''
	global INVALID_MAIL
	global LOG_MODULE
	name=kwg['name']
	if mail in INVALID_MAIL: 
		logger.warning("Fail to add user(Auth Not Valid)",LOG_MODULE)
		return False
	con = '''INSERT INTO AUTH (MAIL,PASSWORD,NAME) 
		VALUES (\'{}\',\'{}\',\'{}\')'''.format(mail, password, name)
	try:
		storage.operation(name='Auth',con=con)
		logger.info("Sucessed to add user",LOG_MODULE)
		return True
	except:
		logger.warning("Fail to add user",LOG_MODULE)
		return False


def change_info(mail,**kwg):
	''' 修改信息
	'''
	#print(kwg)
	for item in kwg:
		if item not in ['password']:
			logger.error("Wrong tag to change user info",LOG_MODULE)
			return False
		con = """UPDATE AUTH SET {} = {}""".format(item,kwg[item])
		storage.operation(name='Auth',con=con)
	return True


def config_user():
	''' 查改成员信息
	*没有添加各种容错
	'''
	logger.critical("Getting all user info!",LOG_MODULE)
	con = '''SELECT mail,password,name from AUTH'''
	info=storage.operation(name='Auth',con=con)
	return info


def check_password(mail,password):
	''' 验证邮箱与密码
	'''
	logger.info("Start check mail ~ password",LOG_MODULE)
	con = "SELECT mail,password from AUTH where mail=\'"+mail+"\'"
	info=storage.operation(name='Auth',con=con)
	if info==[]:return False
	return info[0][1]==password


def _generate_validation_code(mail):
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
		for item in CODE:
			if item[0]==mail:
				del(item)
			print(CODE)
		print(CODE)
		#CODE.clear()
		return True
	return False


def send_check_mail(mail):
	''' 发送验证邮箱验证码
	'''
	from system import mail as system_mail
	logger.info("Constructing mail",LOG_MODULE)
	with open(AUTH_MAIL_PATH) as f:
		word = f.read()
		word=word.replace("IIA-Flag-Code",_generate_validation_code(mail))
		word=word.replace("IIA-Flag-Content","【IIA】您正在注册成为新用户，感谢您的支持！")
	system_mail.send_message(mail,word)


def send_find_password(mail):
	''' 发送找回密码验证码
	'''
	from system import mail as system_mail
	logger.info("Constructing mail",LOG_MODULE)
	with open(AUTH_MAIL_PATH) as f:
		word = f.read()
		word=word.replace("IIA-Flag-Code",_generate_validation_code(mail))
		word=word.replace("IIA-Flag-Content","【IIA】您正在使用找回密码功能, 验证码可能导致IIA账号被盗, 请勿转发或泄漏。")
	system_mail.send_message(mail,word)


def send_change_password(mail):
	''' 发送修改密码验证码
	'''
	from system import mail as system_mail
	logger.info("Constructing mail",LOG_MODULE)
	with open(AUTH_MAIL_PATH) as f:
		word = f.read()
		word=word.replace("IIA-Flag-Code",_generate_validation_code(mail))
		word=word.replace("IIA-Flag-Content","【IIA】您正在使用修改密码功能, 验证码可能导致IIA账号被盗, 请勿转发或泄漏。")
	system_mail.send_message(mail,word)


def remember_user(mail):
	''' 记住账户(邮箱)
	'''
	import setting
	setting.set(['default_mail'],mail,file="./ui/setting.json",js_read=True)
