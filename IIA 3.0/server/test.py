import logger
import random

LOG_MODULE = "Server"

def single_ping(*args):
	''' 收到ping请求
	'''
	return 100

def ping(param=0):
	''' ping并执行一定命令
	'''
	if param == 0:
		logger.info("Get ping request",LOG_MODULE)
		return single_ping()
	elif param == 1:
		logger.info("Get ping request - return a random word",LOG_MODULE)
		return random.randint(0,100)
	else:
		logger.warning("Get unknown type ping request- return single ping",LOG_MODULE)
		return single_ping()