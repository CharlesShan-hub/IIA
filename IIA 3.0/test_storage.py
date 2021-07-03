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
	storage.copy_repository(name='CopyRepoTest',old_name='RepoTest')
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

test_copy_repository()


def test_delete_repositroy():
	''' Delete repo
	'''
	# Delete a repo which is without copy

	# Delete a repo with neither name nor id (invalid)
	#storage.delete_repositroy()
	# Delete a repo with non-exist name (invalid)
	#storage.delete_repositroy(name='RepoNotExist')
	# Delete a repo with non-exist id (invalid)
	#storage.delete_repositroy(repo_id=[1,2,3,4])
#test_delete_repositroy()





#creat_copy_repository(name='copy_datalist',old_name='datalist',log=True)
#creat_copy_repository(name='copy_datalist2',old_name='datalist',log=True)
#creat_copy_repository(name='copy_datalist3.1',old_name='datalist',log=True)
#creat_copy_repository(name='copy_datalist3.2',old_name='copy_datalist3.1',log=True)

# 删除数据仓库
#delete_repositroy(name='bedelete',log=True)
