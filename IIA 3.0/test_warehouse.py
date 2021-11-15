import warehouse
import logger

import random

LOG_MODULE = 'Test Warehouse'

def test_add_SheetWarehouse():
	''' Add info 
	'''
	mail = '1742861545@qq.com'
	name = 'MySheetWarehouse'

	operator = warehouse.SheetWarehouse(name=name,user_id=mail)
	operator.creat()

	con_table = '''CREATE TABLE DataSet1 (NUM1 REAL, NUM2 REAL)'''
	operator.execute(con=con_table)

	#生成一组随机数
	for i in range(50):
		a = random.gauss(10,4)
		b = a*random.triangular(0.5,1.5)
		con = 'INSERT INTO DataSet1 (NUM1,NUM2) VALUES (\''+str(a)+'\',\''+str(b)+'\')'
		operator.execute(con=con)

	# 打印数
	print(warehouse._test_show_info(name,con = '''SELECT NUM1,NUM2 from DataSet1'''))

test_add_SheetWarehouse()