import os
import json

__all__ = [
		'initialize',
		'get',
		'set',
		'del_s'
		]
		
'''
	Check Path and File existence
'''

# Repo info file
ConfigFilePath = "./setting/setting.json"
def initialize():
	with open(ConfigFilePath, 'w', encoding='utf-8') as f:
		content = {
			'Server':{
				'ip':'127.0.0.1',
				'port':80
			}
		}
		f.write(json.dumps(content, indent=4, ensure_ascii=False))

if os.path.exists(ConfigFilePath) == False:
	initialize()

def get(param=[]):
	if type(param) != list:
		param = [param]
	with open(ConfigFilePath,'r') as load_f:
		content = json.load(load_f)
	for item in param:
		if type(item) != str:
			print("wrong!")
		else:
			content = content[item]
	return content

def set(path,con=None):
	if type(path) != list:
		path = [path]
	with open(ConfigFilePath,'r') as load_f:
		content = json.load(load_f)
	temp=content
	last=None
	last_id=None
	for item in path:
		if type(item) != str:
			print("wrong!")
		else:
			if item not in temp:
				temp[item]={}
			last=temp
			last_id=item
			temp=temp[item]
	last[last_id]=con
	with open(ConfigFilePath, 'w', encoding='utf-8') as f:
		f.write(json.dumps(content, indent=4, ensure_ascii=False))
	return content

def del_s(path):
	if type(path) != list:
		path = [path]
	with open(ConfigFilePath,'r') as load_f:
		content = json.load(load_f)
	temp=content
	last=None
	last_id=None
	for item in path:
		if type(item) != str:
			print("wrong!")
		else:
			if item not in temp:
				temp[item]={}
			last=temp
			last_id=item
			temp=temp[item]
	del(last[last_id])
	with open(ConfigFilePath, 'w', encoding='utf-8') as f:
		f.write(json.dumps(content, indent=4, ensure_ascii=False))
	return content
