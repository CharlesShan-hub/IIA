import os
import json

# 检查路径
if os.path.exists('./storage/resources') == False:
	os.makedirs('./storage/resources')

if os.path.exists('./storage/resources/repo_info.json') == False:
	with open('./storage/resources/repo_info.json'\
		, 'w', encoding='utf-8') as f:
		content = {
			'repo_id': []
		}
		f.write(json.dumps(content, indent=4, ensure_ascii=False))

import storage.custom as custom

def creat_repository(name):
	''' 创建新数据仓库
	'''
	return custom.creat_repo(name)

def delete_repositroy(repo_id=[],name=''):
	''' 删除数据库
	本地仓库例子:[0] - [0,0] - [0,0,0]
	              |        - [0,0,1]
	               - [0,1] 

	本地仓库没有云端备份:
	1. 如果删除[0,1]: 某一层级下最后一个备份(无后续结点). 直接删除[0,1]及其信息.
	2. 如果删除[0,0]: 有继承结点或者后续结点. 将[0,0]db文件删除, 信息标记为空但保留位置, 名称标记为空字符串.

	本地仓库有云端备份: 提供两种方案 - 仅删除本地, 删除本地与云端.
	如果要删除云端, 要先对云端操作, 操作失败就停止.
	1. 如果只删除本地仓库: 检查到该仓库有云端备份, 就近删除本地db文件, 信息标记为空但保留位置, 名称标记不变.
	'''
	return custom.delete_repo(repo_id=repo_id,name=name)

def copy_repository(
	name=None,old_name='',old_repo_id=[]):
	''' 创建数据库备份
	''' 
	return custom.copy_repo(old_repo_id=old_repo_id,name=name,old_name=old_name)

def clean_repository():
	''' 整理数据库
	'''
	pass

def cover_repostory():
	''' 覆盖数据库(版本回退)
	'''
	pass

def configure_repostory():
	''' 配置数据库(比如改名, 与自定义标签添加与内容修改)
	'''
	pass

def get_label_repostory():
	''' 获取数据库配置(比如cloud,exist,与自定义标签)
	'''
	pass

