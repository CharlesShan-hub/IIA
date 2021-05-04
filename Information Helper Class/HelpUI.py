import tkinter as tk
import tkinter.scrolledtext as scrolledtext

class HelpUI:
	def __init__(self,*args,title=None, **kwargs):
		""" 帮助模块初始化 """
		# 设置与主窗口
		self.sd = args[0]
		self.cd = args[1]
		self.title = title
		self.data_style = []
		self.data_item = []
		# 创建窗口
		self.help_window = tk.Tk()
		# 创建设置搜索框
		self.entry = tk.Entry(self.help_window,\
			fg=self.cd['front'],bg=self.cd['tback2'],\
			font=(self.sd['font'],self.sd['size']))
		self.entry.bind("<Return>",self.check_help)
		self.entry.pack(fill='x',expand=True,side='top')
		# 帮助文字中显示窗
		self.help_text = scrolledtext.ScrolledText(self.help_window,\
			fg=self.cd['front'],bg=self.cd['back'])
		self.help_text.pack(fill='both',expand=True,side='top')
		if self.title:
			self.show_help()

		self.help_window.mainloop()

	def check_help(self,event=None):
		''' 获取self.title
		'''
		# 确认帮助种类
		self.show_help()
		if self.help == None:
			print(self.entry.get())

	def get_help(self):
		""" 获取帮助文档内容 """
		self.data_style = []
		self.data_item = []
		with open('./help/'+self.title+".txt", "r") as f:  # 打开文件
			self.data = f.readlines()  # 读取文件
		for i in range(len(self.data)):
			if i%2 == 0:
				self.data_style.append(self.data[i][:-1].replace('\\n','\n'))
			else:
				self.data_item.append(self.data[i][:-1].replace('\\n','\n'))

	def show_help(self):
		""" 显示帮助 """
		self.get_help()
		# 清空帮助文档区
		self.help_text.delete(0.0,'end')
		for i in range(len(self.data_item)):
			self.help_text.insert('end',self.data_item[i],self.data_style[i])
		self.help_text.tag_config('Title1',foreground=self.cd["front"],\
			font=(self.sd['font'],self.sd['size']+4,'bold'),justify='center')
		self.help_text.tag_config('Title2',foreground=self.cd["front"],\
			font=(self.sd['font'],self.sd['size']+2,'bold'))
		self.help_text.tag_config('Item',foreground=self.cd["front"],\
			font=(self.sd['font'],self.sd['size']))
		self.help_text.tag_config('Item_bold',foreground=self.cd["front"],\
			font=(self.sd['font'],self.sd['size'],'bold'))

	def destroy(self):
		self.help_window.exit()
		