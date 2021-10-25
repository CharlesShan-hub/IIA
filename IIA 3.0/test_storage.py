''' Initial
	Initial incloud creat default folder and files.
'''
import storage
import logger

LOG_MODULE = 'Test Storage'


def test_add_info():
	''' Add info 
	'''
	con_table = '''CREATE TABLE AUTH (MAIL TEXT PRIMARY KEY NOT NULL, NAME TEXT)'''
	con_info1 = '''INSERT INTO AUTH (MAIL,NAME) VALUES ('charles.shht@gmail.com','Charles')'''
	con_select1 = '''SELECT mail,name  from AUTH'''


	#storage.creat_repository(name='RepoTest',user_id='charles.shht@gmail.com')
	storage.test_add_info(name='RepoTest',con=[con_select1])

test_add_info()

def test_add_user():
	''' Add New User(Account)
	'''
	# Creat new user
	logger.info("Creat new user info (valid type)",LOG_MODULE)
	storage.add_user('charles.shht@gmail.com','111111')
	storage.add_user('1742861545@qq.com','111111')

	# Creat user with new labels
	logger.info("Creat new user info (valid type)",LOG_MODULE)
	storage.add_user('shanhongtian@gmail.com','111111',a=1,b=2,c=1)
#test_add_user()


def test_creat_repository():
	''' Creat New Reposory
	Creat new reposory can return whether to creat successfully
	'''
	# Creat new repo
	logger.info("Creat new repo valid type",LOG_MODULE)
	storage.creat_repository(name='RepoTest',user_id='charles.shht@gmail.com')
	storage.creat_repository(name='RepoTest2',user_id='charles.shht@gmail.com',new_label='12345')
	
	# Creat new repo without user_id
	logger.info("Creat new repo without user_id",LOG_MODULE)
	storage.creat_repository(name='RepoTest3')
	
	# Creat with wrong type parm (invalid)
	logger.info("Creat with wrong type parm (invalid)",LOG_MODULE)
	try:
		storage.creat_repository(name=0,user_id='charles.shht@gmail.com')
	except TypeError as e:
		logger.info(e,LOG_MODULE)
	
	# Creat wrong format name repo (invalid)
	logger.info("Creat wrong format name repo (invalid)",LOG_MODULE)
	storage.creat_repository(name='/User/wrongtype',user_id='charles.shht@gmail.com')
	storage.creat_repository(name='.\\wrongtype',user_id='charles.shht@gmail.com')
	storage.creat_repository(name='wrongtype.txt',user_id='charles.shht@gmail.com')
	storage.creat_repository(name='       ',user_id='charles.shht@gmail.com')

	# Creat repeated named repo (invalid)
	logger.info("Creat repeated named repo (invalid)",LOG_MODULE)
	storage.creat_repository(name='RepoTest',user_id='charles.shht@gmail.com')
#test_creat_repository()


def test_copy_repository():
	''' Copy recent repo
	'''
	# Copy a recent repo
	logger.info("Copy repo in valid type",LOG_MODULE)
	storage.copy_repository(name='RepoTest_2021_7_1',old_name='RepoTest')
	storage.copy_repository(name='RepoTest_2021_7_2',old_name='RepoTest')
	storage.copy_repository(name='RepoTest_2021_7_1(1)',old_name='RepoTest_2021_7_1')
	
	# Copy a recent repo with wrong name (invalid)
	logger.info("Copy a recent repo with wrong name (invalid)",LOG_MODULE)
	storage.copy_repository(name='CopyRepoTest',old_name='NotExist')
	
	# Copy a recent repo with wrong repo_id (invalid)
	logger.info("Copy a recent repo with wrong repo_id (invalid)",LOG_MODULE)
	storage.copy_repository(name='CopyRepoTest',old_repo_id=[-1])
#test_copy_repository()


def test_delete_repository():
	''' Delete repo
	'''
	# Delete a repo which is without copy
	# By default, the repo tree is like this:
	# RepoTest - RepoTest_2021_7_1 - RepoTest_2021_7_1(1)
	#          - RepoTest_2021_7_2
	logger.info("Delete a repo which is without cloud copy",LOG_MODULE)
	storage.delete_repository(name='RepoTest_2021_7_1')
	storage.delete_repository(name='RepoTest_2021_7_2')
	storage.delete_repository(name='RepoTest_2021_7_1(1)')
	
	# Delete a repo with neither name nor id (invalid)
	#storage.delete_repository()
	# Delete a repo with non-exist name (invalid)
	#storage.delete_repository(name='RepoNotExist')
	# Delete a repo with non-exist id (invalid)
	#storage.delete_repository(repo_id=[1,2,3,4])
#test_delete_repository()


def test_delete_repository2():
	# make repo
	storage.creat_repository(name='RepoTest')
	# make copy
	# x - x.1 - x.1.1
	#   - x.2 - x.2.1
	#   - x.3
	storage.copy_repository(name='RepoTest_2021_7_1',old_name='RepoTest')
	storage.copy_repository(name='RepoTest_2021_7_2',old_name='RepoTest')
	storage.copy_repository(name='RepoTest_2021_7_3',old_name='RepoTest')
	storage.copy_repository(name='RepoTest_2021_7_1(1)',old_name='RepoTest_2021_7_1')
	storage.copy_repository(name='RepoTest_2021_7_2(1)',old_name='RepoTest_2021_7_2')
	#storage.copy_repository(name='RepoTest_2021_7_1(2)',old_name='RepoTest_2021_7_1')
	#storage.copy_repository(name='RepoTest_2021_7_1(3)',old_name='RepoTest_2021_7_1')
	#storage.copy_repository(name='RepoTest_2021_7_1(1)(1)',old_name='RepoTest_2021_7_1(1)')
	#storage.copy_repository(name='RepoTest_2021_7_1(1)(2)',old_name='RepoTest_2021_7_1(1)')
	#storage.copy_repository(name='RepoTest_2021_7_1(1)(3)',old_name='RepoTest_2021_7_1(1)')
	# delete
	logger.info("Delete a repo which is without cloud copy",LOG_MODULE)
	storage.delete_repository(name='RepoTest_2021_7_1')
	storage.delete_repository(name='RepoTest_2021_7_2')
	storage.delete_repository(name='RepoTest_2021_7_2(1)')
	storage.delete_repository(name='RepoTest_2021_7_1(1)')
	storage.delete_repository(name='RepoTest_2021_7_3')
	storage.delete_repository(name='RepoTest')
#test_delete_repository2()


def test_configure_repository():
	''' 测试配置数据仓库
	'''
	# 创建数据仓库
	storage.creat_repository(name='RepoTest')
	
	# 返回标签
	con_cloud = storage.configure_repository(name='RepoTest',con_name='cloud')
	logger.info("Get config - cloud - "+str(con_cloud),LOG_MODULE)
	# This print - 'Get config - cloud - False'
	con_exist = storage.configure_repository(name='RepoTest',con_name='exist')
	logger.info("Get config - exist - "+str(con_exist),LOG_MODULE)
	# This print - 'Get config - exist - True'
	logger.info("")

	# 合法创建标签
	storage.configure_repository(name='RepoTest',con_name='label1',con_content='I will be changed!')
	con_new = storage.configure_repository(name='RepoTest',con_name='label1')
	logger.info("Get config - label1 - "+str(con_new),LOG_MODULE)
	storage.configure_repository(name='RepoTest',con_name='label1',con_content='Hello!')
	con_new = storage.configure_repository(name='RepoTest',con_name='label1')
	logger.info("Get config - label1 - "+str(con_new),LOG_MODULE)

	# 创建非法标签
	#storage.configure_repostory(name='RepoTest')
#test_configure_repository()


def test_cover_repository():
	''' 测试版本回退
	'''
	# 创建数据仓库
	storage.creat_repository(name='RepoTest')

	# 创建备份
	storage.copy_repository(name='RepoTest_2021_7_6',old_name='RepoTest')

	# 进行版本回退
	storage.cover_repository(from_name='RepoTest_2021_7_6',to_name='RepoTest')
#test_cover_repository()

