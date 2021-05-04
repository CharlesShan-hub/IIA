import tkinter as tk
from tkinter import messagebox
import random
from tool.Safe import *
from Initialize import ini_jieba

class LoadUI():
	""" 加载界面类
	功能: 
		1. 密码界面与跳过密码
		2. 验证密码是否正确
		3. 密码找回(需要设置过邮箱)
	"""
	def __init__(self, window, *args, **kwargs):
		""" 加载界面初始化 """
		# Logic level 
		# 设置与主窗口
		self.sd = args[0]
		self.cd = args[1]
		self.window = window
		# 检查是否跳过密码
		if self.sd['need_password'] == 'off':
			self.goto_main(packed=False)
		else:
			self.component_declaration()
			self.pack()

	def component_declaration(self):
		""" 加载界面组件创建 """
		# Interface interaction
		# 标题
		self.title = tk.Label(self.window,fg=self.cd['front'], \
			bg=self.cd['back'], font=(self.sd['font'],self.sd['tsize'],'bold'), \
			width=40, height=3, justify="left", anchor="center",\
			text=["Welcome !\n","欢迎!"][self.sd['language_id']])
		# 占位
		self.placeholder = tk.Label(self.window,text = '\n\n\n\n'\
			,bg=self.cd['back'])
		# 密码输入提示
		self.password_input_tip = tk.Label(self.window,text=["Password",\
			"密码"][self.sd['language_id']],bg=self.cd['back'],\
			font=(self.sd['font'],self.sd['size']),fg=self.cd['front'])
		# 密码输入框
		self.password_input_area = tk.Entry(self.window,show="*",\
			fg=self.cd['front'],bg=self.cd['tback2'],\
			font=(self.sd['font'],self.sd['size'])) 
		self.password_input_area.bind("<Return>",self._check_password)
		# 生成验证码
		self.captcha = random.randint(100000,999999)
		# 找回密码按钮
		if self.sd['system'] == 'Mac':
			self.find_password_button = tk.Button(self.window, \
				text=['find password','找回密码'][self.sd['language_id']],\
				width=15, height=1,fg=self.cd['mcfront'],\
				font=(self.sd['font'],self.sd['size']),\
				command=lambda:self._find_password())
		else:
			self.find_password_button = tk.Button(self.window, \
				text=['find password','找回密码'][self.sd['language_id']],\
				width=15, height=1,fg=self.cd['front'],\
				font=(self.sd['font'],self.sd['size']),bg=self.cd['back'],\
				command=lambda:self._find_password())
		# 验证码与获取验证码-框架
		self.captcha_frame = tk.Frame(self.window, bg=self.cd['back'])
		# 发送验证码
		if self.sd['system'] == 'Mac':
			self.send_captcha = tk.Button(self.captcha_frame, \
				text=["Send Capcha","获取验证码"][self.sd['language_id']],\
				width=15, height=1,fg=self.cd['mcfront'],\
				font=(self.sd['font'],self.sd['size']),\
				command=lambda:sent_message(self.sd['mail'],"Capcha:【"\
					+str(self.captcha)+'】.From Information Helper!',\
					self.sd['language_id'],self.window))
		else:
			self.send_captcha = tk.Button(self.captcha_frame, \
				font=(self.sd['font'],self.sd['size']),\
				text=["Send Capcha","获取验证码"][self.sd['language_id']],\
				width=20, height=1,fg=self.cd['front'],bg=self.cd['back'],\
				command=lambda:sent_message(self.sd['mail'],"Capcha:【"\
					+str(self.captcha)+'】.From Information Helper!',\
					self.sd['language_id'],self.window))
		# 验证码输入框
		self.input_captcha = tk.Entry(self.captcha_frame,\
			fg=self.cd['front'],bg=self.cd['tback2'],\
			font=(self.sd['font'],self.sd['size']))
		self.input_captcha.bind("<Return>",self._check_captcha)  

	def pack(self):
		""" 加载界面组件安放 """
		# Interface interaction
		# 标题
		self.title.pack()
		# 占位
		self.placeholder.pack(fill = 'x')
		# 密码输入提示
		self.password_input_tip.pack(fill = 'x')
		# 密码输入框
		self.password_input_area.pack(fill = 'x')
		# 找回密码按钮
		self.find_password_button.pack()
		# 验证码与获取验证码-框架
		self.captcha_frame.pack(fill = 'x')

	def destroy(self):
		""" 加载界面销毁布局 """
		# Interface interaction
		self.title.destroy()
		self.placeholder.destroy()
		self.password_input_tip.destroy()
		self.password_input_area.destroy()
		self.find_password_button.destroy()
		self.captcha_frame.destroy()
		self.send_captcha.destroy()
		self.input_captcha.destroy()

	def goto_main(self,packed):
		""" 进入主界面 
		功能: 
			1. 进行jieba库设置
			2. 布局更改
		参数:
			packed: 是否Load界面经过安放后再进入主界面
		"""
		# Initialize - 初始化分词
		ini_jieba(self.window, self.sd['path'])
		# Interface interaction - 布局更改
		from MainUI import MainUI
		self.main = MainUI(self.window,self.sd,self.cd)
		if packed: self.destroy()
		self.main.pack()

	def _find_password(self):
		""" 找回密码 
		功能: 
			1. 验证是否设置过邮箱, 未设置进行弹窗提示
			2. 设置过邮箱则进行验证码布局显示
		"""
		if self.sd['mail'] == '': 
			messagebox.showinfo(title=['wrong','错误'][self.sd['language_id']],\
				message=['Can‘t find your mail!','您未设置邮箱']\
				[self.sd['language_id']],parent=self.window)
			return False
		else: 
			self.send_captcha.pack(side = "right")
			self.input_captcha.pack(fill = 'x')

	def _check_captcha(self,event):
	    """ 验证码验证 """
	    # Interface interaction
	    def getInputCaptcha():
	        inputCaptcha = str(self.input_captcha.get())
	        self.input_captcha.delete(0, tk.END)
	        return inputCaptcha
	    def showPasswordMind():
	        messagebox.showinfo(parent=self.window,title='注意', \
	        	message='您的密码为:'+get_password()+'\n别再忘了呦')
	    # Logic level
	    if str(self.captcha) == getInputCaptcha():
	        showPasswordMind()
	        self.goto_main(packed=True)

	def _check_password(self,event):
		""" 密码验证 """
		# Interface interaction
		def _recent_password():
		    return str(self.password_input_area.get())
		def _form_interface():
			try: # 如果密码为空, 这步会报错, 用try except忽略它
				self.password_input_area.delete(0, tk.END)
			except:
				pass
		# Logic level
		if _recent_password() == get_password(): 
		    self.goto_main(packed=True)
		_form_interface()		

#help(LoadUI)
