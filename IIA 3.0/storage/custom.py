from storage.implement import *

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


#creat_repo('test.db',log=True)