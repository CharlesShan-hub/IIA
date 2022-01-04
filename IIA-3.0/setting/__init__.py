import os
import json
import logger

__all__ = [
		'initialize',
		'get',
		'set',
		'del_s'
		]

'''
	Init
'''
LOG_MODULE = 'Setting'


'''
	Check Path and File existence
'''
# Repo info file
ConfigFilePath = "./setting/setting.json"
def initialize():
	logger.info("setting.json reinit",LOG_MODULE)
	with open(ConfigFilePath, 'w', encoding='utf-8') as f:
		content = {
			'Server':{
				'ip':'127.0.0.1',
				'port':80
			}
		}
		f.write(json.dumps(content, indent=4, ensure_ascii=False))

if os.path.exists(ConfigFilePath) == False:
	logger.warning("setting.json is missing",LOG_MODULE)
	initialize()

def get(param=[],default=None):
	''' 获取设置
	param: (optional),`list`, 设置内容在setting.json的包含关系
	default: (optional), 设置内容查找失败默认返回的内容

	return: 获取的设置内容
	'''
	logger.debug("getting setting",LOG_MODULE)
	if type(param) != list:
		logger.warning("get() change param "+\
			str(type(param))+"into list",LOG_MODULE)
		param = [param]
	with open(ConfigFilePath,'r') as load_f:
		content = json.load(load_f)
	for item in param:
		if type(item) != str:
			logger.error("get() not str item in param: "\
				+str(item),LOG_MODULE)
			return default
		else:
			content = content[item]
	logger.debug("got setting",LOG_MODULE)
	return content

def set(path,con=None):
	''' 写入设置
	path: `list`, 设置内容在setting.json的包含关系
	con: (optional), 设置成的内容

	return: 设置成功(True)或失败(False)
	'''
	logger.debug("setting setting",LOG_MODULE)
	if type(path) != list:
		logger.warning("get() change param "+\
			str(type(param))+"into list",LOG_MODULE)
		path = [path]
	with open(ConfigFilePath,'r') as load_f:
		content = json.load(load_f)
	temp=content
	last=None
	last_id=None
	for item in path:
		if type(item) != str:
			logger.error("get() not str item in param: "\
				+str(item),LOG_MODULE)
			return False
		else:
			if item not in temp:
				temp[item]={}
			last=temp
			last_id=item
			temp=temp[item]
	last[last_id]=con
	with open(ConfigFilePath, 'w', encoding='utf-8') as f:
		f.write(json.dumps(content, indent=4, ensure_ascii=False))
	logger.debug("set setting",LOG_MODULE)
	return True

def del_s(path):
	''' 删除设置
	path: `list`, 设置内容在setting.json的包含关系

	return: 删除成功(True)或失败(False)
	'''
	logger.debug("del setting",LOG_MODULE)
	if type(path) != list:
		logger.warning("get() change param "+\
			str(type(param))+"into list",LOG_MODULE)
		path = [path]
	with open(ConfigFilePath,'r') as load_f:
		content = json.load(load_f)
	temp=content
	last=None
	last_id=None
	for item in path:
		if type(item) != str:
			logger.error("get() not str item in param: "\
				+str(item),LOG_MODULE)
			return False
		else:
			if item not in temp:
				temp[item]={}
			last=temp
			last_id=item
			temp=temp[item]
	del(last[last_id])
	with open(ConfigFilePath, 'w', encoding='utf-8') as f:
		f.write(json.dumps(content, indent=4, ensure_ascii=False))
	logger.debug("deleted setting",LOG_MODULE)
	return True
