import tkinter as tk

class DatabaseMainUI():
	def __init__(self, window, *args, **kwargs):
		# 设置与主窗口
		self.sd = args[0]
		self.cd = args[1]
		self.window = window

		# 组件
		self.title = tk.Label(window,fg=self.cd['front'], bg=self.cd['back'],\
			font=(self.sd['font'],self.sd['tsize'],'bold'),\
			width=40, height=3, justify="left", anchor="center",\
			text=["DATABASE     SYSTEM\n","数据库系统"][self.sd['language_id']])
		if self.sd['system'] == 'Mac':
			self.back = tk.Button(window, text=["Back to last level","返回上一级"][self.sd['language_id']],\
				command=self.back, width=20, height=3,fg=self.cd['mcfront'],\
				font=(self.sd['font'],self.sd['size']))
			self.db_add = tk.Button(window, text=["Database Add","数据库添加"][self.sd['language_id']],\
				command=self.change_to_database_add, width=20, height=3,fg=self.cd['mcfront'],\
				font=(self.sd['font'],self.sd['size']))
		else:
			self.back = tk.Button(window, text=["Back to last level","返回上一级"][self.sd['language_id']],\
				command=self.back, width=20, height=3,fg=self.cd['front'],bg=self.cd['back'],\
				font=(self.sd['font'],self.sd['size']))
			self.db_add = tk.Button(window, text=["Database Add","数据库添加"][self.sd['language_id']],\
				command=self.change_to_database_add, width=20, height=3,fg=self.cd['front'],bg=self.cd['back'],\
				font=(self.sd['font'],self.sd['size']))

	def pack(self):
		self.title.pack()
		self.back.pack()
		self.db_add.pack()

	def pack_forget(self):
		self.title.pack_forget()
		self.back.pack_forget()
		self.db_add.pack_forget()

	def destroy(self):
		self.title.destroy()
		self.back.destroy()
		self.db_add.destroy()

	def back(self):
		from MainUI import MainUI
		self.main = MainUI(self.window,self.sd,self.cd)
		self.destroy()
		self.main.pack()

	def change_to_database_add(self):
		from DatabaseAddUI import DatabaseAddUI
		self.templates_add = DatabaseAddUI(self.window,self.sd,self.cd)
		self.pack_forget()
		self.templates_add.pack()

