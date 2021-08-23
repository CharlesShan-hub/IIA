import storage

def _password_valid(password):
	''' 密码合法判断
	'''
	pass

def login(mail,password):
	''' 登陆判断
	'''
	print(storage.configure_user(mail,'password'))
	if(password==storage.configure_user(mail,'password')):
		return 100
	else:
		return 403

def regist(mail,password):
	''' 增加用户
	'''
	if _password_valid(password)==False:
		return 403
	# 写入用户名与密码
	if storage.add_user(mail,password) == True:
		return 100
	else:
		return 403

def change_password(mail,password):
	''' 修改密码
	'''
	pass

def find_password():
	''' 找回密码
	'''
	pass
