import tkinter as tk
import tkinter.ttk as ttk
from .CSVTool import *

class BaseFrame(object):
	""" 特定功能模块的底层框架 """
	def __init__(self, window, *args, **kwargs):
		# 设置与主窗口
		self.sd = args[0]
		self.cd = args[1]
		self.window = window
		# 基础框架
		self.bframe = tk.Frame(self.window,bg = self.cd['back'])
		self.rframe = tk.Frame(self.bframe,bg = self.cd['back'],width=self.sd['rwidth'])
		self.lframe = tk.Frame(self.bframe,bg = self.cd['back'],width=self.sd['lwidth'])

	def pack(self):
		""" 底层框架安放 """
		self.bframe.pack(fill='both',expand='true')
		self.rframe.pack(fill='y',side='right',expand='yes')
		self.lframe.pack(fill='y',side='right',expand='yes')

	def pack_forget(self):
		""" 底层框架取消安放 """
		self.lframe.pack_forget()
		self.rframe.pack_forget()
		self.bframe.pack_forget()

	def destroy(self):
		""" 底层框架销毁 """
		self.lframe.destroy()
		self.rframe.destroy()
		self.bframe.destroy()


class ScrollCanvas(object):
	""" 滚动条画布 """
	def __init__(self, window,*args, vsb='y',**kwargs):
		""" 初始化带滚动条的组件
		参数说明:
			vsb: 'y',y方向滚动条; 'x',x方向滚动条; 'both',两个方向滚动条
		"""
		# 设置与主窗口
		self.sd = args[0]
		self.cd = args[1]
		self.window = window
		self.vsb = vsb
		# 创建控件
		self.canvas = tk.Canvas(self.window, borderwidth=0, background=self.cd['back'])          # 画布
		self.frame = tk.Frame(self.canvas, background=self.cd['back'])                           # 画布上的框架
		if self.vsb=='y' or self.vsb=='both':
			self.vsb1 = tk.Scrollbar(self.window, orient="vertical", command=self.canvas.yview)   # 竖向滚动条
			self.canvas.configure(yscrollcommand=self.vsb1.set)
		if self.vsb=='x' or self.vsb=='both':
			self.vsb2 = tk.Scrollbar(self.window, orient="horizontal", command=self.canvas.xview) # 横向滚动条
			self.canvas.configure(xscrollcommand=self.vsb2.set)
		
	def _onFrameConfigure(self):
	    '''Reset the scroll region to encompass the inner frame'''
	    self.canvas.configure(scrollregion=self.canvas.bbox("all"))

	def fill_test(self):
		""" 测试填充效果 """
		for row in range(30):
			items = [['Normal Info','DataBase Info','Remind Info'],\
				['普通信息','数据库信息','提示信息']]
			test_label = FunctionalBlock(self.frame,['Info Type','信息类型'],\
				self.sd,self.cd,items=items[self.sd['language_id']],reduce_=2)
			test_label.pack()

	def pack(self):
		""" 安放控件 """ 
		self.canvas.pack(side="right", fill="both", expand=True)
		if self.vsb=='x' or self.vsb=='both':
			self.vsb2.pack(side='top',fill="x")
		if self.vsb=='y' or self.vsb=='both':
			self.vsb1.pack(side="right", fill="y")
		self.canvas.create_window((0,0),window=self.frame, anchor="nw")
		self.frame.bind("<Configure>", lambda event, canvas=self.canvas: self._onFrameConfigure())

	def pack_forget(self):
		""" 隐藏控件 """
		self.canvas.pack_forget()
		if self.vsb=='x' or self.vsb=='both':
			self.vsb2.pack_forget()
		if self.vsb=='y' or self.vsb=='both':
			self.vsb1.pack_forget()

	def destroy(self):
		""" 摧毁控件 """
		self.canvas.destroy()
		if self.vsb=='x' or self.vsb=='both':
			self.vsb2.destroy()
		if self.vsb=='y' or self.vsb=='both':
			self.vsb1.destroy()


class FunctionalBlock(object):
	""" 定制化功能快
	参数:
	"""
	def __init__(self,window,text,*args,items=[''],locked=True,kind='select',current=0,reduce_=0,key=None):
		# 设置与主窗口
		self.sd = args[0]
		self.cd = args[1]
		self.window = window
		self.kind = kind
		self.key = key
		# 创建内容
		# 创建 - 框架
		self.frame = tk.Frame(self.window,bg=self.cd['back'],width=self.sd['rwidth'])
		# 创建 - 提示标语
		if type(text) == list:
			text = text[self.sd['language_id']]
		self.label = tk.Label(self.frame,text=text, width=int(self.sd['rletter']*2/5)-reduce_,\
			fg=self.cd['front'],bg=self.cd['back'],font=(self.sd['font'],self.sd['size']))
		# 创建 - 复选框类型
		if self.kind == 'select':
			self.combobox = ttk.Combobox(self.frame, width=int(self.sd['rletter']*3/5-1),font=(self.sd['font'],self.sd['size']))
			self.combobox['values'] = (items) # 设置下拉列表的值
			self.combobox.current(current)    # 设置下拉列表默认显示的值
			if locked: self.combobox.configure(state="readonly") # 不可编辑
		# 创建 - 输入框类型
		elif self.kind == 'entry':
		    self.entry = tk.Entry(self.frame,bg=self.cd['back'],fg=self.cd['front'],\
		    	font=(self.sd['font'],self.sd['size']),width=int(self.sd['rletter']*3/5))

	def pack(self):
		""" 安放基本控件 """
		self.frame.pack()
		if self.kind == 'select':
			self.combobox.pack(side='right')
		elif self.kind == 'entry':
			self.entry.pack(side='right')
		self.label.pack(side='right')

	def pack_forget(self):
		""" 隐藏基本控件 """
		self.frame.pack_forget()
		if self.kind == 'select':
			self.combobox.pack_forget()
		elif self.kind == 'entry':
			self.entry.pack_forget()
		self.label.pack_forget()

	def destroy(self):
		""" 销毁基本控件 """
		self.frame.destroy()
		if self.kind == 'select':
			self.combobox.destroy()
		elif self.kind == 'entry':
			self.entry.destroy()
		self.label.destroy()

	def bind(self,str_,fun_):
		""" 复选框的bind """
		self.combobox.bind(str_,fun_)

	def current(self,x=None):
		""" 复选框的current """
		return self.combobox.current(x)

	def set_value(self,x):
		""" 复选框的[value] """
		self.combobox['values'] = x

	def get_key_value_pair(self):
		""" 获取键值对 """
		if self.kind == 'entry':
			return {self.key:eval(self.entry.get())}
		else:
			return {self.key:eval(self.combobox.get())}


class NameListbox(object):
	""" 填充模板名或数据库名或数据表名的列表框 """
	def __init__(self,window,*args,kind='template',side='left'):
		# 设置与主窗口
		self.sd = args[0]
		self.cd = args[1]
		self.kind = kind
		self.window = window
		self.side = side
		# 安放组件
		self.listbox = tk.Listbox(self.window, width=int(0.382*self.sd['lletter']),\
			bg=self.cd['back'],fg=self.cd['front'],font=(self.sd['font'],self.sd['size']))
		self.scrollbar = tk.Scrollbar(self.window)
		self.scrollbar.config(command=self.listbox.yview)
		# 根据类型进行填充
		self.fill()

	def fill(self):
		""" 进行特定内容的填充 """
		self.listbox.delete(0,tk.END)
		if self.kind == 'template':
			for item in loadDataset(self.sd['path']+'/resources/system/template/template.csv'):
				self.listbox.insert("end", item[0])
		elif self.kind == 'database':
			pass
		elif self.kind == 'sheet':
			pass

	def bind(self,str_,fun):
		""" 列表框 """
		self.listbox.bind(str_,fun)		

	def get(self):
		""" 获取选中的字符串"""
		return self.listbox.get(self.listbox.curselection())  

	def pack(self):
		""" 填充模板名或数据库名或数据表名的列表框-安放布局 """
		self.listbox.pack(side=self.side,fill='both')
		self.scrollbar.pack(side=self.side,fill='y')

	def pack_forget(self):
		""" 填充模板名或数据库名或数据表名的列表框-隐藏布局 """
		self.scrollbar.pack_forget()
		self.listbox.pack_forget()

	def destroy(self):
		""" 填充模板名或数据库名或数据表名的列表框-销毁布局 """
		self.scrollbar.destroy()
		self.listbox.destroy()


class QuickTable(object):
	""" 快速搭建表格 """
	def __init__(self,window,*args):
		# 设置与主窗口
		self.sd = args[0]
		self.cd = args[1]
		self.window = window
		# 设置颜色
		ttk.Style().configure("Treeview", background=self.cd['tback2'], foreground=self.cd['tfront'])
		# 安放组件
		self.column = tuple(range(self.sd['min_table']))
		self.treeview = ttk.Treeview(self.window, show="headings", columns=self.column)
		for i in range(len(self.column)):
			self.treeview.column(i,width=100, anchor='center')
		# 整理表格
		self.clear_up_table()

	def clear_up_table(self, number=36,step=0):
		''' 整理表格
		进行清空表格与添加空行的工作
		'''
		if step in [0,1]: 
			# 清空表格
			for child in self.treeview.get_children():
			    self.treeview.delete(child)
		if step in [0,2]:
			# 占空行
			for i in range(number):
			    self.treeview.insert('', 'end', values=[])

	def pack(self,**awgs):
		""" """
		if awgs == {}:
			self.treeview.pack(side='left',fill='both')
		else:
			self.treeview.pack(awgs)

	def pack_forget(self):
		""" """
		self.treeview.pack_forget()

	def destroy(self):
		""" """
		self.treeview.destroy()


class IterationList(list):
	""" 可迭代组件列表器 """

	def __init__(self,refresh=True):
		self.refresh = refresh

	def pack(self):
		""" 安放内部布局 """
		for item in self:
			if type(item) == ttk.Separator:
				if str(item['orient']) == 'horizontal':
					item.pack(fill='x')
				else:
					item.pack(fill='y')
			else:
				item.pack()

	def pack_forget(self):
		""" 隐藏所有内部组件布局 """
		for item in self:
			item.pack_forget()
		if self.refresh:
			self.clear()

	def destroy(self):
		""" 销毁所有内部组件布局 """
		for item in self:
			item.destroy()
		self.clear()


class Page():
	""" 根据下拉菜单进行更换页面的类 """
	def __init__(self,window,*args):
		# 设置与主窗口
		self.sd = args[0]
		self.cd = args[1]
		self.window = window
		# 组件列表
		self.components_list = []
		self.components_list_pack_way = []
		self.destroy_sentence_list = []
		# 更换布局
		self.combobox = None
		self.current_page = None
		self.child_page = None
		# 自身属性
		self.number = 0
		self.kind = 'list' # 'combobox'

	def set_combobox(self,window,tip,items,cpage,current=0):
		""" 更换组件框 """
		self.kind = 'combobox'
		self.child_page = cpage
		self.combobox = FunctionalBlock(window,tip,self.sd,self.cd,\
			items=items[self.sd['language_id']])
		self.combobox.set_value(items[self.sd['language_id']]) # 设置下拉列表的值
		self.combobox.current(current)    # 设置下拉列表默认显示的值
		self.combobox.bind("<<ComboboxSelected>>",self.change_page)
		self.ui_mode = items[current]
		self.components_list.append(self.combobox)
		self.components_list_pack_way.append('')
		self.current_page = current

	def set_child_page(self,cpage,current=0):
		""" 设置子页面 
		注意使用set_combobox的界面不能再使用set_child_page
		current: 如果为-1则不安放子界面
		"""
		if self.child_page!= None: 
			print('不能再次设置')
			return False
		self.child_page = cpage
		self.current_page = current

	def change_page(self,event=None,current=0):
		""" 切换模式 """
		if self.current_page!=-1:
			# 隐藏布局
			self.child_page[self.current_page].pack_forget()
			# 查看进入某种模式
			try: # 通过复选框
				self.current_page = self.combobox.current()
			except: # 手动设置
				self.current_page = current
			# 安放新布局
			self.child_page[self.current_page].pack()
		if self.current_page == -1:
			# 查看进入某种模式
			self.current_page = current
			# 安放新布局
			self.child_page[self.current_page].pack()

	def append(self,x):
		self.number = self.number+1
		self.components_list.append(x)
		self.components_list_pack_way.append(None)

	def append_destroy(self,sentence):
		if type(sentence) != str: print('False')
		self.destroy_sentence_list.append(sentence)

	def pack(self):
		for i in range(len(self.components_list)):
			if self.components_list_pack_way[i]:
				self.components_list[i].pack(**self.components_list_pack_way[i])
			else:
				self.components_list[i].pack()
		# 进入特定模式
		if self.child_page != None:
			if self.current_page==-1:
				pass
			else:
				self.child_page[self.current_page].pack()

	def pack_way(self,**awgs):
		self.components_list_pack_way.pop()
		self.components_list_pack_way.append(awgs)

	def pack_forget(self):
		for sentence in self.destroy_sentence_list:
			exec(sentence)
		for item in self.components_list:
			item.pack_forget()
		if self.child_page != None:
			for item in self.child_page:
				item.pack_forget()

	def destroy(self):
		for sentence in self.destroy_sentence_list:
			exec(sentence)
		for item in self.components_list:
			item.destroy()
		if self.child_page != None:
			for item in self.child_page:
				item.destroy()
"""
    Listbox.delete(0,tk.END)
    count = 1
    if isDataBase: # 填充数据库信息
        for dbPath in getAccessibleDatabase(DBType):
            Listbox.insert("end", '【'+dbPath+'】')
            for item in loadDataset('./resources/database/'+dbPath+'.csv')[1:]:
                Listbox.insert("end", item[0])
    else:          # 填充模板信息
        for item in loadDataset('./resources/system/template/template.csv'):
            if allData:
                item_string = str(count)+":  "
                for item_ in item:
                    item_string = item_string+item_+"  "
            else:
                item_string = item[0]
            Listbox.insert("end", item_string)
            count = count+1
"""

#help(FunctionalBlock)

