'''
#from InformationAddUI import InformationAddUI
from Initialize import *
from tool.Components import *
import tkinter as tk
import os

class Test(tk.Tk):
	def __init__(self, *args, **kwargs):
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
		
		# 待测试界面
			# 基层框架
		testUI = BaseFrame(self,self.setting_dict, self.color_dict)
		testUI.pack()
			# page1.1
		page1_1 = Page(testUI,self.setting_dict,self.color_dict)
		page1_1.append(tk.Label(testUI.rframe,text='Page1.1'))
		page1_1.append(tk.Label(testUI.rframe,text='Page1.1!!'))
			# page1.2
		page1_2 = Page(testUI,self.setting_dict,self.color_dict)
		page1_2.append(tk.Label(testUI.rframe,text='Page1.2'))
		page1_2.append(tk.Label(testUI.rframe,text='Page1.2!!'))
		page1_2.append(tk.Label(testUI.rframe,text='Page1.2!!!!'))
			# page2.1
		page2_1 = Page(testUI,self.setting_dict,self.color_dict)
		page2_1.append(tk.Label(testUI.rframe,text='Page2.1'))
			# page2.2
		page2_2 = Page(testUI,self.setting_dict,self.color_dict)
		page2_2.append(tk.Label(testUI.rframe,text='Page2.2'))
			# page2.3
		page2_3 = Page(testUI,self.setting_dict,self.color_dict)
		page2_3.append(tk.Label(testUI.rframe,text='Page2.3'))
			# page1
		page1 = Page(testUI,self.setting_dict,self.color_dict)
		tip = ['page1 choose','page1选择']
		items = [['page1.1','page1.2'],['界面1.1','界面1.2']]
		child_page = [page1_1,page1_2]
		page1.set_combobox(window=testUI.rframe,\
			tip=tip,items=items,cpage=child_page,current=0)
			# page2
		page2 = Page(testUI,self.setting_dict,self.color_dict)
		tip = ['page2 choose','page2选择']
		items = [['page2.1','page2.2','page2.3'],['界面2.1','界面2.2','界面2.3']]
		child_page = [page2_1,page2_2,page2_3]
		page2.set_combobox(window=testUI.rframe,\
			tip=tip,items=items,cpage=child_page,current=0)
			# page0
		page0 = Page(testUI,self.setting_dict,self.color_dict)
		tip = ['Hello','你好']
		items = [['page1','page2'],['界面1','界面2']]
		child_page = [page1,page2]
		page0.set_combobox(window=testUI.rframe,\
			tip=tip,items=items,cpage=child_page,current=0)

		page0.pack()

	def get_window_positon(self, width, height):
		""" 计算窗口居中的位置 """
		system_metrics = [self.winfo_screenwidth(),self.winfo_screenheight()]
		window_x_position = (system_metrics[0] - width) // 2
		window_y_position = (system_metrics[1] - height) // 2
		return window_x_position, window_y_position


app = Test()
app.mainloop()
'''
'''
from tkinter.filedialog import askopenfilename
from pandas import read_excel
import os

path = askopenfilename()
path_suffix = os.path.splitext(path)[-1]

if path_suffix in ['.xlsx','.xlsm','.xlt','.xls','.et','.ett','.xltx','.xltm','xlsb','odf','ods','odt']:
	#print(read_excel(path,header=1))
	#print(read_excel(path,header=None,names=['a','b','c']))
	#print(read_excel(path,header=1,names=['a','b','c']))
	#print(read_excel(path, header=1, usecols=[2], squeeze=True))
	#print(read_excel(path, header=1, names=['name1','name2','name3'],converters={2:lambda x:x+1}))
	#print(read_excel(path, header=1, names=['name1','name2','name3'],skiprows=lambda x:x in [2,4]))
	data = read_excel(path)

	print(list(data.columns.values))

	print(data.columns.values==[])

	##for row in data.itertuples():
	#	print(list(row))
		#print(getattr(row, 'c1'), getattr(row, 'c2')) # 输出每一行

	print(path)
elif path_suffix == '.txt':
	pass
elif path_suffix == '.csv':
	pass

# .xlsx
# .xlsm
# .xlt
# .xls
# .et
# .ett
# .xltx
# .xltm


# xls, xlsx, xlsm, xlsb, odf, ods and odt

#WPS表格 文件(*.et)
#
'''
'''
import tkinter as tk
import tkinter.ttk as ttk

root = tk.Tk()
a = tk.Label(root)
b = ttk.Separator(root,orient='horizontal')

print(type(a))
print(type(b))
print(type(b) == ttk.Separator)
print(str(b['orient']) == 'horizontal')
print(type(b['orient']))

'''
for i in range(1,14):
	print(i)

