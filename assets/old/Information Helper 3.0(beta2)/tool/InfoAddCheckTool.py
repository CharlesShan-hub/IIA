import time
from .CSVTool import *
from .Path import *

def fun_item_normal_save_check_and_change(info_list,info_type_list):
	""" 普通信息保存核查与修改 """
	# 准备工作
	count = 0
	checked_info_list = []
	for item in info_type_list:
		if item == 'bit':
			if info_list[count] not in ['0','1','True','False','yes','no']:
				print(info_list[count],'not valid')
				return False
			if info_list[count]:
				checked_info_list.append('1')
			else:
				checked_info_list.append('0')
		elif item == 'int':
			if fun_item_normal_save_check_int(info_list[count],-2147483648,2147483647) == False:
				print(info_list[count],'not valid')
				return False
			else:
				checked_info_list.append(info_list[count])
		elif item == 'smallint':
			if fun_item_normal_save_check_int(info_list[count],-32768,32767) == False:
				print(info_list[count],'not valid')
				return False
			else:
				checked_info_list.append(info_list[count])
		elif item == 'tinyint':
			if fun_item_normal_save_check_int(info_list[count],0,255) == False:
				print(info_list[count],'not valid')
				return False
			else:
				checked_info_list.append(info_list[count])
		elif item == 'numeric' or item == 'decimal':
			print('numeric or decimal 未检查')
			checked_info_list.append(info_list[count])
		elif item == 'money':
			if fun_item_normal_save_check_float(info_list[count],-9.22e11,9.22e11) == False:
				print(info_list[count],end='')
				print(' not valid')
				return False
			else:
				checked_info_list.append(float(info_list[count]))
		elif item == 'smallmoney':
			if fun_item_normal_save_check_float(info_list[count],-214748.3648,214748.3647) == False:
				print(info_list[count],end='')
				print(' not valid')
				return False
			else:
				checked_info_list.append(float(info_list[count]))
		elif item == 'float':
			if fun_item_normal_save_check_float(info_list[count],-1.79e308,1.79e308) == False:
				print(info_list[count],end='')
				print(' not valid')
				return False
			else:
				checked_info_list.append(float(info_list[count]))
		elif item == 'real':
			if fun_item_normal_save_check_float(info_list[count],-3.40e38,3.40e38) == False:
				print(info_list[count],end='')
				print(' not valid')
				return False
			else:
				checked_info_list.append(float(info_list[count]))
		elif item == 'datetime': # yyyy-mm-dd hh:mm:ss    2017-07-10 09:25:36 
			checked_info_item = fun_item_normal_save_check_date(info_list[count],-3.40e38,3.40e38)
			if checked_info_item == False:
				print(info_list[count],'not valid')
				return False
			else:
				checked_info_list.append(checked_info_item)
		elif item == 'Smalldatetime':
			checked_info_item = fun_item_normal_save_check_date(info_list[count],-3.40e38,3.40e38)
			if checked_info_item == False:
				print(info_list[count],'not valid')
				return False
			else:
				checked_info_list.append(checked_info_item)
		elif item == 'cursor':
			print('cursor 未检查')
			checked_info_list.append(info_list[count])
		elif item == 'timestamp':
			print('timestamp 未检查')
			checked_info_list.append(info_list[count])
		elif item == 'Uniqueidentifier':
			print('Uniqueidentifier 未检查')
			checked_info_list.append(info_list[count])
		elif item == 'char':
			print('char 未检查')
			checked_info_list.append(info_list[count])
		elif item == 'varchar':
			print('varchar 未检查')
			checked_info_list.append(info_list[count])
		elif item == 'text':
			print('text 未检查')
			checked_info_list.append(info_list[count])
		elif item == 'nchar':
			print('nchar 未检查')
			checked_info_list.append(info_list[count])
		elif item == 'nvarchar':
			print('nvarchar 未检查')
			checked_info_list.append(info_list[count])
		elif item == 'ntext':
			print('ntext 未检查')
			checked_info_list.append(info_list[count])
		elif item == 'binary':
			print('binary 未检查')
			checked_info_list.append(info_list[count])
		elif item == 'varbinary':
			print('varbinary 未检查')
			checked_info_list.append(info_list[count])
		elif item == 'image':
			print('image 未检查')
			checked_info_list.append(info_list[count])
		count = count + 1

	return checked_info_list

def fun_item_normal_save_check_int(item,min_,max_):
	""" 保存信息中的整数部分 """
	try:
		if type(eval(item)) != int:
			return False
		if eval(item) < min_ or eval(item) > max_:
			return False
		return True
	except:
		return False

def fun_item_normal_save_check_float(item,min_,max_):
	""" 保存信息中的小数部分 """
	try:
		check_item = float(item)
		if check_item>max_ or check_item<min_:
			return False
		else:
			return True
	except:
		return False

def fun_item_normal_save_check_date(time_string,min_,max_):
	""" 保存信息中的日期部分 """
	def read_time_time(time_string):
		x = ''
		for letter in time_string:
			if letter in ['0','1','2','3','4','5','6','7','8','9']:
				x = x+letter
			else: break
		if x == '':x='0'
		time_string = time_string[len(x):]
		return x,time_string
	def read_time_split(time_string):
		x = ''
		for letter in time_string:
			if letter not in ['0','1','2','3','4','5','6','7','8','9']:
				x = x+letter
			else: break
		time_string = time_string[len(x):]
		return x,time_string

	time_string = time_string.strip()
	
	# 读取年
	year,time_string = read_time_time(time_string)
	
	# 读取分隔符1
	split1,time_string = read_time_split(time_string)

	# 读取月
	month,time_string = read_time_time(time_string)

	# 读取分隔符2
	split2,time_string = read_time_split(time_string)

	# 读取日
	day,time_string = read_time_time(time_string)
	
	# 读取分隔符3
	split3,time_string = read_time_split(time_string)

	# 读取时
	hour,time_string = read_time_time(time_string)
	
	# 读取分隔符4
	split4,time_string = read_time_split(time_string)

	# 读取分
	minute,time_string = read_time_time(time_string)
	
	# 读取分隔符3
	split5,time_string = read_time_split(time_string)

	# 读取时
	second,time_string = read_time_time(time_string)
	
	# 读取分隔符4
	split6,time_string = read_time_split(time_string)

	string_ = year+split1+month+split2+day+split3+hour+split4+minute+split5+second
	format_ = '%Y'+split1+'%m'+split2+'%d'+split3+'%H'+split4+'%M'+split5+'%S'

	# 检查格式是否正确
	try: 
		time_ = time.strptime(string_,format_)
	except:
		return False

	# 检查时间
	#print(time.mktime(time_))

	return time.strftime("%Y-%m-%d %H:%M:%S", time_)

def fun_item_normal_save_write(base_path, name, line):
	""" 保存信息 """
	path = find_infor_path(name,\
		base_path,update_infor_path_=True)
	if csvWriter(line,path,mode='a+',encoding='utf-8'):
		return True
	else:
		return False