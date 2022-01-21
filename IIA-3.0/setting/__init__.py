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


def load_dict(file=ConfigFilePath,js_read=False):
	''' 加载设置字典
	'''
	with open(file,'r') as load_f:
		if js_read == True:
			c=load_f.read()
			c=c[c.index('{'):]
			temp=""
			for line in c.split("\n"):
				if line.strip()[:2]!='//':
					temp = temp+line+'\n'
			content = json.loads(temp)
		else:
			content = json.loads(load_f.read())
	return content


def write_dict(content,file=ConfigFilePath,js_read=False):
	''' 重新写回设置
	'''
	if js_read==True:
		with open(file,'r') as load_f:
			head = load_f.read()
			head = head[:head.index('{')]
			content = head+json.dumps(content, indent=4, ensure_ascii=False)
	else:
		content = json.dumps(content, indent=4, ensure_ascii=False)
	with open(file, 'w', encoding='utf-8') as f:
		f.write(content)


def get(param=[],default=None,file=ConfigFilePath,js_read=False):
	''' 获取设置
	param: (optional),`list`, 设置内容在setting.json的包含关系
	default: (optional), 设置内容查找失败默认返回的内容
	file: (optional), `str`, 设置文件的路径
	js_read: (optional), `bool`, 是否会有js文件直接引用设置

	return: 获取的设置内容
	'''
	logger.debug("getting setting",LOG_MODULE)
	if type(param) != list:
		logger.warning("get() change param "+\
			str(type(param))+"into list",LOG_MODULE)
		param = [param]

	content = load_dict(file,js_read)
	
	for item in param:
		if type(item) != str:
			logger.error("get() not str item in param: "\
				+str(item),LOG_MODULE)
			return default
		else:
			content = content[item]
	logger.debug("got setting",LOG_MODULE)
	return content

def set(path,con=None,file=ConfigFilePath,js_read=False):
	''' 写入设置
	path: `list`, 设置内容在setting.json的包含关系
	con: (optional), 设置成的内容
	file: (optional), `str`, 设置文件的路径
	js_read: (optional), `bool`, 是否会有js文件直接引用设置

	return: 设置成功(True)或失败(False)
	'''
	logger.debug("setting setting",LOG_MODULE)
	if type(path) != list:
		logger.warning("get() change param "+\
			str(type(param))+"into list",LOG_MODULE)
		path = [path]

	content = load_dict(file,js_read)
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
	write_dict(content,file,js_read)
	logger.debug("set setting",LOG_MODULE)
	return True

def del_s(path,file=ConfigFilePath,js_read=False):
	''' 删除设置
	path: `list`, 设置内容在setting.json的包含关系
	file: (optional), `str`, 设置文件的路径
	js_read: (optional), `bool`, 是否会有js文件直接引用设置

	return: 删除成功(True)或失败(False)
	'''
	logger.debug("del setting",LOG_MODULE)
	if type(path) != list:
		logger.warning("get() change param "+\
			str(type(param))+"into list",LOG_MODULE)
		path = [path]
	
	content = load_dict(file,js_read)
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
	write_dict(content,file,js_read)
	logger.debug("deleted setting",LOG_MODULE)
	return True
