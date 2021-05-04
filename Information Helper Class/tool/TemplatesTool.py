from .CSVTool import *

def get_template_detail(basepath,name=None,all=False,onlyType=False):
	""" 获取模板信息 
	参数说明:
		basepath: 程序主文件路径
		name: 模板或数据表名称
		all: 如果all为True, 返回所有模板信息, 否则返回特定模板信息
	"""
	if name != None:
		data = loadDataset(basepath+'/resources/system/template/'+name+'.csv')
		if onlyType == True:
			data = data[1]
			if data == ['None']: return None
			else: return data
	
	return data

def save_new_template(basepath,name,tem_list,tem_list_type):
	""" 添加新模板
	功能说明:
		1. 新模板添加到templates.csv中
		2. 新模板数据类型保存
		3. 创建空数据表
	参数说明:
		basepath: 程序主文件路径
		name: 新增模板名称
		tem_list: 新增的表格表头
		tem_list_type: 新增的表格每列的数据类型
	"""
	# 1. 新模板添加到templates.csv中
	csvWriter([name]+tem_list,basepath+'/resources/system/template/template.csv','a+')
	# 2. 新模板数据类型保存
	csvWriter(tem_list,basepath+'/resources/system/template/'+name+'.csv','a+')
	if tem_list_type == None:
		csvWriter(['None'],basepath+'/resources/system/template/'+name+'.csv','a+')
	else:
		csvWriter(tem_list_type,basepath+'/resources/system/template/'+name+'.csv','a+')
	# 3. 创建空数据表
	csvWriter([name],basepath+'/resources/user/'+name+'.csv','a+')
	csvWriter(tem_list,basepath+'/resources/user/'+name+'.csv','a+')
	return True


