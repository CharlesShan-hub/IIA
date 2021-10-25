import auth
import logger

import random
import re

LOG_MODULE = "Server"


def _password_valid(password):
	''' 密码合法判断
	'''
	return True

def login(mail,password):
	''' 登陆判断
	'''
	if(auth.check_password(mail,password)):
		return 100
	else:
		return 403

def regist(mail,password,name):
	''' 增加用户
	'''
	#if _password_valid(password)==False:
	#	return 403
	# 写入用户名与密码
	if auth.add_user(mail=mail,password=password,name=name) == True:
		return 100
	else:
		return 403

def find_password(mail,code):
	''' 找回密码
	'''
	# 请求找回密码
	if code=="request":
		code_=auth.generate_validation_code(mail)
		auth.send_find_password(mail,code_)
		return 200
	# 收到验证码(验证码错误)
	if auth.check_validation_code(mail,code)==False:
		logger.warning("Wrong validation code",LOG_MODULE)
		return 403
	# 验证码正确
	return 100

def change_password(mail,password):
	''' 修改密码
	'''
	pass
