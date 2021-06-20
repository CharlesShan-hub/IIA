import tkinter as tk

class MainUI():
	""" 主界面类
	功能:
		提供信息模块, 模板模块, 数据库模块和设置模块的入口
	"""
	def __init__(self, window,*args, **kwargs):
		""" 初始化主界面类 """
		# 设置与主窗口
		self.sd = args[0]
		self.cd = args[1]
		self.window = window

		# 组件
		self.title = tk.Label(window,fg=self.cd['front'], bg=self.cd['back'],\
			font=(self.sd['font'],self.sd['tsize'],'bold'), \
			width=40, height=3, justify="left", anchor="center",\
			text=["Personal Information Control System !\n","个人信息助手"][self.sd['language_id']])
		if self.sd['system'] == 'Mac':
			self.information = tk.Button(window,text=['Information Related','信息模块'][self.sd['language_id']],\
				command=self.change_to_information,\
				width=20, height=3,fg=self.cd['mcfront'],font=(self.sd['font'],self.sd['size']))
			self.template = tk.Button(window,text=['Templates Related','模板模块'][self.sd['language_id']]\
				,command=self.change_to_template,\
				width=20, height=3,fg=self.cd['mcfront'],font=(self.sd['font'],self.sd['size']))
			self.database = tk.Button(window,text=['Database Related','数据库模块'][self.sd['language_id']]\
				,command=self.change_to_database,\
				width=20, height=3,fg=self.cd['mcfront'],font=(self.sd['font'],self.sd['size']))
			self.setting = tk.Button(window,text=['Setting','设置模块'][self.sd['language_id']]\
				,command=self.change_to_setting,\
				width=20, height=3,fg=self.cd['mcfront'],font=(self.sd['font'],self.sd['size']))
		else:
			self.information = tk.Button(window,text='信息模块',command=self.change_to_information,\
				width=20, height=3,fg=self.cd['front'],bg=self.cd['back'],\
				font=(self.sd['font'],self.sd['size']))
			self.template = tk.Button(window,text=['Templates Related','模板模块'][self.sd['language_id']]\
				,command=self.change_to_template,\
				width=20, height=3,fg=self.cd['front'],bg=self.cd['back'],\
				font=(self.sd['font'],self.sd['size']))
			self.database = tk.Button(window,text=['Database Related','数据库模块'][self.sd['language_id']]\
				,command=self.change_to_database,\
				width=20, height=3,fg=self.cd['front'],bg=self.cd['back'],\
				font=(self.sd['font'],self.sd['size']))
			self.setting = tk.Button(window,text=['Setting','设置模块'][self.sd['language_id']]\
				,command=self.change_to_setting,\
				width=20, height=3,fg=self.cd['front'],bg=self.cd['back'],\
				font=(self.sd['font'],self.sd['size']))

	def pack(self):
		""" 主界面安放布局 """
		self.title.pack()
		self.information.pack()
		self.template.pack()
		self.database.pack()
		self.setting.pack()

	def destroy(self):
		""" 销毁布局 """
		self.title.destroy()
		self.information.destroy()
		self.template.destroy()
		self.database.destroy()
		self.setting.destroy()

	def change_to_information(self):
		""" 切换至信息模块 """
		from InformationMainUI import InformationMainUI
		self.information_main = InformationMainUI(self.window,self.sd,self.cd)
		self.destroy()
		self.information_main.pack()

	def change_to_template(self):
		""" 切换至模板模块 """
		from TemplatesMainUI import TemplatesMainUI
		self.templates_Main = TemplatesMainUI(self.window,self.sd,self.cd)
		self.destroy()
		self.templates_Main.pack()

	def change_to_database(self):
		""" 切换至数据库模块 """
		from DatabaseMainUI import DatabaseMainUI
		self.database_main = DatabaseMainUI(self.window,self.sd,self.cd)
		self.destroy()
		self.database_main.pack()

	def change_to_setting(self):
		""" 切换至设置模块 """
		from SettingMainUI import SettingMainUI
		self.setting_main = SettingMainUI(self.window,self.sd,self.cd)
		self.destroy()
		self.setting_main.pack()
