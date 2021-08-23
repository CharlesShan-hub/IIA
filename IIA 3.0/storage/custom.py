from storage.implement import *

###########################################################
''' Core Region 
	These functions are called by functions in __init__.py

	**User Info 用户信息部分**
	add_u(): 添加新用户
	get_user_info(): 获取用户信息

	**Repo Part 仓库部分**
	_get_operat_repo_id(): 获取正在被操作的数据仓库的repo_id,错误返回false
	_clean_repo_info(): 删除多余占位仓库信息
	creat_repo(): 创建新仓库
	copy_repo(): 创建备份仓库
	delete_repo(): 删除仓库
	configure_repo(): 增改查仓库信息
	cover_repo(): 仓库版本回退

'''
def add_u(mail,password,**kwg):
	''' 新建用户
	'''
	if valid_mail(mail)==False:
		logger.warning("Failed to add user - mail:"+mail+" is not valid")
		return False
	if valid_password(password)==False:
		logger.warning("Failed to add user - password:"+password+" is not valid")
		return False

	result = save_user_info(mail,password)

	# 保存用户配置
	for item in kwg:
		change_user_property(mail,item,kwg[item])

	return result


def configure_u(mail,con_name=None, con_content=None, mode='auto'):
	''' 配置或获取用户信息
	'''
	# 返回用户全部信息
	if con_name == None:
		return get_user_info(mail)
	# 返回用户信息
	if (mode=='get') or (mode=='auto' and con_content==None):
		return get_user_property(mail,con_name)
	# 设置仓库信息(没有标签则创建)
	change_user_property(mail,con_name,con_content)
	return True


def _get_operat_repo_id(repo_id=[],name=''):
	''' 获取正在被操作的数据仓库的repo_id,错误返回false
	'''
	if repo_id == []: # 没有repo_id, 根据名称获取repo_id
		logger.info("Getting repo_id")
		repo_id = get_repo_id(name)
		if repo_id == False:
			logger.warning("Failed to match(get) repo - "+name+", id="+str(repo_id))
			return False
	else: # 有repo_id, 不管名称
		logger.info("Validate repo_id")
		if exist_repo_id(repo_id)==False:
			logger.warning("Failed to match(validate) repo - "+name+", id="+str(repo_id))
			return False
	return repo_id


def _clean_repo_info(repo_id=None):
	''' 删除多余占位仓库信息
	'''
	logger.info("[Push] Dualing with node - "+str(repo_id))
	# 加载信息
	all_repo_info = load_json(ConfigFilePath)
	# 验证错误
	if type(repo_id)!=list:
		raise ValueError("repo_id should be list type!")
	# repo_id为空, 则默认模式为全部仓库
	if repo_id == None:
		logger.info("Clearing excess placeholder information - all trees")
		cleaned_trees = []
		for item in all_repo_info['repo_id']:
			if item[0] not in cleaned_trees:
				logger.info("Going to clean repo tree - "+str([item[0]]))
				_clean_repo_info([item[0]])
				cleaned_trees.append(item[0])
		return True
	# 进行以某结点为根结点的信息清理
	# Step1: 子节点的清理
	logger.info("Step1 - clean child node of - "+str(repo_id))
	for child_repo_id in reversed(get_child_repo_id(repo_id)):
		_clean_repo_info(child_repo_id)
	# Step2: 自己的清理
	logger.info("Step2 - clean node itself - "+str(repo_id))
	cloud = get_repo_property(repo_id,'cloud')
	end_point = is_end_point_repo(repo_id)
	if get_repo_property(repo_id,'exist') == True:
		logger.info("Meet exist point - "+str(repo_id))
		logger.info("[Pop] node - "+str(repo_id))
		return True
	if cloud==False and end_point==True:
		logger.info("Meet end point - "+str(repo_id))
		delete_repo_info(repo_id,placeholder=False)
		logger.info("[Pop] node - "+str(repo_id))
		return True
	logger.info("[Pop] node - "+str(repo_id))
	return True


def creat_repo(name,**kwg):
	''' 创建新仓库
	'''
	# 检查变量类型
	if(type(name)!=str):
		logger.warning("creat_repo() - name should be `str` type")
		raise TypeError("creat_repo() - name should be `str` type")
		return False

	logger.info("Start creat new repo - "+name)
	# 检查名称合法性
	if valid_repo_name(name)==False:
		logger.warning("Failed to creat new repo - "+name)
		return False

	# 检查可访问性合法性
	if 'user_id' not in kwg:
		logger.warning("creat_repo() - need user_id")
		return False

	# 新建数据库文件
	creat_database(name)
	# 获取数据仓库ID - repo_id
	repo_id = creat_repo_id()
	# 保存仓库信息
	save_repo_info(repo_id,name)
	# 保存仓库配置
	for item in kwg:
		change_repo_property(repo_id,item,kwg[item])
	logger.info("Succeeded to creat new repo - "+name)
	return True


def copy_repo(name,old_name='',old_repo_id=[]):
	''' 创建备份仓库
	'''
	# 检查变量类型
	if(type(name)!=str or type(old_name)!=str):
		logger.warning("copy_repo() - name,old_name should be `str` type")
		raise TypeError("copy_repo() - name,old_name should be `str` type")
		return False
	if(type(old_repo_id)!=list):
		logger.warning("copy_repo() - old_repo_id_ should be `list` type")
		raise TypeError("copy_repo() - old_repo_id_ should be `list` type")
		return False

	logger.info("Start make copy repo "+name+", id="+str(old_repo_id))

	# 验证新仓库名称
	if valid_repo_name(name)==False:
		logger.warning("Failed to creat new repo - "+name)
		return False

	# 获取或验证被复制的仓库的repo_id - 当名称与id冲突时, 以id为主
	old_repo_id = _get_operat_repo_id(repo_id=old_repo_id,name=old_name)
	if old_repo_id == False:
		logger.warning("Failed to copy repo - "+name)
		return False

	# 构造新ID, 并保存信息
	repo_id = creat_repo_id(mode='copy',old_repo_id=old_repo_id)

	# 保存文件信息
	save_repo_info(repo_id,name)

	# 复制文件
	copy_repo_file(old_repo_id=old_repo_id,repo_id=repo_id)

	logger.info("Succeeded to copy repo - "+name)
	return True


def delete_repo(repo_id=[],name=''):
	''' 删除仓库
	'''
	# 检查变量类型
	if(type(name)!=str):
		logger.warning("delete_repo() - name should be `str` type")
		raise TypeError("delete_repo() - name should be `str` type")
		return False
	if(type(repo_id)!=list):
		logger.warning("delete_repo() - repo_id should be `list` type")
		raise TypeError("delete_repo() - repo_id should be `list` type")
		return False
	logger.info("Start delete repo: name="+name+", id="+str(repo_id))

	# 获取或验证被复制的仓库的repo_id - 当名称与id冲突时, 以id为主
	repo_id = _get_operat_repo_id(repo_id=repo_id,name=name)
	if repo_id == False:
		logger.warning("Failed to delete repo - "+name)

	# 获取结点信息
	cloud = get_repo_property(repo_id,'cloud')
	end_point = is_end_point_repo(repo_id)
	
	# 无云端备份, 非尾结点
	if cloud == False and end_point==False:
		delete_repo_file(repo_id)
		delete_repo_info(repo_id,placeholder=True)
		
	# 无云端备份, 尾结点
	elif cloud==False and end_point==True:
		delete_repo_file(repo_id)
		delete_repo_info(repo_id,placeholder=True)
		_clean_repo_info(repo_id=[repo_id[0]])

	# 有云端备份
	elif cloud == True:
		pass

	return True


def configure_repo(repo_id=[],name='',con_name=None, con_content=None, mode='auto'):
	''' 增改查仓库信息
	这里注意content为None时, 就变成返回模式了, 而不是创建一个内容为None的标签.
	如果真的希望创建一个内容为None的标签, 请设置mode.
	:param mode(optional): 
		'auto': 自动选择设置标签与获取标签值
		'set': 设置标签模式(创建一个内容为None的标签时用这个)
		'get': 获取标签模式
	'''
	# 检查变量类型
	if(type(name)!=str):
		logger.warning("configure_repo() - name should be `str` type")
		raise TypeError("configure_repo() - name should be `str` type")
		return False
	if(type(repo_id)!=list):
		logger.warning("configure_repo() - repo_id should be `list` type")
		raise TypeError("configure_repo() - repo_id should be `list` type")
		return False
	if mode!='auto' and mode!='set' and mode!='get':
		logger.warning("configure_repo() - mode should be 'auto' or 'set' or 'get'!")
		raise TypeError("configure_repo() - mode should be 'auto' or 'set' or 'get'!")
		return False

	logger.info("Start change repo config: name="+name+", id="+str(repo_id))

	# 获取或验证被复制的仓库的repo_id - 当名称与id冲突时, 以id为主
	repo_id = _get_operat_repo_id(repo_id=repo_id,name=name)
	if repo_id == False:
		logger.warning("Failed to configure repo - "+name)

	# 返回仓库信息
	if (mode=='get') or (mode=='auto' and con_content==None):
		return get_repo_property(repo_id,con_name)
	# 设置仓库信息(没有标签则创建)
	change_repo_property(repo_id,con_name,con_content)
	return True


def cover_repo(from_name='',to_name='',from_repo_id=[],to_repo_id=[]):
	''' 数据仓库版本回退
	'''
	# 获取或验证被复制的仓库的repo_id - 当名称与id冲突时, 以id为主
	from_repo_id = _get_operat_repo_id(repo_id=from_repo_id,name=from_name)
	to_repo_id = _get_operat_repo_id(repo_id=to_repo_id,name=to_name)
	if from_repo_id == False or to_repo_id == False :
		logger.warning("Failed to cover repo")
	logger.info("Try to cover repo from "+str(from_repo_id)+" to "+str(to_repo_id))

	# 进行合法性验证
	if is_child_repo_id(to_name,from_name) == False:
		logger.warning("Unlegal to cover repo! (Not copy relationship!)")
		return False
	# 目前仅支持 没有网络备份的仓库的被覆盖
	if get_repo_property(to_repo_id,'cloud') == True:
		logger.warning("Unlegal to cover repo! (Have online copy!)")
		return False

	# 进行修改 - 覆盖文件
	

	# 进行修改 - 配置信息覆盖


	return True


###########################################################
''' Design Region 
	You can write your own functions in this place. Change
	the functions in ```Core Design``` to call your own-designed
	functions.
'''

# Write your code here
# ...





