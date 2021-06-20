import tkinter as tk
import tkinter.ttk as ttk
from tkinter.filedialog import askopenfilename
from tkinter import messagebox
from tool.Components import *
from tool.TemplatesTool import *
from tool.InfoAddCheckTool import *
from tool.OuterImport import *
from HelpUI import HelpUI

class InformationAddUI():
	""" 信息添加模块
	功能:
		普通信息:  普通信息逐条添加, 普通信息通过excel等添加, 普通信息通过数据表添加
		数据表信息:数据表逐条添加信息,数据表通过excel等添加信息, 数据表通过普通信息添加
		提示信息:  提示信息逐条添加
	"""

	def __init__(self, window, *args, **kwargs):
		""" 信息添加模块初始化 """
		# 设置与主窗口
		self.sd = args[0]
		self.cd = args[1]
		self.window = window
		# 查看进入某种模式 - 'item','outer','inner'
		self.add_mode = 0#self.sd['info_insert_way']
		# 逐条添加默认添加模式 - 'Normal','DataBase','Remind'
		self.add_mode_item = 0#'Normal'
		# 组件声明
		self.components()

	def back(self):
		""" 信息添加模块取消布局安放并返回信息模块主界面 """
		# Interface interaction
		from InformationMainUI import InformationMainUI
		self.information_main = InformationMainUI(self.window,self.sd,self.cd)
		self.destroy()
		self.information_main.pack()

	def pack(self):
		""" 安放 """
		self.page0.pack()

	def pack_forget(self):
		""" 取消安放 """
		self.page0.pack_forget()

	def destroy(self):
		""" 销毁 """ 
		self.page0.destroy()

	#-----------------------------------#
	# 第零层级: 组件声明

	def components(self):
		""" 大标题与返回按钮,主框架与功能控制
			page0
		"""
		# Interface interaction
		self.page0 = Page(self.window,self.sd,self.cd)
		# 大标题
		self.title = tk.Label(self.window,fg=self.cd['front'], \
			bg=self.cd['back'], font=(self.sd['font'],self.sd['tsize'],'bold'), \
			width=40, height=3, justify="left", anchor="center",\
			text=["INFORMATION     ADD\n","信息添加"][self.sd['language_id']])
		self.page0.append(self.title)
		# 返回按钮
		if self.sd['system'] == 'Mac':
			self.back = tk.Button(self.window, text=["Back to last level","返回上一级"]\
				[self.sd['language_id']],font=(self.sd['font'],self.sd['size']),\
				command=self.back, width=20, height=2,fg=self.cd['mcfront'])
		else:
			self.back = tk.Button(self.window, text=["Back to last level","返回上一级"]\
				[self.sd['language_id']],command=self.back, width=20, \
				height=2,fg=self.cd['front'],bg=self.cd['back'],\
				font=(self.sd['font'],self.sd['size']))
		self.page0.append(self.back)
		# 底层框架
		self.bframe = BaseFrame(self.window,self.sd,self.cd)
		self.page0.append(self.bframe)
		# 逐条添加-组件声明 page1
		self.components_item()
		# 外部添加-组件声明 page2
		self.components_outer()
		# 内部添加-组件声明 page3
		self.components_inner()
		# 功能切换框
		tip = ['Add Way','添加方式']
		items = [['Add In Turn','Add from Outer','Add from Inner'],\
				 ['逐项添加','外部添加','内部添加']]
		child_page = [self.page1,self.page2,self.page3]
		self.page0.set_combobox(window=self.bframe.rframe,tip=tip,items=items,\
			cpage=child_page,current=self.add_mode)

	####################################
	# 第一层级: 组件声明

	def components_item(self):
		""" 逐条添加(普通信息, 数据表信息, 提示信息) 
			page1
		"""
		# 逐条添加内容类型选择 - 普通信息 page1_1
		self.components_item_normal()
		# 逐条添加内容类型选择 - 数据库信息 page1_2
		self.components_item_database()
		# 逐条添加内容类型选择 - 提示信息 page1_3
		self.components_item_remind()

		# Interface interaction
		self.page1 = Page(self.window,self.sd,self.cd)
		# 逐项信息添加模式 - 信息类型 Page1
		tip = ['Info Type','信息类型']
		items = [['Normal Info','DataBase Info','Remind Info'],\
				 ['普通信息','数据库信息','提示信息']]
		child_page = [self.page1_1,self.page1_2,self.page1_3]
		self.page1.set_combobox(window=self.bframe.rframe,\
			tip=tip,items=items,cpage=child_page,current=0)

		# 变量
			# 用户选择的模板名
		self.template_choosed = None
		self.page1.append_destroy('self.template_choosed=None')
			# 用户选择的模板的设置与细节
		self.template_choosed_detail = None
		self.page1.append_destroy('self.template_choosed_detail=None')
			# 用户输入是否正确
		self.components_item_normal_valid = False
		self.page1.append_destroy('self.components_item_normal_valid=False')

	def components_outer(self):
		""" 外部添加(普通信息, 数据表信息, 提示信息) 
			page2
		"""
		# 逐条添加内容类型选择 - 普通信息 page1_1
		self.components_outer_normal()
		# 逐条添加内容类型选择 - 数据库信息 page1_2
		self.components_outer_database()
		# 逐条添加内容类型选择 - 提示信息 page1_3
		self.components_outer_remind()
		# Interface interaction
		self.page2 = Page(self.window,self.sd,self.cd)

		# 逐项信息添加模式 - 信息类型 Page2
		tip = ['Info Type','信息类型']
		items = [['Normal Info','DataBase Info','Remind Info'],\
				 ['普通信息','数据库信息','提示信息']]
		child_page = [self.page2_1,self.page2_2,self.page2_3]
		self.page2.set_combobox(window=self.bframe.rframe,\
			tip=tip,items=items,cpage=child_page,current=0)

	def components_inner(self):
		""" 内部添加(普通信息, 数据表信息)
			page3
		"""
		# 逐条添加内容类型选择 - 普通信息 page3_1
		self.components_inner_normal()
		# 逐条添加内容类型选择 - 数据库信息 page3_2
		self.components_inner_database()
		# Interface interaction
		self.page3 = Page(self.window,self.sd,self.cd)

		# 逐项信息添加模式 - 信息类型 Page3
		tip = ['Info Type','信息类型']
		items = [['Normal Info','DataBase Info'],\
				 ['普通信息','数据库信息']]
		child_page = [self.page3_1,self.page3_2]
		self.page3.set_combobox(window=self.bframe.rframe,\
			tip=tip,items=items,cpage=child_page,current=0)

	####################################
	# 第二层级: 逐条添加 - 组件声明

	def components_item_normal(self):
		""" 逐条添加(普通信息) 
			page1_1
		"""
		# Interface interaction
		self.page1_1 = Page(self.window,self.sd,self.cd)
		# 左侧模板选择框
		self.components_item_normal_listbox = NameListbox(self.bframe.lframe,self.sd,self.cd)
		self.components_item_normal_listbox.bind('<ButtonRelease-1>',self.fun_item_normal_choose)
		self.page1_1.append(self.components_item_normal_listbox)
		# 左侧模板预览
		self.components_item_normal_table = QuickTable(self.bframe.lframe,self.sd,self.cd)
		self.page1_1.append(self.components_item_normal_table)
		# 保存信息按钮
		if self.sd['system'] == 'Mac':
			self.components_item_normal_save = tk.Button(self.bframe.rframe, \
				text=["Save","保存"][self.sd['language_id']],\
				width=int(self.sd['rletter']), height=1,fg=self.cd['mcfront'],\
				font=(self.sd['font'],self.sd['size']),\
				command=self.fun_item_normal_save)
		else:
			self.components_item_normal_save = tk.Button(self.bframe.rframe, \
				text=["Save","保存"][self.sd['language_id']],\
				width=int(self.sd['rletter']), height=1,fg=self.cd['front'],bg=self.cd['back'],\
				font=(self.sd['font'],self.sd['size']),\
				command=self.fun_item_normal_save)
		self.page1_1.append(self.components_item_normal_save)
		# 动态组件框
		self.components_item_normal_sframe = ScrollCanvas(self.bframe.rframe,self.sd,self.cd)
		self.page1_1.append(self.components_item_normal_sframe)
		# 信息添加区列表(类型提示与输入框)
		self.components_item_normal_list = IterationList()
		self.page1_1.append(self.components_item_normal_list)
		# 信息名称提示窗列表
		self.components_item_normal_list_name =  IterationList(refresh=True)
		self.page1_1.append(self.components_item_normal_list_name)
		# 保存信息
		self.components_item_normal_list_save = []

		# 变量
			# 选中的模板名称
		self.template_choosed_name = None
		self.page1_1.append_destroy('self.template_choosed_name = None')
			# 选中的模板类型(如果有类型则为列表, 无类型为None)
		self.template_choosed_type = None
		self.page1_1.append_destroy('self.template_choosed_type = None')
			# 选中模板全部信息(模板内容与类型)
		self.template_choosed_detail = None
		self.page1_1.append_destroy('self.template_choosed_detail = None')

	def components_item_database(self):
		""" 逐条添加(数据库信息) 
			page1_2
		"""
		# Interface interaction
		self.page1_2 = Page(self.window,self.sd,self.cd)

	def components_item_remind(self):
		""" 逐条添加(提示信息) 
			page1_3
		"""
		# Interface interaction
		self.page1_3 = Page(self.window,self.sd,self.cd)

	def fun_item_normal_choose(self,event):
		""" 获取用户选择的模板名 """
		# 取消原有布局
		for item in self.components_item_normal_list_name:
			item.pack_forget()
		for item in self.components_item_normal_list:
			item.pack_forget()
		# 更改选中模板
		self.template_choosed_name = \
			self.components_item_normal_listbox.get()
		# 查看模板类型(是否规定数据类型)
		self.template_choosed_type = get_template_detail(\
			self.sd['path'],name=self.template_choosed_name,onlyType=True)
		# 进行右侧输入框更改
		self.template_choosed_detail = get_template_detail(\
			self.sd['path'],name=self.template_choosed_name)
		# 进行输入框动态摆放
		for i in range(len(self.template_choosed_detail[0])):
			# 名称提示
			content_name = tk.Label(self.components_item_normal_sframe.frame,\
				fg=self.cd['front'],bg=self.cd['back'], font=(self.sd['font'],\
				self.sd['size']), text=self.template_choosed_detail[0][i])
			content_name.pack()
			self.components_item_normal_list_name.append(content_name)
			# 输入框
			if self.template_choosed_type:
				content = FunctionalBlock(self.components_item_normal_sframe.frame,\
					''+self.template_choosed_detail[1][i]+':', \
					self.sd,self.cd,kind='entry')
			else:
				content = FunctionalBlock(self.components_item_normal_sframe.frame,\
					['Any Type:','任意类型:'][self.sd['language_id']], \
					self.sd,self.cd,kind='entry')
			content.pack()
			self.components_item_normal_list.append(content)

	def fun_item_normal_save(self):
		""" 保存信息 """
		# 是否进行信息选择
		if self.template_choosed_name == None: return False
		# 信息输入合法性判断
		self.components_item_normal_list_save = []
		for item in self.components_item_normal_list:
			self.components_item_normal_list_save.append(item.entry.get())
		if self.template_choosed_type:
			self.components_item_normal_list_save = fun_item_normal_save_check_and_change(\
				self.components_item_normal_list_save,self.template_choosed_type)
		if self.components_item_normal_list_save==False: return False
		# 进行信息保存
		if fun_item_normal_save_write(self.sd['path'],self.template_choosed_name,\
			self.components_item_normal_list_save):
			for item in self.components_item_normal_list:
				item.entry.delete(0,'end')

	####################################
	# 第二层级: 外部添加 - 组件声明

	def components_outer_normal(self):
		""" 外部添加(普通信息) 
			page2_1
		"""
		# Interface interaction
		self.page2_1 = Page(self.window,self.sd,self.cd)
		# 左侧模板选择框
		self.components_outer_normal_listbox = NameListbox(self.bframe.lframe,self.sd,self.cd,side='left')
		self.components_outer_normal_listbox.bind('<ButtonRelease-1>',self.fun_outer_normal_choose)
		self.page2_1.append(self.components_outer_normal_listbox)
		# 左侧模板预览
		self.components_outer_normal_table = QuickTable(self.bframe.lframe,self.sd,self.cd)
		self.page2_1.append(self.components_outer_normal_table)
		#self.page2_1.pack_way(side='right',fill='both')
		# 隐藏模板选择框按钮-文字
		self.components_outer_normal_hide_var = tk.StringVar()
		self.components_outer_normal_hide_var.set(["Hide","隐藏"][self.sd['language_id']])
		# 隐藏模板选择框按钮
		if self.sd['system'] == 'Mac':
			self.components_outer_normal_hide = tk.Button(self.bframe.rframe,\
				textvariable=self.components_outer_normal_hide_var,\
				width=int(self.sd['rletter']), height=1,fg=self.cd['mcfront'],\
				font=(self.sd['font'],self.sd['size']),\
				command=self.fun_outer_normal_hide)
		else:
			self.components_outer_normal_hide = tk.Button(self.bframe.rframe,\
				textvariable=self.components_outer_normal_hide_var,\
				width=int(self.sd['rletter']), height=1,fg=self.cd['front'],bg=self.cd['back'],\
				font=(self.sd['font'],self.sd['size']),\
				command=self.fun_outer_normal_hide)
		self.page2_1.append(self.components_outer_normal_hide)
		# 选择文件路径
		if self.sd['system'] == 'Mac':
			self.components_outer_normal_file = tk.Button(self.bframe.rframe,\
				text=['file','选择文件'][self.sd['language_id']],\
				width=int(self.sd['rletter']), height=1,fg=self.cd['mcfront'],\
				font=(self.sd['font'],self.sd['size']),\
				command=self.fun_outer_normal_file)
		else:
			self.components_outer_normal_file = tk.Button(self.bframe.rframe,\
				text=['file','选择文件'][self.sd['language_id']],\
				width=int(self.sd['rletter']), height=1,fg=self.cd['front'],bg=self.cd['back'],\
				font=(self.sd['font'],self.sd['size']),\
				command=self.fun_outer_normal_file)
		self.page2_1.append(self.components_outer_normal_file)
		# 安放各种参数的框架
		self.components_outer_normal_parameter_frame = ScrollCanvas(self.bframe.rframe,self.sd,self.cd)
		self.page2_1.append(self.components_outer_normal_parameter_frame)
		# 设置excel参数
		self.components_outer_normal_excel()
		# 设置csv参数
		self.components_outer_normal_csv()
		# 设置txt参数
		self.components_outer_normal_txt()
		# 设置子页
		self.page2_1.set_child_page([self.page2_1_excel,self.page2_1_csv,self.page2_1_txt],current=-1)

		# 变量
			# 选中的模板名称
		self.template_choosed_name = None
		self.page2_1.append_destroy('self.template_choosed_name = None')
			# 选中的模板类型(如果有类型则为列表, 无类型为None)
		self.template_choosed_type = None
		self.page2_1.append_destroy('self.template_choosed_type = None')
			# 选中模板全部信息(模板内容与类型)
		self.template_choosed_detail = None
		self.page2_1.append_destroy('self.template_choosed_detail = None')
			# 待导入文件路径
		self.file_path = None
		self.page2_1.append_destroy('self.file_path = None')
			# 待导入的数据
		self.data = None
		self.page2_1.append_destroy('self.data = None')

	def components_outer_normal_excel(self):
		""" 从excel文件中添加的参数 """
		# Interface interaction
		self.page2_1_excel = Page(self.window,self.sd,self.cd)

		# 各种参数输入的列表
		self.components_outer_normal_parameter_excel = IterationList(refresh=False)
		self.page2_1_excel.append(self.components_outer_normal_parameter_excel)

		# 帮助按钮
		if self.sd['system'] == 'Mac':
			self.components_outer_normal_help = tk.Button(\
				self.components_outer_normal_parameter_frame.frame,\
				text=["help","帮助"][self.sd['language_id']],\
				width=int(self.sd['rletter']), height=1,fg=self.cd['mcfront'],\
				font=(self.sd['font'],self.sd['size']),\
				command=lambda:self.fun_outer_normal_help(kind = 'excel'))
		else:
			self.components_outer_normal_help = tk.Button(\
				self.components_outer_normal_parameter_frame.frame,\
				text=["help","帮助"][self.sd['language_id']],\
				width=int(self.sd['rletter']), height=1,fg=self.cd['front'],bg=self.cd['back'],\
				font=(self.sd['font'],self.sd['size']),\
				command=lambda:self.fun_outer_normal_help(kind = 'excel'))
		self.components_outer_normal_parameter_excel.append(\
			self.components_outer_normal_help)

		# 导入参数选择提示
		self.components_outer_normal_parameter_tip1 = tk.Label(\
			self.components_outer_normal_parameter_frame.frame,\
			text=['Parameters of Data Importing','信息导入参数']\
			[self.sd['language_id']], width=int(self.sd['rletter']),\
			fg=self.cd['front'],bg=self.cd['back'],\
			font=(self.sd['font'],self.sd['size'],'bold'))
		self.components_outer_normal_parameter_excel.append(\
			self.components_outer_normal_parameter_tip1)

		# 参数-表名(excel) - name
		items=['0','1','"Sheet1"','"Sheet2"','"Name"']
		self.components_outer_normal_parameter_sheet_name = FunctionalBlock(\
			self.components_outer_normal_parameter_frame.frame,\
			['sheet name:','表名:'][self.sd['language_id']], \
			self.sd,self.cd,items=items,locked=False,key='sheet_name')
		self.components_outer_normal_parameter_excel.append(\
			self.components_outer_normal_parameter_sheet_name)

		# 参数-表头行数(excel) - header
		items=['0','1','2,','3,','None',"['0', '1']"]
		self.components_outer_normal_parameter_header = FunctionalBlock(\
			self.components_outer_normal_parameter_frame.frame,\
			['header:','表头行数:'][self.sd['language_id']], \
			self.sd,self.cd,items=items,locked=False,key='header')
		self.components_outer_normal_parameter_excel.append(\
			self.components_outer_normal_parameter_header)

		# 参数-表头内容(excel) - names
		items=['None', "[0, 1, 2]",'[0]','[1]',"'A:E'","'A, C, E:F'"]
		self.components_outer_normal_parameter_names = FunctionalBlock(\
			self.components_outer_normal_parameter_frame.frame,\
			['names:','表头内容:'][self.sd['language_id']],\
			self.sd,self.cd,items=items,locked=False,key='names')
		self.components_outer_normal_parameter_excel.append(\
			self.components_outer_normal_parameter_names)

		# 参数-表头内容(excel) - index_col
		items=['None','0','1',"[0, 1]"]
		self.components_outer_normal_parameter_index_col = FunctionalBlock(\
			self.components_outer_normal_parameter_frame.frame,\
			['index_col:','行索引:'][self.sd['language_id']],\
			self.sd,self.cd,items=items,locked=False,key='index_col')
		self.components_outer_normal_parameter_excel.append(\
			self.components_outer_normal_parameter_index_col)

		# 参数-表头内容(excel) - usecols
		items=['None', "[0, 1, 2]",'[0]','[1]',"'A:E'","'A, C, E:F'"]
		self.components_outer_normal_parameter_usecols = FunctionalBlock(\
			self.components_outer_normal_parameter_frame.frame,\
			['usecols:','指定列:'][self.sd['language_id']],\
			self.sd,self.cd,items=items,locked=False,key='usecols')
		self.components_outer_normal_parameter_excel.append(\
			self.components_outer_normal_parameter_usecols)

		# 参数-表头内容(excel) - true_values
		items=['None', "['a','b']"]
		self.components_outer_normal_parameter_true_values = FunctionalBlock(\
			self.components_outer_normal_parameter_frame.frame,\
			['true_values:','认成真:'][self.sd['language_id']],\
			self.sd,self.cd,items=items,locked=False,key='true_values')
		self.components_outer_normal_parameter_excel.append(\
			self.components_outer_normal_parameter_true_values)

		# 参数-表头内容(excel) - false_values
		items=['None', "['a','b']"]
		self.components_outer_normal_parameter_false_values = FunctionalBlock(\
			self.components_outer_normal_parameter_frame.frame,\
			['false_values:','认成假:'][self.sd['language_id']],\
			self.sd,self.cd,items=items,locked=False,key='false_values')
		self.components_outer_normal_parameter_excel.append(\
			self.components_outer_normal_parameter_false_values)

		# 参数-表头内容(excel) - converters
		items=['None', "{0:bool, 1:int}",\
			"{'name1':lambda x:2*x, name2':lambda x:x+1}"]
		self.components_outer_normal_parameter_converters = FunctionalBlock(\
			self.components_outer_normal_parameter_frame.frame,\
			['converters:','转换器:'][self.sd['language_id']],\
			self.sd,self.cd,items=items,locked=False,key='converters')
		self.components_outer_normal_parameter_excel.append(\
			self.components_outer_normal_parameter_converters)

		# 参数-表头内容(excel) - skiprows
		items=['None', '3', "[3, 4, 5]", "lambda x: x in [2,4]"]
		self.components_outer_normal_parameter_skiprows = FunctionalBlock(\
			self.components_outer_normal_parameter_frame.frame,\
			['skiprows:','跳过行:'][self.sd['language_id']],\
			self.sd,self.cd,items=items,locked=False,key='skiprows')
		self.components_outer_normal_parameter_excel.append(\
			self.components_outer_normal_parameter_skiprows)

		# 参数-表头内容(excel) - nrows
		# nrows=3 读取前三行
		items=['None', '5']
		self.components_outer_normal_parameter_nrows = FunctionalBlock(\
			self.components_outer_normal_parameter_frame.frame,\
			['nrows:','前几行:'][self.sd['language_id']],\
			self.sd,self.cd,items=items,locked=False,key='nrows')
		self.components_outer_normal_parameter_excel.append(\
			self.components_outer_normal_parameter_nrows)

		# 参数-表头内容(excel) - na_values
		items=['None', 'cat', "['cat', 'dog']"]
		self.components_outer_normal_parameter_na_values = FunctionalBlock(\
			self.components_outer_normal_parameter_frame.frame,\
			['na_values:','认成空:'][self.sd['language_id']],\
			self.sd,self.cd,items=items,locked=False,key='na_values')
		self.components_outer_normal_parameter_excel.append(\
			self.components_outer_normal_parameter_na_values)

		# 参数-表头内容(excel) - keep_default_na
		items=['True','False']
		self.components_outer_normal_parameter_keep_default_na = FunctionalBlock(\
			self.components_outer_normal_parameter_frame.frame,\
			['KeepDefaultNa:','导入空值:'][self.sd['language_id']],\
			self.sd,self.cd,items=items,locked=True,key='keep_default_na')
		self.components_outer_normal_parameter_excel.append(\
			self.components_outer_normal_parameter_keep_default_na)

		# 参数-表头内容(excel) - convert_float
		# 把1.0转化成1
		items=['False','True']
		self.components_outer_normal_parameter_convert_float = FunctionalBlock(\
			self.components_outer_normal_parameter_frame.frame,\
			['convert_float:','整浮点数转化:'][self.sd['language_id']],\
			self.sd,self.cd,items=items,locked=True,key='convert_float')
		self.components_outer_normal_parameter_excel.append(\
			self.components_outer_normal_parameter_convert_float)

		# 参数-表头内容(excel) - verbose
		items=['True','False']
		self.components_outer_normal_parameter_verbose = FunctionalBlock(\
			self.components_outer_normal_parameter_frame.frame,\
			['verbose:','检测空值:'][self.sd['language_id']],\
			self.sd,self.cd,items=items,locked=True,key='verbose')
		self.components_outer_normal_parameter_excel.append(\
			self.components_outer_normal_parameter_verbose)

		# 参数-表头内容(excel) - na_filter
		items=['True','False']
		self.components_outer_normal_parameter_na_filter = FunctionalBlock(\
			self.components_outer_normal_parameter_frame.frame,\
			['na_filter:','标记空值:'][self.sd['language_id']],\
			self.sd,self.cd,items=items,locked=True,key='na_filter')
		self.components_outer_normal_parameter_excel.append(\
			self.components_outer_normal_parameter_na_filter)

		# 功能-导入数据
		if self.sd['system'] == 'Mac':
			self.components_outer_normal_import_data = tk.Button(\
				self.components_outer_normal_parameter_frame.frame, \
				text=["Preview","预览"][self.sd['language_id']],\
				width=int(self.sd['rletter']), height=1,fg=self.cd['mcfront'],\
				font=(self.sd['font'],self.sd['size']),\
				command=lambda:self.fun_outer_normal_preview(kind='excel'))
		else:
			self.components_outer_normal_import_data = tk.Button(\
				self.components_outer_normal_parameter_frame.frame, \
				text=["Preview","预览"][self.sd['language_id']],\
				width=int(self.sd['rletter']), height=1,fg=self.cd['front'],bg=self.cd['back'],\
				font=(self.sd['font'],self.sd['size']),\
				command=lambda:self.fun_outer_normal_preview(kind='excel'))
		self.components_outer_normal_parameter_excel.append(\
			self.components_outer_normal_import_data)

		# 分割线
		self.components_outer_normal_parameter_sep = ttk.Separator(\
			self.components_outer_normal_parameter_frame.frame,orient='horizontal')
		self.components_outer_normal_parameter_excel.append(\
			self.components_outer_normal_parameter_sep)

		# 数据处理参数选择提示
		self.components_outer_normal_parameter_tip2 = tk.Label(\
			self.components_outer_normal_parameter_frame.frame,\
			text=['Parameters of Data Processing','信息处理参数']\
			[self.sd['language_id']], width=int(self.sd['rletter']),\
			fg=self.cd['front'],bg=self.cd['back'],\
			font=(self.sd['font'],self.sd['size'],'bold'))
		self.components_outer_normal_parameter_excel.append(\
			self.components_outer_normal_parameter_tip2)
		
		# 占位(为了美观)
		self.components_outer_normal_parameter_placeholder = tk.Label(\
			self.components_outer_normal_parameter_frame.frame,\
			text='\n\n\n\n\n', width=int(self.sd['rletter']),\
			fg=self.cd['front'],bg=self.cd['back'],\
			font=(self.sd['font'],self.sd['size']))
		self.components_outer_normal_parameter_excel.append(\
			self.components_outer_normal_parameter_placeholder)

	def components_outer_normal_csv(self):
		""" 从csv文件中添加的参数 """
		# Interface interaction
		self.page2_1_csv = Page(self.window,self.sd,self.cd)

		# 各种参数输入的列表
		self.components_outer_normal_parameter_csv = IterationList(refresh=False)
		self.page2_1_csv.append(self.components_outer_normal_parameter_csv)

		# 帮助按钮
		if self.sd['system'] == 'Mac':
			self.components_outer_normal_help = tk.Button(\
				self.components_outer_normal_parameter_frame.frame,\
				text=["help","帮助"][self.sd['language_id']],\
				width=int(self.sd['rletter']), height=1,fg=self.cd['mcfront'],\
				font=(self.sd['font'],self.sd['size']),\
				command=lambda:self.fun_outer_normal_help(kind = 'csv'))
		else:
			self.components_outer_normal_help = tk.Button(\
				self.components_outer_normal_parameter_frame.frame,\
				text=["help","帮助"][self.sd['language_id']],\
				width=int(self.sd['rletter']), height=1,fg=self.cd['front'],bg=self.cd['back'],\
				font=(self.sd['font'],self.sd['size']),\
				command=lambda:self.fun_outer_normal_help(kind = 'csv'))
		self.components_outer_normal_parameter_csv.append(\
			self.components_outer_normal_help)

		# 导入参数选择提示
		self.components_outer_normal_parameter_csv_tip1 = tk.Label(\
			self.components_outer_normal_parameter_frame.frame,\
			text=['Parameters of Data Importing','信息导入参数']\
			[self.sd['language_id']], width=int(self.sd['rletter']),\
			fg=self.cd['front'],bg=self.cd['back'],\
			font=(self.sd['font'],self.sd['size'],'bold'))
		self.components_outer_normal_parameter_csv.append(\
			self.components_outer_normal_parameter_csv_tip1)

		# 参数-表名(excel) - sep
		items=['","']
		self.components_outer_normal_parameter_sep = FunctionalBlock(\
			self.components_outer_normal_parameter_frame.frame,\
			['sep:','分隔符:'][self.sd['language_id']], \
			self.sd,self.cd,items=items,locked=False,key='sep')
		self.components_outer_normal_parameter_csv.append(\
			self.components_outer_normal_parameter_sep)

		# 参数-表头行数(excel) - header
		items=['0','1','2,','3,','None',"['0', '1']"]
		self.components_outer_normal_parameter_header = FunctionalBlock(\
			self.components_outer_normal_parameter_frame.frame,\
			['header:','表头行数:'][self.sd['language_id']], \
			self.sd,self.cd,items=items,locked=False,key='header')
		self.components_outer_normal_parameter_csv.append(\
			self.components_outer_normal_parameter_header)

		# 参数-表头内容(excel) - names
		items=['None', "[0, 1, 2]",'[0]','[1]',"'A:E'","'A, C, E:F'"]
		self.components_outer_normal_parameter_names = FunctionalBlock(\
			self.components_outer_normal_parameter_frame.frame,\
			['names:','表头内容:'][self.sd['language_id']],\
			self.sd,self.cd,items=items,locked=False,key='names')
		self.components_outer_normal_parameter_csv.append(\
			self.components_outer_normal_parameter_names)

		# 参数-表头内容(excel) - index_col
		items=['None','0','1',"[0, 1]"]
		self.components_outer_normal_parameter_index_col = FunctionalBlock(\
			self.components_outer_normal_parameter_frame.frame,\
			['index_col:','行索引:'][self.sd['language_id']],\
			self.sd,self.cd,items=items,locked=False,key='index_col')
		self.components_outer_normal_parameter_csv.append(\
			self.components_outer_normal_parameter_index_col)

		# 参数-表头内容(excel) - usecols
		items=['None', "[0, 1, 2]",'[0]','[1]',"'A:E'","'A, C, E:F'"]
		self.components_outer_normal_parameter_usecols = FunctionalBlock(\
			self.components_outer_normal_parameter_frame.frame,\
			['usecols:','指定列:'][self.sd['language_id']],\
			self.sd,self.cd,items=items,locked=False,key='usecols')
		self.components_outer_normal_parameter_csv.append(\
			self.components_outer_normal_parameter_usecols)

		# 参数-表头内容(excel) - prefix
		items=['None', "X"]
		self.components_outer_normal_parameter_prefix = FunctionalBlock(\
			self.components_outer_normal_parameter_frame.frame,\
			['prefix:','列名前缀:'][self.sd['language_id']],\
			self.sd,self.cd,items=items,locked=False,key='prefix')
		self.components_outer_normal_parameter_csv.append(\
			self.components_outer_normal_parameter_prefix)

		# 参数-表头内容(excel) - prefix
		items=['None', "X"]
		self.components_outer_normal_parameter_prefix = FunctionalBlock(\
			self.components_outer_normal_parameter_frame.frame,\
			['prefix:','列名前缀:'][self.sd['language_id']],\
			self.sd,self.cd,items=items,locked=False,key='prefix')
		self.components_outer_normal_parameter_csv.append(\
			self.components_outer_normal_parameter_prefix)

		# 功能-导入数据
		if self.sd['system'] == 'Mac':
			self.components_outer_normal_import_data = tk.Button(\
				self.components_outer_normal_parameter_frame.frame, \
				text=["Preview","预览"][self.sd['language_id']],\
				width=int(self.sd['rletter']), height=1,fg=self.cd['mcfront'],\
				font=(self.sd['font'],self.sd['size']),\
				command=lambda:self.fun_outer_normal_preview(kind='csv'))
		else:
			self.components_outer_normal_import_data = tk.Button(\
				self.components_outer_normal_parameter_frame.frame, \
				text=["Preview","预览"][self.sd['language_id']],\
				width=int(self.sd['rletter']), height=1,fg=self.cd['front'],bg=self.cd['back'],\
				font=(self.sd['font'],self.sd['size']),\
				command=lambda:self.fun_outer_normal_preview(kind='csv'))
		self.components_outer_normal_parameter_csv.append(\
			self.components_outer_normal_import_data)

	def components_outer_normal_txt(self):
		""" 从txt文件中添加的参数 """
		# Interface interaction
		self.page2_1_txt = Page(self.window,self.sd,self.cd)
		# 各种参数输入的列表
		self.components_outer_normal_parameter_txt = IterationList(refresh=False)
		self.page2_1_txt.append(self.components_outer_normal_parameter_txt)

		# 帮助按钮
		if self.sd['system'] == 'Mac':
			self.components_outer_normal_help = tk.Button(\
				self.components_outer_normal_parameter_frame.frame,\
				text=["help","帮助"][self.sd['language_id']],\
				width=int(self.sd['rletter']), height=1,fg=self.cd['mcfront'],\
				font=(self.sd['font'],self.sd['size']),\
				command=lambda:self.fun_outer_normal_help(kind = 'txt'))
		else:
			self.components_outer_normal_help = tk.Button(\
				self.components_outer_normal_parameter_frame.frame,\
				text=["help","帮助"][self.sd['language_id']],\
				width=int(self.sd['rletter']), height=1,fg=self.cd['front'],bg=self.cd['back'],\
				font=(self.sd['font'],self.sd['size']),\
				command=lambda:self.fun_outer_normal_help(kind = 'txt'))
		self.components_outer_normal_parameter_txt.append(\
			self.components_outer_normal_help)

		# 导入参数选择提示
		self.components_outer_normal_parameter_txt_tip1 = tk.Label(\
			self.components_outer_normal_parameter_frame.frame,\
			text=['Parameters of Data Importing','信息导入参数']\
			[self.sd['language_id']], width=int(self.sd['rletter']),\
			fg=self.cd['front'],bg=self.cd['back'],\
			font=(self.sd['font'],self.sd['size'],'bold'))
		self.components_outer_normal_parameter_txt.append(\
			self.components_outer_normal_parameter_txt_tip1)

		# 参数-表名(excel) - sep
		items=['"  "']
		self.components_outer_normal_parameter_sep = FunctionalBlock(\
			self.components_outer_normal_parameter_frame.frame,\
			['sep:','分隔符:'][self.sd['language_id']], \
			self.sd,self.cd,items=items,locked=False,key='sep')
		self.components_outer_normal_parameter_txt.append(\
			self.components_outer_normal_parameter_sep)

		# 功能-导入数据
		if self.sd['system'] == 'Mac':
			self.components_outer_normal_import_data = tk.Button(\
				self.components_outer_normal_parameter_frame.frame, \
				text=["Preview","预览"][self.sd['language_id']],\
				width=int(self.sd['rletter']), height=1,fg=self.cd['mcfront'],\
				font=(self.sd['font'],self.sd['size']),\
				command=lambda:self.fun_outer_normal_preview(kind='txt'))
		else:
			self.components_outer_normal_import_data = tk.Button(\
				self.components_outer_normal_parameter_frame.frame, \
				text=["Preview","预览"][self.sd['language_id']],\
				width=int(self.sd['rletter']), height=1,fg=self.cd['front'],bg=self.cd['back'],\
				font=(self.sd['font'],self.sd['size']),\
				command=lambda:self.fun_outer_normal_preview(kind='txt'))
		self.components_outer_normal_parameter_txt.append(\
			self.components_outer_normal_import_data)

	def components_outer_database(self):
		""" 外部添加(数据库信息) 
			page2_2
		"""
		# Interface interaction
		self.page2_2 = Page(self.window,self.sd,self.cd)

	def components_outer_remind(self):
		""" 外部添加(提示信息) 
			page2_3
		"""
		# Interface interaction
		self.page2_3 = Page(self.window,self.sd,self.cd)

	def fun_outer_normal_hide(self):
		""" 隐藏模板选择框 """
		# 隐藏
		if self.components_outer_normal_hide_var.get() == \
			["Hide","隐藏"][self.sd['language_id']]:
			self.components_outer_normal_listbox.pack_forget()
			self.components_outer_normal_hide_var.set(\
				["Show","显示"][self.sd['language_id']])
		# 显示
		elif self.components_outer_normal_hide_var.get() == \
			["Show","显示"][self.sd['language_id']]:
			self.components_outer_normal_table.pack_forget()
			self.components_outer_normal_listbox.pack()
			self.components_outer_normal_hide_var.set(\
				["Hide","隐藏"][self.sd['language_id']])
			self.components_outer_normal_table.pack()

	def fun_outer_normal_file(self):
		""" 选择要导入的文件 """
		self.file_path = askopenfilename()
		if self.file_path == '': 
			self.file_path = None
			return False
		path_suffix = os.path.splitext(self.file_path)[-1]
		if path_suffix in ['.xlsx','.xlsm','.xlt','.xls','.et',\
			'.ett','.xltx','.xltm','xlsb','odf','ods','odt']:
			self.page2_1.change_page(current=0)
		elif path_suffix == '.csv':
			self.page2_1.change_page(current=1)
		elif path_suffix == '.txt':
			self.page2_1.change_page(current=2)
		else:
			messagebox.showinfo(parent=self.window,title='Wrong',\
				message=['Do not support: '+path_suffix,\
					'不支持当前格式: '+path_suffix][self.sd['language_id']])

	def fun_outer_normal_preview(self,kind):
		""" 导入数据 """
		if self.file_path == None: return False
		# 导入数据
		if kind == 'excel':
			kwargs={}
			for item in self.components_outer_normal_parameter_excel:
				if type(item) == FunctionalBlock:
					kwargs.update(item.get_key_value_pair())
			self.data = load_excel(self.file_path,**kwargs)
		elif kind == 'csv':
			kwargs={}
			for item in self.components_outer_normal_parameter_csv:
				if type(item) == FunctionalBlock:
					kwargs.update(item.get_key_value_pair())
			self.data = load_csv(self.file_path,**kwargs)
		elif kind == 'txt':
			kwargs={}
			for item in self.components_outer_normal_parameter_txt:
				if type(item) == FunctionalBlock:
					kwargs.update(item.get_key_value_pair())
			self.data = load_csv(self.file_path,**kwargs)
		# 展示数据
		self.components_outer_normal_table.clear_up_table(step=1)
		self.components_outer_normal_table.treeview.insert('', 'end',values=list(self.data.columns.values))
		for row in self.data.itertuples():
			self.components_outer_normal_table.treeview.insert('', 'end', values=list(row)[1:])
		self.components_outer_normal_table.clear_up_table(step=2)

	def fun_outer_normal_import(self,kind):
		""" """
		pass

	def fun_outer_normal_choose(self,event=None):
		""" 选择要添加的模板 """
		# 更改选中模板
		self.template_choosed_name = \
			self.components_outer_normal_listbox.get()
		# 查看模板类型(是否规定数据类型)
		self.template_choosed_type = get_template_detail(\
			self.sd['path'],name=self.template_choosed_name,onlyType=True)
		# 进行右侧输入框更改
		self.template_choosed_detail = get_template_detail(\
			self.sd['path'],name=self.template_choosed_name)

	def fun_outer_normal_help(self,event=None,kind='excel'):
		if kind == 'excel':
			title = ['read_excel_parameter_English',\
				'read_excel_parameter_简体中文'][self.sd['language_id']]
			self.testhelp = HelpUI(self.sd,self.cd,title=title)
		elif kind == 'csv':
			title = ['read_csv_parameter_English',\
				'read_csv_parameter_简体中文'][self.sd['language_id']]
			self.testhelp = HelpUI(self.sd,self.cd,title=title)
		elif kind == 'txt':
			title = ['read_txt_parameter_English',\
				'read_txt_parameter_简体中文'][self.sd['language_id']]
			self.testhelp = HelpUI(self.sd,self.cd,title=title)

	####################################
	# 第二层级: 内部添加 - 组件声明

	def components_inner_normal(self):
		""" 内部添加(普通信息) 
			page3_1
		"""
		# Interface interaction
		self.page3_1 = Page(self.window,self.sd,self.cd)

	def components_inner_database(self):
		""" 内部添加(数据库信息) 
			page3_2
		"""
		# Interface interaction
		self.page3_2 = Page(self.window,self.sd,self.cd)
