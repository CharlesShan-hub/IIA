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

def regist(mail,password,name,code):
	''' 增加用户
	'''
	#if _password_valid(password)==False:
	#	return 403
	# Request to create a new user
	if code=="request":
		auth.send_check_mail(mail)
		return 200
	# Verification code received (verification code error)
	if auth.check_validation_code(mail,code)==False:
		logger.warning("Wrong validation code",LOG_MODULE)
		return 403
	# Write user name and password
	if auth.add_user(mail=mail,password=password,name=name,code=code) == True:
		return 100


def find_password(mail,code):
	''' 找回密码
	'''
	# 请求找回密码
	if code=="request":
		auth.send_find_password(mail)
		return 200
	# 收到验证码(验证码错误)
	if auth.check_validation_code(mail,code)==False:
		logger.warning("Wrong validation code",LOG_MODULE)
		return 403
	# 验证码正确
	return 100

def change_password(mail,code,password):
	''' 修改密码
	'''
	# 请求修改密码
	if code=="request":
		auth.send_change_password(mail)
		return 200
	# 收到验证码(验证码错误)
	if auth.check_validation_code(mail,code)==False:
		logger.warning("Wrong validation code",LOG_MODULE)
		return 403
	# 验证码正确
	auth.change_info(mail,password=password)
	return 100

def remember_user(mail):
	''' 记录用户
	'''
	auth.remember_user(mail)
