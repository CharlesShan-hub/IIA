import sqlite3
import csv
import json

#####################################################
# 基础文件
# csv文件读写
def load_csv(path,encoding='UTF-8'):
	''' 获取数据
	:param path: 数据集路径
	:return data: 获取的数据
	'''
	data = []
	with open(path, 'r', encoding=encoding) as f:
		for line in csv.reader(f):
			data.append(line)
	return data

def load_json(path,encoding='UTF-8'):
	''' 获取数据
	'''
	with open(path, 'r', encoding='UTF-8') as f:
		a = json.load(f)    #此时a是一个字典对象
	return a

def write_json(path, content, encoding='UTF-8'):
	''' 写入数据
	'''
	with open(path, 'w', encoding='utf-8') as f:
		f.write(json.dumps(content, indent=4, ensure_ascii=False))

#####################################################
# 基础功能

# 数据仓库 -> 数据库文件
# 数据仓库名称合法性检查
def repo_name_valid(name,log=False):
	all_repo_info = load_json("./storage/resources/repo_info.json")
	for item in all_repo_info['repo_id']:
		if name == all_repo_info[str(item)]["name"]:
			if log==True:
				print("The name of the repo is repeated.")
			return False
	if log==True:
		print("Repo name valid.")
	return True

# 数据仓库id repo_id 生成
def creat_repo_id():
	all_repo_info = load_json("./storage/resources/repo_info.json")
	new_id = 0
	for item in all_repo_info['repo_id']:
		if new_id <= item[0]:
			new_id = new_id+1
	return [new_id]

# 通过名称获取数据仓库id 
def get_repo_id(name):
	''' 成功返回repo_id, 失败返回false
	'''
	all_repo_info = load_json("./storage/resources/repo_info.json")
	try:
		for one_repo_id in all_repo_info["repo_id"]:
			if all_repo_info[str(one_repo_id)]['name'] == name:
				return one_repo_id
		return False
	except:
		return False

# 判断输入的repo_id是否存在
def exist_repo_id(repo_id):
	all_repo_info = load_json("./storage/resources/repo_info.json")
	return repo_id in all_repo_info['repo_id']

# 构建某个仓库的备份的信息并保存
def creat_copy_repo_info(old_repo_id,name):
	if exist_repo_id(old_repo_id) == False:
		return False
	repo_id = list(old_repo_id)
	repo_id.append(0)
	path = "./storage/resources/repo_info.json"
	all_repo_info = load_json(path)

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

	all_repo_info[str(repo_id)] = {"name":name}
	write_json(path, all_repo_info)

# 数据库文件的创建
def creat_database(name,log=False):
	path = "./storage/resources/"+name+".db"
	conn = sqlite3.connect(path)
	if log==True:
		print("Opened database successfully")

# 保存数据仓库信息
def save_repo_info(repo_id,repo_name):
	path = "./storage/resources/repo_info.json"
	all_repo_info = load_json(path)
	all_repo_info['repo_id'].append(repo_id)
	all_repo_info[str(repo_id)] = {"name":repo_name}
	write_json(path, all_repo_info)

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