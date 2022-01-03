from project.custom import *
import storage

__all__ = []

'''
	初始化
'''
# 构建任务信息仓库
if storage.exist_repository("Project")==False:
	storage.creat_repository(name='Project',user_id='System')
	con_table = '''CREATE TABLE TEST (MAIL TEXT PRIMARY KEY NOT NULL, PASSWORD TEXT, NAME TEXT)'''
	storage.add_info(name='Project',con=con_table)



'''
	API
'''

#新建项目->每个项目包括一个清单,里边描述了项目的组成,介绍等等

def add_mission():
	''' 新建项目
	'''
	return _add_mission()
