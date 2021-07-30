import storage

def _password_valid(password):
	''' 密码合法判断
	'''
	pass

def _name_valid(name):
	''' 名称合法判断
	'''
	pass

def login(password,mail):
	''' 登陆判断
	'''
	print(password)
	print(storage.configure_user(mail,'password'))
	if(password==storage.configure_user(mail,'password')):
		return 100
	else:
		return 403

def regist(name,password,mail):
	''' 增加用户
	'''
	if _name_valid(name)==False:
		return 403
	if _password_valid(password)==False:
		return 403
	# 写入用户名与密码
	if storage.add_user(name,password,mail) == True:
		return 100
	else:
		return 403

def change_password(name,password):
	''' 修改密码
	'''
	pass

def find_password():
	''' 找回密码
	'''
	pass
