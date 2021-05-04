from LoadUI import LoadUI
from Initialize import *
from tool.TemplatesTool import save_new_template
import tkinter as tk
import os

class App(tk.Tk):
	""" 信息助手应用类
	功能: 
		创建不同种类的数据库分区, 数据库分区中包含数据集或数据库文件.
		应用提供了增删改查信息和信息的组织形式的功能.
	注(更新或优化思路):
		以后可以选择根据“Menu”进行的页面转换.
	"""
	def __init__(self, *args, **kwargs):
		""" 自动开始信息助手应用 """
		# 加载本地路径
		self.setting_dict = {"path":os.getcwd()}
		# 文件初始化
		ini_check(self.setting_dict["path"])
		# 音乐初始化
		ini_music(self.setting_dict["path"])
		# 设置与变量初始化
		self.setting_dict = ini_setting(self.setting_dict["path"])
		self.setting_dict['path'] = os.getcwd()
		# 加载调色板
		self.color_dict = ini_palette(self.setting_dict['palette'],\
			self.setting_dict['dark_mod'])
		# 窗口初始化
		tk.Tk.__init__(self, *args, **kwargs)
		self.pos = pos = self.get_window_positon(self.setting_dict['window_width'],\
		    self.setting_dict['window_height'])
		self.geometry(str(self.setting_dict['window_width'])+'x'\
			+str(self.setting_dict['window_height'])\
			+'+'+str(self.pos[0])+'+'+str(self.pos[1]))
		self.title('Information Helper')  #设置窗口标题
		self["background"] = self.color_dict["back"]
		# 进入加载界面(密码界面)
		load = LoadUI(self,self.setting_dict, self.color_dict)

	def get_window_positon(self, width, height):
		""" 计算窗口居中的位置 """
		system_metrics = [self.winfo_screenwidth(),self.winfo_screenheight()]
		window_x_position = (system_metrics[0] - width) // 2
		window_y_position = (system_metrics[1] - height) // 2
		return window_x_position, window_y_position

app = App()
app.mainloop()
