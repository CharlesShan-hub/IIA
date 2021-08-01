import sqlite3
import csv
import json
import logger
import os
from shutil import copyfile

#####################################################
''' 底层文件操作
	ConfigFilePath: 数据仓库配置文件路径
	UserFilePath: 用户信息配置文件路径
	load_csv(path,encoding='UTF-8'): 读取csv文件
	load_json(path,encoding='UTF-8'): 读取json文件
	write_json(path, content, encoding='UTF-8'): 写json文件
	delete_file(path): 删除文件
	copy_file(path_from,path_to): 拷贝文件
	creat_database(name): 创建数据库文件
'''
# Path of Config File
ConfigFilePath = './storage/resources/repo_info.json'
# Path of User info File
UserFilePath = './storage/resources/user_info.json'
# Attributes of Repo config
RepoAtr = ['name','exist','cloud','open','visible']


def load_csv(path,encoding='UTF-8'):
	''' 获取数据
	:param path: 数据集路径
	:param encoding(optional): 编码类型
	:return data: 获取的数据
	'''
	data = []
	with open(path, 'r', encoding=encoding) as f:
		for line in csv.reader(f):
			data.append(line)
	logger.info("Load csv - "+path)
	return data


def load_json(path,encoding='UTF-8'):
	''' 获取数据
	:param path: 数据集路径
	:param encoding(optional): 编码类型
	:return data: 获取的数据
	'''
	with open(path, 'r', encoding='UTF-8') as f:
		data = json.load(f)    #此时a是一个字典对象
	logger.info("Load json - "+path)
	return data


def write_json(path, content, encoding='UTF-8'):
	''' json写入数据
	'''
	logger.info("Write json - "+path)
	with open(path, 'w', encoding='utf-8') as f:
		f.write(json.dumps(content, indent=4, ensure_ascii=False))


def add_json_config(data,name,content):
	''' json加入内容
	'''
	data[name] = content
	return data

def delete_file(path):
	''' 文件删除
	'''
	if(os.path.exists(path)):
		os.remove(path)
		logger.info("File/Path deleted - "+path)
	else:
		logger.info("File/Path failed delete - "+path)


def copy_file(path_from,path_to):
	''' 文件复制
	'''
	if(os.path.exists(path_from)):
		copyfile(path_from, path_to)
		logger.info("File/Path copied - "+path_to)
	else:
		logger.info("File/Path failed copied - "+path_to)


def creat_database(name):
	''' 数据库文件的创建
	'''
	logger.info("Creat new database - "+name)
	path = "./storage/resources/"+name+".db"
	conn = sqlite3.connect(path)
	logger.info("Successfully created new database - "+name)


#####################################################
''' 用户信息
	valid_user_name(name): 名称合法性检查
	valid_mail(mail): 邮箱合法性检查
	valid_password(password): 密码合法性检查
	get_user_info(mail): 获取用户信息
	save_user_info(name): 添加/保存用户信息
	get_user_property(mail,con): 查看用户信息
	change_user_property(mail,con_name,con_content): 修改/添加用户信息
'''
def valid_user_name(name):
	''' 名称合法性检查
	'''
	logger.info("Check user_name valid - "+name)
	if name.strip() == '':
		logger.warning("wrong name type: list of space")
		return False
	return True


def valid_mail(mail): 
	''' 邮箱合法性检查
	'''
	logger.info("Check user_mail valid - "+mail)
	all_user_info = load_json(UserFilePath)
	if mail.strip() == '':
		logger.warning("wrong mail type: list of space")
		return False
	if mail in all_user_info:
		logger.warning("Invalid mail! (Have same mail)")
		return False
	return True


def valid_password(password): 
	''' 密码合法性检查
	'''
	logger.info("Check user_password valid")
	return True


def get_user_info(mail): 
	''' 获取用户信息
	''' 
	all_user_info = load_json(UserFilePath)
	if mail in all_user_info:
		return all_user_info[mail]
	else:
		return False


def save_user_info(name,password,mail): 
	''' 添加/保存用户信息
	'''
	logger.info("Changing/adding user info - "+name+" "+mail)
	all_user_info = load_json(UserFilePath)
	all_user_info[mail] = {'name':name,'password':password}
	write_json(UserFilePath, all_user_info)
	return True


def get_user_property(mail,con):
	''' 查看用户信息
	:param mail: 用户邮箱当作ID
	:param con: 信息名称
	'''
	logger.info("Getting user info - "+con)
	all_user_info = load_json(UserFilePath)
	try:
		return all_user_info[mail][con]
	except:
		return False


def change_user_property(mail,con_name,con_content):
	''' 修改/添加用户信息
	:param mail: 用户邮箱当作ID
	:param con: 信息名称
	'''
	logger.info("Changing/adding user info - "+con_name+" "+str(con_content))
	all_user_info = load_json(ConfigFilePath)
	all_user_info[mail][con_name] = con_content
	write_json(UserFilePath, all_user_info)
	return True


#####################################################
''' 数据仓库属性
	valid_repo_name(name): 名称合法性检查
	creat_repo_id(mode='new',old_repo_id=None): 生成数据仓库ID
	exist_repo_id(repo_id): 判断输入的repo_id是否存在
	get_repo_id(name): 通过名称获取数据仓库id
	get_child_repo_id(repo_id): 查看某数据仓库的下一层结点
	get_repo_property(repo_id,con): 查看数据仓库的属性
	save_repo_info(repo_id,repo_name,args**): 保存(新)仓库信息
	copy_repo_file(old_repo_id,repo_id): 复制仓库信息
	delete_repo_file(repo_id): 删除仓库信息
	is_end_point_repo(repo_id): 确认是某层的最后一个结点
'''
def _get_sub_repo_id(repo_id,repo_id_list=None):
	''' 获取当前id插入位置
	:param repo_id: 待插入的仓库ID
	:param repo_id_list(optional): 已有ID列表
	'''
	# 获取待插入列表
	if repo_id_list == None:
		repo_id_list = load_json(ConfigFilePath)['repo_id']
	# 如果列表为空, 直接插入
	if len(repo_id_list) == 0:
		return 1
	# repo_id为头结点
	if len(repo_id) == 1:
		filtered = list(filter(lambda x:x[0]>repo_id[0],repo_id_list))
		if filtered == []:
			return len(repo_id_list)
		return repo_id_list.index(filtered[0])
	# repo_id是子头结点
	if(repo_id[-1]==0):
		return repo_id_list.index(repo_id[:-1])+1
	# repo_id是某个中间的结点
	temp = repo_id.copy()
	temp[-1] = temp[-1]-1
	return repo_id_list.index(temp)+1
	

def valid_repo_name(name):
	''' 数据仓库名称合法性检查
	:param name: 数据仓库名称
	:return : 是否合法
	'''
	logger.info("Check repo_name valid - "+name)
	# 检查名称是否符合命名规范
	for item in ['\\','/','.']:
		if item in name:
			logger.warning("wrong char '"+item+"' in name - "+name)
			return False
	if name.strip() == '':
		logger.warning("wrong name type: list of space")
		return False
	# 检查名称是否重复
	all_repo_info = load_json(ConfigFilePath)
	for item in all_repo_info['repo_id']:
		if name == all_repo_info[str(item)]["name"]:
			logger.info("Check repo_name valid - False")
			return False
	logger.info("Check repo_name valid - True")
	return True


def creat_repo_id(mode='new',old_repo_id=None):
	''' 数据仓库id repo_id 生成
	:param mode(optional): 
		'new'-生成新的数据仓库ID
		'copy'-生成某一仓库的复制数据仓库的ID
	:param old_repo_id(optional): 当生成复制仓库ID时, 传入被复制仓库的ID
	:return :生成的repo_id
	'''
	all_repo_info = load_json(ConfigFilePath)
	if mode=='new':
		logger.info("Start creat new repo_id")
		new_id = 0
		for item in all_repo_info['repo_id']:
			if new_id <= item[0]:
				new_id = new_id+1
		logger.info("New repo_id - "+str([new_id]))
		return [new_id]
	elif mode=='copy':
		logger.info("Start creat copy repo_id")
		#if exist_repo_id(old_repo_id) == False:
		#	logger.warning("Failed to creat repo_id!")
		#	return False
		repo_id = list(old_repo_id)
		repo_id.append(0)
		try:
			sub = all_repo_info['repo_id'].index(repo_id)
			while(sub!=len(all_repo_info['repo_id'])-1):
				repo_id[-1] = repo_id[-1]+1
				sub = sub+1
				if(all_repo_info['repo_id'][sub]!=repo_id):
					return repo_id
			repo_id[-1] = repo_id[-1]+1
			return repo_id
		except ValueError:
			return repo_id 
	else:
		logger.warning("Failed to creat repo_id!")
		raise TypeError("Wrong type of mode (should be 'new' or 'copy' only!)")
		return False


def exist_repo_id(repo_id):
	''' 判断输入的repo_id是否存在
	:param repo_id: 数据仓库ID
	:return : 是否存在
	'''
	logger.info("Verifing ID exists - "+str(repo_id))
	all_repo_info = load_json(ConfigFilePath)
	return repo_id in all_repo_info['repo_id']


def get_repo_id(name):
	''' 通过名称获取数据仓库id
	:param name: 数据仓库名称
	:return :成功返回repo_id, 失败返回false
	'''
	logger.info("Getting repo_id by name ("+name+")")
	all_repo_info = load_json(ConfigFilePath)
	try:
		for one_repo_id in all_repo_info["repo_id"]:
			if all_repo_info[str(one_repo_id)]['name'] == name:
				logger.info("Got repo_id - "+str(one_repo_id))
				return one_repo_id
		logger.warning("Failed to get repo_id by name - "+name)
		return False
	except:
		logger.warning("Unexpected thing happened")
		return False


def is_child_repo_id(child_repo_id, repo_id):
	''' 判断第一个结点是不是第二个的子结点
	'''
	if len(child_repo_id)<=len(repo_id):
		return False
	return child_repo_id[:len(repo_id)] == repo_id


def get_child_repo_id(repo_id):
	''' 获取某个仓库的下一层结点
	'''
	all_repo_id = load_json(ConfigFilePath)["repo_id"]
	def _is_sub_list(x):
		if len(x)!=len(repo_id)+1:
			return False
		return x[:len(repo_id)] == repo_id
	return list(filter(_is_sub_list, all_repo_id))


def get_repo_property(repo_id,con):
	''' 查看数据仓库的属性
	:param repo_id: 数据仓库ID
	:param con: 属性名称
	'''
	logger.info("Getting repo property - "+con)
	all_repo_info = load_json(ConfigFilePath)
	return all_repo_info[str(repo_id)][con]


def change_repo_property(repo_id,con_name,con_content):
	''' 查看数据仓库的属性
	:param repo_id: 数据仓库ID
	:param con: 属性名称
	'''
	logger.info("Changing/adding repo property - "+con_name+" "+str(con_content))
	all_repo_info = load_json(ConfigFilePath)
	all_repo_info[str(repo_id)][con_name] = con_content
	write_json(ConfigFilePath, all_repo_info)
	return True


def save_repo_info(repo_id,repo_name,exist=True,cloud=False):
	''' 保存数据仓库信息
	:param repo_id: 数据仓库ID
	:param repo_name: 数据仓库名称
	:param exist(optional): 仓库是否存在(占位信息不存在数据库文件)
	:param cloud(optional): 仓库是否存在云端备份
	'''
	logger.info("Save repo info (repo_id = "+str(repo_id)+")")
	all_repo_info = load_json(ConfigFilePath)
	all_repo_info['repo_id'].insert(
		_get_sub_repo_id(repo_id,all_repo_info['repo_id']),repo_id)
	all_repo_info[str(repo_id)] = {
		"name":repo_name,
		"exist": exist,
		"cloud": cloud
	}
	write_json(ConfigFilePath, all_repo_info)


def copy_repo_file(old_repo_id,repo_id):
	''' 复制仓库文件
	:param lod_repo_id: 被复制仓库ID
	:param repo_id: 新仓库ID
	'''
	logger.info("Start copy repo store file")
	path_from = './storage/resources/'+get_repo_property(old_repo_id,'name')+'.db'
	path_to = './storage/resources/'+get_repo_property(repo_id,'name')+'.db'
	copy_file(path_from,path_to)


def delete_repo_file(repo_id):
	''' 删除仓库文件
	:param repo_id: 仓库ID
	'''
	logger.info("Start delete repo store file")
	path = './storage/resources/'+get_repo_property(repo_id,'name')+'.db'
	delete_file(path)


def delete_repo_info(repo_id,placeholder):
	''' 删除仓库信息
	:param repo_id: 仓库ID
	:param placeholder: 是否保留占位符
	'''
	logger.info("Start delete repo info, placeholder - "+str(placeholder))
	if placeholder == False:
		all_repo_info = load_json(ConfigFilePath)
		all_repo_info['repo_id'].remove(repo_id)
		del all_repo_info[str(repo_id)]
		write_json(ConfigFilePath, all_repo_info)
		logger.info("Successfully delete repo info - "+str(repo_id))
		return True
	else:
		change_repo_property(repo_id,'name','')
		change_repo_property(repo_id,'exist',False)
		return True


def is_end_point_repo(repo_id):
	''' 确认是某层的最后一个结点
		a - a1 - a1_1
		  - a2 
		那么a1_1与a2符合要求(没有后继结点, 没有下一个兄弟结点)
	:param repo_id: 查询的仓库ID
	:return :是否是某一层的尾结点
	'''
	logger.info("Checking if end point of a layer - "+str(repo_id))
	all_repo_info = load_json(ConfigFilePath)
	if repo_id not in all_repo_info['repo_id']:
		logger.warning("repo_id is unexpected")
		raise ValueError("repo_id is unexpected")
		return False
	# 是否有子结点
	child_repo_id = repo_id.copy()
	child_repo_id.append(0)
	have_child_node = child_repo_id in all_repo_info['repo_id']
	logger.info("Checking if have child node - "+str(have_child_node))
	# 是否有后继结点
	next_repo_id = repo_id.copy()
	next_repo_id[-1] = next_repo_id[-1]+1
	have_next_node = False
	for item in all_repo_info['repo_id']:
		if next_repo_id != item: continue
		if all_repo_info[str(next_repo_id)]['exist'] == True:
			have_next_node = True
			break
	logger.info("Checking if have next node - "+str(have_next_node))
	# 是否某一层的尾结点
	is_end_node = have_next_node==False and have_child_node==False
	logger.info("If end node - "+str(is_end_node))
	return is_end_node

	
"""
# 获取数据仓库互联信息
def get_repo_family_info(repo_id):
	all_repo_info = load_json(ConfigFilePath)
	temp = {"repo_id":[]}
	for one_repo_id in all_repo_info["repo_id"]:
		if one_repo_id[0] == repo_id[0]:
			temp["repo_id"].append(one_repo_id)
			temp[str(one_repo_id)] = all_repo_info[str(one_repo_id)]
	return temp

# 构建某个仓库的备份的信息并保存
def creat_copy_repo_info(old_repo_id,repo_name):
	if exist_repo_id(old_repo_id) == False:
		return False
	repo_id = list(old_repo_id)
	repo_id.append(0)
	all_repo_info = load_json(ConfigFilePath)

	repo_id_index = all_repo_info["repo_id"].index(old_repo_id)
	flag = False
	count = 1
	# 找到并列备份
	print(repo_id)
	try:
		while repo_id == all_repo_info["repo_id"][repo_id_index+count]:
			repo_id[-1] = repo_id[-1] + 1
			print(repo_id)
			count = count+1
			flag = True
	except IndexError:
		pass
	if flag == True:
		all_repo_info["repo_id"].insert(repo_id_index+count,repo_id)
	else:
		all_repo_info["repo_id"].insert(repo_id_index+1,repo_id)

	all_repo_info[str(repo_id)] = {
		"name":repo_name,
		"exist": True,
		"cloud": False
	}
	write_json(ConfigFilePath, all_repo_info)


def copy_repo_file(old_repo_id=old_repo_id,repo_id=repo_id):



# 数据表 -> 数据库数据表
# 数据表文件的创建
def creat_sheet(path,log=False):
	conn = sqlite3.connect(path)
	if log==True:
		print("Opened database successfully")
	c = conn.cursor()
	c.execute('''CREATE TABLE COMPANY
		(ID INT PRIMARY KEY     NOT NULL,
		NAME           TEXT    NOT NULL,
		AGE            INT     NOT NULL,
		ADDRESS        CHAR(50),
		SALARY         REAL);''')
	if log==True:
		print("Table created successfully")
	conn.commit()
	conn.close()
"""
