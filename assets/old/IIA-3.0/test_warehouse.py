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

#test_add_SheetWarehouse()



def fun1():
	print("Hello World")

def fun2(**kwg):
	print("Three Numbers",kwg['a'],kwg['b'],kwg['c'])

my_high_repo = warehouse.Warehouse(name='my_high_repo',mail='1742861545@qq.com')
#my_high_repo.set_fun(fun1)
#my_high_repo.run_fun("fun1")
#my_high_repo.set_fun(fun2)
#my_high_repo.run_fun("fun2",a=1,b=2,c=3)

#my_high_repo.creat_base_repo(name="TestRepo1")
#my_high_repo.creat_base_repo(name="TestRepo2")

#my_high_repo.creat_table()

#print(my_high_repo.real)
#my_high_repo.creat_warehouse()
#print(my_high_repo.real)

#print(my_high_repo.add_base_repo(name="TestRepo1"))
#print(my_high_repo.exist_base_repo(name="TestRepo1"))
#print(my_high_repo.exist_base_repo(name="TestRepo2"))

#con =  '''CREATE TABLE BIRTHDAY (NAME TEXT, YEAR INT, MON INT,DAY INT)'''
#print(my_high_repo.operation_base_repo(name="TestRepo1",con=con))






def add_people(self,**kwg):
	con_list = 'INSERT INTO BIRTHDAY (NAME,YEAR,MON,DAY) VALUES ("{}","{}","{}","{}")'.format(kwg['name'],kwg['year'],kwg['mon'],kwg['day'])
	self.operation_base_repo(name="TestRepo1",con=con_list)
my_high_repo.set_fun(add_people)

def get_birthday(self,**kwg):
	con = '''SELECT NAME,YEAR,MON,DAY from BIRTHDAY'''
	print(self.operation_base_repo(name="TestRepo1",con=con))
my_high_repo.set_fun(get_birthday)





def delete_charles():
	con = 'DELETE from BIRTHDAY where NAME="{}"'.format('Charles Shan')
	my_high_repo.operation_base_repo(name="TestRepo1",con=con)


my_high_repo.run_fun("add_people",name='Charles Shan',year=2000,mon=2,day=26)
my_high_repo.run_fun("get_birthday")
#delete_charles()


