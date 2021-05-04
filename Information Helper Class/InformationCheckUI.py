import tkinter as tk

class InformationCheckUI():
	""" 信息查改模块
	功能:
		全部列出(内部信息经过整理)(选择全部列出还是只列出前10项) - 检查
		根据模板或数据表查询(是否添加数据表查询经过设置)        - 检查
		关键字检索(支持选择数据库分区(支持选择1-n个))          - 检查
		SQL语句查询(SQL语句帮助文档, SQL语句辅助输入, 指定或所有数据库的数据表表头提示区) - 检查
		提示信息搜索                                       - 检查
	"""
	def __init__(self, window, *args, **kwargs):
		""" 信息查改模块初始化 """
		# 设置与主窗口
		self.sd = args[0]
		self.cd = args[1]
		self.window = window
		# 组件
		# 大标题与返回按钮
		self.info_title_components()
		# 主框架与功能控制
		self.info_switchover_components()
		# 进入特定功能
		self.info_init()

	def info_init(self):
		""" 进入特定添加模式 """
		pass

	def info_title_components(self):
		""" 大标题与返回按钮 """
		# Interface interaction
		# 大标题
		self.title = tk.Label(self.window,fg=self.cd['front'], bg=self.cd['back'], font=("黑体", 23), \
			width=40, height=3, justify="left", anchor="center",\
			text=["INFORMATION     CHECK\n","信息查改"][self.sd['language_id']])
		if self.sd['system'] == 'Mac':
			self.back = tk.Button(self.window, text=["Back to last level","返回上一级"][self.sd['language_id']],\
				command=self.back, width=20, height=3,fg=self.cd['mcfront'])
		else:
			self.back = tk.Button(self.window, text=["Back to last level","返回上一级"][self.sd['language_id']],\
				command=self.back, width=20, height=3,fg=self.cd['front'],bg=self.cd['back'])
	
	def info_switchover_components(self):
		""" 主框架与功能控制 """
		# Interface interaction
		pass

	def pack(self):
		self.title.pack()
		self.back.pack()

	def pack_forget(self):
		self.title.pack_forget()
		self.back.pack_forget()

	def back(self):
		from InformationMainUI import InformationMainUI
		self.information_main = InformationMainUI(self.window,self.sd,self.cd)
		self.pack_forget()
		self.information_main.pack()
