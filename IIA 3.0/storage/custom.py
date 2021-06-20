from storage.implement import *

def get_operat_repo_id(repo_id=None,name=None,log=False):
	""" 获取正在被操作的数据仓库的repo_id
	错误返回false
	"""
	# 获取或验证被删除的仓库的repo_id
	# 当名称与id冲突时, 以id为主
	if repo_id == None:
		if log==True:
			print("getting old repo_id")
		repo_id = get_repo_id(name=name)
		if repo_id == False:
			if log==True:
				print("repo_id does not exist!")
			return False
	else:
		if exist_repo_id()==False:
			if log==True:
				print("repo_id does not exist!")
			return
	if log==True:
		print("repo_id is",repo_id)
	return repo_id

def creat_repo(name,log=False):
	''' 创建新仓库
	'''
	# 检查名称合法性
	if repo_name_valid(name)==False:
		return
	# 新建数据库文件
	creat_database(name,log=log)
	# 获取数据仓库ID - repo_id
	repo_id = creat_repo_id()
	# 保存仓库信息
	save_repo_info(repo_id,name)

def copy_repo(name=None,old_name=None,old_repo_id=None,log=False):
	''' 创建备份仓库
	'''
	# 验证新仓库名称
	if repo_name_valid(name,log=log)==False:
		return
	# 获取或验证被复制的仓库的repo_id
	# 当名称与id冲突时, 以id为主
	if old_repo_id == None:
		if log==True:
			print("copy_repo: getting old repo_id")
		old_repo_id = get_repo_id(name=old_name)
		if old_repo_id == False:
			if log==True:
				print("copy_repo: old repo_id does not exist!")
			return
	else:
		if exist_repo_id()==False:
			if log==True:
				print("copy_repo: old repo_id does not exist!")
			return
	if log==True:
		print("copy_repo: old repo_id is",old_repo_id)
	# 构造新ID, 并保存信息
	if log==True:
		print("copy_repo: getting new repo_id")
	creat_copy_repo_info(old_repo_id,name)
	# 新建数据库文件
	creat_database(name,log=log)

def delete_repo(repo_id=None,name=None,log=False):
	''' 删除仓库
	'''
	# 判断与获取仓库repo_id
	repo_id = get_operat_repo_id(repo_id=repo_id,name=name,log=log)
	if(repo_id==False):
		return
	# 判断仓库是否已被删除
	if get_repo_property(repo_id,'exist')==False:
		return
	# 判断仓库是否可能存在网络备份
	if get_repo_property(repo_id,'cloud')==True:
		print("目前不支持存在网络备份的仓库删除")
		return
	# 获取数据仓库互联信息
	repos_info = get_repo_family_info(repo_id)
	# 判断是否可以彻底删除
	flag = True
	for item in repos_info['repo_id']:
		if item['exist'] == True and item != eval(repo_id):
			flag = False
	if log==True:
		print("是否可以彻底删除:",flag)
	# 进行删除操作
	file_delete(path)
	repo_info_change('delete','single',repo_id)




#creat_repo('test.db',log=True)