import tkinter as tk
from DatabaseMainUI import DatabaseMainUI
from tool.Components import *

class DatabaseAddUI():
	""" 数据库添加界面
	功能概述:
		1. 添加数据库分区(选择数据库为智能数据库或高速数据库)
		2. 说明(介绍数据库分区)
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
		#self.add_mode = 'normal'
		# 普通模板默认添加模式 - 'item','inner'
		#self.add_mode_normal = 'item'
		# 数据表默认添加模式 - 'item','inner'
		#self.add_mode_database = 'item'

		# 组件
		self.components()

	def back(self):
		""" 返回 """
		from DatabaseMainUI import DatabaseMainUI
		self.database_main = DatabaseMainUI(self.window,self.sd,self.cd)
		self.destroy()
		self.database_main.pack()

	#-----------------------------------#
	# 第零层级: 组件声明

	def components(self):
		""" 主界面组件声明 """
		# 主界面布局
		self.title = tk.Label(self.window,fg=self.cd['front'], bg=self.cd['back'],\
			font=(self.sd['font'],self.sd['tsize'],'bold'),\
			width=40, height=3, justify="left", anchor="center",\
			text=["DATABASE     ADD\n","模板添加"][self.sd['language_id']])
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
		#items = [['Add Templates','Add Data Sheets'],['添加模板','添加数据表']]
		#elf.changeUI = FunctionalBlock(self.bframe.rframe,['Add Type','添加类型'],\
		#	self.sd,self.cd,items=items[self.sd['language_id']])
		#self.changeUI.combobox.bind("<<ComboboxSelected>>",self.ui_change)

		# 组件-普通模板
		#self.components_normal()

		# 组件-数据表
		#self.components_database()

	#----------------------------------#
	# 第零层级: 信息添加模块本身的安放与销毁

	def pack(self):
		self.title.pack()
		self.back.pack()
		self.bframe.pack()
		#self.changeUI.pack()
		#self.ui_init()

	def pack_forget(self):
		self.title.pack_forget()
		self.back.pack_forget()
		self.bframe.pack_forget()
		#self.changeUI.pack_forget()
		#self.pack_forget_normal()
		#self.pack_forget_database()

	def destroy(self):
		self.title.destroy()
		self.back.destroy()
		self.bframe.destroy()
		#self.changeUI.destroy()
		#self.destroy_normal()
		#self.destroy_database()

	################