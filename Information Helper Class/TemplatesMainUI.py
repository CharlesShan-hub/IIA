import tkinter as tk

class TemplatesMainUI():
	def __init__(self, window, *args, **kwargs):
		# 设置与主窗口
		self.sd = args[0]
		self.cd = args[1]
		self.window = window

		# 组件
		self.title = tk.Label(window,fg=self.cd['front'], bg=self.cd['back'],\
			font=(self.sd['font'],self.sd['tsize'],'bold'),\
			width=40, height=3, justify="left", anchor="center",\
			text=["TEMPLATE     SYSTEM\n","模版系统"][self.sd['language_id']])
		if self.sd['system'] == 'Mac':
			self.back = tk.Button(window, text=["Back to last level","返回上一级"][self.sd['language_id']],\
				command=self.back, width=20, height=3,fg=self.cd['mcfront'],\
				font=(self.sd['font'],self.sd['size']))
			self.tem_add = tk.Button(window, text=["Templates Add","模板添加"][self.sd['language_id']],\
				command=self.change_to_templates_add, width=20, height=3,fg=self.cd['mcfront'],\
				font=(self.sd['font'],self.sd['size']))
			self.tem_check = tk.Button(window, text=["Templates Check","模板查看"][self.sd['language_id']],\
				command=self.change_to_templates_check, width=20, height=3,fg=self.cd['mcfront'],\
				font=(self.sd['font'],self.sd['size']))
			self.tem_change = tk.Button(window, text=["Templates Change","模板更改"][self.sd['language_id']],\
				command=self.change_to_templates_change, width=20, height=3,fg=self.cd['mcfront'],\
				font=(self.sd['font'],self.sd['size']))
		else:
			self.back = tk.Button(window, text=["Back to last level","返回上一级"][self.sd['language_id']],\
				command=self.back, width=20, height=3,fg=self.cd['front'],bg=self.cd['back'],\
				font=(self.sd['font'],self.sd['size']))
			self.tem_add = tk.Button(window, text=["Templates Add","模板添加"][self.sd['language_id']],\
				command=self.change_to_templates_add, width=20, height=3,fg=self.cd['front'],bg=self.cd['back'],\
				font=(self.sd['font'],self.sd['size']))
			self.tem_check = tk.Button(window, text=["Templates Add","模板查看"][self.sd['language_id']],\
				command=self.change_to_templates_check, width=20, height=3,fg=self.cd['front'],bg=self.cd['back'],\
				font=(self.sd['font'],self.sd['size']))
			self.tem_change = tk.Button(window, text=["Templates Add","模板修改"][self.sd['language_id']],\
				command=self.change_to_templates_change, width=20, height=3,fg=self.cd['front'],bg=self.cd['back'],\
				font=(self.sd['font'],self.sd['size']))

	def pack(self):
		self.title.pack()
		self.back.pack()
		self.tem_add.pack()
		self.tem_check.pack()
		self.tem_change.pack()

	def pack_forget(self):
		self.title.pack_forget()
		self.back.pack_forget()
		self.tem_add.pack_forget()
		self.tem_check.pack_forget()
		self.tem_change.pack_forget()

	def back(self):
		from MainUI import MainUI
		self.main = MainUI(self.window,self.sd,self.cd)
		self.pack_forget()
		self.main.pack()

	def change_to_templates_add(self):
		from TemplatesAddUI import TemplatesAddUI
		self.templates_add = TemplatesAddUI(self.window,self.sd,self.cd)
		self.pack_forget()
		self.templates_add.pack()
	
	def change_to_templates_check(self):
		from TemplatesCheckUI import TemplatesCheckUI
		self.templates_check = TemplatesCheckUI(self.window,self.sd,self.cd)
		self.pack_forget()
		self.templates_check.pack()

	def change_to_templates_change(self):
		from TemplatesChangeUI import TemplatesChangeUI
		self.templates_change = TemplatesChangeUI(self.window,self.sd,self.cd)
		self.pack_forget()
		self.templates_change.pack()
