import tkinter as tk

class SettingMainUI():
	def __init__(self, window, *args, **kwargs):
		# 设置与主窗口
		self.sd = args[0]
		self.cd = args[1]
		self.window = window

		# 组件
		self.title = tk.Label(window,fg=self.cd['front'], bg=self.cd['back'], font=("黑体", 23), \
			width=40, height=3, justify="left", anchor="center",\
			text=["SETTING     SYSTEM\n","设置系统"][self.sd['language_id']])
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
		from MainUI import MainUI
		self.main = MainUI(self.window,self.sd,self.cd)
		self.pack_forget()
		self.main.pack()
