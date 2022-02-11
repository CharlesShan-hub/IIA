import setting
import logger

LOG_MODULE = "Server"

def get_layout(mail):
	'''
	'''
	logger.info("Get Layout",LOG_MODULE)
	return setting.get(['General',mail,'dashboard'],default={})


def set_layout(mail,layout):
	'''
	'''
	logger.info("Set Layout",LOG_MODULE)
	setting.set(['General',mail,'dashboard'],layout)
	return 