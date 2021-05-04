import tkinter as tk
import tkinter.ttk as ttk
import tkinter.scrolledtext as scrolledtext
from tkinter import messagebox
from tool.Path import *
from tool.Components import *
from tool.TemplatesTool import save_new_template
from help.HelpSqliteDataType import *
from help.HelpTemplate import *

class TemplatesAddUI():
	""" 模板添加模块
	功能: 
		普通模板的添加 - 逐项添加, 根据数据库模版转换 
		数据库模板(数据表)的添加 - 逐项添加(手动输入边界条件), SQL语句创建, 普通模板+边界条件转换
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
		两种大模式组件声明: (normal,database)
			components_normal              普通信息模板
			components_database            数据库数据表
		两大添加模式相关: - 'normal','inner'
			ui_init                        进入特定添加模式                    \
			ui_pack_forget_current         隐藏当前布局                        |-- 改变布局 (ui_+)
			ui_change                      改变切换模式                        /
			pack_normal                    安放添加普通模板                 \
			pack_database                  安放添加数据库模板                |
			pack_forget_normal             隐藏添加普通模板                  |-- 布局_name (pack等+)
			pack_forget_database           隐藏添加数据库模板                |
			destroy_normal                 销毁添加普通模板                 |
			destroy_database               销毁添加数据库模板               /
	"""
	#####################################
	# 第零层级: 初始化模块
	def __init__(self, window, *args, **kwargs):
		""" 初始化 """
		# 设置与主窗口
		self.sd = args[0]
		self.cd = args[1]
		self.window = window
		# 查看进入某种模式 - 'normal','database'
		self.add_mode = 'normal'
		# 普通模板默认添加模式 - 'item','inner'
		self.add_mode_normal = 'item'
		# 数据表默认添加模式 - 'item','inner'
		self.add_mode_database = 'item'

		# 组件
		self.components()

	def back(self):
		""" 返回 """
		from TemplatesMainUI import TemplatesMainUI
		self.templates_main = TemplatesMainUI(self.window,self.sd,self.cd)
		self.destroy()
		self.templates_main.pack()

	#-----------------------------------#
	# 第零层级: 组件声明

	def components(self):
		""" 主界面组件声明 """
		# 主界面布局
		self.title = tk.Label(self.window,fg=self.cd['front'], bg=self.cd['back'],\
			font=(self.sd['font'],self.sd['tsize'],'bold'),\
			width=40, height=3, justify="left", anchor="center",\
			text=["TEMPLATE     ADD\n","模板添加"][self.sd['language_id']])
		if self.sd['system'] == 'Mac':
			self.back = tk.Button(self.window, text=["Back to last level","返回上一级"][self.sd['language_id']],\
				command=self.back, width=20, height=2,fg=self.cd['mcfront'],\
				font=(self.sd['font'],self.sd['size']))
		else:
			self.back = tk.Button(self.window, text=["Back to last level","返回上一级"][self.sd['language_id']],\
				command=self.back, width=20, height=2,fg=self.cd['front'],bg=self.cd['back'],\
				font=(self.sd['font'],self.sd['size']))
		# 底层框架
		self.bframe = BaseFrame(self.window,self.sd,self.cd)
		# 功能切换框
		items = [['Add Templates','Add Data Sheets'],['添加模板','添加数据表']]
		self.changeUI = FunctionalBlock(self.bframe.rframe,['Add Type','添加类型'],\
			self.sd,self.cd,items=items[self.sd['language_id']])
		self.changeUI.combobox.bind("<<ComboboxSelected>>",self.ui_change)

		# 组件-普通模板
		self.components_normal()

		# 组件-数据表
		self.components_database()

	#----------------------------------#
	# 第零层级: 信息添加模块本身的安放与销毁

	def pack(self):
		self.title.pack()
		self.back.pack()
		self.bframe.pack()
		self.changeUI.pack()
		self.ui_init()

	def pack_forget(self):
		self.title.pack_forget()
		self.back.pack_forget()
		self.bframe.pack_forget()
		self.changeUI.pack_forget()
		self.pack_forget_normal()
		self.pack_forget_database()

	def destroy(self):
		self.title.destroy()
		self.back.destroy()
		self.bframe.destroy()
		self.changeUI.destroy()
		self.destroy_normal()
		self.destroy_database()

	####################################
	# 第一层级: 组件声明

	def components_normal(self):
		""" 组件-普通模板 """
		#1 逐条添加内容类型选择 - 公用组件
			# 构建组建列表
		self.components_list_normal = []
			# 逐项信息添加模式 - 信息类型
		items = [['Item Insert','Inner Insert'],['逐项添加','内部添加']]
		self.item_temp_from = FunctionalBlock(self.bframe.rframe,['Add Way','添加方式'],\
			self.sd,self.cd,items=items[self.sd['language_id']])
		self.item_temp_from.combobox.bind("<<ComboboxSelected>>",self.ui_normal_change)
		self.components_list_normal.append(self.item_temp_from)
		# 2
		self.components_normal_item()
		# 3
		self.components_normal_inner()

	def components_database(self):
		""" 组件-数据表 """
		#1 逐条添加内容类型选择 - 公用组件
			# 构建组建列表
		self.components_list_database = []
			# 逐项信息添加模式 - 信息类型
		items = [['Item Insert','Inner Insert'],['逐项添加','内部添加']]
		self.item_db_from = FunctionalBlock(self.bframe.rframe,['Add Way','添加方式'],\
			self.sd,self.cd,items=items[self.sd['language_id']])
		self.item_db_from.combobox.bind("<<ComboboxSelected>>",self.ui_database_change)
		self.components_list_database.append(self.item_db_from)
		# 2
		self.components_database_item()
		# 3
		self.components_database_inner()

	#---------------------------------#
	# 第一层级: 2种大添加模式相关: - 'normal','database'

	def ui_init(self):
		""" 进入特定添加模式 """
		if self.add_mode == 'normal':
			# 逐项添加
			self.pack_normal()
		elif self.add_mode == 'database':
			# 内部添加
			self.pack_database()

	def ui_pack_forget_current(self):
		""" 隐藏当前布局 """ 
		if self.add_mode == 'normal':
			self.pack_forget_normal()
		elif self.add_mode == 'database':
			self.pack_forget_database()

	def ui_change(self,event):
		""" 切换模式 """
		# 隐藏布局
		self.ui_pack_forget_current()
		# 查看进入某种模式
		self.add_mode = ['normal','database'][self.changeUI.combobox.current()]
		# 安放新布局
		self.ui_init()

	def pack_normal(self):
		""" 安放添加普通模板 """
		self.item_temp_from.pack()
		self.ui_normal_init()

	def pack_database(self):
		""" 安放添加数据库模板 """
		self.item_db_from.pack()
		self.ui_database_init()

	def pack_forget_normal(self):
		""" 隐藏添加普通模板 """
		for item in self.components_list_normal:
			item.pack_forget()
		self.pack_forget_normal_item()
		self.pack_forget_normal_inner()

	def pack_forget_database(self):
		""" 隐藏添加数据库模板 """
		for item in self.components_list_database:
			item.pack_forget()
		self.pack_forget_database_item()
		self.pack_forget_database_inner()

	def destroy_normal(self):
		""" 销毁添加普通模板 """
		for item in self.components_list_normal:
			item.destroy()
		self.destroy_normal_item()
		self.destroy_normal_inner()

	def destroy_database(self):
		""" 销毁添加数据库模板 """
		for item in self.components_list_database:
			item.destroy()
		self.destroy_database_item()
		self.destroy_database_inner()

	####################################
	# 第二层级: 普通模板 - 组件声明

	def components_normal_item(self):
		""" 普通模板-逐条添加 """
		# 逐条添加内容类型选择 - 公用组件
			# 构建组建列表
		self.components_list_normal_item = []

		# 添加项目
		if self.sd['system'] == 'Mac':
			self.components_normal_item_add = tk.Button(self.bframe.rframe, \
				text=["Add Item","添加输入框"][self.sd['language_id']],\
				width=int(self.sd['rletter']), height=1,fg=self.cd['mcfront'],\
				font=(self.sd['font'],self.sd['size']),\
				command=self.fun_normal_item_add)
		else:
			self.components_normal_item_add = tk.Button(self.bframe.rframe, \
				text=["Add Item","添加输入框"][self.sd['language_id']],\
				width=int(self.sd['rletter']), height=1,fg=self.cd['front'],bg=self.cd['back'],\
				font=(self.sd['font'],self.sd['size']),\
				command=self.fun_normal_item_add)
		self.components_list_normal_item.append(self.components_normal_item_add)

		# 减少项目
		if self.sd['system'] == 'Mac':
			self.components_normal_item_reduce = tk.Button(self.bframe.rframe, \
				text=["Reduce Item","减少输入框"][self.sd['language_id']],\
				width=int(self.sd['rletter']), height=1,fg=self.cd['mcfront'],\
				font=(self.sd['font'],self.sd['size']),\
				command=self.fun_normal_item_reduce)
		else:
			self.components_normal_item_reduce = tk.Button(self.bframe.rframe, \
				text=["Reduce Item","减少输入框"][self.sd['language_id']],\
				width=int(self.sd['rletter']), height=1,fg=self.cd['front'],bg=self.cd['back'],\
				font=(self.sd['font'],self.sd['size']),\
				command=self.fun_normal_item_reduce)
		self.components_list_normal_item.append(self.components_normal_item_reduce)

		# 保存
		if self.sd['system'] == 'Mac':
			self.components_normal_item_save = tk.Button(self.bframe.rframe, \
				text=["Save","保存"][self.sd['language_id']],\
				width=int(self.sd['rletter']), height=1,fg=self.cd['mcfront'],\
				font=(self.sd['font'],self.sd['size']),\
				command=self.fun_normal_item_save)
		else:
			self.components_normal_item_save = tk.Button(self.bframe.rframe, \
				text=["Save","保存"][self.sd['language_id']],\
				width=int(self.sd['rletter']), height=1,fg=self.cd['front'],bg=self.cd['back'],\
				font=(self.sd['font'],self.sd['size']),\
				command=self.fun_normal_item_save)
		self.components_list_normal_item.append(self.components_normal_item_save)

		# 合法性
		self.components_normal_item_valid = False

		# 滚动条框架
		self.components_normal_item_sframe = ScrollCanvas(self.bframe.rframe,self.sd,self.cd)
		self.components_list_normal_item.append(self.components_normal_item_sframe)

		# 添加窗口列表
		self.components_normal_item_list = IterationList()
		self.components_list_normal_item.append(self.components_normal_item_list)

		# 填写模板名称
		self.components_normal_item_name = FunctionalBlock(self.components_normal_item_sframe.frame,\
			['Name:','模板名:'], self.sd,self.cd,kind='entry')
		self.components_list_normal_item.append(self.components_normal_item_name)

		# 添加窗口类型列表
		self.components_normal_item_type_list = IterationList()
		self.components_list_normal_item.append(self.components_normal_item_type_list)

		# 分隔符列表
		self.components_normal_item_sep_list = IterationList()
		self.components_list_normal_item.append(self.components_normal_item_sep_list)

		# 帮助选择复选窗-框架
		items = [['Data Type','Template'],['数据类型','模板']]
		self.components_normal_item_help_frame = tk.Frame(self.bframe.lframe)
		self.components_list_normal_item.append(self.components_normal_item_help_frame)

		# 帮助选择下拉列表
		self.components_normal_item_help_combobox = ttk.Combobox(self.components_normal_item_help_frame,\
			width=int(self.sd['lletter']*1/5),font=(self.sd['font'],self.sd['size']))
		self.components_normal_item_help_combobox['value'] = items[self.sd['language_id']]
		self.components_normal_item_help_combobox.current(0)
		self.components_normal_item_help_combobox.bind("<<ComboboxSelected>>",self.fun_normal_item_help)
		self.components_list_normal_item.append(self.components_normal_item_help_combobox)

		# 帮助选择搜索窗
		self.components_normal_item_help_entry = tk.Entry(self.components_normal_item_help_frame,\
			width=int(self.sd['lletter']*4/5),font=(self.sd['font'],self.sd['size']),\
			fg=self.cd['front'],bg=self.cd['tback2'])
		self.components_list_normal_item.append(self.components_normal_item_help_entry)

		# 帮助文字中显示窗
		self.components_normal_item_help_text = scrolledtext.ScrolledText(self.bframe.lframe,\
			fg=self.cd['front'],bg=self.cd['back'])
		self.fun_normal_item_help()
		self.components_list_normal_item.append(self.components_normal_item_help_text)

	def components_normal_inner(self):
		""" 普通模板-内部添加 """
		#1 逐条添加内容类型选择 - 公用组件
			# 构建组建列表
		self.components_list_normal_inner = []

		# 添加项目

	#-----------------------------------#
	# 第二层级: 普通模板: 功能函数

	def fun_normal_item_add(self):
		""" 添加输入框 """
		# 分割线
		add_item_sep = ttk.Separator(self.components_normal_item_sframe.frame,orient='horizontal')
		add_item_sep.pack(fill='x')
		self.components_normal_item_sep_list.append(add_item_sep)

		# 输入模板项目名称
		add_item = FunctionalBlock(self.components_normal_item_sframe.frame,['Item:','项目:'],\
			self.sd,self.cd,kind='entry')
		add_item.pack()
		self.components_normal_item_list.append(add_item)

		# 选择输入数据类型
		items = [
			['unset','bit','int','char','text','float','real','smallint','tinyint',\
				'numeric','decimal','money','smallmoney',\
				'datetime','smalldatetime','cursor','timestamp','Uniqueidentifier',\
				'varchar','nchar','nvarchar','ntext','binary','varbinary','image'],\
			['不设置','bit','int','char','text','float','real','smallint','tinyint',\
				'numeric','decimal','money','smallmoney',\
				'datetime','smalldatetime','cursor','timestamp','Uniqueidentifier',\
				'varchar','nchar','nvarchar','ntext','binary','varbinary','image']]
		add_item_type = FunctionalBlock(self.components_normal_item_sframe.frame,['Item Type:','项目类型:'],\
			self.sd,self.cd,items=items[self.sd['language_id']])
		add_item_type.pack()
		self.components_normal_item_type_list.append(add_item_type)

	def fun_normal_item_reduce(self):
		""" 减少输入框 """
		if len(self.components_normal_item_list):
			self.components_normal_item_list.pop().destroy()
			self.components_normal_item_sep_list.pop().destroy()
			self.components_normal_item_type_list.pop().destroy()

	def fun_normal_item_save_check(self):
		""" 保存前的检查 """
		self.components_normal_item_valid=[]
		# 检查模板名称
		# 模板不能只有空格
		tname = self.components_normal_item_name.entry.get().strip()
		if tname == '':
			messagebox.showinfo(parent=self.window,title='Wrong',\
				message=['Template names cannot contain Spaces only',\
					'模板名中不能只有空格'][self.sd['language_id']])
			self.components_normal_item_valid=False
		if tname == 'template':
			messagebox.showinfo(parent=self.window,title='Wrong',\
				message=['Template names cannot be '+tname,\
					'模板名不可以为'+tname][self.sd['language_id']])
			self.components_normal_item_valid=False
		# 模板不能有非法字符
		invalid = ['\\', '/', ':', '*', '?', '"', '<', '>', '|']
		for char_ in invalid:
			if char_ in tname:
				messagebox.showinfo(parent=self.window,title='Wrong',\
					message=["'"+char_+"'' shouldn't in template name",'模板名中不能有:'\
						+char_][self.sd['language_id']])
				self.components_normal_item_valid=False

		# 检查内容
		# 项目名不能为0
		if len(self.components_normal_item_list) < 1:
			messagebox.showinfo(parent=self.window,title='Wrong',\
				message=['Should have at least one project',\
				'至少要有一个项目'][self.sd['language_id']])
			self.components_normal_item_valid=False
		# 项目名框中不能为空
		for item in self.components_normal_item_list:
			if item.entry.get().strip() == '':
				self.components_normal_item_valid.append('empty')
				break
		for item in self.components_normal_item_type_list:
			if item.combobox.current() == 0:
				self.components_normal_item_valid.append('none type')
				break

	def fun_normal_item_save(self):
		""" 保存 """
		# 合法性确认
		self.fun_normal_item_save_check()
		if self.components_normal_item_valid == False:
			return False
		if 'empty' in self.components_normal_item_valid:
			if messagebox.askyesno(parent=self.window,title='Attention',\
					message=['There are empty characters in your template, '\
					'do you want to go ahead and add?',\
					'您的模板中有空字符, 您继续要添加吗?'][self.sd['language_id']]) == False:
				return False
		if 'none type' in self.components_normal_item_valid:
			if messagebox.askyesno(parent=self.window,title='Attention',\
					message=['Your template type is unset data type, '\
					'do you want to continue to add?',\
					'您的模板类型为未设置数据类型, 您要继续添加吗?']\
					[self.sd['language_id']]) == False:
				return False

		# 获取不重名模板名称
		tname=un_repeat_name(self.components_normal_item_name.entry.get().strip(),\
			path=self.sd['path']+'/resources/system/template/template.csv',_from='template')

		# 构建数据模板
		tem_list = []
		for item in range(len(self.components_normal_item_list)):
			tem_list.append(self.components_normal_item_list[item].entry.get().strip())
		tem_list_type = []
		if 'none type' in self.components_normal_item_valid:
			tem_list_type = None
		else:
			for item in range(len(self.components_normal_item_type_list)):
				tem_list_type.append(self.components_normal_item_type_list[item].combobox.get())

		# 最后询问是否添加
		if messagebox.askyesno(parent=self.window,title='Attention',\
				message=['You are about to add the template '+tname,\
				'您即将添加模板'+tname][self.sd['language_id']]) == False:
			return False

		# 进行模板保存
		save_new_template(self.sd['path'],tname,tem_list,tem_list_type)

		# 布局清理
		while len(self.components_normal_item_list):
			self.components_normal_item_list.pop().destroy()
			self.components_normal_item_sep_list.pop().destroy()
			self.components_normal_item_type_list.pop().destroy()
		self.components_normal_item_name.entry.delete(0,'end')

	def fun_normal_item_help(self,event=None):
		""" 显示帮助 """
		# 清空帮助文档区
		self.components_normal_item_help_text.delete(0.0,'end')
		# 数据类型介绍
		if self.components_normal_item_help_combobox.current() == 0:
			if self.sd['language']=='简体中文': 
				path = self.sd['path'] + '/help/sqlite data type (简体中文).csv'
			elif self.sd['language']=='English': 
				path = self.sd['path'] + '/help/sqlite data type (English).csv'
			help_sqlite_datatype(self.components_normal_item_help_text,path,self.sd,self.cd)
		# ‘模板’本身介绍
		elif self.components_normal_item_help_combobox.current() == 1:
			help_template(self.components_normal_item_help_text,self.sd,self.cd)

	#-----------------------------------#
	# 第二层级: 普通模板: - 'item','database'

	def ui_normal_init(self):
		""" 普通模板-进入特定添加模式 """
		if self.add_mode_normal == 'item':
			# 逐项添加
			self.pack_normal_item()
		elif self.add_mode_normal == 'inner':
			# 内部添加
			self.pack_normal_inner()

	def ui_normal_pack_forget_current(self):
		""" 普通模板-隐藏当前布局 """
		if self.add_mode_normal == 'item':
			# 逐项添加
			self.pack_forget_normal_item()
		elif self.add_mode_normal == 'inner':
			# 内部添加
			self.pack_forget_normal_inner()

	def ui_normal_change(self,event):
		""" 普通模板-更换内部布局 """
		# 隐藏布局
		self.ui_normal_pack_forget_current()
		# 查看进入某种模式
		self.add_mode_normal = ['item','inner'][self.item_temp_from.combobox.current()]
		# 安放新布局
		self.ui_normal_init()

	def pack_normal_item(self):
		""" 安放添加普通模板 - 逐项添加 """
		self.components_normal_item_add.pack()
		self.components_normal_item_reduce.pack()
		self.components_normal_item_save.pack()
		self.components_normal_item_sframe.pack()
		self.components_normal_item_name.pack()
		self.components_normal_item_help_frame.pack(side='top')
		self.components_normal_item_help_combobox.pack(side='right')
		self.components_normal_item_help_entry.pack(fill='x',expand=True,side='right')
		self.components_normal_item_help_text.pack(fill='both',expand=True)

	def pack_normal_inner(self):
		""" 安放添加数据库模板 - 内部添加 """
		pass

	def pack_forget_normal_item(self):
		""" 隐藏添加普通模板 - 逐项添加 """
		for item in self.components_list_normal_item:
			item.pack_forget()

	def pack_forget_normal_inner(self):
		""" 隐藏添加数据库模板 - 内部添加 """
		for item in self.components_list_normal_inner:
			item.pack_forget()

	def destroy_normal_item(self):
		""" 销毁添加普通模板 - 逐项添加 """
		for item in self.components_list_normal_item:
			item.destroy()

	def destroy_normal_inner(self):
		""" 销毁添加数据库模板 - 内部添加 """
		for item in self.components_list_normal_inner:
			item.destroy()

	####################################
	# 第二层级: 数据库添加 - 组件声明

	def components_database_item(self):
		""" """
		# 逐条添加内容类型选择 - 公用组件
			# 构建组建列表
		self.components_list_database_item = []

		# 添加项目
		if self.sd['system'] == 'Mac':
			self.components_database_item_add = tk.Button(self.bframe.rframe, \
				text=["Add Item","添加输入框"][self.sd['language_id']],\
				width=int(self.sd['rletter']), height=1,fg=self.cd['mcfront'],\
				font=(self.sd['font'],self.sd['size']),\
				command=self.fun_database_item_add)
		else:
			self.components_database_item_add = tk.Button(self.bframe.rframe, \
				text=["Add Item","添加输入框"][self.sd['language_id']],\
				width=int(self.sd['rletter']), height=1,fg=self.cd['front'],bg=self.cd['back'],\
				font=(self.sd['font'],self.sd['size']),\
				command=self.fun_database_item_add)
		self.components_list_database_item.append(self.components_database_item_add)

		# 减少项目
		if self.sd['system'] == 'Mac':
			self.components_database_item_reduce = tk.Button(self.bframe.rframe, \
				text=["Reduce Item","减少输入框"][self.sd['language_id']],\
				width=int(self.sd['rletter']), height=1,fg=self.cd['mcfront'],\
				font=(self.sd['font'],self.sd['size']),\
				command=self.fun_database_item_reduce)
		else:
			self.components_database_item_reduce = tk.Button(self.bframe.rframe, \
				text=["Reduce Item","减少输入框"][self.sd['language_id']],\
				width=int(self.sd['rletter']), height=1,fg=self.cd['front'],bg=self.cd['back'],\
				font=(self.sd['font'],self.sd['size']),\
				command=self.fun_database_item_reduce)
		self.components_list_database_item.append(self.components_database_item_reduce)

		# 保存
		if self.sd['system'] == 'Mac':
			self.components_database_item_save = tk.Button(self.bframe.rframe, \
				text=["Save","保存"][self.sd['language_id']],\
				width=int(self.sd['rletter']), height=1,fg=self.cd['mcfront'],\
				font=(self.sd['font'],self.sd['size']),\
				command=self.fun_database_item_save)
		else:
			self.components_database_item_save = tk.Button(self.bframe.rframe, \
				text=["Save","保存"][self.sd['language_id']],\
				width=int(self.sd['rletter']), height=1,fg=self.cd['front'],bg=self.cd['back'],\
				font=(self.sd['font'],self.sd['size']),\
				command=self.fun_database_item_save)
		self.components_list_database_item.append(self.components_database_item_save)

		# 合法性
		self.components_database_item_valid = False

		# 滚动条框架
		self.components_database_item_sframe = ScrollCanvas(self.bframe.rframe,self.sd,self.cd)
		self.components_list_database_item.append(self.components_database_item_sframe)

		# 添加窗口列表
		self.components_database_item_list = IterationList()
		self.components_list_database_item.append(self.components_database_item_list)

		# 填写模板名称
		self.components_database_item_name = FunctionalBlock(self.components_database_item_sframe.frame,\
			['Name:','模板名:'], self.sd,self.cd,kind='entry')
		self.components_list_database_item.append(self.components_database_item_name)

		# 添加窗口类型列表
		self.components_database_item_type_list = IterationList()
		self.components_list_database_item.append(self.components_database_item_type_list)

		# 分隔符列表
		self.components_database_item_sep_list = IterationList()
		self.components_list_database_item.append(self.components_database_item_sep_list)

		# 左侧数据库选择窗
		self.components_database_item_sheet_choose = NameListbox(\
			self.bframe.lframe,self.sd,self.cd,kind='sheet')
		self.components_list_database_item.append(self.components_database_item_sheet_choose)

		# 左侧帮助内容框架
		self.components_database_item_lframe1 = tk.Frame(self.bframe.lframe)
		self.components_database_item_lframe2 = tk.Frame(self.components_database_item_lframe1)
		self.components_list_database_item.append(self.components_database_item_lframe1)
		self.components_list_database_item.append(self.components_database_item_lframe2)

		# 帮助选择下拉列表
		items = [['Data Type','Template'],['数据类型','模板']]
		self.components_database_item_help_combobox = ttk.Combobox(self.components_database_item_lframe2,\
			width=int(self.sd['lletter']*1/5),font=(self.sd['font'],self.sd['size']))
		self.components_database_item_help_combobox['value'] = items[self.sd['language_id']]
		self.components_database_item_help_combobox.current(0)
		#self.components_database_item_help_combobox.bind("<<ComboboxSelected>>",self.fun_normal_item_help)
		self.components_list_database_item.append(self.components_database_item_help_combobox)

		# 帮助选择搜索窗
		self.components_database_item_help_entry = tk.Entry(self.components_database_item_lframe2,\
			font=(self.sd['font'],self.sd['size']),fg=self.cd['front'],bg=self.cd['tback2'])
		self.components_list_database_item.append(self.components_database_item_help_entry)

		# 左侧帮助文字中显示窗
		self.components_database_item_help_text = scrolledtext.ScrolledText(self.components_database_item_lframe1,\
			fg=self.cd['front'],bg=self.cd['back'])
		self.fun_normal_item_help()
		self.components_list_database_item.append(self.components_database_item_help_text)

	def components_database_inner(self):
		""" """
		# 逐条添加内容类型选择 - 公用组件
			# 构建组建列表
		self.components_list_database_inner = []

	#-----------------------------------#
	# 第二层级: 数据库模板: 功能函数

	def fun_database_item_add(self):
		""" 数据库数据表逐项添加-增加数据项 """
		# 分割线
		add_item_sep = ttk.Separator(self.components_database_item_sframe.frame,orient='horizontal')
		add_item_sep.pack(fill='x')
		self.components_database_item_sep_list.append(add_item_sep)

		# 输入模板项目名称
		add_item = FunctionalBlock(self.components_database_item_sframe.frame,['Item:','项目:'],\
			self.sd,self.cd,kind='entry')
		add_item.pack()
		self.components_database_item_list.append(add_item)

		# 选择输入数据类型
		items = [
			['bit','int','char','text','float','real','smallint','tinyint',\
				'numeric','decimal','money','smallmoney',\
				'datetime','smalldatetime','cursor','timestamp','Uniqueidentifier',\
				'varchar','nchar','nvarchar','ntext','binary','varbinary','image'],\
			['bit','int','char','text','float','real','smallint','tinyint',\
				'numeric','decimal','money','smallmoney',\
				'datetime','smalldatetime','cursor','timestamp','Uniqueidentifier',\
				'varchar','nchar','nvarchar','ntext','binary','varbinary','image']]
		add_item_type = FunctionalBlock(self.components_database_item_sframe.frame,['Item Type:','项目类型:'],\
			self.sd,self.cd,items=items[self.sd['language_id']])
		add_item_type.pack()
		self.components_database_item_type_list.append(add_item_type)

	def fun_database_item_reduce(self):
		""" 数据库数据表逐项添加-减少数据项 """
		if len(self.components_database_item_list):
			self.components_database_item_list.pop().destroy()
			self.components_database_item_sep_list.pop().destroy()
			self.components_database_item_type_list.pop().destroy()

	def fun_database_item_save_valid(self):
		""" """
		pass

	def fun_database_item_save(self):
		""" 数据库数据表逐项添加-保存 """
		self.fun_database_item_save_valid()

	#-----------------------------------#
	# 第二层级: 数据库模板: - 'item','database'

	def ui_database_init(self):
		""" 数据库模板-进入特定添加模式 """
		if self.add_mode_database == 'item':
			# 逐项添加
			self.pack_database_item()
		elif self.add_mode_database == 'inner':
			# 内部添加
			self.pack_database_inner()

	def ui_database_pack_forget_current(self):
		""" 数据库模板-隐藏当前布局 """
		if self.add_mode_database == 'item':
			# 逐项添加
			self.pack_forget_database_item()
		elif self.add_mode_database == 'inner':
			# 内部添加
			self.pack_forget_database_inner()

	def ui_database_change(self,event):
		""" 数据库模板-更换内部布局 """
		# 隐藏布局
		self.ui_database_pack_forget_current()
		# 查看进入某种模式
		self.add_mode_database = ['item','inner'][self.item_db_from.combobox.current()]
		# 安放新布局
		self.ui_database_init()

	def pack_database_item(self):
		""" 安放添加普通模板 - 逐项添加 """
		self.components_database_item_add.pack()
		self.components_database_item_reduce.pack()
		self.components_database_item_save.pack()
		self.components_database_item_sframe.pack()
		self.components_database_item_name.pack()
		self.components_database_item_sheet_choose.pack()
		self.components_database_item_lframe1.pack(side='left',fill='both',expand=True)
		self.components_database_item_lframe2.pack(side='top')
		self.components_database_item_help_entry.pack(side='left',fill='x',expand=True)
		self.components_database_item_help_combobox.pack(side='left')
		self.components_database_item_help_text.pack(side='top',fill='both',expand=True)

	def pack_database_inner(self):
		""" 安放添加数据库模板 - 内部添加 """
		pass

	def pack_forget_database_item(self):
		""" 隐藏添加普通模板 - 逐项添加 """
		for item in self.components_list_database_item:
			item.pack_forget()

	def pack_forget_database_inner(self):
		""" 隐藏添加数据库模板 - 内部添加 """
		for item in self.components_list_database_inner:
			item.pack_forget()

	def destroy_database_item(self):
		""" 销毁添加普通模板 - 逐项添加 """
		for item in self.components_list_database_item:
			item.destroy()

	def destroy_database_inner(self):
		""" 销毁添加数据库模板 - 内部添加 """
		for item in self.components_list_database_inner:
			item.destroy()
