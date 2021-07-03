from storage.implement import *
import logger

###########################################################
''' Core Region 
	These functions are called by functions in __init__.py
'''
def _get_operat_repo_id(repo_id=[],name=''):
	''' 获取正在被操作的数据仓库的repo_id,错误返回false
	'''
	if repo_id == []: # 没有repo_id, 根据名称获取repo_id
		logger.info("Getting repo_id")
		repo_id = get_repo_id(name)
		if repo_id == False:
			logger.warning("Failed to match(get) repo - "+name+", id="+str(repo_id))
			return False
	else: # 有repo_id, 不管名称
		logger.info("Validate repo_id")
		if exist_repo_id(repo_id)==False:
			logger.warning("Failed to match(validate) repo - "+name+", id="+str(repo_id))
			return False
	return repo_id


def creat_repo(name):
	''' 创建新仓库
	'''
	# 检查变量类型
	if(type(name)!=str):
		logger.warning("creat_repo() - name should be `str` type")
		raise TypeError("creat_repo() - name should be `str` type")
		return False

	logger.info("Start creat new repo - "+name)
	# 检查名称合法性
	if repo_name_valid(name)==False:
		logger.warning("Failed to creat new repo - "+name)
		return False
	# 新建数据库文件
	creat_database(name)
	# 获取数据仓库ID - repo_id
	repo_id = creat_repo_id()
	# 保存仓库信息
	save_repo_info(repo_id,name)

	logger.info("Succeeded to creat new repo - "+name)
	return True


def copy_repo(name,old_name='',old_repo_id=[]):
	''' 创建备份仓库
	'''
	# 检查变量类型
	if(type(name)!=str or type(old_name)!=str):
		logger.warning("copy_repo() - name,old_name should be `str` type")
		raise TypeError("copy_repo() - name,old_name should be `str` type")
		return False
	if(type(old_repo_id)!=list):
		logger.warning("copy_repo() - old_repo_id_ should be `list` type")
		raise TypeError("copy_repo() - old_repo_id_ should be `list` type")
		return False

	logger.info("Start make copy repo "+name+", id="+str(old_repo_id))

	# 验证新仓库名称
	if repo_name_valid(name)==False:
		logger.warning("Failed to creat new repo - "+name)
		return False

	# 获取或验证被复制的仓库的repo_id - 当名称与id冲突时, 以id为主
	old_repo_id = _get_operat_repo_id(repo_id=old_repo_id,name=old_name)
	if old_repo_id == False:
		logger.warning("Failed to copy repo - "+name)
		return False

	# 构造新ID, 并保存信息
	logger.info("Getting new repo_id")

	return True
	# 未完成, 正在构建
	#new_repo_id = 
	#creat_copy_repo_info(old_repo_id,name)
	# 新建数据库文件
	#creat_database(name,log=log)


def delete_repo(repo_id=[],name=''):
	''' 删除仓库
	'''
	# 检查变量类型
	if(type(name)!=str):
		logger.warning("delete_repo() - name should be `str` type")
		raise TypeError("delete_repo() - name should be `str` type")
		return False
	if(type(repo_id)!=list):
		logger.warning("delete_repo() - repo_id should be `list` type")
		raise TypeError("delete_repo() - repo_id should be `list` type")
		return False

	logger.info("Start delete repo: name="+name+", id="+str(repo_id))

	# 获取或验证被复制的仓库的repo_id - 当名称与id冲突时, 以id为主
	repo_id = _get_operat_repo_id(repo_id=repo_id,name=name)
	if repo_id == False:
		logger.warning("Failed to delete repo - "+name)

	return True

	# 进行删除操作目前没有写完!!!
	# 删除数据库文件
	#delete_repo_file()
	# 清除依赖信息
	#delete_repo_info()



###########################################################
''' Design Region 
	You can write your own functions in this place. Change
	the functions in ```Core Design``` to call your own-designed
	functions.
'''

# Write your code here
# ...

"""
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

def get_operat_repo_id(repo_id=None,name=None,log=False):
	''' 获取正在被操作的数据仓库的repo_id
	错误返回false
	'''
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
"""



