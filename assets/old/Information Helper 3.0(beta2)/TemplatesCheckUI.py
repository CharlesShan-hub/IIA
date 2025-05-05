import tkinter as tk

class TemplatesCheckUI():
	""" 模板添加模块
	功能: 
		普通模板的添加 - 逐项添加, 根据数据库模版转换 
		数据库模板(数据表)的添加 - 逐项添加(手动输入边界条件), SQL语句创建, 普通模板+边界条件转换
	"""
	def __init__(self, window, *args, **kwargs):
		# 设置与主窗口
		self.sd = args[0]
		self.cd = args[1]
		self.window = window

		# 组件
		self.title = tk.Label(window,fg=self.cd['front'], bg=self.cd['back'], font=("黑体", 23), \
			width=40, height=3, justify="left", anchor="center",\
			text=["TEMPLATE     CHECK\n","模板查看"][self.sd['language_id']])
		if self.sd['system'] == 'Mac':
			self.back = tk.Button(window, text=["Back to last level","返回上一级"][self.sd['language_id']],\
				command=self.back, width=20, height=3,fg=self.cd['mcfront'])
		else:
			self.back = tk.Button(window, text=["Back to last level","返回上一级"][self.sd['language_id']],\
				command=self.back, width=20, height=3,fg=self.cd['front'],bg=self.cd['back'])

	def pack(self):
		self.title.pack()
		self.back.pack()

	def pack_forget(self):
		self.title.pack_forget()
		self.back.pack_forget()

	def back(self):
		from TemplatesMainUI import TemplatesMainUI
		self.templates_main = TemplatesMainUI(self.window,self.sd,self.cd)
		self.pack_forget()
		self.templates_main.pack()
