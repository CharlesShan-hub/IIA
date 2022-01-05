from storage.custom import *

'''
	Check Path and File existence
'''
__all__ = [
		'exist_repository',
		'creat_repository'
		]

# Folders
if os.path.exists('./storage/resources') == False:
	os.makedirs('./storage/resources')

# Repo info file
if os.path.exists(ConfigFilePath) == False:
	with open(ConfigFilePath, 'w', encoding='utf-8') as f:
		content = {
			'repo_id': []
		}
		f.write(json.dumps(content, indent=4, ensure_ascii=False))


'''
	API
'''

def exist_repository(name,**kwg):
	''' 检查某数据仓库是否存在
	'''
	return exist_repo(name,**kwg)


def creat_repository(name,**kwg):
	''' 创建新数据仓库
	'''
	return creat_repo(name,**kwg)


def copy_repository(
	name=None,old_name='',old_repo_id=[]):
	''' 创建数据库备份
	''' 
	return copy_repo(old_repo_id=old_repo_id,name=name,old_name=old_name)


def delete_repository(repo_id=[],name=''):
	''' 删除数据库
	本地仓库例子:[0] - [0,0] - [0,0,0]
	              |        - [0,0,1]
	               - [0,1] 

	本地仓库没有云端备份:
	1. 如果删除[0,1]: 某一层级下最后一个备份(无后续结点). 直接删除[0,1]及其信息.
	2. 如果删除[0,0]: 有继承结点或者后续结点. 将[0,0]db文件删除, 信息标记为空但保留位置, 名称标记为空字符串.

	本地仓库有云端备份: 提供两种方案 - 仅删除本地, 删除本地与云端.
	如果要删除云端, 要先对云端操作, 操作失败就停止.
	1. 如果只删除本地仓库: 检查到该仓库有云端备份, 就仅删除本地db文件, 信息标记为空但保留位置, 名称标记不变.
	2. 如果要同时删除云端仓库: 就按照“本地仓库没有云端备份”的方法, 同时操作本地与云端.(注意云端或本地都有可能是占位结点)
	3. 如果仅删除云端备份: 本地不动, 云端按照“本地仓库没有云端备份的方法”操作.(注意云端有可能是占位结点)

	返回值是删除删除成功与否
	'''
	return delete_repo(repo_id=repo_id,name=name)


def configure_repository(repo_id=[],name='',con_name=None, con_content=None, mode='auto'):
	''' 配置数据库(比如改名, 与自定义标签添加与内容修改与获取)
	'''
	return configure_repo(repo_id,name,con_name, con_content, mode)


def cover_repository(from_name='',to_name='',from_repo_id=[],to_repo_id=[]):
	''' 覆盖数据库(版本回退)
	'''
	return cover_repo(from_name,to_name,from_repo_id,to_repo_id)


def info_repository(repo_id=[],name='',mail=''):
	''' 获取仓库信息
	'''
	return info_repo(repo_id=repo_id,name=name,mail=mail)


def add_info(repo_id=[],name='',con=""):
	return t_add_info(repo_id=repo_id,name=name,con=con)


def test_add_info(repo_id=[],name='',con=""):
	return t_add_info(repo_id=repo_id,name=name,con=con)

