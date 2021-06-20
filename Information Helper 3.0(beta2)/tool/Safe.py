from tkinter import messagebox
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr 
from .CSVTool import *

def get_password(path = './resources/system/setting/setting.csv'):
    ''' getpassword 获取密码
    Gets the decrypted password from the password file
    从密码文件中获取解密好的密码
    :return password: Decrypted password 解密好的密码
    '''
    for line in loadDataset(path):
        if line[0:2] == ['Me','password']:
            if line[2:] == ['']: return ''
            return password_translation(line[2:],1)
    print("Error! Didn't find password!")
    return ''

def password_translation(word,mode):
    ''' Encrypt and decrypt passwords 进行字符串的加密与解密
    You can also create your own set of encryption algorithms, just modify this function.
    你也可以自己的创建一套加密算法,只需修改本函数.
    
    :param word: The word used to encrypt and decrypt a password 进行密码的加密与解密的词
    :param mode: mode = 0, encryption; mode = 1, decryption    mode=0,加密;mode=1,解密
    :return password: The modified string 加密后的列表与解密后的字符串
    '''
    if mode == 0: # encryption
        password = []
        for i in range(len(word)):
            password.append(str(ord(word[i])+2*i))
        return password
    if mode == 1: # decryption 
        password = ''
        for i in range(len(word)):
            password = password+chr(int(word[i])-2*i)
        return password 

def sent_message(mail,word,language,window):
	''' sent email 发邮件
	:params mail: Return address 收信人地址
	:params word: Content sent 发送的内容
	'''
	def sentmail():
		ret=True
		try:
			msg=MIMEText(word,'plain','utf-8')
			msg['From']=formataddr(["FromRunoob",my_sender])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
			msg['To']=formataddr(["FK",my_user])              # 括号里的对应收件人邮箱昵称、收件人邮箱账号
			msg['Subject']="Information Helper 验证码"         # 邮件的主题，也可以说是标题

			server=smtplib.SMTP_SSL("smtp.qq.com", 465)  # 发件人邮箱中的SMTP服务器，端口是25
			server.login(my_sender, my_pass)  # 括号中对应的是发件人邮箱账号、邮箱密码
			server.sendmail(my_sender,[my_user,],msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
			server.quit()  # 关闭连接
		except:  # 如果 try 中的语句没有执行，则会执行下面的 ret=False
		    ret=False
		return ret
	if mail == '':
		return False
	ask_if_find_password = messagebox.askyesno('askyesno',['Sure To Send ?','确认发送验证码?'][language], parent=window)
	if ask_if_find_password:
	    my_sender='1742861545@qq.com'    # 发件人邮箱账号
	    my_pass = 'pqgqozwuwcvtdjeh'     # 发件人邮箱密码
	    my_user=mail                     # 收件人邮箱账号
	    if sentmail():print("邮件发送成功")
	    else: print("邮件发送失败") 
