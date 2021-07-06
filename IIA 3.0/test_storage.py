''' Initial
	Initial incloud creat default folder and files.
'''
import storage
import logger

def test_creat_repository():
	''' Creat New Reposory
	Creat new reposory can return whether to creat successfully
	'''
	# Creat new repo
	logger.info("**********************************")
	logger.info("Creat new repo valid type\n")
	storage.creat_repository(name='RepoTest')
	logger.info("")
	storage.creat_repository(name='RepoTest2')
	logger.info("")

	# Creat with wrong type parm (invalid)
	logger.info("**********************************")
	logger.info("Creat with wrong type parm (invalid)\n")
	try:
		storage.creat_repository(name=0)
	except TypeError as e:
		logger.info(e)
	logger.info("")

	# Creat wrong format name repo (invalid)
	logger.info("**********************************")
	logger.info("Creat wrong format name repo (invalid)\n")
	storage.creat_repository(name='/User/wrongtype')
	logger.info("")
	storage.creat_repository(name='.\\wrongtype')
	logger.info("")
	storage.creat_repository(name='wrongtype.txt')
	logger.info("")
	storage.creat_repository(name='       ')

	# Creat repeated named repo (invalid)
	logger.info("**********************************")
	logger.info("Creat repeated named repo (invalid)\n")
	storage.creat_repository(name='RepoTest')
	logger.info("")
#test_creat_repository()


def test_copy_repository():
	''' Copy recent repo
	'''
	# Copy a recent repo
	logger.info("**********************************")
	logger.info("Copy repo in valid type\n")
	storage.copy_repository(name='RepoTest_2021_7_1',old_name='RepoTest')
	logger.info("")
	storage.copy_repository(name='RepoTest_2021_7_2',old_name='RepoTest')
	logger.info("")
	storage.copy_repository(name='RepoTest_2021_7_1(1)',old_name='RepoTest_2021_7_1')
	logger.info("")

	# Copy a recent repo with wrong name (invalid)
	logger.info("**********************************")
	logger.info("Copy a recent repo with wrong name (invalid)\n")
	storage.copy_repository(name='CopyRepoTest',old_name='NotExist')
	logger.info("")
	
	# Copy a recent repo with wrong repo_id (invalid)
	logger.info("**********************************")
	logger.info("Copy a recent repo with wrong repo_id (invalid)\n")
	storage.copy_repository(name='CopyRepoTest',old_repo_id=[-1])
	logger.info("")
#test_copy_repository()


def test_delete_repository():
	''' Delete repo
	'''
	# Delete a repo which is without copy
	# By default, the repo tree is like this:
	# RepoTest - RepoTest_2021_7_1 - RepoTest_2021_7_1(1)
	#          - RepoTest_2021_7_2
	logger.info("**********************************")
	logger.info("Delete a repo which is without cloud copy\n")
	storage.delete_repository(name='RepoTest_2021_7_1')
	logger.info("")
	storage.delete_repository(name='RepoTest_2021_7_2')
	logger.info("")
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
	logger.info("")
	# make copy
	# x - x.1 - x.1.1
	#   - x.2 - x.2.1
	#   - x.3
	storage.copy_repository(name='RepoTest_2021_7_1',old_name='RepoTest')
	logger.info("")
	storage.copy_repository(name='RepoTest_2021_7_2',old_name='RepoTest')
	logger.info("")
	storage.copy_repository(name='RepoTest_2021_7_3',old_name='RepoTest')
	logger.info("")
	storage.copy_repository(name='RepoTest_2021_7_1(1)',old_name='RepoTest_2021_7_1')
	logger.info("")
	storage.copy_repository(name='RepoTest_2021_7_2(1)',old_name='RepoTest_2021_7_2')
	logger.info("")
	#storage.copy_repository(name='RepoTest_2021_7_1(2)',old_name='RepoTest_2021_7_1')
	#storage.copy_repository(name='RepoTest_2021_7_1(3)',old_name='RepoTest_2021_7_1')
	#storage.copy_repository(name='RepoTest_2021_7_1(1)(1)',old_name='RepoTest_2021_7_1(1)')
	#storage.copy_repository(name='RepoTest_2021_7_1(1)(2)',old_name='RepoTest_2021_7_1(1)')
	#storage.copy_repository(name='RepoTest_2021_7_1(1)(3)',old_name='RepoTest_2021_7_1(1)')
	# delete
	storage.delete_repository(name='RepoTest_2021_7_1')
	logger.info("")
	storage.delete_repository(name='RepoTest_2021_7_2')
	logger.info("")
	storage.delete_repository(name='RepoTest_2021_7_2(1)')
	logger.info("")
	storage.delete_repository(name='RepoTest_2021_7_1(1)')
	logger.info("")
	storage.delete_repository(name='RepoTest_2021_7_3')
	logger.info("")
	storage.delete_repository(name='RepoTest')
	logger.info("")
#test_delete_repository2()


def test_configure_repository():
	''' 测试配置数据仓库
	'''
	# 创建数据仓库
	storage.creat_repository(name='RepoTest')
	logger.info("")

	# 返回标签
	con_cloud = storage.configure_repository(name='RepoTest',con_name='cloud')
	logger.info("Get config - cloud - "+str(con_cloud)+'\n')
	# This print - 'Get config - cloud - False'
	con_exist = storage.configure_repository(name='RepoTest',con_name='exist')
	logger.info("Get config - exist - "+str(con_exist)+'\n')
	# This print - 'Get config - exist - True'
	logger.info("")

	# 合法创建标签
	storage.configure_repository(name='RepoTest',con_name='label1',con_content='I will be changed!')
	con_new = storage.configure_repository(name='RepoTest',con_name='label1')
	logger.info("Get config - label1 - "+str(con_new)+'\n')
	storage.configure_repository(name='RepoTest',con_name='label1',con_content='Hello!')
	con_new = storage.configure_repository(name='RepoTest',con_name='label1')
	logger.info("Get config - label1 - "+str(con_new)+'\n')

	# 创建非法标签
	#storage.configure_repostory(name='RepoTest')
	#logger.info("")
#test_configure_repository()


def test_cover_repository():
	''' 测试版本回退
	'''
	# 创建数据仓库
	storage.creat_repository(name='RepoTest')
	logger.info("")

	# 创建备份
	storage.copy_repository(name='RepoTest_2021_7_6',old_name='RepoTest')
	logger.info("")

	# 进行版本回退
	storage.cover_repository(from_name='RepoTest_2021_7_6',to_name='RepoTest')
	logger.info("")
test_cover_repository()

