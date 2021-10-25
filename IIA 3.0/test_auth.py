import auth
import logger

LOG_MODULE = 'Test Auth'

def test_add_user():
	''' 添加个人信息
	'''
	#创建个人信息
	logger.info("添加个人信息",LOG_MODULE)
	result=auth.add_user(mail='charles.shht@gmail.com',password='111111',name='Charles')
	logger.info("添加个人信息状态"+str(result),LOG_MODULE)
	result=auth.add_user(mail='1742861545@qq.com',password='111111',name='Charles')
	logger.info("添加个人信息状态"+str(result),LOG_MODULE)
test_add_user()

def test_config_user():
	''' 打印所有个人信息
	'''
	logger.info("打印所有个人信息",LOG_MODULE)
	print(auth.config_user())
test_config_user()

def test_check_password():
	''' 检查密码
	'''
	logger.info("测试邮箱密码匹配",LOG_MODULE)
	result=auth.check_password('1742861545@qq.com','111111')
	logger.info("邮箱密码匹配状态"+str(result),LOG_MODULE)
	result=auth.check_password('charles.shht@gmail.com','111111')
	logger.info("邮箱密码匹配状态"+str(result),LOG_MODULE)
test_check_password()

