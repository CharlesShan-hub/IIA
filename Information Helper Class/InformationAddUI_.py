import tkinter as tk
import tkinter.ttk as ttk
from tool.Components import *
from tool.TemplatesTool import *
from tool.InfoAddCheckTool import *

class InformationAddUI():
	""" 信息添加模块
	功能:
		普通信息:  普通信息逐条添加, 普通信息通过excel等添加, 普通信息通过数据表添加
		数据表信息:数据表逐条添加信息,数据表通过excel等添加信息, 数据表通过普通信息添加
		提示信息:  提示信息逐条添加
	函数整理:
		###########################################################################################
		初始化:
			__init__                       初始化
		改变界面:
			back                           信息添加模块取消布局安放并返回信息模块主界面
		###########################################################################################
		主界面组件声明:
			components                     大标题与返回按钮,主框架与功能控制   --- components
		主界面安放与消除:
			pack                           信息添加模块布局安放             \
			pack_forget                    信息添加模块取消布局安放          |- 布局 (pack等+)
			destroy                        信息添加模块销毁布局             /
		###########################################################################################
		三种大模式组件声明:
			components_item                逐条添加(普通信息, 数据表信息, 提示信息)   \
			components_outer               外部添加(普通信息, 数据表信息)            | -  components_name
			components_inner               内部添加(普通信息, 数据表信息)            /
		三种大添加模式相关: - 'item','outer','inner'
			ui_init                        进入特定添加模式(逐条, 外部, 内部)     \
			ui_pack_forget_current         隐藏当前布局(逐条, 外部, 内部)        |-- 改变布局 (ui_+)
			ui_change                      改变切换模式(逐条, 外部, 内部)        /
			pack_item                      安放逐项添加模板                  \
			pack_outer                     安放逐项添加模板                  |
			pack_inner                     安放内部添加模板                  |- 布局_name (pack等+)
			pack_forget_item               隐藏逐项添加模板                  | 
			pack_forget_outer              隐藏外部添加模板                  |
			pack_forget_inner              隐藏内部添加模板                  |
			destroy_item                   销毁逐项添加模板                  |
			destroy_outer                  销毁外部添加模板                  |
			destroy_inner                  销毁内部添加模板                  /
		###########################################################################################
		逐条添加相关: - 'Normal','DataBase','Remind'
			ui_item_init                   逐条添加-进入特定添加模式   \
			ui_item_pack_forget_current    逐条添加-隐藏当前布局      |- 改变布局 (ui_item_+)
			ui_item_change_ui              逐条添加-更换内部布局      /
			pack_item_normal               逐条添加-普通信息-模板安放    \
			pack_item_database             逐条添加-数据库信息-模板安放  |
			pack_item_remind               逐条添加-提示信息-模板安放    |
			pack_forget_item_normal        逐条添加-普通信息-模板取消    |
			pack_forget_item_database      逐条添加-数据库信息-模板取消  |-- 布局_item_name (pack等+)
			pack_forget_item_remind        逐条添加-提示信息-模板取消    |
			destroy_item_normal            逐条添加-普通信息-模板销毁    |
			destroy_item_database          逐条添加-数据库信息-模板销毁  |
			destroy_item_remind            逐条添加-提示信息-模板销毁   /
			fun_item_normal_choose         获取用户选择的模板名      -逻辑功能
		###########################################################################################
		外部添加相关:
			info_init_outer                外部添加-进入特定添加模式
			pack_forget_current_outer      外部添加-隐藏当前布局
			info_change_ui_outer           外部添加-更换内部布局
		###########################################################################################
		内部添加相关:
			info_init_inner                内部添加-进入特定添加模式
			pack_forget_current_inner      内部添加-隐藏当前布局
			info_change_ui_inner           内部添加-更换内部布局
		###########################################################################################

	布局摆放方法:
		每一层级的单独组建都放到一个属于自己的列表中,
		比如 逐条添加-普通信息列表: self.info_item_normal_components_list
		不同层级的取消布局或销毁, 需要进行自己层级的
		组件列表的取消布局或销毁以及子层级的取消布局或销毁.

	组件名称整理:
		主界面 - components_title():
			self.title                                Label                主界面标题
			self.back                                 Button               返回按钮
		主界面框架与控制 - components_switchover():
			self.bframe                               BaseFrame            底层框架
			self.changeUI                             FunctionalBlock      切换界面('item','outer','inner')
		逐条添加 - components_item():
			self.components_list_item                 list                 构建组建列表
		逐条添加 - normal - components_item_normal()
			self.components_list_item_normal          list                 构建组建列表
			self.components_item_normal_listbox       NameListbox          模板选择窗
			self.components_item_normal_table         QuickTable           模板预览表格
			self.components_item_normal_sframe        ScrollCanvas         动态组件框
		逐条添加 - databse - components_item_database()
			self.components_list_item_database        list                 构建组建列表
		逐条添加 - remind - components_item_remind()
			self.components_list_item_remind          list                 构建组建列表
		外部添加 - components_outer():
			self.components_list_outer                list                 构建组建列表
		内部添加 - components_inner():
			self.components_list_inner                IterationList        构建组建列表

	变量整理:
		self.template_choosed                         str                  用户选择的模板名
	"""
	#####################################
	# 第零层级: 初始化模块

	def __init__(self, window, *args, **kwargs):
		""" 信息添加模块初始化 """
		# 设置与主窗口
		self.sd = args[0]
		self.cd = args[1]
		self.window = window
		# 查看进入某种模式 - 'item','outer','inner'
		self.add_mode = self.sd['info_insert_way']
		# 逐条添加默认添加模式 - 'Normal','DataBase','Remind'
		self.add_mode_item = 'Normal'
		# 组件声明
		self.components()

	def back(self):
		""" 信息添加模块取消布局安放并返回信息模块主界面 """
		# Interface interaction
		from InformationMainUI import InformationMainUI
		self.information_main = InformationMainUI(self.window,self.sd,self.cd)
		self.destroy()
		self.information_main.pack()

	#-----------------------------------#
	# 第零层级: 组件声明

	def components(self):
		""" 大标题与返回按钮,主框架与功能控制 """
		# Interface interaction
		# 大标题
		self.title = tk.Label(self.window,fg=self.cd['front'], \
			bg=self.cd['back'], font=(self.sd['font'],self.sd['tsize'],'bold'), \
			width=40, height=3, justify="left", anchor="center",\
			text=["INFORMATION     ADD\n","信息添加"][self.sd['language_id']])
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
		# 底层框架
		self.bframe = BaseFrame(self.window,self.sd,self.cd)
		# 功能切换框
		items = [['Add In Turn','Add from Outer','Add from Inner'],\
				 ['逐项添加','外部添加','内部添加']]
		self.changeUI = FunctionalBlock(self.bframe.rframe,['Add Way','添加方式'],\
			self.sd,self.cd,items=items[self.sd['language_id']])
		self.changeUI.combobox.bind("<<ComboboxSelected>>",self.ui_change)
		# 逐条添加-组件声明
		self.components_item()
		# 外部添加-组件声明
		self.components_outer()
		# 内部添加-组件声明
		self.components_inner()

	#----------------------------------#
	# 第零层级: 信息添加模块本身的安放与销毁

	def pack(self):
		""" 信息添加模块布局安放 """
		# Interface interaction
		self.title.pack()
		self.back.pack()
		self.bframe.pack()
		self.changeUI.pack()
		self.ui_init()

	def pack_forget(self):
		""" 信息添加模块取消布局安放 """
		# Interface interaction
		self.title.pack_forget()
		self.back.pack_forget()
		self.pack_forget_item()
		self.pack_forget_outer()
		self.pack_forget_inner()
		self.changeUI.pack_forget()
		self.bframe.pack_forget()

	def destroy(self):
		""" 信息添加模块销毁布局 """
		# Interface interaction
		self.title.destroy()
		self.back.destroy()
		self.destroy_item()
		self.destroy_outer()
		self.destroy_inner()
		self.changeUI.destroy()
		self.bframe.destroy()

	####################################
	# 第一层级: 组件声明

	def components_item(self):
		""" 逐条添加(普通信息, 数据表信息, 提示信息) """
		# Interface interaction
		#0 初始化变量
			# 用户选择的模板名
		self.template_choosed = None
			# 用户选择的模板的设置与细节
		self.template_choosed_detail = None
			# 用户输入是否正确
		self.components_item_normal_valid = False
		#1 逐条添加内容类型选择 - 公用组件
			# 构建组建列表
		self.components_list_item = []
			# 逐项信息添加模式 - 信息类型
		items = [['Normal Info','DataBase Info','Remind Info'],\
				 ['普通信息','数据库信息','提示信息']]
		self.item_info_type = FunctionalBlock(self.bframe.rframe,['Info Type','信息类型'],\
			self.sd,self.cd,items=items[self.sd['language_id']])
		self.item_info_type.combobox.bind("<<ComboboxSelected>>",self.ui_item_change)
		self.components_list_item.append(self.item_info_type)

		#2 逐条添加内容类型选择 - 普通信息
		self.components_item_normal()
		
		#3 逐条添加内容类型选择 - 数据库信息
		self.components_item_database()
		
		#4 逐条添加内容类型选择 - 提示信息
		self.components_item_remind()

	def components_outer(self):
		""" 外部添加(普通信息, 数据表信息) """
		# Interface interaction
		#1 逐条添加内容类型选择 - 公用组件
			# 构建组建列表
		self.components_list_outer = []

	def components_inner(self):
		""" 内部添加(普通信息, 数据表信息) """
		# Interface interaction
		#1 逐条添加内容类型选择 - 公用组件
			# 构建组建列表
		self.components_list_inner = []

	#---------------------------------#
	# 第一层级: 三种大添加模式相关: - 'item','outer','inner'

	def ui_init(self):
		""" 进入特定添加模式 """
		if self.add_mode == 'item':
			# 逐项添加
			self.pack_item()
		elif self.add_mode == 'outer':
			# 外部添加
			self.pack_outer()
		elif self.add_mode == 'inner':
			# 内部添加
			self.pack_inner()

	def ui_pack_forget_current(self):
		""" 隐藏当前布局 """ 
		if self.add_mode == 'item':
			self.pack_forget_item()
		elif self.add_mode == 'outer':
			self.pack_forget_outer()
		elif self.add_mode == 'inner':
			self.pack_forget_inner()

	def ui_change(self,event):
		""" 切换模式 """
		# 隐藏布局
		self.ui_pack_forget_current()
		# 查看进入某种模式
		self.add_mode = ['item','outer','inner'][self.changeUI.combobox.current()]
		# 安放新布局
		self.ui_init()

	def pack_item(self):
		""" 安放逐项添加模板 """
		self.item_info_type.pack()
		self.ui_item_init()

	def pack_outer(self):
		""" 安放外部添加模板 """
		self.ui_outer_init()

	def pack_inner(self):
		""" 安放内部添加模板 """
		self.ui_inner_init()

	def pack_forget_item(self):
		""" 隐藏逐项添加模板 """
		for item in self.components_list_item:
			item.pack_forget()
		self.pack_forget_item_normal()
		self.pack_forget_item_database()
		self.pack_forget_item_remind()
			# 用户选择的模板名
		self.template_choosed = None
			# 用户选择的模板的设置与细节
		self.template_choosed_detail = None

	def pack_forget_outer(self):
		""" 隐藏外部添加模板 """
		for item in self.components_list_outer:
			item.pack_forget()

	def pack_forget_inner(self):
		""" 隐藏内部添加模板 """
		for item in self.components_list_inner:
			item.pack_forget()

	def destroy_item(self):
		""" 销毁逐项添加模板 """
		for item in self.components_list_item:
			item.destroy()
		self.destroy_item_normal()
		self.destroy_item_database()
		self.destroy_item_remind()
			# 用户选择的模板名
		self.template_choosed = None
			# 用户选择的模板的设置与细节
		self.template_choosed_detail = None

	def destroy_outer(self):
		""" 销毁外部添加模板 """
		for item in self.components_list_outer:
			item.destroy()

	def destroy_inner(self):
		""" 销毁内部添加模板 """
		for item in self.components_list_inner:
			item.destroy()

	####################################
	# 第二层级: 逐条添加 - 组件声明

	def components_item_normal(self):
		""" 逐条添加(普通信息) """
		# 组建列表
		self.components_list_item_normal = []
		# 左侧模板选择框
		self.components_item_normal_listbox = NameListbox(self.bframe.lframe,self.sd,self.cd)
		self.components_item_normal_listbox.bind('<ButtonRelease-1>',self.fun_item_normal_choose)
		self.components_list_item_normal.append(self.components_item_normal_listbox)
		# 左侧模板预览
		self.components_item_normal_table = QuickTable(self.bframe.lframe,self.sd,self.cd)
		self.components_list_item_normal.append(self.components_item_normal_table)
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
		self.components_list_item_normal.append(self.components_item_normal_save)
		# 动态组件框
		self.components_item_normal_sframe = ScrollCanvas(self.bframe.rframe,self.sd,self.cd)
		self.components_list_item_normal.append(self.components_item_normal_sframe)
		# 信息添加区列表(类型提示与输入框)
		self.components_item_normal_list = IterationList()
		self.components_list_item_normal.append(self.components_item_normal_list)
		# 信息名称提示窗列表
		self.components_item_normal_list_name =  IterationList()
		self.components_list_item_normal.append(self.components_item_normal_list_name)
		# 保存信息
		self.components_item_normal_list_save = []

	def components_item_database(self):
		""" 逐条添加(数据库信息) """
		# 构建组建列表
		self.components_list_item_database = []

	def components_item_remind(self):
		""" 逐条添加(提示信息) """
		# 构建组建列表
		self.components_list_item_remind = []

	#-----------------------------------#
	# 第二层级: 逐条添加相关: - 'Normal','DataBase','Remind'
	
	def ui_item_init(self):
		""" 逐条添加-进入特定添加模式 """
		if self.add_mode_item == 'Normal':
			# 逐项添加
			self.pack_item_normal()
		elif self.add_mode_item == 'DataBase':
			# 外部添加
			self.pack_item_database()
		elif self.add_mode_item == 'Remind':
			# 内部添加
			self.pack_item_remind()

	def ui_item_pack_forget_current(self):
		""" 逐条添加-隐藏当前布局 """ 
		if self.add_mode_item == 'Normal':
			self.pack_forget_item_normal()
		elif self.add_mode_item == 'DataBase':
			self.pack_forget_item_database()
		elif self.add_mode_item == 'Remind':
			self.pack_forget_item_remind()

	def ui_item_change(self,event):
		""" 逐条添加-更换内部布局 """
		# 隐藏布局
		self.ui_item_pack_forget_current()
		# 获取当前逐条添加默认添加模式
		self.add_mode_item = ['Normal','DataBase','Remind'][self.item_info_type.combobox.current()]
		# 安放新布局
		self.ui_item_init()

	def pack_item_normal(self):
		""" 逐条添加-普通信息-模板安放 """
		self.components_item_normal_listbox.pack()
		self.components_item_normal_table.pack()
		self.components_item_normal_save.pack()
		self.components_item_normal_sframe.pack()

	def pack_item_database(self):
		""" 逐条添加-数据库信息-模板安放 """
		pass

	def pack_item_remind(self):
		""" 逐条添加-提示信息-模板安放 """
		pass

	def pack_forget_item_normal(self):
		""" 逐条添加-普通信息-模板取消 """
		for item in self.components_list_item_normal:
			item.pack_forget()

	def pack_forget_item_database(self):
		""" 逐条添加-数据库信息-模板取消 """
		for item in self.components_list_item_database:
			item.pack_forget()

	def pack_forget_item_remind(self):
		""" 逐条添加-提示信息-模板取消 """
		for item in self.components_list_item_remind:
			item.pack_forget()

	def destroy_item_normal(self):
		""" 逐条添加-普通信息-模板销毁 """
		for item in self.components_list_item_normal:
			item.destroy()

	def destroy_item_database(self):
		""" 逐条添加-数据库信息-模板销毁 """
		for item in self.components_list_item_database:
			item.destroy()

	def destroy_item_remind(self):
		""" 逐条添加-提示信息-模板销毁 """
		for item in self.components_list_item_remind:
			item.destroy()

	#----------------------------------#
	# 第二层级: 逐条添加: 特定功能

	def fun_item_normal_choose(self,event):
		""" 获取用户选择的模板名 """
		# 取消原有布局
		for item in self.components_item_normal_list_name:
			item.pack_forget()
		for item in self.components_item_normal_list:
			item.pack_forget()
		# 更改选中模板
		self.template_choosed = self.components_item_normal_listbox.get()
		# 查看模板类型(是否规定数据类型)
		template_type = get_template_detail(self.sd['path'],name=self.template_choosed,onlyType=True)
		# 进行右侧输入框更改
		self.template_choosed_detail = get_template_detail(self.sd['path'],self.template_choosed)
		for i in range(len(self.template_choosed_detail[0])):
			# 名称提示
			content_name = tk.Label(self.components_item_normal_sframe.frame,fg=self.cd['front'],\
				bg=self.cd['back'], font=(self.sd['font'],self.sd['size']), text=self.template_choosed_detail[0][i])
			content_name.pack()
			self.components_item_normal_list_name.append(content_name)
			# 输入框
			if template_type:
				content = FunctionalBlock(self.components_item_normal_sframe.frame,\
					''+self.template_choosed_detail[1][i]+':', self.sd,self.cd,kind='entry')
			else:
				content = FunctionalBlock(self.components_item_normal_sframe.frame,\
					['Any Type:','任意类型:'][self.sd['language_id']], self.sd,self.cd,kind='entry')
			content.pack()
			self.components_item_normal_list.append(content)

	def fun_item_normal_save_check(self):
		""" 保存信息-检查 """
		# 模板约束条件
		template_type = get_template_detail(self.sd['path'],name=self.template_choosed,onlyType=True)
		# 是否需要约束
		if template_type == False:
			print('无需进行模板类型检查')
			return True
		# 信息列表
		self.components_item_normal_list_save = []
		for item in self.components_item_normal_list:
			self.components_item_normal_list_save.append(item.entry.get())
		# 信息判断与修改
		self.components_item_normal_list_save = \
			fun_item_normal_save_check_and_change(\
				self.components_item_normal_list_save,template_type)

	def fun_item_normal_save(self):
		""" 保存信息 """

		# 是否进行信息选择
		if len(self.components_item_normal_list) < 1: return False
		# 信息输入合法性判断
		self.fun_item_normal_save_check()
		# 进行信息保存
		if self.components_item_normal_list_save!= False:
			for item in self.components_item_normal_list_save:
				print(item)

	####################################
	# 第二层级: 外部添加 - 组件声明

	#def components_outer_???(self):

	#----------------------------------#
	# 第二层级: 外部添加相关: - ['表格'(有选择表单等等),'数据集']添加到'Normal','DataBase'
	def ui_outer_init(self):
		""" 外部添加-进入特定添加模式 """
		pass

	def ui_outer_pack_forget_current(self):
		""" 外部添加-隐藏当前布局 """
		pass

	def ui_outer_change(self,event):
		""" 外部添加-更换内部布局 """
		pass

	####################################
	# 第二层级: 内部添加 - 组件声明

	#def components_inner_???(self):

	#----------------------------------#
	# 第二层级: 内部添加相关
	def ui_inner_init(self):
		""" 内部添加-进入特定添加模式 """
		pass

	def ui_inner_pack_forget_current(self):
		""" 内部添加-隐藏当前布局 """
		pass

	def ui_inner_change(self,event):
		""" 内部添加-更换内部布局 """
		pass

#help(InformationAddUI)
