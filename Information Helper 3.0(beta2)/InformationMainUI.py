import tkinter as tk

class InformationMainUI():
	""" 信息控制类
	功能: 
		提供进入信息添加, 信息查改, 信息分析的入口
	"""
	def __init__(self, window, *args, **kwargs):
		""" 初始化信息控制类界面 """
		# 设置与主窗口
		self.sd = args[0]
		self.cd = args[1]
		self.window = window

		# 组件
		self.title = tk.Label(window,fg=self.cd['front'], bg=self.cd['back'],\
			font=(self.sd['font'],self.sd['tsize'],'bold'), \
			width=40, height=3, justify="left", anchor="center",\
			text=["INFORMATION     SYSTEM\n","信息系统"][self.sd['language_id']])
		if self.sd['system'] == 'Mac':
			self.back = tk.Button(window, text=["Back to last level","返回上一级"][self.sd['language_id']],\
				command=self.back, width=20, height=3,fg=self.cd['mcfront'],\
				font=(self.sd['font'],self.sd['size']))
			self.info_add = tk.Button(window, text=["Information Add","信息添加"][self.sd['language_id']],\
				command=self.change_to_info_add, width=20, height=3,fg=self.cd['mcfront'],\
				font=(self.sd['font'],self.sd['size']))
			self.info_check = tk.Button(window, text=["Information Check","信息查改"][self.sd['language_id']],\
				command=self.change_to_info_check, width=20, height=3,fg=self.cd['mcfront'],\
				font=(self.sd['font'],self.sd['size']))
			self.info_analysis = tk.Button(window, text=["Information Analysis","信息分析"][self.sd['language_id']],\
				command=self.change_to_info_analysis, width=20, height=3,fg=self.cd['mcfront'],\
				font=(self.sd['font'],self.sd['size']))
		else:
			self.back = tk.Button(window, text=["Back to last level","返回上一级"][self.sd['language_id']],\
				command=self.back, width=20, height=3,fg=self.cd['front'],bg=self.cd['back'],\
				font=(self.sd['font'],self.sd['size']))
			self.info_add = tk.Button(window, text=["Information Add","信息添加"][self.sd['language_id']],\
				command=self.change_to_info_add, width=20, height=3,fg=self.cd['front'],bg=self.cd['back'],\
				font=(self.sd['font'],self.sd['size']))
			self.info_check = tk.Button(window, text=["Information Check","信息查改"][self.sd['language_id']],\
				command=self.change_to_info_check, width=20, height=3,fg=self.cd['front'],bg=self.cd['back'],\
				font=(self.sd['font'],self.sd['size']))
			self.info_analysis = tk.Button(window, text=["Information Analysis","信息分析"][self.sd['language_id']],\
				command=self.change_to_info_analysis, width=20, height=3,fg=self.cd['front'],bg=self.cd['back'],\
				font=(self.sd['font'],self.sd['size']))

	def pack(self):
		""" 安放信息控制界面 """
		self.title.pack()
		self.back.pack()
		self.info_add.pack()
		self.info_check.pack()
		self.info_analysis.pack()

	def destroy(self):
		""" 销毁消息控制界面 """
		self.title.destroy()
		self.back.destroy()
		self.info_add.destroy()
		self.info_check.destroy()
		self.info_analysis.destroy()

	def back(self):
		""" 返回到主界面 """
		from MainUI import MainUI
		self.main = MainUI(self.window,self.sd,self.cd)
		self.destroy()
		self.main.pack()

	def change_to_info_add(self):
		""" 进入信息添加界面 """
		from InformationAddUI import InformationAddUI
		self.information_add = InformationAddUI(self.window,self.sd,self.cd)
		self.destroy()
		self.information_add.pack()

	def change_to_info_check(self):
		""" 进入信息查改界面 """
		from InformationCheckUI import InformationCheckUI
		self.information_check = InformationCheckUI(self.window,self.sd,self.cd)
		self.destroy()
		self.information_check.pack()

	def change_to_info_analysis(self):
		""" 进入信息分析界面 """
		from InformationAnalysisUI import InformationAnalysisUI
		self.information_analysis = InformationAnalysisUI(self.window,self.sd,self.cd)
		self.destroy()
		self.information_analysis.pack()

#help(InformationMainUI)
