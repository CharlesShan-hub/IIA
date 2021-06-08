from storage.custom import *

"""
class repository():
	''' 仓库
	'''
	# 仓库拥有自己的ID, 用来判断仓库版本迭代信息
	repo_id = None
	
	def __init__(self,repo_id):
		self.repo_id = repo_id

	def creat_repo(self,name,log=False):
		''' 创建仓库
		'''
		creat_repo(name,log=log)

	def copy_repo(self):
		''' 备份仓库
		'''
		pass

	def copy_local_repo(self):
		''' 本分仓库至本地
		'''
		pass

	def copy_net_repo(self):
		''' 备份仓库到服务器
		'''
		pass

	def del_repo(self):
		''' 删除仓库
		'''
		pass
"""

def creat_new_repository(name,log=False):
	""" 创建新数据仓库
	"""
	creat_repo(name,log=log)

def creat_copy_repository(
	name=None,old_name=None,old_repo_id=None,log=False):
	""" 创建数据库备份
	""" 
	copy_repo(old_repo_id=old_repo_id,name=name,old_name=old_name,log=log)



#def 
#a = repository()
#a.creat_repo('test.db',log=True)
