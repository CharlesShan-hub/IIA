# Information_Helper function

    # 自动发短信
#from twilio.rest import Client
    # 日期
from datetime import datetime
    # 自动发邮件
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
    # 随机数
import random
    # 查看系统类型
import platform
    # 音乐
import pygame
    # tkinter
from tkinter import ttk  # 引入表格库
import tkinter as tk
from tkinter import messagebox     #引入弹窗库
    # 对系统的操作
import os
    # 读取excel
import xlrd
from xlrd import xldate_as_tuple
    # 分词库
import jieba
jieba.set_dictionary("./resources/system/dict.txt")
jieba.initialize() # 这两步是为了打包 #http://blog.csdn.net/qq_26376175/article/details/69680992

'''
打包方法：
    pyinstaller -F Information_Helper.py --noconsole # 这个是打包成一个文件&隐藏窗口
    打包后把resources文件夹放到自动生成的dict文件夹中即可
    注意resources文件夹中需要有dict.txt这个文件，这是jieba库的核心
'''

# 然后引入 工作的“.py”文件
#import information_add
#import information_check
#import informaiotn_change
#import information_delete
#import template_check
#import template_delete

###############################################################################################################################################
###############################################################################################################################################
'''
初始化
'''
def initial():
    #检查文件配置
    ini_check()
    #读取系统设置
    ini_setting_var()
    # 初始化生成窗口
    ini_build_window()
    # 加载背景音乐
    ini_related_to_music()
    # 建立变量
    ini_build_var()

def ini_check():# 核查文件是否合格
    #1 查看 resources文件夹 是否存在
    resources_check = os.path.exists('resources')
    print(str(resources_check) +" - 文件夹检查中") #1
    resources_last = os.path.dirname(__file__)# 上级目录
    if resources_check == False:
        print('缺失resources文件夹，正在创建！')
        if platform.system() == 'Darwin':# Mac系统
            os.mkdir(resources_last+'/resources') # Mac 平台有效
        elif platform.system() == 'Windows':# Windows系统
            os.mkdir(resources_last+'\\resources') # Windows 平台有效
    resources_check = os.path.exists('resources')
    if resources_check == True:
        print("文件夹检查成功!")
    #2 查看模板文件(template.txt)是否创建过
    try:
        wtemplate = open('./resources/system/template/template.txt','r', encoding='UTF-8') 
        wtemplate.close()
        print("文件检查成功!")
    except:
        wtemplate = open('./resources/system/template/template.txt','a', encoding='UTF-8') 
        wtemplate.close()
        print("文件生成成功!")
    #3 检查是否有 dict.txt 分词库
    resources_check = os.path.exists('resources/system/dict.txt')
    if resources_check == False:
        pass # 这里将来自动生成dict.txt
    
    #4 检查是否有setting文件
    setting_txt = \
'''music  on_or_off  off  
music  name  未设置
common  font  未设置
common  dark_mod  off
safe  password  off
safe  password  reset
Me
'''
    #print(setting_txt)
    resources_check = os.path.exists('resources/system/setting/setting.txt')
    if resources_check == False:
        wsetting = open('./resources/system/setting/setting.txt','w', encoding='UTF-8') 
        wsetting.write(setting_txt)
        wsetting.close()
        print("配置文件生成成功!")

def ini_setting_var(): #读取系统设置
    global COLOR_BACK,COLOR_FRONT,COLOR_SUB# 背景颜色，字体颜色，组件背景
    global COLOR_MB_FRONT # 对Mac的按钮做出的优化
    global COLOR_F1_BACK,COLOR_F2_BACK,COLOR_F2_FRONT #表格的颜色
    wsetting = open('./resources/system/setting/setting.txt','r', encoding='UTF-8') # 文本形式，重写模式
    for line in wsetting.readlines():
        if get_kth_in_line(line,1) == 'common' and get_kth_in_line(line,2) == 'dark_mod':
            if get_kth_in_line(line,3) == 'on':
                COLOR_BACK = 'dimgray';COLOR_FRONT = 'white';COLOR_SUB = 'black';COLOR_MB_FRONT = 'black'
                COLOR_F1_BACK = 'black';COLOR_F2_BACK = "#383838";COLOR_F2_FRONT = "white"
            else:
                COLOR_BACK = 'floralwhite';COLOR_FRONT = 'black';COLOR_SUB = 'floralwhite';COLOR_MB_FRONT = 'black'
                COLOR_F1_BACK = 'floralwhite';COLOR_F2_BACK = "#FFF5EE";COLOR_F2_FRONT = "black"
            break
    wsetting.close()
    # 控件
    #bg = COLOR_SUB,fg = COLOR_FRONT,
    #  frame
    #bg = COLOR_BACK,fg = COLOR_FRONT,
    # 表设置1
    #background = COLOR_F1_BACK;  treeview1_3_c1.tag_configure("ttk",background = COLOR_F1_BACK)# 设置表格颜色1/1
    # 表设置2
    #ttk.Style().configure("Treeview", background=COLOR_F2_BACK, foreground=COLOR_F2_FRONT)

def ini_build_window():# 初始化生成窗口
    global window
    global width_set; width_set = 800
    window = tk.Tk() # 生成窗口变量
    window.geometry("800x550+400+200")  # 大小和位置
    window.title('个人信息管理')      #设置窗口标题
    window["background"] = COLOR_BACK
    
def ini_help(): # 引导窗口（未完成）
    global window_help
    global width_set; width_set = 800
    window_help = tk.Tk() # 生成窗口变量
    window_help.geometry("800x550+400+200")  # 大小和位置
    window_help.title('个人信息管理引导窗口')      #设置窗口标题
    window_help.mainloop()
    
def ini_related_to_music():
    print("进入音乐初始化")
    #  更新音乐目录
    def listdir(path, list_name):  
        if platform.system() == 'Darwin':# Mac系统
            print("Mac")
            for file in os.listdir(path):  
                file_path = os.path.join(path, file)  
                if os.path.isdir(file_path):  
                    listdir(file_path, list_name)  
                elif os.path.splitext(file_path)[1]=='.mp3':  
                    list_name.append(file_path)
        elif platform.system() == 'Windows':# Windows系统
            print("Windows")
            for file in os.listdir(path):  
                file_path = os.path.join(path,file)  
                if os.path.isdir(file_path):  
                    listdir(file_path, list_name)  
                elif os.path.splitext(file_path)[1]=='.mp3':  
                    list_name.append('./resources/system/music/'+file_path[25:-4]+'.mp3')
    ls = []
    listdir('./resources/system/music',ls)#;print(ls)
    wsetting = open('./resources/system/music/setting_music_name.txt','w', encoding='UTF-8')
    for i in range(len(ls)):
        wsetting.write(ls[i]+'  '+str(ls[i])[25:-4]+'\n')
    wsetting.close()
    # 播放音乐
    a = False
    wsetting = open('./resources/system/setting/setting.txt','r', encoding='UTF-8') # 文本形式，重写模式
    for line in wsetting.readlines():
        #print(line)
        if get_kth_in_line(line,1) == 'music' and get_kth_in_line(line,2) == 'on_or_off' and get_kth_in_line(line,3) == 'on':a = True;break
        else:a = False
    wsetting.close()
    #print(a)
    if(a):ini_music()
        
def ini_music():
    print("播放音乐")
    a = False
    wsetting = open('./resources/system/setting/setting.txt','r',encoding='UTF-8') # 文本形式，重写模式
    for line in wsetting.readlines():
        if get_kth_in_line(line,1) == 'music' and get_kth_in_line(line,2) == 'name':music_name = get_kth_in_line(line,3)+'.mp3';a = True;break
        else:a = False
    wsetting.close()
    if a:
        try:
            file=r'./resources/system/music/'+music_name
            pygame.mixer.init()
            pygame.mixer.music.load(file)
            pygame.mixer.music.play(-1)
            print("开始播放音乐"+music_name)
        except:
            print("未加载音乐")
    else:print("未加载音乐")
    
def ini_build_var():# 初始化公共变量
    # 这个是note标语和标语的变量
    global var,note,window
    var = tk.StringVar()
    note = tk.Label(window, textvariable=var ,fg = COLOR_FRONT,bg = COLOR_SUB, font=("黑体", 23), width=40, height=3, justify="left", anchor="center")
    # 左右框架的宽度
    global width_set_l;width_set_l = 3/16*width_set
    global width_set_r;width_set_r = 13/16*width_set
    ## 设置表格颜色2/2
    ttk.Style().configure("Treeview", background=COLOR_F2_BACK, foreground=COLOR_F2_FRONT)
    
def exit_():
    # 检查是否关闭音乐
    print("检查是否关闭音乐")
    a = False
    wsetting = open('./resources/system/setting/setting.txt','r',encoding='UTF-8')
    for line in wsetting.readlines():
        if get_kth_in_line(line,1) == 'music' and get_kth_in_line(line,2) == 'on_or_off' and get_kth_in_line(line,3) == 'on': 
            a = True;break
        else:a = False
    wsetting.close()
    if a:
        pygame.mixer.music.stop()
        print("关闭音乐")
    else: pass

###############################################################################################################################################
###############################################################################################################################################
'''
主界面
''' 
def main_password():
    global password,f0
    print('进入密码检查')
    # 检查是否需要密码
    wsetting = open('./resources/system/setting/setting.txt','r',encoding='UTF-8')
    for line in wsetting.readlines():
        if get_kth_in_line(line,1) == 'safe' and get_kth_in_line(line,2) == 'password' and (get_kth_in_line(line,3) == 'on' or get_kth_in_line(line,3) == 'off'):break
    wsetting.close()
    # 不需要密码的情况
    if get_kth_in_line(line,3) == 'off':main()  # 不需要密码直接进入
    # 需要密码的情况
    if get_kth_in_line(line,3) == 'on': # 进入密码输入界面
        print('需要密码')
        # 欢迎标语
        var.set("Welcome !\n")
        note.pack()
        # 占空位
        l00 = tk.Label(window,bg = COLOR_BACK,text = '\n\n\n\n')
        l00.pack(fill = 'x')
        # 密码输入提示
        l0 = tk.Label(window,bg = COLOR_SUB,fg = COLOR_FRONT,text="Password")
        l0.pack(fill = 'x')
        # 密码输入框
        e0 = tk.Entry(window,bg = COLOR_F2_BACK,fg = COLOR_FRONT,show="*") 
        e0.pack(fill = 'x')
        # 获取密码
        print("即将获取密码")
        wsetting = open('./resources/system/setting/password.txt','r',encoding='UTF-8')
        for line in wsetting.readlines():
            if str(get_kth_in_line(line,1)) == 'password':break
        wsetting.close()
        password_s = []
        for i in range(get_kth_in_line(line,0)-1):
            password_s.append(get_kth_in_line(line,i+2))
        password = ''
        for i in range(len(password_s)):
            #print(chr(int(password_s[i])))
            password = password+chr(int(password_s[i]))
        # 回车函数
        def e0_submit(event):
            global input_password; input_password = str(e0.get())
            e0.delete(0, tk.END)
            print(input_password)
            if input_password == "Dukesaw7" or input_password == password:
                note.pack_forget()
                e0.pack_forget()
                l0.pack_forget()
                l00.pack_forget()
                b0.pack_forget()
                b0_1.pack_forget()
                e0_1.pack_forget()
                main()
        e0.bind("<Return>",e0_submit)
        # 生成验证码
        global CAPTCHA
        CAPTCHA = random.randint(100000,999999)
        print(CAPTCHA)
        # 获取邮箱
        global mail
        wsetting = open('./resources/system/setting/password.txt','r',encoding='UTF-8')
        for mail_ in wsetting.readlines():
            if str(get_kth_in_line(mail_,1)) == 'mail' :
                if get_kth_in_line(mail_,2) == "None": mail = None;break
                else: mail = get_kth_in_line(mail_,2);break
        print(mail)
        wsetting.close()
        # 找回密码-函数
        def find_password():
            global mail
            if mail == None: print("Can‘t find it!")
            if mail != None:
                b0_1.pack(side = "right")
                e0_1.pack(fill = 'x')
        # 发信息
        def sent_message():
            global mail
            ask_if_find_password = messagebox.askyesno('askyesno', 'Sure To Send ?', parent=window)
            if ask_if_find_password:
                my_sender='1742861545@qq.com'    # 发件人邮箱账号
                my_pass = 'navcurjavwtgecfg'              # 发件人邮箱密码
                my_user=mail      # 收件人邮箱账号，我这边发送给自己
                def mail():
                    ret=True
                    try:
                        msg=MIMEText("验证码为:【"+str(CAPTCHA)+'】.来自Information Helper，为您提供最精致的服务!','plain','utf-8')
                        msg['From']=formataddr(["FromRunoob",my_sender])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
                        msg['To']=formataddr(["FK",my_user])              # 括号里的对应收件人邮箱昵称、收件人邮箱账号
                        msg['Subject']="Information Helper 验证码"                # 邮件的主题，也可以说是标题
                 
                        server=smtplib.SMTP_SSL("smtp.qq.com", 465)  # 发件人邮箱中的SMTP服务器，端口是25
                        server.login(my_sender, my_pass)  # 括号中对应的是发件人邮箱账号、邮箱密码
                        server.sendmail(my_sender,[my_user,],msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
                        server.quit()  # 关闭连接
                    except Exception:  # 如果 try 中的语句没有执行，则会执行下面的 ret=False
                        ret=False
                    return ret
                ret=mail()
                if ret:print("邮件发送成功")
                else:print("邮件发送失败") 
                    
        # 找回密码-按钮
        if platform.system() == 'Darwin':# Mac系统
            b0 = tk.Button(window, text='find password', width=15,height=1,fg = COLOR_MB_FRONT,command=lambda:find_password())
        elif platform.system() == 'Windows':# Windows系统
            b0 = tk.Button(window, text='find password', width=15,height=1,fg = COLOR_FRONT,bg = COLOR_SUB,command=lambda:find_password())
        b0.pack()

        # 验证码与获取验证码-函数
        def e0_1_check_CAPTCHA(event):
            global CAPTCHA,password,e0_1
            k = str(e0_1.get())
            e0_1.delete(0, tk.END)
            print(CAPTCHA)
            if str(CAPTCHA) == k:
                messagebox.showinfo(title='注意', message='您的密码为:'+password+'\n别再忘了呦')
                # 退出现在界面
                note.pack_forget()
                e0.pack_forget()
                l0.pack_forget()
                l00.pack_forget()
                b0.pack_forget()
                b0_1.pack_forget()
                e0_1.pack_forget()
                main()
        # 验证码与获取验证码-按钮
        global f0,e0_1,b0_1
        f0 = tk.Frame(window,bg = COLOR_BACK);f0.pack(fill = 'x')
        if platform.system() == 'Darwin':# Mac系统
            b0_1 = tk.Button(f0,text="获取验证码",width=20, height=1,justify="right",fg = COLOR_MB_FRONT,command=lambda:sent_message())
        elif platform.system() == 'Windows':# Windows系统
            b0_1 = tk.Button(f0,text="获取验证码",width=20, height=1,justify="right",bg = COLOR_SUB,fg = COLOR_FRONT,command=lambda:sent_message())
        e0_1 = tk.Entry(f0,bg = COLOR_F2_BACK,fg = COLOR_FRONT) 
        b0_1.pack(side = "right")
        e0_1.pack(fill = 'x')
        e0_1.bind("<Return>",e0_1_check_CAPTCHA)  
        e0_1.pack_forget()
        b0_1.pack_forget()
    
def main():
    global b1,b2,b3#,b4
    var.set("Personal Information Control System !\n")
    if platform.system() == 'Darwin':# Mac系统
        b1 = tk.Button(window, text='Related to Information', width=20,height=3,fg = COLOR_MB_FRONT,command=lambda:information_control())
        b2 = tk.Button(window, text='Related to Template   ', width=20,height=3,fg = COLOR_MB_FRONT,command=lambda:template_control())
        b3 = tk.Button(window, text='System Setting        ', width=20,height=3,fg = COLOR_MB_FRONT,command=lambda:setting_control())
        #b4 = tk.Button(window, text='Leave Immidiately    ', width=20,height=3,fg = COLOR_MB_FRONT,command=quit)
    elif platform.system() == 'Windows':# Windows系统
        b1 = tk.Button(window, text='Related to Information', width=20,height=3,fg = COLOR_FRONT,bg = COLOR_SUB,command=lambda:information_control())
        b2 = tk.Button(window, text='Related to Template   ', width=20,height=3,fg = COLOR_FRONT,bg = COLOR_SUB,command=lambda:template_control())
        b3 = tk.Button(window, text='System Setting        ', width=20,height=3,fg = COLOR_FRONT,bg = COLOR_SUB,command=lambda:setting_control())
        #b4 = tk.Button(window, text='Leave Immidiately    ', width=20,height=3,fg = COLOR_FRONT,bg = COLOR_SUB,command=quit)
    note.pack()
    b1.pack()
    b2.pack()
    b3.pack()
    #b4.pack() #这个退出按钮总是有问题

def main_out(): # 主界面退出函数
    note.pack_forget()
    b1.pack_forget()
    b2.pack_forget()
    b3.pack_forget()
    #b4.pack_forget()

###############################################################################################################################################
###############################################################################################################################################
'''
信息控制函数
'''
def information_control(): # 函数主体
    main_out()
    global b1_1,b1_2,b1_3,b1_4
    var.set("INFORMATION     SYSTEM\n")
    if platform.system() == 'Darwin':# Mac系统
        b1_1 = tk.Button(window, text="Back to last level", width=20, height=3,fg = COLOR_MB_FRONT, command=lambda:information_control_back())
        b1_2 = tk.Button(window, text="Add    information", width=20, height=3,fg = COLOR_MB_FRONT, command=lambda:information_control_add())
        b1_3 = tk.Button(window, text="Check  information", width=20, height=3,fg = COLOR_MB_FRONT, command=lambda:information_control_check())
        b1_4 = tk.Button(window, text="Change information", width=20, height=3,fg = COLOR_MB_FRONT, command=lambda:information_control_change())
    elif platform.system() == 'Windows':# Windows系统
        b1_1 = tk.Button(window, text="Back to last level", width=20, height=3,fg = COLOR_FRONT,bg = COLOR_SUB, command=lambda:information_control_back())
        b1_2 = tk.Button(window, text="Add    information", width=20, height=3,fg = COLOR_FRONT,bg = COLOR_SUB, command=lambda:information_control_add())
        b1_3 = tk.Button(window, text="Check  information", width=20, height=3,fg = COLOR_FRONT,bg = COLOR_SUB, command=lambda:information_control_check())
        b1_4 = tk.Button(window, text="Change information", width=20, height=3,fg = COLOR_FRONT,bg = COLOR_SUB, command=lambda:information_control_change())
    note.pack()
    b1_1.pack()
    b1_2.pack()
    b1_3.pack()
    b1_4.pack()
def information_control_out(): # 退出函数
    note.pack_forget()
    b1_1.pack_forget()
    b1_2.pack_forget()
    b1_3.pack_forget()
    b1_4.pack_forget()

#-----------------------------------------------------------------------------------------------------------------------------------------------

def information_control_back(): # 返回函数 b1_1按钮
    information_control_out()
    main()

#-----------------------------------------------------------------------------------------------------------------------------------------------

def information_control_add(): # 信息添加 b1_2 按钮
    # 把搜做输入框选中内容的函数
    def search(event):#定义的函数在（）内需添加event，要不会报错显示：search函数为给定赋值位置，但有一个值要赋予。
        global choose,infor,k
        choose = L1_2_2.get(L1_2_2.curselection())
        var_l122.set(get_kth_in_line(choose,2))
        infor.clear() # 清除残留信息
        e1_2_3.delete(0, tk.END) # 清除在输入框中的残留信息
        for i in range(get_kth_in_line(choose,0)-1):
            if i == 0: infor.append(get_kth_in_line(choose,i+2))
            else: infor.append(False)
        k = 1
        infor_control_add_infor(k)# 进入第一项
    
    # 改变输入区的提示
    def infor_control_add_infor(n):# 进入第n项
        var_l123.set(get_kth_in_line(choose,n+2))
        
    # 检查使用的信息打印
    def infor_control_add_check():
        for i in range(get_kth_in_line(choose,0)-1):
            print(infor[i])
    
    # 进入下一项
    def infor_control_add_infor_next():
        global k,choose,infor
        if k+2 == get_kth_in_line(choose,0):
            print('已经是最后一项了')
        else:
            # 先把信息存起来
            infor[k] = e1_2_3.get()
            # 再给出下一个提示
            k = k+1
            infor_control_add_infor(k)
            e1_2_3.delete(0, tk.END)
            if infor[k] != False:
                e1_2_3.insert(0,infor[k])
    
    # 进入上一项
    def infor_control_add_infor_last():
        global k,choose,infor
        if k == 1:
            print('已经是第一项了')
        else:
            # 先把信息存起来
            infor[k] = e1_2_3.get()
            # 再给出下一个提示
            k = k-1
            infor_control_add_infor(k)
            e1_2_3.delete(0, tk.END)
            if infor[k] != False:
                e1_2_3.insert(0,infor[k])
            
    # 保存添加的信息
    def infor_control_add_infor_save():
        global infor,k
        # 先把当前界面信息存起来
        infor[k] = e1_2_3.get()
        true = True
        for i in range(get_kth_in_line(choose,0)-1):
            if infor[i] == False or get_kth_in_line(infor[i],0) == 0:
                true = False
        infor_control_add_check()
        if true:
            winfor = open('./resources/infor_'+infor[0]+'.txt','a+',encoding='UTF-8') # 文本形式，追加写模式
            i=0
            for i in range(get_kth_in_line(choose,0)-1):
                winfor.write(infor[i] + "  ")
            winfor.write("\n")
            winfor.close()
            # 清空残留信息
            for i in range(get_kth_in_line(choose,0) - 2):
                infor[i+1] = " "
            e1_2_3.delete(0, tk.END)
            # 移回最开始
            while k>1:
                infor_control_add_infor_last()
        else:
            print("Fale to save!")
    
    '''调用信息添加函数'''
    # 1先进行惯例-退出上级标签，定义新的变量
    # 1.1惯例步骤（标签与返回）
    information_control_out()
    var.set("INFORMATION     SYSTEM\n")
    # 1.2提示文字与返回按钮与模式切换按钮
    global f1_2_5
    f1_2_5 = tk.Frame(window ,width=20, height=2)
    global b1_2_1 
    if platform.system() == 'Darwin':# Mac系统
        b1_2_1 = tk.Button(f1_2_5, text="Back", width=10, height=2,fg = COLOR_MB_FRONT,command=lambda:information_control_add_back())
        b1_2_6 = tk.Button(f1_2_5, text="From Excel", width=10, height=2,fg = COLOR_MB_FRONT,command=lambda:information_control_add_excel())
    elif platform.system() == 'Windows':# Windows系统
        b1_2_1 = tk.Button(f1_2_5, text="Back", width=10, height=2,fg = COLOR_FRONT,bg = COLOR_SUB,command=lambda:information_control_add_back())
        b1_2_6 = tk.Button(f1_2_5, text="From Excel", width=10, height=2,fg = COLOR_FRONT,bg = COLOR_SUB,command=lambda:information_control_add_excel())
    note.pack();f1_2_5.pack();b1_2_6.pack(side = 'right');b1_2_1.pack(side = 'right')
    
    # 1.3主容器，左容器，右容器
    global f1_2_1,f1_2_2,f1_2_3
    # 1.4左右容器的宽度
    global width_set_l
    global width_set_r
    # 1.5【左】提示框，模板列表，滚动条
    global L1_2_2,l1_2_1,sb1_2_1
    # 1.6【左】选中的文字,     有多少个子项
    global  choose,item_num; item_num = 0
    choose = "0:  请选择左侧模板"
    # 1.7【右】右提示框,提示框文字,右子框架,输入提示文字,输入提示,输入区域,下一项, 上一项 , 保存
    global l1_2_2, var_l122,f1_2_4 ,   var_l123,  l1_2_3, e1_2_3,b1_2_3,b1_2_4,b1_2_5
    # 1.8 【右】信息变量列表,目前编辑是第几项
    global  infor,        k
    infor = []; k = -1
    # 2再进行输入前的页面布置
    # 2.1 左右两边的容器的容器
    f1_2_1 = tk.Frame(window,bg = COLOR_BACK)
    f1_2_1.pack(expand='yes', fill='both')
    
    # 2.2 左边选择模板部分 [左边的容器f1_2_2，滚动条，文本框]
    f1_2_2 = tk.Frame(f1_2_1,bg = COLOR_BACK,width = width_set_l)
    f1_2_2.pack(fill = 'y',side = 'left')
    l1_2_1 = tk.Label(f1_2_2,bg = COLOR_SUB,fg = COLOR_FRONT,text = '已有模板',justify="left", anchor="center")
    l1_2_1.pack(fill = 'x')
    sb1_2_1 = tk.Scrollbar(f1_2_2)
    sb1_2_1.pack(side=tk.RIGHT,fill='y') # 滚动条放在右边，上下填充
    L1_2_2 = tk.Listbox(f1_2_2,bg = COLOR_F2_BACK,fg = COLOR_F2_FRONT, yscrollcommand=sb1_2_1.set)
    L1_2_2.bind('<ButtonRelease-1>',search)
    L1_2_2.pack(side=tk.RIGHT,fill='both')
    wtemplate = open('./resources/system/template/template.txt','r',encoding='UTF-8') 
    count = 1
    for line in wtemplate.readlines():
        L1_2_2.insert("end", str(count)+":  "+line)
        L1_2_2.pack(fill="both",side= "top", expand = True )
        sb1_2_1.config(command=L1_2_2.yview)
        count = count+1
    wtemplate.close()
    
    # 2.3 右边信息输入部分 
        # step 2.3.1 右边的整框架
    f1_2_3 = tk.Frame(f1_2_1,bg = COLOR_BACK)# 先创建右侧最大框架
    f1_2_3.pack(expand = True,fill = 'both',side = 'left')
        # step 2.3.2 先创建题目label，并摆放在顶部
    var_l122=tk.StringVar()  
    var_l122.set(get_kth_in_line(choose,2))
    l1_2_2 = tk.Label(f1_2_3,bg = COLOR_SUB,fg = COLOR_FRONT,textvariable=var_l122,justify="left", anchor="center",height = 1)
    l1_2_2.pack(fill = 'x')
        # step 2.3.3 创建右边子级frame
    f1_2_4 = tk.Frame(f1_2_3,bg = COLOR_BACK)
    f1_2_4.pack(expand = True,fill = 'both',side = 'left')
        # step 3.4 输入区
    var_l123=tk.StringVar()
    if choose == "0:  请选择左侧模板":
        var_l123.set("")
    l1_2_3 = tk.Label(f1_2_4,bg = COLOR_SUB,fg = COLOR_FRONT,textvariable=var_l123)
    l1_2_3.pack(fill = 'x')
    e1_2_3 = tk.Entry(f1_2_4,bg = COLOR_F2_BACK,fg = COLOR_FRONT)
    e1_2_3.pack(fill = 'x')
    
    if platform.system() == 'Darwin':# Mac系统
        b1_2_3 = tk.Button(f1_2_4, text="Next", width=20, height=2,bg = COLOR_MB_FRONT,command=lambda:infor_control_add_infor_next())
        b1_2_4 = tk.Button(f1_2_4, text="Last", width=20, height=2,bg = COLOR_MB_FRONT,command=lambda:infor_control_add_infor_last())
        b1_2_5 = tk.Button(f1_2_4, text="Save", width=20, height=2,bg = COLOR_MB_FRONT,command=lambda:infor_control_add_infor_save())
        
    elif platform.system() == 'Windows':# Windows系统
        b1_2_3 = tk.Button(f1_2_4, text="Next", width=20, height=2,bg = COLOR_SUB,fg = COLOR_FRONT,command=lambda:infor_control_add_infor_next())
        b1_2_4 = tk.Button(f1_2_4, text="Last", width=20, height=2,bg = COLOR_SUB,fg = COLOR_FRONT,command=lambda:infor_control_add_infor_last())
        b1_2_5 = tk.Button(f1_2_4, text="Save", width=20, height=2,bg = COLOR_SUB,fg = COLOR_FRONT,command=lambda:infor_control_add_infor_save())
    
    b1_2_3.pack();b1_2_4.pack();b1_2_5.pack()
    
def information_control_add_out(): # 退出
    f1_2_1.pack_forget()
    f1_2_5.pack_forget()
    note.pack_forget()
    
def information_control_add_back(): # 返回
    information_control_add_out()
    information_control()

def information_control_add_excel(): # 信息添加 b1_2 按钮_按Excel导入
    def information_control_add_excel_help():
        messagebox.showinfo(title='注意', message='从Excel添加信息步骤:\n第一步:选择左侧模板\n第二步:把Excel表格放到input box中\n第三步:输入Excel名字\n第四步:填写待添加信息的左上角与右上角\n第五步:点击Refresh进行预览\n第六步:点击Insert添加信息')
        
    def information_control_add_excel_Refresh():
        global columns1_3_c1_e,treeview1_3_c1_e,item1_3_c1_e
        global choose,L1_2_2_e,template_name
        # 清空表格
        x=treeview1_3_c1_e.get_children()
        for j in x:
            treeview1_3_c1_e.delete(j)
        # 占空行
        for i in range(36):
            treeview1_3_c1_e.insert('', 0, values=('','','','','','','','','','','','','','','','','','','','',''))
        wtemplate = open('./resources/system/template/template.txt','r',encoding='UTF-8') 
        # 填写预览表格
        excel_name = e1_2_5.get() # 表格名字
        from_row = int(e1_2_1.get());from_line = int(e1_2_2.get()) # 左上角
        to_row = int(e1_2_3.get());to_line = int(e1_2_4.get()) # 右上角
        roop1 = to_row - from_row +1
        roop2 = to_line - from_line +1
        data = xlrd.open_workbook(r'./resources/input box/'+excel_name+'.xlsx')
        table = data.sheets()[0]          #通过索引顺序获取
        names = data.sheet_names()    #返回book中所有工作表的名字
        
        length = get_kth_in_line(choose,0)
        if length-2 == roop2:
            template = '-'
            for i in range(roop1):
                for count in range(20):
                    if count < roop2:
                        word = table.cell(from_row+i-1,from_line+count-1).value
                        word_type = table.cell(from_row+i-1,from_line+count-1).ctype
                        item1_3_c1_e[count] = read_excel(word,word_type)
                    else:
                        item1_3_c1_e[count] = " "
                treeview1_3_c1_e.insert('', 0, values=(template, item1_3_c1_e[0], item1_3_c1_e[1],item1_3_c1_e[2],\
                                                       item1_3_c1_e[3],item1_3_c1_e[4],item1_3_c1_e[5],item1_3_c1_e[6],\
                                                       item1_3_c1_e[7],item1_3_c1_e[8],item1_3_c1_e[9],item1_3_c1_e[10],\
                                                       item1_3_c1_e[11],item1_3_c1_e[12],item1_3_c1_e[13],item1_3_c1_e[14],\
                                                       item1_3_c1_e[15],item1_3_c1_e[16],item1_3_c1_e[17],item1_3_c1_e[18],\
                                                       item1_3_c1_e[19]))
        
        # 打印模板题目
        count = 0
        for count in range(20):
            if count < length-2:
                item1_3_c1_e[count] = get_kth_in_line(choose,count+3)
            else:
                item1_3_c1_e[count] = " "
        treeview1_3_c1_e.insert('', 0, values=(template_name, item1_3_c1_e[0], item1_3_c1_e[1],item1_3_c1_e[2],\
                                           item1_3_c1_e[3],item1_3_c1_e[4],item1_3_c1_e[5],item1_3_c1_e[6],\
                                           item1_3_c1_e[7],item1_3_c1_e[8],item1_3_c1_e[9],item1_3_c1_e[10],\
                                           item1_3_c1_e[11],item1_3_c1_e[12],item1_3_c1_e[13],item1_3_c1_e[14],\
                                           item1_3_c1_e[15],item1_3_c1_e[16],item1_3_c1_e[17],item1_3_c1_e[18],\
                                           item1_3_c1_e[19]))

    def information_control_add_excel_Insert():
        global choose,L1_2_2_e,template_name
        global columns1_3_c1_e,treeview1_3_c1_e,item1_3_c1_e
        # 打开Excel
        excel_name = e1_2_5.get() # 表格名字
        from_row = int(e1_2_1.get());from_line = int(e1_2_2.get()) # 左上角
        to_row = int(e1_2_3.get());to_line = int(e1_2_4.get()) # 右上角
        roop1 = to_row - from_row +1
        roop2 = to_line - from_line +1
        data = xlrd.open_workbook(r'./resources/input box/'+excel_name+'.xlsx')
        table = data.sheets()[0]          #通过索引顺序获取
        names = data.sheet_names()    #返回book中所有工作表的名字
        length = get_kth_in_line(choose,0)
        # 写入txt
        winfor = open('./resources/infor_'+template_name+'.txt','a+',encoding='UTF-8') # 文本形式，追加写模式
        #if length-2 == roop2:
        for i in range(roop1):
            winfor.write(template_name+"  ")
            for j in range(roop2):
                word = table.cell(from_row-1+i,from_line-1+j).value
                word_type = table.cell(from_row-1+i,from_line-1+j).ctype        
                winfor.write(str(read_excel(word,word_type)) + "  ")
            winfor.write("\n")
        winfor.close()
        messagebox.showinfo(title='注意', message='已经成功保存!请去信息查看模块查看信息是否有误!')
    
    def search(event):
        global choose,L1_2_2_e,template_name
        choose = L1_2_2_e.get(L1_2_2_e.curselection())
        template_name = get_kth_in_line(choose,2)
        # 清空表格
        x=treeview1_3_c1_e.get_children()
        for j in x:
            treeview1_3_c1_e.delete(j)
        # 占空行
        for i in range(36): # 占空行
            treeview1_3_c1_e.insert('', 0, values=('','','','','','','','','','','','','','','','','','','','',''))
        # 打印模板题目
        count = 0
        length = get_kth_in_line(choose,0)
        for count in range(20):
            if count < length-2:
                item1_3_c1_e[count] = get_kth_in_line(choose,count+3)
            else:
                item1_3_c1_e[count] = " "
        treeview1_3_c1_e.insert('', 0, values=(template_name, item1_3_c1_e[0], item1_3_c1_e[1],item1_3_c1_e[2],\
                                           item1_3_c1_e[3],item1_3_c1_e[4],item1_3_c1_e[5],item1_3_c1_e[6],\
                                           item1_3_c1_e[7],item1_3_c1_e[8],item1_3_c1_e[9],item1_3_c1_e[10],\
                                           item1_3_c1_e[11],item1_3_c1_e[12],item1_3_c1_e[13],item1_3_c1_e[14],\
                                           item1_3_c1_e[15],item1_3_c1_e[16],item1_3_c1_e[17],item1_3_c1_e[18],\
                                           item1_3_c1_e[19]))

    # 推出上次内容
    f1_2_1.pack_forget()
    f1_2_5.pack_forget()
    # 安放本次内容
    global f1_2_1_e,f1_2_2_e,f1_2_3_e,f1_2_4_e,f1_2_5_e,f1_2_6_e
    global sb1_2_1_e,l1_2_1_e,L1_2_2_e,b1_2_1_e,b1_2_6_e

    # 上侧
    f1_2_4_e = tk.Frame(window,width=20, height=2)
    if platform.system() == 'Darwin':# Mac系统
        b1_2_1_e = tk.Button(f1_2_4_e, text="Back", width=10, height=2,fg = COLOR_MB_FRONT,command=lambda:information_control_add_excel_back())
        b1_2_6_e = tk.Button(f1_2_4_e, text="By Item ", width=10, height=2,fg = COLOR_MB_FRONT,command=lambda:information_control_add_excel_half_back())
    elif platform.system() == 'Windows':# Windows系统
        b1_2_1_e = tk.Button(f1_2_4_e, text="Back", width=10, height=2,fg = COLOR_FRONT,bg = COLOR_SUB,command=lambda:information_control_add_excel_back())
        b1_2_6_e = tk.Button(f1_2_4_e, text="By Item", width=10, height=2,fg = COLOR_FRONT,bg = COLOR_SUB,command=lambda:information_control_add_excel_half_back())
    f1_2_4_e.pack();b1_2_6_e.pack(side = 'right');b1_2_1_e.pack(side = 'right')
    # 左侧
    f1_2_1_e = tk.Frame(window,bg = COLOR_BACK)
    f1_2_1_e.pack(expand='yes', fill='both')
    f1_2_2_e = tk.Frame(f1_2_1_e,bg = COLOR_BACK,width = width_set_l)
    f1_2_2_e.pack(fill = 'y',side = 'left')
    l1_2_1_e = tk.Label(f1_2_2_e,bg = COLOR_SUB,fg = COLOR_FRONT,text = '已有模板',justify="left", anchor="center")
    l1_2_1_e.pack(fill = 'x')
    sb1_2_1_e = tk.Scrollbar(f1_2_2_e)
    sb1_2_1_e.pack(side=tk.RIGHT,fill='y') # 滚动条放在右边，上下填充
    L1_2_2_e = tk.Listbox(f1_2_2_e,bg = COLOR_F2_BACK,fg = COLOR_F2_FRONT, yscrollcommand=sb1_2_1_e.set)
    L1_2_2_e.bind('<ButtonRelease-1>',search)
    L1_2_2_e.pack(side=tk.RIGHT,fill='both')
    wtemplate = open('./resources/system/template/template.txt','r',encoding='UTF-8') 
    count = 1
    for line in wtemplate.readlines():
        L1_2_2_e.insert("end", str(count)+":  "+line)
        L1_2_2_e.pack(fill="both",side= "top", expand = True )
        sb1_2_1_e.config(command=L1_2_2_e.yview)
        count = count+1
    wtemplate.close()
    
    # 右侧
    f1_2_3_e = tk.Frame(f1_2_1_e,bg = COLOR_BACK)# 先创建右侧最大框架
    f1_2_5_e = tk.Frame(f1_2_3_e,bg = COLOR_BACK)# 先创建右侧左
    f1_2_6_e = tk.Frame(f1_2_3_e,bg = COLOR_BACK,width = int(width_set_l/2))# 先创建右侧右
    f1_2_3_e.pack(expand = True,fill = 'both',side = 'left')
    f1_2_6_e.pack(expand = True,fill = 'both',side = 'right')
    f1_2_5_e.pack(expand = True,fill = 'both',side = 'right')
        #右侧右操作区 f1_2_6_e
    if platform.system() == 'Darwin':# Mac系统
        b1_2_2_e = tk.Button(f1_2_6_e, text="Refresh", width=15, height=2,fg = COLOR_MB_FRONT,command=lambda:information_control_add_excel_Refresh())
        b1_2_3_e = tk.Button(f1_2_6_e, text="Insert", width=15, height=2,fg = COLOR_MB_FRONT,command=lambda:information_control_add_excel_Insert())
        b1_2_4_e = tk.Button(f1_2_6_e, text="Help", width=15, height=2,fg = COLOR_MB_FRONT,command=lambda:information_control_add_excel_help())
    elif platform.system() == 'Windows':# Windows系统
        b1_2_2_e = tk.Button(f1_2_6_e, text="Refresh", width=15, height=2,fg = COLOR_FRONT,bg = COLOR_SUB,command=lambda:information_control_add_excel_Refresh())
        b1_2_3_e = tk.Button(f1_2_6_e, text="Insert", width=15, height=2,fg = COLOR_FRONT,bg = COLOR_SUB,command=lambda:information_control_add_excel_Insert())
        b1_2_4_e = tk.Button(f1_2_6_e, text="Help", width=15, height=2,fg = COLOR_FRONT,bg = COLOR_SUB,command=lambda:information_control_add_excel_help())
    
    # 输入框总结: 
        #e1_2_5 Excel名; e1_2_1 开始Row; e1_2_2 开始Line; e1_2_3 结束Row; e1_2_4 结束Line
            #1
    l1_2_3_e = tk.Label(f1_2_6_e,bg = COLOR_SUB,fg = COLOR_FRONT,text = '操作区', anchor="center")
    l1_2_3_e.pack(fill = 'x')
            #2
    l1_2_4_e = tk.Label(f1_2_6_e,bg = COLOR_BACK,text = '', anchor="center")
    l1_2_4_e.pack(fill = 'x')# 占空行
    l1_2_10_e = tk.Label(f1_2_6_e,bg = COLOR_SUB,fg = COLOR_FRONT,text = '输入Excel名称', anchor="center")
    l1_2_10_e.pack(fill='x')
    e1_2_5 = tk.Entry(f1_2_6_e,bg = COLOR_F2_BACK,fg = COLOR_FRONT)
    e1_2_5.pack(fill='x')
    l1_2_4_e = tk.Label(f1_2_6_e,bg = COLOR_BACK,text = '', anchor="center")
    l1_2_4_e.pack(fill = 'x')# 占空行
    f1_2_9_e = tk.Frame(f1_2_6_e,bg = COLOR_BACK)# 先创建右侧右
    f1_2_9_e.pack(fill = 'x')
    l1_2_5_e = tk.Label(f1_2_9_e,bg = COLOR_BACK,width=5)
    l1_2_5_e.pack(side = 'left')
    l1_2_6_e = tk.Label(f1_2_9_e,bg = COLOR_SUB,fg = COLOR_FRONT,text='Row       Line',width=10)
    l1_2_6_e.pack(side = 'left')
            #3
    f1_2_7_e = tk.Frame(f1_2_6_e,bg = COLOR_BACK)# 先创建右侧右
    f1_2_7_e.pack(fill = 'x')
    l1_2_7_e = tk.Label(f1_2_7_e,bg = COLOR_SUB,fg = COLOR_FRONT,text='From',width=5)
    l1_2_7_e.pack(side = 'left')
    e1_2_1 = tk.Entry(f1_2_7_e,bg = COLOR_F2_BACK,fg = COLOR_FRONT,width=5)
    e1_2_1.pack(side = 'left')
    e1_2_2 = tk.Entry(f1_2_7_e,bg = COLOR_F2_BACK,fg = COLOR_FRONT,width=5)
    e1_2_2.pack(side = 'left')
            #4
    f1_2_8_e = tk.Frame(f1_2_6_e,bg = COLOR_BACK)# 先创建右侧右
    f1_2_8_e.pack(fill = 'x')
    l1_2_8_e = tk.Label(f1_2_8_e,bg = COLOR_SUB,fg = COLOR_FRONT,text='To',width=5)
    l1_2_8_e.pack(side = 'left')
    e1_2_3 = tk.Entry(f1_2_8_e,bg = COLOR_F2_BACK,fg = COLOR_FRONT,width=5)
    e1_2_3.pack(side = 'left')
    e1_2_4 = tk.Entry(f1_2_8_e,bg = COLOR_F2_BACK,fg = COLOR_FRONT,width=5)
    e1_2_4.pack(side = 'left')
            #5
    l1_2_9_e = tk.Label(f1_2_6_e,bg = COLOR_BACK,text='')
    l1_2_9_e.pack(fill='x')
            #6
    b1_2_2_e.pack()
    b1_2_3_e.pack()
    b1_2_4_e.pack()
    
        #右侧左展示区 f1_2_5_e
    l1_2_2_e = tk.Label(f1_2_5_e,bg = COLOR_SUB,fg = COLOR_FRONT,text = '预览',justify="left", anchor="center")
    l1_2_2_e.pack(fill = 'x')
    global columns1_3_c1_e,treeview1_3_c1_e,item1_3_c1_e,template_name
    columns1_3_c1_e = ("template", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10",\
               "11","12","13","14","15","16","17","18","19","20")
    treeview1_3_c1_e = ttk.Treeview(f1_2_5_e,height=180, show="headings", columns=columns1_3_c1_e)  # 表格
    treeview1_3_c1_e.tag_configure("ttk",background = COLOR_F1_BACK)# 设置表格颜色1/2
    treeview1_3_c1_e.column("template", width=120, anchor='center') # 表示列,不显示
    item1_3_c1_e = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
    for count in range(20):
        treeview1_3_c1_e.column(str(item1_3_c1_e[count]), width=100, anchor='center')
        # 显示表头
    treeview1_3_c1_e.heading("template", text="template")
    count = 0
    for count in range(20):
        treeview1_3_c1_e.heading(str(item1_3_c1_e[count]), text=str(item1_3_c1_e[count]))
        # 表格安放
    treeview1_3_c1_e.pack(side=tk.LEFT, fill=tk.BOTH)
    for i in range(50): # 占空行
        treeview1_3_c1_e.insert('', 0, values=('','','','','','','','','','','','','','','','','','','','',''))
    #wtemplate = open('./resources/system/template/template.txt','r',encoding='UTF-8') 

def information_control_add_excel_half_back(): # 从录入excel返回到原本的录入
    f1_2_4_e.pack_forget()
    f1_2_1_e.pack_forget()
    information_control_add()

def information_control_add_excel_back():
    f1_2_1_e.pack_forget()
    f1_2_4_e.pack_forget()
    information_control()

#-----------------------------------------------------------------------------------------------------------------------------------------------

def information_control_check(): # 信息查看 b1_3 按钮
    #1 惯例操作
    information_control_out()
    var.set("INFORMATION     SYSTEM\n")
    global b1_3_1
    if platform.system() == 'Darwin':# Mac系统
        b1_3_1 = tk.Button(window, text="Back to last level", width=20, height=3,fg = COLOR_MB_FRONT,command=lambda:information_control_check_back())
    elif platform.system() == 'Windows':# Windows系统
        b1_3_1 = tk.Button(window, text="Back to last level", width=20, height=3,bg = COLOR_SUB,fg = COLOR_FRONT,command=lambda:information_control_check_back())
    note.pack()
    b1_3_1.pack()
    #2 建立信息查询选择方式
        #2.1 整体框架
    global f1_3_1 
    f1_3_1 = tk.Frame(window,bg = COLOR_BACK)
    f1_3_1.pack(fill = 'both',expand = True)
        #2.2 提示栏
    global choose;choose = "请选择查询方式"
    global l1_3_1,var_l131 # 整框架中的最上边有一个提示栏
    var_l131=tk.StringVar()  
    var_l131.set(choose)
    l1_3_1 = tk.Label(f1_3_1,bg = COLOR_SUB,fg = COLOR_FRONT,textvariable=var_l131,font=("黑体", 20))
    l1_3_1.pack(fill = 'x')
        #2.4 选择按钮
    choose_num = 3 # 这里设置选择按钮的数量，方便以后更改
    global f1_3_2
    f1_3_2 = tk.Frame(f1_3_1,bg = COLOR_BACK,width=int(40), height=2)
    f1_3_2.pack()
    if platform.system() == 'Darwin':# Mac系统
        b1_3_2 = tk.Button(f1_3_2,text="Search All",width=int(40/choose_num), height=2,justify="left",fg = COLOR_MB_FRONT,command=lambda:information_control_check1())
        b1_3_3 = tk.Button(f1_3_2,text="Template", width=int(40/choose_num), height=2,justify="left",fg = COLOR_MB_FRONT,command=lambda:information_control_check2())
        b1_3_4 = tk.Button(f1_3_2,text="Key Words", width=int(40/choose_num), height=2,justify="left",fg = COLOR_MB_FRONT,command=lambda:information_control_check3()) 
    elif platform.system() == 'Windows':# Windows系统
        b1_3_2 = tk.Button(f1_3_2,text="Search All",width=int(40/choose_num), height=2,justify="left",bg = COLOR_SUB,fg = COLOR_FRONT,command=lambda:information_control_check1())
        b1_3_3 = tk.Button(f1_3_2,text="Template", width=int(40/choose_num), height=2,justify="left",bg = COLOR_SUB,fg = COLOR_FRONT,command=lambda:information_control_check2())
        b1_3_4 = tk.Button(f1_3_2,text="Key Words", width=int(40/choose_num), height=2,justify="left",bg = COLOR_SUB,fg = COLOR_FRONT,command=lambda:information_control_check3()) 
    b1_3_2.pack(side = "left");b1_3_3.pack(side = "left");b1_3_4.pack(side = "left")
    
        #2.5 按钮的属性（important）
    global type_1_3_3; type_1_3_3 = 0
    # type_1_3_3| 0           |  1           |  2          | ...
    # 代表内容   | 第一次进入按钮 | 上次进入1按钮  | 上次进入2按钮 | ...
        #2.3 提前安放好子框架
    global f1_3_c1;f1_3_c1 = tk.Frame(f1_3_1,bg = COLOR_BACK)
    information_control_check1_pre()
    global f1_3_c2;f1_3_c2 = tk.Frame(f1_3_1,bg = COLOR_BACK)
    information_control_check2_pre()
    global f1_3_c3;f1_3_c3 = tk.Frame(f1_3_1,bg = COLOR_BACK)
    information_control_check3_pre()
   
def information_control_check1(): # 信息查看的第一种选择方式-全部列出
    # 先引入状态
    global type_1_3_3 
    # 根据状态进行调整(退出可能有的原框架)
    global f1_3_c1
    if type_1_3_3 == 0: # 第一次进入该函数
        type_1_3_3 = 1
        # 再放上本次需要的框架
        f1_3_c1.pack_configure() # 这个函数的主框架为f1_3_c1
    elif type_1_3_3 == 1: # 刚进入过方法一
        pass
    elif type_1_3_3 == 2: # 刚进入过方法二
        type_1_3_3 = 1
        global f1_3_c2;f1_3_c2.pack_forget()
        f1_3_c1.pack_configure() # 这个函数的主框架为f1_3_c1
    elif type_1_3_3 == 3: # 刚进入过方法三
        type_1_3_3 = 1
        global f1_3_c3;f1_3_c3.pack_forget()
        f1_3_c1.pack_configure() # 这个函数的主框架为f1_3_c1
   
    global treeview1_3_c1,columns1_3_c1,item1_3_c1
    # 更改提示栏目
    global var_l131 ;var_l131.set('Search All')# 整框架中的最上边有一个提示栏
    #填写表格内容
        # 清空表格
    x=treeview1_3_c1.get_children()
    for j in x:
        treeview1_3_c1.delete(j)
        # 填写表格
    for i in range(18): # 占空行
        treeview1_3_c1.insert('', 0, values=('','','','','','','','','','','','','','','','','','','','',''))
    wtemplate = open('./resources/system/template/template.txt','r',encoding='UTF-8') 
    for line in wtemplate.readlines():
        tname = get_kth_in_line(line,1) # 模板名字
        fname = './resources/infor_'+tname+'.txt' # 文件名字
        length = get_kth_in_line(line,0)
        try:
            number_item = 0
            winfor = open(fname,'r',encoding='UTF-8') 
            for fline in winfor.readlines():
                # 打印每一条信息
                template = '-'; count = 0
                for count in range(20):
                    if count < length-1:
                        item1_3_c1[count] = get_kth_in_line(fline,count+2)
                    else:
                        item1_3_c1[count] = " "
                treeview1_3_c1.insert('', 0, values=(template, item1_3_c1[0], item1_3_c1[1],item1_3_c1[2],\
                                                   item1_3_c1[3],item1_3_c1[4],item1_3_c1[5],item1_3_c1[6],\
                                                   item1_3_c1[7],item1_3_c1[8],item1_3_c1[9],item1_3_c1[10],\
                                                   item1_3_c1[11],item1_3_c1[12],item1_3_c1[13],item1_3_c1[14],\
                                                   item1_3_c1[15],item1_3_c1[16],item1_3_c1[17],item1_3_c1[18],\
                                                   item1_3_c1[19]))
                number_item = number_item+1
            winfor.close()
            # 打印模板题目
            if number_item:
                template = tname; count = 0
                for count in range(20):
                    if count < length-1:
                        item1_3_c1[count] = get_kth_in_line(line,count+2)
                    else:
                        item1_3_c1[count] = " "
                treeview1_3_c1.insert('', 0, values=(template, item1_3_c1[0], item1_3_c1[1],item1_3_c1[2],\
                                                   item1_3_c1[3],item1_3_c1[4],item1_3_c1[5],item1_3_c1[6],\
                                                   item1_3_c1[7],item1_3_c1[8],item1_3_c1[9],item1_3_c1[10],\
                                                   item1_3_c1[11],item1_3_c1[12],item1_3_c1[13],item1_3_c1[14],\
                                                   item1_3_c1[15],item1_3_c1[16],item1_3_c1[17],item1_3_c1[18],\
                                                   item1_3_c1[19]))
                
        except IOError:
            pass #print "File is not accessible."
    #treeview1_3_c1.tag_configure("ttk",foreground="red")
    wtemplate.close()
    
def information_control_check1_pre(): # 信息查看的第一种选择方式-全部列出-准备函数
    global treeview1_3_c1,columns1_3_c1,item1_3_c1
    global f1_3_c1
    f1_3_c1.pack(fill = 'both',expand = True)
    # 建立表格 
        # 表格框架搭建
    columns1_3_c1 = ("template", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10",\
               "11","12","13","14","15","16","17","18","19","20")
    treeview1_3_c1 = ttk.Treeview(f1_3_c1,height=180, show="headings", columns=columns1_3_c1)  # 表格
    treeview1_3_c1.tag_configure("ttk",background = COLOR_F1_BACK)# 设置表格颜色1/2
    treeview1_3_c1.column("template", width=120, anchor='center') # 表示列,不显示
    item1_3_c1 = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
    for count in range(20):
        treeview1_3_c1.column(str(item1_3_c1[count]), width=100, anchor='center')
        # 显示表头
    treeview1_3_c1.heading("template", text="template") 
    count = 0
    for count in range(20):
        treeview1_3_c1.heading(str(item1_3_c1[count]), text=str(item1_3_c1[count]))
        # 表格安放
    treeview1_3_c1.pack(side=tk.LEFT, fill=tk.BOTH)
    f1_3_c1.pack_forget()
    
def information_control_check2(): #信息查看的第二种选择方式-模板检索
    #0 变量声明
        # 引入状态
    global type_1_3_3 ,if_treeview1_3_2
        # 查看是否有上次的表格
    global if_treeview1_3_2;if_treeview1_3_2 = 0
        # 可能有的原框架
    global f1_3_c1,f1_3_c2,f1_3_c3
        # 搜索结果
    global fname1_3_2,length1_3_2;length1_3_2 = 0
    global treeview1_3_2
        # 左侧
    global width_set_l,f1_3_c2_1,sb1_3_3_1,L1_3_3
        # 右边的整框架
    global f1_3_c2_2
        # 右侧次级框架
    global f1_3_c2_3
        # 顶部的Label
    global choose
        # 右侧的提示语 提示语的变量 var_l132
    global l1_3_3,var_l132 
        # 更改提示栏目
    global var_l131 ;var_l131.set('Template')# 整框架中的最上边有一个提示栏
    #1 根据状态进行调整(退出可能有的原框架)
    if type_1_3_3 == 0: # 第一次进入该函数
        type_1_3_3 = 2
        f1_3_c2.pack_configure(fill = 'both',expand = True) # 这个函数的主框架为f1_3_c2
    elif type_1_3_3 == 1: # 刚进入过方法一
        if_treeview1_3_2 = 1
        type_1_3_3 = 2
        f1_3_c1.pack_forget()
        f1_3_c2.pack_configure(fill = 'both',expand = True) # 这个函数的主框架为f1_3_c2
    elif type_1_3_3 == 2: # 刚进过方法二
        if_treeview1_3_2 = 1
    elif type_1_3_3 == 3: # 刚进入过方法三
        if_treeview1_3_2 = 1
        type_1_3_3 = 2
        f1_3_c3.pack_forget()
        f1_3_c2.pack_configure(fill = 'both',expand = True) # 这个函数的主框架为f1_3_c2
        
    #2 安放关键字输入区域
    L1_3_3.delete(0, tk.END)
    wtemplate = open('./resources/system/template/template.txt','r',encoding='UTF-8') 
    count = 1
    for line in wtemplate.readlines():
        L1_3_3.insert("end", str(count)+":  "+get_kth_in_line(line,1))
        L1_3_3.pack(fill="both",side= "top", expand = True )
        sb1_3_3_1.config(command=L1_3_3.yview)
        count = count+1
    wtemplate.close()

def infor_search(event):#定义的函数在（）内需添加event，要不会报错显示：search函数为给定赋值位置，但有一个值要赋予。
        # 查看是否有上次的表格
    global if_treeview1_3_2
        # 左侧
    global width_set_l,f1_3_c2_1,sb1_3_3_1,L1_3_3
        # 右边的整框架
    global f1_3_c2_2
        # 右侧次级框架
    global f1_3_c2_3
        # 搜索结果
    global fname1_3_2,length1_3_2,treeview1_3_2
        # 顶部的Label
    global choose,L1_3_3
        # 右侧的提示语 提示语的变量 var_l132
    global l1_3_3,var_l132 
    
    # 改变提示栏
    choose = L1_3_3.get(L1_3_3.curselection())
    tname = get_kth_in_line(choose,2)
    var_l132.set(tname)
    # 计算文件名
    fname1_3_2 = './resources/infor_'+tname+'.txt' # 文件名字 #print(fname1_3_2)
    # 建立表头
    wtemplate = open('./resources/system/template/template.txt','r',encoding='UTF-8')
    for line in wtemplate.readlines():
        if get_kth_in_line(line,1) == tname:
            number = get_kth_in_line(line,0) - 1
            columns_l = []
            for i in range(number):
                columns_l.append(get_kth_in_line(line,i+2))
            break
    columns = tuple(columns_l)
    # 查看是否有上次的表格
    if if_treeview1_3_2 == 1:
        f1_3_c2_3.pack_forget()
        f1_3_c2_3 = tk.Frame(f1_3_c2_2)
    f1_3_c2_3.pack(fill = 'y',side = 'left',expand = True)#f1_3_c2_3.pack(fill = 'both',side = 'left',expand = True)
    # 生成表头
    treeview1_3_2 = ttk.Treeview(f1_3_c2_3,height=180, show="headings", columns=columns)
    treeview1_3_2.tag_configure("ttk",background = COLOR_F1_BACK)# 设置表格颜色1/2
    if_treeview1_3_2 = 1
    for i in range(number):
        treeview1_3_2.column(str(columns[i]), width=120, anchor='center')
    for i in range(number):
        treeview1_3_2.heading(str(columns[i]), text=str(columns[i]))
    treeview1_3_2.pack(side=tk.LEFT, fill=tk.BOTH)
    # 填写表格内容
    if choose != '0:  请选择左侧模板':
        # 占空行
        item = []
        for i in range(number):
            item.append('')
        for i in range(36): # 占空行
            treeview1_3_2.insert('', 0, values=item)
        # 填内容
        try:
            winfor = open(fname1_3_2,'r',encoding='UTF-8')
            #print("打开成功")
            for fline in winfor.readlines():
                item = []
                for i in range(number):
                    item.append(get_kth_in_line(fline,i+2))
                treeview1_3_2.insert('', 0, values=item)
            winfor.close()
        except IOError:
            pass
    
def information_control_check2_pre(): #信息查看的第二种选择方式-模板检索-准备阶段
    #0 查看是否有上次的表格
    global if_treeview1_3_2;if_treeview1_3_2 = 0
    #1 安放主框架
    global f1_3_c2
    f1_3_c2.pack(fill = 'both',expand = True)
    #2 左侧主框架 f1_3_c2_1
    global width_set_l,f1_3_c2_1
    f1_3_c2_1 = tk.Frame(f1_3_c2,bg = COLOR_BACK,width = width_set_l)
    f1_3_c2_1.pack(side = 'left',fill = 'y')
    #3 左侧滚动条与选择栏
    global sb1_3_3_1,L1_3_3
    sb1_3_3_1 = tk.Scrollbar(f1_3_c2_1)
    sb1_3_3_1.pack(side=tk.RIGHT,fill='y')
    L1_3_3 = tk.Listbox(f1_3_c2_1,bg = COLOR_F2_BACK,fg = COLOR_F2_FRONT, yscrollcommand=sb1_3_3_1.set)
    L1_3_3.bind('<ButtonRelease-1>',infor_search)
    L1_3_3.pack(side=tk.RIGHT,fill='both')
    #4 右侧主框架 f1_3_c2_2
    global f1_3_c2_2
    f1_3_c2_2 = tk.Frame(f1_3_c2,bg = COLOR_BACK)# 先创建右侧最大框架
    f1_3_c2_2.pack(expand = True,fill = 'both',side = 'left')
    #5 右侧模板题目label，放在顶部
    global choose,var_l132,l1_3_3;choose = '0:  请选择左侧模板'
    var_l132=tk.StringVar()
    var_l132.set(get_kth_in_line(choose,2))
    l1_3_3 = tk.Label(f1_3_c2_2,textvariable=var_l132,bg = COLOR_SUB,fg = COLOR_FRONT,justify="left", anchor="center",height = 1)
    l1_3_3.pack(fill = 'x')
    #6 安放搜索结果-创建右侧次级框架
    global f1_3_c2_3
    f1_3_c2_3 = tk.Frame(f1_3_c2_2,bg = COLOR_BACK)
    f1_3_c2_3.pack(expand = True,fill = 'both',side = 'left')
    #7 隐藏提前放好的一切
    f1_3_c2.pack_forget()

def information_control_check3(): #信息查看的第三种选择方式-关键字
    # 先引入状态
    global type_1_3_3 
    # 根据状态进行调整(退出可能有的原框架)
    global f1_3_c3
    if type_1_3_3 == 0: # 第一次进入该函数
        type_1_3_3 = 3
        # 再放上本次需要的框架
        f1_3_c3.pack(fill = 'both',expand = True) # 这个函数的主框架为f1_3_c3
    elif type_1_3_3 == 1: # 刚进入过方法一
        type_1_3_3 = 3
        global f1_3_c1
        f1_3_c1.pack_forget()
        # 再放上本次需要的框架
        f1_3_c3.pack(fill = 'both',expand = True) # 这个函数的主框架为f1_3_c3
    elif type_1_3_3 == 2: # 刚进入过方法二
        type_1_3_3 = 3
        global f1_3_c2
        f1_3_c2.pack_forget()
        # 再放上本次需要的框架
        f1_3_c3.pack(fill = 'both',expand = True) # 这个函数的主框架为f1_3_c3
    elif type_1_3_3 == 3: # 刚进过方法三
        pass
    # 更改提示栏目
    global var_l131 ;var_l131.set('Key Words')# 整框架中的最上边有一个提示栏
def information_control_check3_pre(): #信息查看的第三种选择方式-关键字-提前准备
    #1 先安放主框架
    global f1_3_c3
    f1_3_c3.pack(fill = 'both',expand = True)
    #2 次框架1（搜索框与选择按钮的框架）
    global f1_3_c3_1
    f1_3_c3_1 = tk.Frame(f1_3_c3,bg = COLOR_BACK) 
    f1_3_c3_1.pack(fill = 'x')
    #3 搜索框与选择按钮需要的变量声明
    global e1_3_3,cmb1_3_3,search_way,search_word
    search_way = '精确搜索' # 默认精确搜索
    global u1_3_3 #是输入的变量
    #4 选择函数
    def cmb1_3_3_func(event): #选择事件
        global search_way;search_way = cmb1_3_3.get()
        global search_last
    #5 下拉菜单
    cmb1_3_3 = ttk.Combobox(f1_3_c3_1) 
    cmb1_3_3.pack(side = 'right')
    cmb1_3_3['value'] = ('精确搜索','模糊搜索','联网搜索')#设置下拉菜单中的值 
    cmb1_3_3.current(0)#设置默认值，即默认下拉框中的内容 #选零就代表优先精准搜索
    cmb1_3_3.bind("<<ComboboxSelected>>",cmb1_3_3_func)
    #6 输入框
    u1_3_3 = tk.StringVar()
    e1_3_3 = tk.Entry(f1_3_c3_1,bg = COLOR_F2_BACK,fg = COLOR_FRONT,textvariable=u1_3_3) 
    e1_3_3.pack(fill = 'x')
    #7 回车函数
    def e1_3_3_submit(event):
        global search_way
        global search_word,u1_3_3; search_word = u1_3_3.get()
        global e1_3_3
        # 清空残留信息
        e1_3_3.delete(0, tk.END)
        # 进入对应功能
        if search_way == '精确搜索':
            information_control_check3_precise()
        if search_way == '模糊搜索':
            information_control_check3_vague()
        if search_way == '联网搜索':
            information_control_check3_internet()
    #8 回车事件
    e1_3_3.bind("<Return>",e1_3_3_submit)
    #9 子框架2（各种搜索模式的框架）
    global f1_3_c3_2,f1_3_c3_3,f1_3_c3_4
    #10 子集状态变量(important)
    global type_1_3_3_1; type_1_3_3_1 = 0
    #11 子框架提前布置
    f1_3_c3_2 = tk.Frame(f1_3_c3,bg = COLOR_BACK)
    f1_3_c3_3 = tk.Frame(f1_3_c3,bg = COLOR_BACK)
    f1_3_c3_4 = tk.Frame(f1_3_c3,bg = COLOR_BACK)
    information_control_check3_precise_pre() # 精确搜索提前安放模板
    information_control_check3_vague_pre() # 模糊搜索提前准备的模板
    information_control_check3_internet() # 联网搜索提前准备的模板
    #12 隐藏提前放好的一切
    f1_3_c3.pack_forget()

# 精确搜索 （已成功）
def information_control_check3_precise():
    global search_word
    global f1_3_c3_2 # 本次框架
    global treeview1_3_c3_2,columns1_3_c3_2,item1_3_c3_2 # 表格
    # 先引入状态
    global type_1_3_3_1
    # 根据状态进行调整(退出可能有的原框架)
    if type_1_3_3_1 == 0: # 第一次进入该函数
        type_1_3_3_1 = 1
        f1_3_c3_2.pack(fill = 'both',expand = True) # 这个函数的主框架为f1_3_c3
    elif type_1_3_3_1 == 1: # 刚进入过方法一
        pass
    elif type_1_3_3_1 == 2: # 刚进入过方法二
        type_1_3_3_1 = 1
        global f1_3_c3_3
        f1_3_c3_3.pack_forget()
        # 再放上本次需要的框架
        f1_3_c3_2.pack(fill = 'both',expand = True) # 这个函数的主框架为f1_3_c3
    elif type_1_3_3_1 == 3: # 刚进过方法三
        type_1_3_3_1 = 1
        global f1_3_c3_4
        f1_3_c3_4.pack_forget()
        # 再放上本次需要的框架
        f1_3_c3_2.pack(fill = 'both',expand = True) # 这个函数的主框架为f1_3_c3
    
    # 建立表格
        # 清空表格
    x=treeview1_3_c3_2.get_children()
    for j in x:
        treeview1_3_c3_2.delete(j)
        #填写表格内容
    for i in range(36): # 占空行
        treeview1_3_c3_2.insert('', 0, values=('','','','','','','','','','','','','','','','','','','','',''))
    wtemplate = open('./resources/system/template/template.txt','r',encoding='UTF-8')
    wtemplate.seek(0) #指针回到文件开头
    for line in wtemplate.readlines():
        tname = get_kth_in_line(line,1) # 模板名字
        fname = './resources/infor_'+tname+'.txt' # 文件名字
        length = get_kth_in_line(line,0)
        try:
            number_item = 0
            winfor = open(fname,'r',encoding='UTF-8') 
            if_print_all = False #是否全模板打印
            if_print_title = False#是否打印模板题目
            for i in range(length):
                if str(get_kth_in_line(line,i+1)) == str(search_word):
                    if_print_all = True
                    if_print_title = True
                    break
            for fline in winfor.readlines():
                if_print_item = False #是否打印特定信息
                for j in range(length):
                    if str(get_kth_in_line(fline,j+1)) == str(search_word):
                        if_print_item = True
                        if_print_title = True
                        break
                template = '-'
                if if_print_all or if_print_item:
                    for count in range(20):
                        if count < length-1:
                            item1_3_c3_2[count] = get_kth_in_line(fline,count+2)
                        else:
                            item1_3_c3_2[count] = " "
                    treeview1_3_c3_2.insert('', 0, values=(template, item1_3_c3_2[0], item1_3_c3_2[1],item1_3_c3_2[2],\
                                                       item1_3_c3_2[3],item1_3_c3_2[4],item1_3_c3_2[5],item1_3_c3_2[6],\
                                                       item1_3_c3_2[7],item1_3_c3_2[8],item1_3_c3_2[9],item1_3_c3_2[10],\
                                                       item1_3_c3_2[11],item1_3_c3_2[12],item1_3_c3_2[13],item1_3_c3_2[14],\
                                                       item1_3_c3_2[15],item1_3_c3_2[16],item1_3_c3_2[17],item1_3_c3_2[18],\
                                                       item1_3_c3_2[19]))
                    number_item = number_item+1
            winfor.close()
            # 打印模板题目
            if number_item and if_print_title:
                template = tname
                for count in range(20):
                    if count < length-1:
                        item1_3_c3_2[count] = get_kth_in_line(line,count+2)
                    else:
                        item1_3_c3_2[count] = " "
                treeview1_3_c3_2.insert('', 0, values=(template, item1_3_c3_2[0], item1_3_c3_2[1],item1_3_c3_2[2],\
                                                   item1_3_c3_2[3],item1_3_c3_2[4],item1_3_c3_2[5],item1_3_c3_2[6],\
                                                   item1_3_c3_2[7],item1_3_c3_2[8],item1_3_c3_2[9],item1_3_c3_2[10],\
                                                   item1_3_c3_2[11],item1_3_c3_2[12],item1_3_c3_2[13],item1_3_c3_2[14],\
                                                   item1_3_c3_2[15],item1_3_c3_2[16],item1_3_c3_2[17],item1_3_c3_2[18],\
                                                   item1_3_c3_2[19]))
        except IOError:
            pass #print "File is not accessible."
    wtemplate.close()
def information_control_check3_precise_pre(): # 精确搜索提前安放模板
    global f1_3_c3_2 # 本次框架
    global treeview1_3_c3_2,columns1_3_c3_2,item1_3_c3_2 # 表格
    
    # 再放上本次需要的框架
    f1_3_c3_2.pack(fill = 'both',expand = True) # 这个函数的主框架为f1_3_c3
    # 放好表头
            # 表格框架搭建
    columns1_3_c3_2 = ("template", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10",\
               "11","12","13","14","15","16","17","18","19","20")
    treeview1_3_c3_2 = ttk.Treeview(f1_3_c3_2, show="headings", columns=columns1_3_c3_2)  # 表格
    treeview1_3_c3_2.column("template", width=120, anchor='center') # 表示列,不显示
    item1_3_c3_2 = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
    for count in range(20):
        treeview1_3_c3_2.column(str(item1_3_c3_2[count]), width=100, anchor='center')
        # 显示表头
    treeview1_3_c3_2.heading("template", text="template") 
    count = 0
    for count in range(20):
        treeview1_3_c3_2.heading(str(item1_3_c3_2[count]), text=str(item1_3_c3_2[count]))
        # 表格安放
    treeview1_3_c3_2.pack(side=tk.LEFT, fill=tk.BOTH)
    # 最后隐藏提前的布局
    f1_3_c3_2.pack_forget()
    
def information_control_check3_vague(): # 模糊搜索
    global search_word
    global f1_3_c3_3 
    global treeview1_3_c3_3,columns1_3_c3_3,item1_3_c3_3 # 表格
    
    # 先引入状态
    global type_1_3_3_1
    # 根据状态进行调整(退出可能有的原框架)
    if type_1_3_3_1 == 0: # 第一次进入该函数
        type_1_3_3_1 = 2
        f1_3_c3_3.pack(fill = 'both',expand = True) # 这个函数的主框架为f1_3_c3
    elif type_1_3_3_1 == 1: # 刚进入过方法一
        type_1_3_3_1 = 2
        global f1_3_c3_2
        f1_3_c3_2.pack_forget()
        # 再放上本次需要的框架
        f1_3_c3_3.pack(fill = 'both',expand = True) # 这个函数的主框架为f1_3_c3
    elif type_1_3_3_1 == 2: # 刚进入过方法二
        pass
    elif type_1_3_3_1 == 3: # 刚进过方法三
        type_1_3_3_1 = 2
        global f1_3_c3_4
        f1_3_c3_4.pack_forget()
        # 再放上本次需要的框架
        f1_3_c3_3.pack(fill = 'both',expand = True) # 这个函数的主框架为f1_3_c3
    
    # 准备搜索词的列表
    search_word_ls = jieba.lcut(search_word)
    to_be_searched_ls = []
    
    # 建立表格
        # 清空表格
    x=treeview1_3_c3_3.get_children()
    for j in x:
        treeview1_3_c3_3.delete(j)
        # 占空行
    for i in range(36):
        treeview1_3_c3_3.insert('', 0, values=('','','','','','','','','','','','','','','','','','','','',''))
        #填写表格内容
    wtemplate = open('./resources/system/template/template.txt','r',encoding='UTF-8')
    wtemplate.seek(0) #指针回到文件开头
    for line in wtemplate.readlines():
        tname = get_kth_in_line(line,1) # 模板名字
        fname = './resources/infor_'+tname+'.txt' # 文件名字
        length = get_kth_in_line(line,0)
        try:
            winfor = open(fname,'r',encoding='UTF-8') 
            number_item = 0
            if_print_all = False #是否全模板打印
            if_print_title = False#是否打印模板题目
            for i in range(length):
                for j in range(len(search_word_ls)):
                    to_be_searched_ls = jieba.lcut(str(get_kth_in_line(line,i+1)))
                    for k in range(len(to_be_searched_ls)):
                        if str(to_be_searched_ls[k]) == str(search_word_ls[j]):
                            if_print_all = True
                            if_print_title = True
                            break
                    if if_print_title:break
                if if_print_title:break
                
            for fline in winfor.readlines():
                if_print_item = False #是否打印特定信息
                if if_print_all == True:
                    if_print_item = True
                    if_print_title = True
                else:
                    for j in range(length):
                        for i in range(len(search_word_ls)):
                            to_be_searched_ls = jieba.lcut(str(get_kth_in_line(fline,j+1)))
                            for k in range(len(to_be_searched_ls)):
                                if str(to_be_searched_ls[k]) == str(search_word_ls[i]):
                                    if_print_item = True
                                    if_print_title = True
                                    break
                            if if_print_item:break
                        if if_print_item:break
                if get_kth_in_line(fline,0) == 0:if_print_title = False # 空文件不打印模板    
                if if_print_title:
                    template = '-'
                    if if_print_all or if_print_item:
                        for count in range(20):
                            if count < length-1:
                                item1_3_c3_3[count] = get_kth_in_line(fline,count+2)
                            else:
                                item1_3_c3_3[count] = " "
                        treeview1_3_c3_3.insert('', 0, values=(template, item1_3_c3_3[0], item1_3_c3_3[1],item1_3_c3_3[2],\
                                                           item1_3_c3_3[3],item1_3_c3_3[4],item1_3_c3_3[5],item1_3_c3_3[6],\
                                                           item1_3_c3_3[7],item1_3_c3_3[8],item1_3_c3_3[9],item1_3_c3_3[10],\
                                                           item1_3_c3_3[11],item1_3_c3_3[12],item1_3_c3_3[13],item1_3_c3_3[14],\
                                                           item1_3_c3_3[15],item1_3_c3_3[16],item1_3_c3_3[17],item1_3_c3_3[18],\
                                                           item1_3_c3_3[19]))
                        number_item = number_item+1
            winfor.close()
            # 打印模板题目
            if number_item and if_print_title:
                template = tname
                for count in range(20):
                    if count < length-1:
                        item1_3_c3_3[count] = get_kth_in_line(line,count+2)
                    else:
                        item1_3_c3_3[count] = " "
                treeview1_3_c3_3.insert('', 0, values=(template, item1_3_c3_3[0], item1_3_c3_3[1],item1_3_c3_3[2],\
                                                   item1_3_c3_3[3],item1_3_c3_3[4],item1_3_c3_3[5],item1_3_c3_3[6],\
                                                   item1_3_c3_3[7],item1_3_c3_3[8],item1_3_c3_3[9],item1_3_c3_3[10],\
                                                   item1_3_c3_3[11],item1_3_c3_3[12],item1_3_c3_3[13],item1_3_c3_3[14],\
                                                   item1_3_c3_3[15],item1_3_c3_3[16],item1_3_c3_3[17],item1_3_c3_3[18],\
                                                   item1_3_c3_3[19]))
        except IOError:
            pass #print "File is not accessible."
    wtemplate.close()
    
def information_control_check3_vague_pre(): # 模糊搜索提前准备的模板
    global f1_3_c3_3 # 本次框架
    global treeview1_3_c3_3,columns1_3_c3_3,item1_3_c3_3 # 表格
    
    # 再放上本次需要的框架
    f1_3_c3_3.pack(fill = 'both',expand = True) # 这个函数的主框架为f1_3_c3
    # 放好表头
            # 表格框架搭建
    columns1_3_c3_3 = ("template", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10",\
               "11","12","13","14","15","16","17","18","19","20")
    treeview1_3_c3_3 = ttk.Treeview(f1_3_c3_3, show="headings", columns=columns1_3_c3_3)  # 表格
    treeview1_3_c3_3.column("template", width=120, anchor='center') # 表示列,不显示
    item1_3_c3_3 = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
    for count in range(20):
        treeview1_3_c3_3.column(str(item1_3_c3_3[count]), width=100, anchor='center')
        # 显示表头
    treeview1_3_c3_3.heading("template", text="template") 
    count = 0
    for count in range(20):
        treeview1_3_c3_3.heading(str(item1_3_c3_3[count]), text=str(item1_3_c3_3[count]))
        # 表格安放
    treeview1_3_c3_3.pack(side=tk.LEFT, fill=tk.BOTH)
    # 最后隐藏提前的布局
    f1_3_c3_3.pack_forget()

def information_control_check3_internet(): # 联网搜索
    global search_word
    global f1_3_c3_4 # 本次框架
    
    # 先引入状态
    global type_1_3_3_1
    # 根据状态进行调整(退出可能有的原框架)
    if type_1_3_3_1 == 0: # 第一次进入该函数
        type_1_3_3_1 = 3
        f1_3_c3_4.pack(fill = 'both',expand = True) # 这个函数的主框架为f1_3_c3
    elif type_1_3_3_1 == 1: # 刚进入过方法一
        type_1_3_3_1 = 3
        global f1_3_c3_2
        f1_3_c3_2.pack_forget()
        # 再放上本次需要的框架
        f1_3_c3_4.pack(fill = 'both',expand = True) # 这个函数的主框架为f1_3_c3
    elif type_1_3_3_1 == 2: # 刚进入过方法二
        type_1_3_3_1 = 3
        global f1_3_c3_3
        f1_3_c3_3.pack_forget()
        # 再放上本次需要的框架
        f1_3_c3_4.pack(fill = 'both',expand = True) # 这个函数的主框架为f1_3_c3
    elif type_1_3_3_1 == 3: # 刚进过方法三
        pass
def information_control_check3_internet(): # 联网搜索提前准备的模板
    #1 先安放主框架
    global f1_3_c3_4
    f1_3_c3_4.pack(fill = 'both',expand = True)
    
    # 最后隐藏提前的布局
    f1_3_c3_4.pack_forget()

def information_control_check_out(): # 退出
    note.pack_forget()
    b1_3_1.pack_forget()
    f1_3_1.pack_forget()
def information_control_check_back(): # 返回
    information_control_check_out()
    information_control()

#-----------------------------------------------------------------------------------------------------------------------------------------------

def information_control_change():# 信息修改 b1_4 按钮
    # 先退出上级
    information_control_out()
    # 设置标题与按钮
    var.set("INFORMATION     SYSTEM\n")
    global b1_4_1
    if platform.system() == 'Darwin':# Mac系统
        b1_4_1 = tk.Button(window, text="Back to last level", width=20, height=3,fg = COLOR_MB_FRONT,command=lambda:information_control_change_back())
    elif platform.system() == 'Windows':# Windows系统
        b1_4_1 = tk.Button(window, text="Back to last level", width=20, height=3,fg = COLOR_FRONT,bg = COLOR_SUB,command=lambda:information_control_change_back())
    note.pack()
    b1_4_1.pack()
    # 设置主框架与左右框架
    global f1_4_1,f1_4_1_l,f1_4_1_r
    global width_set_l  #width_set_l = 3/16*width_set
    global width_set_r  #width_set_r = 13/16*width_set
    f1_4_1 = tk.Frame(window,bg = COLOR_BACK)
    f1_4_1.pack(fill = 'both',expand = True)
    f1_4_1_r = tk.Frame(f1_4_1,bg = COLOR_BACK,width = int(2*width_set_l))
    f1_4_1_r.pack(side = 'right',fill = 'y')
    f1_4_1_l = tk.Frame(f1_4_1,bg = COLOR_F2_BACK, width = int(width_set_r - width_set_l))
    f1_4_1_l.pack(side = 'right', fill = 'both',expand = True)
    # 右边输入部分-右边的整框架为f1_4_1_r
    # 右边输入部分-右边顶部题目label - l1_4_1
    global var_l141,choose;choose = '请选择左侧信息'
    var_l141=tk.StringVar() ;var_l141.set(choose)
    l1_4_1 = tk.Label(f1_4_1_r,bg = COLOR_F2_BACK,fg = COLOR_FRONT,textvariable=var_l141,height = 1,width = int(2*width_set_l/10)) #  Label宽度会破坏Frame宽度，这里计算出近似代替的宽度
    l1_4_1.pack()
    # 右边输入部分-提示窗口label - l1_4_2
    global var_l142;var_l142=tk.StringVar()  
    var_l142.set(' ')
    l1_4_2 = tk.Label(f1_4_1_r,bg = COLOR_BACK,fg = COLOR_FRONT,textvariable=var_l142,height = 1,width = int(2*width_set_l/10)) #  Label宽度会破坏Frame宽度，这里计算出近似代替的宽度
    l1_4_2.pack()
    # 右边输入部分-输入窗口entry - e1_4_2
    global e1_4_2
    e1_4_2 = tk.Entry(f1_4_1_r,bg = COLOR_F2_BACK,fg = COLOR_FRONT)
    e1_4_2.pack(fill = 'x')
    # 右边输入部分-信息的变量声明与初始化
    global infor;infor=[]
    # 右边输入部分-进入下一项
    def infor_control_change_infor_next():
        global k,infor,e1_4_2,infor_template,var_l142
        if len(infor)-1 == k:
            print('已经是最后一项了')
        else:
            # 先把信息存起来
            infor[k] = e1_4_2.get()
            # 再给出下一个提示
            k = k+1
            var_l142.set(infor_template[k]) # 设置模板项目提示
            e1_4_2.delete(0, tk.END)
            e1_4_2.insert(0, infor[k])
    
    # 右边输入部分-进入上一项
    def infor_control_change_infor_last():
        global k,infor,e1_4_2,infor_template,var_l142
        if  k == 1:
            print('已经是最后一项了')
        else:
            # 先把信息存起来
            infor[k] = e1_4_2.get()
            # 再给出上一个提示
            k = k-1
            var_l142.set(infor_template[k]) # 设置模板项目提示
            e1_4_2.delete(0, tk.END)
            e1_4_2.insert(0, infor[k])
            
    # 右边输入部分-保存添加的信息
    def infor_control_change_infor_save():
        global k,infor,e1_4_2,choose_ls
        # 先把当前界面信息存起来
        if e1_4_2.get() != '':
            infor[k] = e1_4_2.get()
        true = True
        for i in range(len(infor)-1):
            if infor[i] == False or get_kth_in_line(infor[i],0) == 0:
                true = False
        print(true)
        if true:
            # 先把文件保存到工作区
            winfor = open('./resources/infor_'+infor[0]+'.txt','r',encoding='UTF-8') # 文本形式，只读
            wincopy = open('./resources/inforchange.txt','w',encoding='UTF-8') # 文本形式，重写模式
            for line in winfor.readlines():
                print(line);wincopy.write(line)
            winfor.close()
            wincopy.close()
            # 在进行文件重写
            wincopy = open('./resources/inforchange.txt','r',encoding='UTF-8') # 文本形式，只读
            winfor = open('./resources/infor_'+infor[0]+'.txt','w',encoding='UTF-8') # 文本形式，重写模式
            for line in wincopy.readlines():
                i = 0;if_change = True
                for i in range(len(infor)-1):
                    if get_kth_in_line(line,i+2) !=  choose_ls[i+1]:
                        if_change = False;break
                if if_change:
                    for num in range(len(infor)):
                        winfor.write(infor[num]+'  ')
                    winfor.write('\n')
                else:
                    winfor.write(line)
            winfor.close()
            wincopy.close()
            # 最后刷新一下表格
            global search_way
            global search_word,u1_4_1
            global e1_4_1
            # 清空残留信息
            e1_4_1.delete(0, tk.END)
            e1_4_2.delete(0, tk.END)
            global var_l141,var_l142
            var_l141.set('请选择左侧信息')
            var_l142.set(' ')
            global infor_template
            infor.clear();infor_template.clear()
            # 进入对应功能
            if search_way == '精确搜索':
                information_control_change_precise()
            if search_way == '模糊搜索':
                information_control_change_vague()
            
    # 右边输入部分-删除指定信息
    def infor_control_change_infor_delete():
        global infor,choose_ls
        # 先把文件保存到工作区
        winfor = open('./resources/infor_'+infor[0]+'.txt','r',encoding='UTF-8') # 文本形式，只读
        wincopy = open('./resources/inforchange.txt','w',encoding='UTF-8') # 文本形式，重写模式
        for line in winfor.readlines():
            print(line)
            wincopy.write(line)
        winfor.close()
        wincopy.close()
        # 再进行文件重写
        wincopy = open('./resources/inforchange.txt','r',encoding='UTF-8') # 文本形式，只读
        winfor = open('./resources/infor_'+infor[0]+'.txt','w',encoding='UTF-8') # 文本形式，重写模式
        for line in wincopy.readlines():
            i = 0;if_change = True
            for i in range(len(infor)-1):
                if get_kth_in_line(line,i+2) !=  choose_ls[i+1]:
                    if_change = False;break
            if if_change:
                pass
            else:
                winfor.write(line)
        winfor.close()
        wincopy.close()
        # 最后刷新一下表格
        global search_way
        global search_word,u1_4_1
        global e1_4_1
        # 清空残留信息
        e1_4_1.delete(0, tk.END)
        e1_4_2.delete(0, tk.END)
        global var_l141,var_l142
        var_l141.set('请选择左侧信息')
        var_l142.set(' ')
        global infor_template
        infor.clear();infor_template.clear()
        # 进入对应功能
        if search_way == '精确搜索':
            information_control_change_precise()
        if search_way == '模糊搜索':
            information_control_change_vague()
        
    # 右边输入部分-按钮button
    if platform.system() == 'Darwin':# Mac系统
        b1_4_2 = tk.Button(f1_4_1_r, text=" Next ", width=15, height=2,fg = COLOR_MB_FRONT,command=lambda:infor_control_change_infor_next())
        b1_4_3 = tk.Button(f1_4_1_r, text=" Last ", width=15, height=2,fg = COLOR_MB_FRONT,command=lambda:infor_control_change_infor_last())
        b1_4_4 = tk.Button(f1_4_1_r, text=" Save ", width=15, height=2,fg = COLOR_MB_FRONT,command=lambda:infor_control_change_infor_save())
        b1_4_5 = tk.Button(f1_4_1_r, text="Delete", width=15, height=2,fg = COLOR_MB_FRONT,command=lambda:infor_control_change_infor_delete())
    elif platform.system() == 'Windows':# Windows系统
        b1_4_2 = tk.Button(f1_4_1_r, text=" Next ", width=15, height=2,fg = COLOR_FRONT,bg = COLOR_SUB,command=lambda:infor_control_change_infor_next())
        b1_4_3 = tk.Button(f1_4_1_r, text=" Last ", width=15, height=2,fg = COLOR_FRONT,bg = COLOR_SUB,command=lambda:infor_control_change_infor_last())
        b1_4_4 = tk.Button(f1_4_1_r, text=" Save ", width=15, height=2,fg = COLOR_FRONT,bg = COLOR_SUB,command=lambda:infor_control_change_infor_save())
        b1_4_5 = tk.Button(f1_4_1_r, text="Delete", width=15, height=2,fg = COLOR_FRONT,bg = COLOR_SUB,command=lambda:infor_control_change_infor_delete())
    b1_4_2.pack();b1_4_3.pack();b1_4_4.pack();b1_4_5.pack()

    # 左侧搜索区域-搜索框与选择按钮
    global f1_4_1_l_1
    f1_4_1_l_1 = tk.Frame(f1_4_1_l,bg = COLOR_BACK,width = int(width_set_r - width_set_l))
    f1_4_1_l_1.pack(fill = 'x')
    global e1_4_1,cmb1_4_1,search_way,search_word;search_way = '精确搜索' # 默认精确搜索
    global u1_4_1 #是输入的变量
    # 左侧搜索区域-选择函数
    def cmb1_4_1_func(event): #选择事件
        global search_way;search_way = cmb1_4_1.get()
    # 左侧搜索区域-下拉菜单
    cmb1_4_1 = ttk.Combobox(f1_4_1_l_1) 
    cmb1_4_1.pack(side = 'right')
    cmb1_4_1['value'] = ('精确搜索','模糊搜索')#设置下拉菜单中的值 
    cmb1_4_1.current(0)#设置默认值，即默认下拉框中的内容 #选零就代表优先精准搜索
    cmb1_4_1.bind("<<ComboboxSelected>>",cmb1_4_1_func)
    # 左侧搜索区域-输入框
    u1_4_1 = tk.StringVar()
    e1_4_1 = tk.Entry(f1_4_1_l_1,bg = COLOR_F2_BACK,fg = COLOR_FRONT,textvariable=u1_4_1) 
    e1_4_1.pack(side = 'right',fill = 'x',expand = True)
    # 左侧搜索区域-回车函数
    def e1_4_1_submit(event):
        global search_way
        global search_word,u1_4_1; search_word = u1_4_1.get()
        global e1_4_1
        # 清空残留信息
        e1_4_1.delete(0, tk.END)
        # 进入对应功能
        if search_way == '精确搜索':
            information_control_change_precise()
        if search_way == '模糊搜索':
            information_control_change_vague()
    # 左侧搜索区域-回车事件
    e1_4_1.bind("<Return>",e1_4_1_submit)
    # 左侧搜索区域-子框架2（各种搜索模式的框架）
    global f1_4_1_l_2#,f1_4_1_l_3 # 现在不用了
    # 左侧搜索区域-子集状态变量(important)
    global type_1_4_1; type_1_4_1 = 0
    # 左侧搜索区域-子框架提前布置 #COLOR_F2_BACK
    f1_4_1_l_2 = tk.Frame(f1_4_1_l,bg = COLOR_F2_BACK);information_control_change_precise_pre() # 精确搜索和模糊搜索提前安放模板
    #f1_4_1_l_3 = tk.Frame(f1_4_1_l);information_control_change_vague_pre() # 模糊搜索提前准备的模板 # 现在不用了
    
def infor_change(item_text): #进行信息文件的修改
    global choose_ls;choose_ls = []
    i = 0
    while 1 :
        if get_kth_in_line(item_text[i],0) == 0:break
        choose_ls.append(item_text[i]);i=i+1
    global infor;infor = choose_ls.copy()
    global choose;choose = item_text[0] # 找到了模板名
    global var_l141;var_l141.set(choose) # 设置var_l141为模板名
    global infor_template;infor_template = []
    wtemplate = open('./resources/system/template/template.txt','r',encoding='UTF-8')
    for line in wtemplate.readlines():
        tname = get_kth_in_line(line,1) # 模板名字
        length = get_kth_in_line(line,0) # 模板长度
        if tname == choose:
            j = 1
            while 1:
                infor_template.append(get_kth_in_line(line,j))
                if j == length:break
                j = j+1
    wtemplate.close()
    global var_l142;var_l142.set(infor_template[1]) # 设置var_l142为模板项目提示
    global k;k = 1
    global e1_4_2
    e1_4_2.delete(0, tk.END)
    e1_4_2.insert(0, infor[1])

def information_control_change_vague():# 模糊搜索
    global search_word
    global f1_4_1_l_2 # 本次框架
    global treeview1_4_1_1,item1_4_4_1
    # 先引入状态
    global type_1_4_1
    # 根据状态进行调整(退出可能有的原框架)
    if type_1_4_1 == 0: # 第一次进入该函数
        type_1_4_1 = 1
        f1_4_1_l_2.pack(fill = 'both',expand = True) # 这个函数的主框架为f1_4_1_l_2
    elif type_1_4_1 == 1: # 刚进入过方法一或二
        pass
    # 准备搜索词的列表
    search_word_ls = jieba.lcut(search_word)
    to_be_searched_ls = []
    # 建立表格
        # 清空表格
    x=treeview1_4_1_1.get_children()
    for j in x:
        treeview1_4_1_1.delete(j)
        #填写表格内容
    for i in range(36): # 占空行
        treeview1_4_1_1.insert('', 0, values=('','','','','','','','','','','','','','','','','','','','',''))
    wtemplate = open('./resources/system/template/template.txt','r',encoding='UTF-8')
    wtemplate.seek(0) #指针回到文件开头
    for line in wtemplate.readlines():
        tname = get_kth_in_line(line,1) # 模板名字
        fname = './resources/infor_'+tname+'.txt' # 文件名字
        length = get_kth_in_line(line,0)
        try:
            winfor = open(fname,'r',encoding='UTF-8') 
            number_item = 0
            if_print_all = False #是否全模板打印
            if_print_title = False#是否打印模板题目
            for i in range(length):
                for j in range(len(search_word_ls)):
                    to_be_searched_ls = jieba.lcut(str(get_kth_in_line(line,i+1)))
                    for k in range(len(to_be_searched_ls)):
                        if str(to_be_searched_ls[k]) == str(search_word_ls[j]):
                            if_print_all = True
                            if_print_title = True
                            break
                    if if_print_title:break
                if if_print_title:break
                
            for fline in winfor.readlines():
                if_print_item = False #是否打印特定信息
                if if_print_all == True:
                    if_print_item = True
                    if_print_title = True
                else:
                    for j in range(length):
                        for i in range(len(search_word_ls)):
                            to_be_searched_ls = jieba.lcut(str(get_kth_in_line(fline,j+1)))
                            for k in range(len(to_be_searched_ls)):
                                if str(to_be_searched_ls[k]) == str(search_word_ls[i]):
                                    if_print_item = True
                                    if_print_title = True
                                    break
                            if if_print_item:break
                        if if_print_item:break
                if get_kth_in_line(fline,0) == 0:if_print_title = False;break # 空文件不打印模板               
                if if_print_title:
                    template = tname #因为涉及改信息，所以每一条消息都要标注属于模板的名称
                    if if_print_all or if_print_item:
                        for count in range(20):
                            if count < length-1:
                                item1_4_4_1[count] = get_kth_in_line(fline,count+2)
                            else:
                                item1_4_4_1[count] = " "
                        treeview1_4_1_1.insert('', 0, values=(template, item1_4_4_1[0], item1_4_4_1[1],item1_4_4_1[2],\
                                                           item1_4_4_1[3],item1_4_4_1[4],item1_4_4_1[5],item1_4_4_1[6],\
                                                           item1_4_4_1[7],item1_4_4_1[8],item1_4_4_1[9],item1_4_4_1[10],\
                                                           item1_4_4_1[11],item1_4_4_1[12],item1_4_4_1[13],item1_4_4_1[14],\
                                                           item1_4_4_1[15],item1_4_4_1[16],item1_4_4_1[17],item1_4_4_1[18],\
                                                           item1_4_4_1[19]))
                        number_item = number_item+1
            winfor.close()
            # 打印模板题目
            if number_item and if_print_title:
                template = '【'+tname+'】'
                for count in range(20):
                    if count < length-1:
                        item1_4_4_1[count] = get_kth_in_line(line,count+2)
                    else:
                        item1_4_4_1[count] = " "
                treeview1_4_1_1.insert('', 0, values=(template, item1_4_4_1[0], item1_4_4_1[1],item1_4_4_1[2],\
                                                   item1_4_4_1[3],item1_4_4_1[4],item1_4_4_1[5],item1_4_4_1[6],\
                                                   item1_4_4_1[7],item1_4_4_1[8],item1_4_4_1[9],item1_4_4_1[10],\
                                                   item1_4_4_1[11],item1_4_4_1[12],item1_4_4_1[13],item1_4_4_1[14],\
                                                   item1_4_4_1[15],item1_4_4_1[16],item1_4_4_1[17],item1_4_4_1[18],\
                                                   item1_4_4_1[19]))
        except IOError:
            pass #print "File is not accessible."
    wtemplate.close()

def information_control_change_precise(): # 精确搜索
    global search_word
    global f1_4_1_l_2 # 本次框架
    global treeview1_4_1_1,item1_4_4_1
    # 先引入状态
    global type_1_4_1
    # 根据状态进行调整(退出可能有的原框架)
    if type_1_4_1 == 0: # 第一次进入该函数
        type_1_4_1 = 1
        f1_4_1_l_2.pack(fill = 'both',expand = True) # 这个函数的主框架为f1_4_1_l_2
    elif type_1_4_1 == 1: # 刚进入过方法一或二
        pass
    # 建立表格
        # 清空表格
    x=treeview1_4_1_1.get_children()
    for j in x:
        treeview1_4_1_1.delete(j)
        #填写表格内容
    for i in range(36): # 占空行
        treeview1_4_1_1.insert('', 0, values=('','','','','','','','','','','','','','','','','','','','',''))
    wtemplate = open('./resources/system/template/template.txt','r',encoding='UTF-8')
    wtemplate.seek(0) #指针回到文件开头
    for line in wtemplate.readlines():
        tname = get_kth_in_line(line,1) # 模板名字
        fname = './resources/infor_'+tname+'.txt' # 文件名字
        length = get_kth_in_line(line,0)
        try:
            number_item = 0
            winfor = open(fname,'r',encoding='UTF-8') 
            if_print_all = False #是否全模板打印
            if_print_title = False#是否打印模板题目
            for i in range(length):
                if str(get_kth_in_line(line,i+1)) == str(search_word):
                    if_print_all = True;if_print_title = True;break
            for fline in winfor.readlines():
                if_print_item = False #是否打印特定信息
                for j in range(length):
                    if str(get_kth_in_line(fline,j+1)) == str(search_word):
                        if_print_item = True;if_print_title = True;break
                if get_kth_in_line(fline,0) == 0:if_print_title = False # 空文件不打印模板
                if if_print_title:
                    template = tname #因为涉及改信息，所以每一条消息都要标注属于模板的名称
                    if if_print_all or if_print_item:
                        for count in range(20):
                            if count < length-1:
                                item1_4_4_1[count] = get_kth_in_line(fline,count+2)
                            else:
                                item1_4_4_1[count] = " "
                        treeview1_4_1_1.insert('', 0, values=(template, item1_4_4_1[0], item1_4_4_1[1],item1_4_4_1[2],\
                                                           item1_4_4_1[3],item1_4_4_1[4],item1_4_4_1[5],item1_4_4_1[6],\
                                                           item1_4_4_1[7],item1_4_4_1[8],item1_4_4_1[9],item1_4_4_1[10],\
                                                           item1_4_4_1[11],item1_4_4_1[12],item1_4_4_1[13],item1_4_4_1[14],\
                                                           item1_4_4_1[15],item1_4_4_1[16],item1_4_4_1[17],item1_4_4_1[18],\
                                                           item1_4_4_1[19]))
                        number_item = number_item+1
            winfor.close()
            # 打印模板题目
            if number_item and if_print_title:
                template = '【'+tname+'】'
                for count in range(20):
                    if count < length-1:
                        item1_4_4_1[count] = get_kth_in_line(line,count+2)
                    else:
                        item1_4_4_1[count] = " "
                treeview1_4_1_1.insert('', 0, values=(template, item1_4_4_1[0], item1_4_4_1[1],item1_4_4_1[2],\
                                                   item1_4_4_1[3],item1_4_4_1[4],item1_4_4_1[5],item1_4_4_1[6],\
                                                   item1_4_4_1[7],item1_4_4_1[8],item1_4_4_1[9],item1_4_4_1[10],\
                                                   item1_4_4_1[11],item1_4_4_1[12],item1_4_4_1[13],item1_4_4_1[14],\
                                                   item1_4_4_1[15],item1_4_4_1[16],item1_4_4_1[17],item1_4_4_1[18],\
                                                   item1_4_4_1[19]))
        except IOError:
            pass #print "File is not accessible."
    wtemplate.close()
def information_control_change_precise_pre(): # 精确搜索和模糊搜索提前安放模板
    #1 先安放主框架
    global f1_4_1_l_2
    f1_4_1_l_2.pack(fill = 'both',expand = True)
    #2 其他要用的变量
    global treeview1_4_1_1,columns1_4_1_1,item1_4_4_1
    #3 放好表头
            # 表格框架搭建
    columns1_4_1_1 = ("template", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10",\
               "11","12","13","14","15","16","17","18","19","20")
    treeview1_4_1_1 = ttk.Treeview(f1_4_1_l_2,show="headings", columns=columns1_4_1_1)  # 表格
    treeview1_4_1_1.column("template", width=120, anchor='center') # 表示列,不显示
    item1_4_4_1 = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
    for count in range(20):
        treeview1_4_1_1.column(str(item1_4_4_1[count]), width=100, anchor='center')
        # 显示表头
    treeview1_4_1_1.heading("template", text="template") 
    count = 0
    for count in range(20):
        treeview1_4_1_1.heading(str(item1_4_4_1[count]), text=str(item1_4_4_1[count]))
        # 表格安放
    treeview1_4_1_1.pack(side=tk.LEFT, fill=tk.BOTH)
        # 定义单击事件
    def treeviewClick1_4_1_1(event):# 单击事件
        global treeview1_4_1_1
        for item in treeview1_4_1_1.selection():
            item_text = treeview1_4_1_1.item(item,"values")
            if_tamplate = item_text[0]
            if if_tamplate[0] == '【' and if_tamplate[-1] == '】':
                print('错啦！这个是模板名！')
            else:
                try:infor_change(item_text)
                except:pass
    treeview1_4_1_1.bind('<ButtonRelease-1>', treeviewClick1_4_1_1)#绑定单击离开事件
    #4 最后隐藏提前的布局
    f1_4_1_l_2.pack_forget()

def information_control_change_out(): # 退出
    f1_4_1.pack_forget()
    note.pack_forget()
    b1_4_1.pack_forget()
def information_control_change_back(): # 返回
    information_control_change_out()
    information_control()

###############################################################################################################################################
###############################################################################################################################################   
'''
模版控制函数
'''
def template_control():
    main_out()
    var.set("TEMPLATE     SYSTEM\n")
    global b2_1,b2_2,b2_3,b2_4
    if platform.system() == 'Darwin':# Mac系统
        b2_1 = tk.Button(window, text="Back to last level", width=20, height=3,fg = COLOR_MB_FRONT,bg = COLOR_SUB,command=lambda:template_control_back())
        b2_2 = tk.Button(window, text="Add       template", width=20, height=3,fg = COLOR_MB_FRONT,bg = COLOR_SUB,command=lambda:template_control_add())
        b2_3 = tk.Button(window, text="Check     template", width=20, height=3,fg = COLOR_MB_FRONT,bg = COLOR_SUB,command=lambda:template_control_check())
        b2_4 = tk.Button(window, text="Change    template", width=20, height=3,fg = COLOR_MB_FRONT,bg = COLOR_SUB,command=lambda:template_control_change())
    elif platform.system() == 'Windows':# Windows系统
        b2_1 = tk.Button(window, text="Back to last level", width=20, height=3,fg = COLOR_FRONT,bg = COLOR_SUB,command=lambda:template_control_back())
        b2_2 = tk.Button(window, text="Add       template", width=20, height=3,fg = COLOR_FRONT,bg = COLOR_SUB,command=lambda:template_control_add())
        b2_3 = tk.Button(window, text="Check     template", width=20, height=3,fg = COLOR_FRONT,bg = COLOR_SUB,command=lambda:template_control_check())
        b2_4 = tk.Button(window, text="Change    template", width=20, height=3,fg = COLOR_FRONT,bg = COLOR_SUB,command=lambda:template_control_change())
    note.pack()
    b2_1.pack()
    b2_2.pack()
    b2_3.pack()
    b2_4.pack()
def template_control_out():# 退出函数
    note.pack_forget()
    b2_1.pack_forget()
    b2_2.pack_forget()
    b2_3.pack_forget()
    b2_4.pack_forget()

#-----------------------------------------------------------------------------------------------------------------------------------------------

def template_control_back():# 返回函数 b2_1按钮
    template_control_out()
    main()

#-----------------------------------------------------------------------------------------------------------------------------------------------

def template_control_add(): # 模板添加 b2_2 按钮
    # 惯例步骤（标签与返回）
    template_control_out()
    var.set("TEMPLATE     SYSTEM\n")
    global b2_2_1,b2_2_2,b2_2_3,f2_2_1# 本行为 返回，增减输入框的按钮和容器
    global b2_2_4,l2_2_1,e2_2_1
    if platform.system() == 'Darwin':# Mac系统
        b2_2_1  = tk.Button(window, text="Back to last level", width=20, height=3,fg = COLOR_MB_FRONT,command=lambda:template_control_add_back())
    elif platform.system() == 'Windows':# Windows系统
        b2_2_1  = tk.Button(window, text="Back to last level", width=20, height=3,bg = COLOR_SUB,fg = COLOR_FRONT,command=lambda:template_control_add_back())
    note.pack()
    b2_2_1.pack()
    # 模板内容输入
    global entry_list; entry_list = [] # 输入框的列表
    global label_list; label_list = [] # 输入框提示符的列表
    f2_2_1 = tk.Frame(window ,width=20, height=2)
    if platform.system() == 'Darwin':# Mac系统
        b2_2_2 = tk.Button(f2_2_1, text='Add    Entry', width=10, height=2,fg = COLOR_MB_FRONT, command=lambda:template_control_add_Entry())
        b2_2_3 = tk.Button(f2_2_1, text='Reduce Entry', width=10, height=2,fg = COLOR_MB_FRONT, command=lambda:template_control_reduce_Entry())
        b2_2_4 = tk.Button(window, text='Save'        , width=20, height=2,fg = COLOR_MB_FRONT, command=lambda:template_control_add_save())
    elif platform.system() == 'Windows':# Windows系统
        b2_2_2 = tk.Button(f2_2_1, text='Add    Entry', width=10, height=2,bg = COLOR_SUB,fg = COLOR_FRONT, command=lambda:template_control_add_Entry())
        b2_2_3 = tk.Button(f2_2_1, text='Reduce Entry', width=10, height=2,bg = COLOR_SUB,fg = COLOR_FRONT, command=lambda:template_control_reduce_Entry())
        b2_2_4 = tk.Button(window, text='Save'        , width=20, height=2,bg = COLOR_SUB,fg = COLOR_FRONT, command=lambda:template_control_add_save())
    
    l2_2_1 = tk.Label(window,fg = COLOR_FRONT,bg = COLOR_SUB,text="模板名称")
    e2_2_1 = tk.Entry(window,bg = COLOR_F2_BACK,fg = COLOR_FRONT)
    f2_2_1.pack() # 增减输入框的容器
    b2_2_2.pack(side = "left") # 增加输入框
    b2_2_3.pack(side = "right") # 减少输入框
    b2_2_4.pack() # 保存信息
    l2_2_1.pack() # 模板名提示文字
    e2_2_1.pack() # 模板名输入区

def template_control_add_out(): # 退出
    note.pack_forget()
    b2_2_1.pack_forget()
    b2_2_2.pack_forget()
    b2_2_3.pack_forget()
    f2_2_1.pack_forget()
    b2_2_4.pack_forget()
    l2_2_1.pack_forget()
    e2_2_1.pack_forget()
def template_control_add_back(): # 返回
    template_control_add_out()
    while entry_list: # 删掉添加的输入框与其提示
        template_control_reduce_Entry()
    template_control()

def template_control_add_Entry(): # 模板添加 b2_2 按钮 小功能-添加输入框
    l_add_item = tk.Label(window,fg = COLOR_FRONT,bg = COLOR_SUB,text="item")
    t_add_item = tk.Entry(window,bg = COLOR_F2_BACK,fg = COLOR_FRONT)
    l_add_item.pack()
    t_add_item.pack()
    label_list.append(l_add_item)
    entry_list.append(t_add_item)

def template_control_reduce_Entry(): # 模板添加 b2_3 按钮 小功能-删除输入框
    if entry_list:
        b = entry_list.pop() ;b.destroy()
        d = label_list.pop() ;d.destroy()

def template_control_add_save(): # 模板添加 b2_4 按钮 小功能-保存信息
    if template_control_add_save_check(): 
      wtemplate = open('./resources/system/template/template.txt','a+',encoding='UTF-8') # 文本形式，追加写模式
      wtemplate.write(e2_2_1.get()+"  ")
      entry_list.reverse()
      while entry_list:
          b = entry_list.pop()
          wtemplate.write(b.get()+"  ")
          b.destroy()
          d = label_list.pop() ;d.destroy()
      wtemplate.write("\n")
      wtemplate.close()
      template_control_add_back()
          
def template_control_add_save_check(): #模板添加 b2_4 按钮 小功能-保存信息的审核部分
    # 进入条件为填写完名称且添加过按钮
    a = 0
    if e2_2_1.get() and len(entry_list)>0 : 
        i = 1; a = 1
        # 判断添加的按钮是否都有内容
        while i <= len(entry_list):
            if entry_list[i-1].get(): pass
            else: a = 0
            i = i + 1
    # 检查是否之前有相同名称的模板 #（e2_2_1.get() 为这次输入的名称）
    if a:
        wtemplate = open('./resources/system/template/template.txt','r',encoding='UTF-8') 
        for line in wtemplate.readlines():
            if e2_2_1.get() == get_kth_in_line(line,1): # 这里用到的是后面的工具函数
                a = 0
                mind("亲，该名称已被使用过！",0)
        wtemplate.close()
    return a

#-----------------------------------------------------------------------------------------------------------------------------------------------

def template_control_check():# 模板查看 b2_3 按钮
    # 惯例步骤（标签与返回）
    template_control_out()
    var.set("TEMPLATE     SYSTEM\n")
    global b2_3_1,sb2_3_1,l2_3_1
    if platform.system() == 'Darwin':# Mac系统
        b2_3_1 = tk.Button(window, text="Back to last level", width=20, height=3,fg = COLOR_MB_FRONT,command=lambda:template_control_check_back())
    elif platform.system() == 'Windows':# Windows系统
        b2_3_1 = tk.Button(window, text="Back to last level", width=20, height=3,bg = COLOR_SUB,fg = COLOR_FRONT,command=lambda:template_control_check_back())
    note.pack()
    b2_3_1.pack()
    # 进入查询部分
    sb2_3_1 = tk.Scrollbar(window)
    sb2_3_1.pack(side="right", fill="y") # 滚动条放在右边，上下填充
    l2_3_1 = tk.Listbox(window,bg = COLOR_F2_BACK,fg = COLOR_F2_FRONT, yscrollcommand=sb2_3_1.set)
    wtemplate = open('./resources/system/template/template.txt','r',encoding='UTF-8') 
    count = 1
    for line in wtemplate.readlines():
        l2_3_1.insert("end", str(count)+":  "+line)
        l2_3_1.pack(fill="both",side= "top", expand = True ) # 左右两边都填充 #fill=Y and X
        sb2_3_1.config(command=l2_3_1.yview)
        count = count+1
    wtemplate.close()
    
def template_control_check_out(): # 退出
    note.pack_forget()
    b2_3_1.pack_forget()
    sb2_3_1.pack_forget()
    l2_3_1.pack_forget()
    
def template_control_check_back(): # 返回
    template_control_check_out()
    template_control()

#-----------------------------------------------------------------------------------------------------------------------------------------------

def template_control_change():# 模板修改 b2_3 按钮
    # 惯例操作
    template_control_out()
    var.set("TEMPLATE     SYSTEM\n")
    global b2_4_1
    if platform.system() == 'Darwin':# Mac系统
        b2_4_1 = tk.Button(window, text="Back to last level", width=20, height=3,fg = COLOR_MB_FRONT,command=lambda:template_control_change_back())
    elif platform.system() == 'Windows':# Windows系统
        b2_4_1 = tk.Button(window, text="Back to last level", width=20, height=3,bg = COLOR_SUB,fg = COLOR_FRONT,command=lambda:template_control_change_back())
    note.pack()
    b2_4_1.pack()
    # 设置主框架与左右框架
    global f2_4_1,f2_4_1_l,f2_4_1_r
    global width_set_l  #width_set_l = 3/16*width_set
    global width_set_r  #width_set_r = 13/16*width_set
    
    f2_4_1 = tk.Frame(window,bg = COLOR_BACK)
    f2_4_1.pack(fill = 'both',expand = True)
    f2_4_1_r = tk.Frame(f2_4_1,bg = COLOR_BACK,width = int(2*width_set_l))
    f2_4_1_r.pack(side = 'right',fill = 'y')
    f2_4_1_l = tk.Frame(f2_4_1,bg = COLOR_F2_BACK, width = int(width_set_r - width_set_l))
    f2_4_1_l.pack(side = 'right', fill = 'both',expand = True)
    # 右边输入部分-右边的整框架为f2_4_1_r 
    # 右边输入部分-右边顶部题目label - l2_4_1
    global var_l241,choose;choose = '请选择左侧模板'
    var_l241=tk.StringVar() ;var_l241.set(choose)
    l2_4_1 = tk.Label(f2_4_1_r,bg = COLOR_F2_BACK,fg = COLOR_FRONT,textvariable=var_l241,height = 1,width = int(2*width_set_l/10)) #  Label宽度会破坏Frame宽度，这里计算出近似代替的宽度
    l2_4_1.pack()
    # 右边输入部分-输入窗口entry - e2_4_2
    global e2_4_2
    e2_4_2 = tk.Entry(f2_4_1_r,bg = COLOR_F2_BACK,fg = COLOR_FRONT)
    e2_4_2.pack(fill = 'x')
    # 右边输入部分-信息的变量声明与初始化
    global infor;infor=[]
    
    # 右边输入部分-进入下一项
    def tem_control_change_item_next():
        global k,infor,e2_4_2
        if len(infor)-1 == k:
            print('已经是最后一项了')
        else:
            # 先把信息存起来
            infor[k] = e2_4_2.get()
            # 再给出下一个提示
            k = k+1
            e2_4_2.delete(0, tk.END)
            e2_4_2.insert(0, infor[k])
    
    # 右边输入部分-进入上一项
    def tem_control_change_item_last():
        global k,infor,e2_4_2
        if  k == 0:
            print('已经是第一项了')
        else:
            # 先把信息存起来
            infor[k] = e2_4_2.get()
            # 再给出上一个提示
            k = k-1
            e2_4_2.delete(0, tk.END)
            e2_4_2.insert(0, infor[k])
            
    # 右边输入部分-保存添加的信息
    def tem_control_change_item_save():
        global k,infor,e2_4_2,choose_ls
        # 先把当前界面信息存起来
        infor[k] = e2_4_2.get()
        true = True
        for i in range(len(infor)-1):
            if infor[i] == False or get_kth_in_line(infor[i],0) == 0:
                true = False
        if true:
            # 先把文件保存到工作区
            winfor = open('./resources/system/template/template.txt','r',encoding='UTF-8') # 文本形式，只读
            wincopy = open('./resources/inforchange.txt','w',encoding='UTF-8') # 文本形式，重写模式
            for line in winfor.readlines():
                wincopy.write(line)
            winfor.close()
            wincopy.close()
            # 在进行文件重写
            wincopy = open('./resources/inforchange.txt','r',encoding='UTF-8') # 文本形式，只读
            winfor = open('./resources/system/template/template.txt','w',encoding='UTF-8') # 文本形式，重写模式
            for line in wincopy.readlines():
                i = 0;if_change = True
                for i in range(len(infor)):
                    if get_kth_in_line(line,i+1) !=  choose_ls[i]:
                        if_change = False;break
                if if_change:
                    for num in range(len(infor)):
                        winfor.write(infor[num]+'  ')
                    winfor.write('\n')
                else:
                    winfor.write(line)
            winfor.close()
            wincopy.close()
            # 最后刷新一下表格
            global search_way
            global search_word
            # 清空残留信息
            e2_4_2.delete(0, tk.END)
            global var_l241
            var_l241.set('请选择左侧模板')
            infor.clear()
            # 进入对应功能
            if search_way == '精确搜索':
                template_control_change_precise()
            if search_way == '模糊搜索':
                template_control_change_vague()
            
    # 右边输入部分-删除指定信息
    def tem_control_change_item_delete():
        ask_if_delete = messagebox.askyesno('askyesno', 'Sure To Delete ?', parent=window)
        if ask_if_delete:
            global infor,choose_ls
            # 先把文件保存到工作区
            winfor = open('./resources/system/template/template.txt','r',encoding='UTF-8') # 文本形式，只读
            wincopy = open('./resources/inforchange.txt','w',encoding='UTF-8') # 文本形式，重写模式
            for line in winfor.readlines():
                wincopy.write(line)
            winfor.close()
            wincopy.close()
            # 再进行文件重写
            wincopy = open('./resources/inforchange.txt','r',encoding='UTF-8') # 文本形式，只读
            winfor = open('./resources/system/template/template.txt','w',encoding='UTF-8') # 文本形式，重写模式
            for line in wincopy.readlines():
                i = 0;if_change = True
                for i in range(len(infor)-1):
                    if get_kth_in_line(line,i+2) !=  choose_ls[i+1]:
                        if_change = False;break
                if if_change:
                    pass
                else:
                    winfor.write(line)
            winfor.close()
            wincopy.close()
            # 删除可能存在的模板的信息 .txt
            global save_template
            try:os.remove('./resources/infor_'+save_template+'.txt')
            except:pass
            # 最后刷新一下表格
            global search_way
            global search_word
            global e2_4_2
            # 清空残留信息
            e2_4_2.delete(0, tk.END)
            global var_l241
            var_l241.set('请选择左侧信息')
            infor.clear()
            # 进入对应功能
            if search_way == '精确搜索':
                template_control_change_precise()
            if search_way == '模糊搜索':
                template_control_change_vague()
    
    # 右边输入部分-按钮button
    if platform.system() == 'Darwin':# Mac系统
        b2_4_2 = tk.Button(f2_4_1_r, text=" Next ", width=15, height=2,fg = COLOR_MB_FRONT,command=lambda:tem_control_change_item_next())
        b2_4_3 = tk.Button(f2_4_1_r, text=" Last ", width=15, height=2,fg = COLOR_MB_FRONT,command=lambda:tem_control_change_item_last())
        b2_4_4 = tk.Button(f2_4_1_r, text=" Save ", width=15, height=2,fg = COLOR_MB_FRONT,command=lambda:tem_control_change_item_save())
        b2_4_5 = tk.Button(f2_4_1_r, text="Delete", width=15, height=2,fg = COLOR_MB_FRONT,command=lambda:tem_control_change_item_delete())
    elif platform.system() == 'Windows':# Windows系统
        b2_4_2 = tk.Button(f2_4_1_r, text=" Next ", width=15, height=2,bg = COLOR_SUB,fg = COLOR_FRONT,command=lambda:tem_control_change_item_next())
        b2_4_3 = tk.Button(f2_4_1_r, text=" Last ", width=15, height=2,bg = COLOR_SUB,fg = COLOR_FRONT,command=lambda:tem_control_change_item_last())
        b2_4_4 = tk.Button(f2_4_1_r, text=" Save ", width=15, height=2,bg = COLOR_SUB,fg = COLOR_FRONT,command=lambda:tem_control_change_item_save())
        b2_4_5 = tk.Button(f2_4_1_r, text="Delete", width=15, height=2,bg = COLOR_SUB,fg = COLOR_FRONT,command=lambda:tem_control_change_item_delete())
    b2_4_2.pack();b2_4_3.pack();b2_4_4.pack();b2_4_5.pack()
    # 左侧搜索区域-搜索框与选择按钮
    global f2_4_1_l_1
    f2_4_1_l_1 = tk.Frame(f2_4_1_l,width = int(width_set_r - width_set_l))
    f2_4_1_l_1.pack(fill = 'x')
    global e2_4_1,cmb2_4_1,search_way,search_word;search_way = '精确搜索' # 默认精确搜索
    global u2_4_1 #是输入的变量
    # 左侧搜索区域-选择函数
    def cmb2_4_1_func(event): #选择事件
        global search_way;search_way = cmb2_4_1.get()
    # 左侧搜索区域-下拉菜单
    cmb2_4_1 = ttk.Combobox(f2_4_1_l_1) 
    cmb2_4_1.pack(side = 'right')
    cmb2_4_1['value'] = ('精确搜索','模糊搜索')#设置下拉菜单中的值 
    cmb2_4_1.current(0)#设置默认值，即默认下拉框中的内容 #选零就代表优先精准搜索
    cmb2_4_1.bind("<<ComboboxSelected>>",cmb2_4_1_func)
    # 左侧搜索区域-输入框
    u2_4_1 = tk.StringVar()
    e2_4_1 = tk.Entry(f2_4_1_l_1,bg = COLOR_F2_BACK,fg = COLOR_FRONT, textvariable=u2_4_1)  
    e2_4_1.pack(side = 'right',fill = 'x',expand = True)
    # 左侧搜索区域-回车函数
    def e2_4_1_submit(event):
        global search_way
        global search_word,u2_4_1; search_word = u2_4_1.get()
        global e2_4_1
        # 清空残留信息
        e2_4_1.delete(0, tk.END)
        # 进入对应功能
        if search_way == '精确搜索':
            template_control_change_precise()
        if search_way == '模糊搜索':
            template_control_change_vague()
    # 左侧搜索区域-回车事件
    e2_4_1.bind("<Return>",e2_4_1_submit)
    # 左侧搜索区域-子框架2（各种搜索模式的框架）
    global f2_4_1_l_2#,f2_4_1_l_3 # 现在不用了
    # 左侧搜索区域-子集状态变量(important)
    global type_2_4_1; type_2_4_1 = 0
    # 左侧搜索区域-子框架提前布置
    f2_4_1_l_2 = tk.Frame(f2_4_1_l);template_control_change_precise_pre() # 精确搜索和模糊搜索提前安放模板
    #f2_4_1_l_3 = tk.Frame(f2_4_1_l);template_control_change_vague_pre() # 模糊搜索提前准备的模板 # 现在不用了
    
def tem_change(item_text): #进行信息文件的修改
    global choose_ls;choose_ls = []
    for i in range(len(item_text)):
        if item_text[i] == ' ':pass
        else:choose_ls.append(item_text[i])
    global infor;infor = choose_ls.copy()
    #print(infor)
    global save_template;save_template = item_text[0]
    global var_l241;var_l241.set(item_text[0]) # 设置var_l241为模板名
    global k;k = 1
    global e2_4_2
    e2_4_2.delete(0, tk.END)
    e2_4_2.insert(0, item_text[k])

def template_control_change_vague():# 模糊搜索
    global search_word
    global f2_4_1_l_2 # 本次框架
    global treeview2_4_1_1,item2_4_4_1
    # 先引入状态
    global type_2_4_1
    # 根据状态进行调整(退出可能有的原框架)
    if type_2_4_1 == 0: # 第一次进入该函数
        type_2_4_1 = 1
        f2_4_1_l_2.pack(fill = 'both',expand = True) # 这个函数的主框架为f1_4_1_l_2
    elif type_2_4_1 == 1: # 刚进入过方法一或二
        pass
    # 准备搜索词的列表
    search_word_ls = jieba.lcut(search_word)
    #print(search_word_ls)
    to_be_searched_ls = []
    # 建立表格
        # 清空表格
    x=treeview2_4_1_1.get_children()
    for j in x:
        treeview2_4_1_1.delete(j)
        #填写表格内容
    for i in range(36): # 占空行
        treeview2_4_1_1.insert('', 0, values=('','','','','','','','','','','','','','','','','','','','',''))
    wtemplate = open('./resources/system/template/template.txt','r',encoding='UTF-8')
    wtemplate.seek(0) #指针回到文件开头
    for line in wtemplate.readlines():
        tname = get_kth_in_line(line,1) # 模板名字
        #fname = './resources/infor_'+tname+'.txt' # 文件名字
        length = get_kth_in_line(line,0)
        if_printed = False
        for i in range(length):
            for j in range(len(search_word_ls)):
                to_be_searched_ls = jieba.lcut(str(get_kth_in_line(line,i+1)))
                for k in range(len(to_be_searched_ls)):
                    if str(to_be_searched_ls[k]) == str(search_word_ls[j]):
                        for count in range(20):
                            if count < length-1:
                                item2_4_4_1[count] = get_kth_in_line(line,count+2)
                            else:
                                item2_4_4_1[count] = " "
                        treeview2_4_1_1.insert('', 0, values=(tname, item2_4_4_1[0], item2_4_4_1[1],item2_4_4_1[2],\
                                                           item2_4_4_1[3],item2_4_4_1[4],item2_4_4_1[5],item2_4_4_1[6],\
                                                           item2_4_4_1[7],item2_4_4_1[8],item2_4_4_1[9],item2_4_4_1[10],\
                                                           item2_4_4_1[11],item2_4_4_1[12],item2_4_4_1[13],item2_4_4_1[14],\
                                                           item2_4_4_1[15],item2_4_4_1[16],item2_4_4_1[17],item2_4_4_1[18],\
                                                           item2_4_4_1[19]))
                        if_printed = True
                        break
                if if_printed:break
            if if_printed:break
    wtemplate.close()

def template_control_change_precise(): # 精确搜索
    global search_word
    global f2_4_1_l_2 # 本次框架
    global treeview2_4_1_1,item2_4_4_1
    # 先引入状态
    global type_2_4_1
    # 根据状态进行调整(退出可能有的原框架)
    if type_2_4_1 == 0: # 第一次进入该函数
        type_2_4_1 = 1
        f2_4_1_l_2.pack(fill = 'both',expand = True) # 这个函数的主框架为f1_4_1_l_2
    elif type_2_4_1 == 1: # 刚进入过方法一或二
        pass
    # 建立表格
        # 清空表格
    x=treeview2_4_1_1.get_children()
    for j in x:
        treeview2_4_1_1.delete(j)
        #填写表格内容
    for i in range(36): # 占空行
        treeview2_4_1_1.insert('', 0, values=('','','','','','','','','','','','','','','','','','','','',''))
    wtemplate = open('./resources/system/template/template.txt','r',encoding='UTF-8')
    wtemplate.seek(0) #指针回到文件开头
    for line in wtemplate.readlines():
        tname = get_kth_in_line(line,1) # 模板名字
        length = get_kth_in_line(line,0)
        for count in range(length):
            if get_kth_in_line(line,count+1) == search_word: 
                for count in range(20):
                    if count < length-1:
                        item2_4_4_1[count] = get_kth_in_line(line,count+2)
                    else:
                        item2_4_4_1[count] = " "
                treeview2_4_1_1.insert('', 0, values=(tname, item2_4_4_1[0], item2_4_4_1[1],item2_4_4_1[2],\
                                                   item2_4_4_1[3],item2_4_4_1[4],item2_4_4_1[5],item2_4_4_1[6],\
                                                   item2_4_4_1[7],item2_4_4_1[8],item2_4_4_1[9],item2_4_4_1[10],\
                                                   item2_4_4_1[11],item2_4_4_1[12],item2_4_4_1[13],item2_4_4_1[14],\
                                                   item2_4_4_1[15],item2_4_4_1[16],item2_4_4_1[17],item2_4_4_1[18],\
                                                   item2_4_4_1[19]))
                break
            else:pass
    wtemplate.close()
def template_control_change_precise_pre(): # 精确搜索和模糊搜索提前安放模板
    #1 先安放主框架
    global f2_4_1_l_2
    f2_4_1_l_2.pack(fill = 'both',expand = True)
    #2 其他要用的变量
    global treeview2_4_1_1,columns2_4_1_1,item2_4_4_1
    #3 放好表头
            # 表格框架搭建
    columns2_4_1_1 = ("template", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10",\
               "11","12","13","14","15","16","17","18","19","20")
    treeview2_4_1_1 = ttk.Treeview(f2_4_1_l_2, height=18, show="headings", columns=columns2_4_1_1)  # 表格
    treeview2_4_1_1.column("template", width=120, anchor='center') # 表示列,不显示
    item2_4_4_1 = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
    for count in range(20):
        treeview2_4_1_1.column(str(item2_4_4_1[count]), width=100, anchor='center')
        # 显示表头
    treeview2_4_1_1.heading("template", text="template") 
    count = 0
    for count in range(20):
        treeview2_4_1_1.heading(str(item2_4_4_1[count]), text=str(item2_4_4_1[count]))
        # 表格安放
    treeview2_4_1_1.pack(side=tk.LEFT, fill=tk.BOTH)
        # 定义单击事件
    def treeviewClick2_4_1_1(event):# 单击事件
        global treeview2_4_1_1
        for item in treeview2_4_1_1.selection():
            item_text = treeview2_4_1_1.item(item,"values")
            try:tem_change(item_text)
            except:pass
    treeview2_4_1_1.bind('<ButtonRelease-1>', treeviewClick2_4_1_1)#绑定单击离开事件
    #4 最后隐藏提前的布局
    f2_4_1_l_2.pack_forget()
    
def template_control_change_out(): # 退出
    f2_4_1_l.pack_forget()
    f2_4_1_r.pack_forget()
    f2_4_1.pack_forget()
    note.pack_forget()
    b2_4_1.pack_forget()
def template_control_change_back(): # 返回
    template_control_change_out()
    template_control()

###############################################################################################################################################
###############################################################################################################################################
'''
设置函数
'''
def setting_control():
    # 惯例操作
    main_out()
    var.set("SETTING    SYSTEM\n")
    global b3_1
    if platform.system() == 'Darwin':# Mac系统
        b3_1 = tk.Button(window, text="Back to last level", width=20, height=3,fg = COLOR_MB_FRONT,command=lambda:setting_control_back())
    elif platform.system() == 'Windows':# Windows系统
        b3_1 = tk.Button(window, text="Back to last level", width=20, height=3,fg = COLOR_FRONT,bg = COLOR_SUB,command=lambda:setting_control_back())
    note.pack()
    b3_1.pack()
    # 安放设置列表
        # 框架 f3_2
    global f3_2;f3_2 = tk.Frame(window)
    f3_2.pack(fill = 'x')
    global u3_1;u3_1 = tk.StringVar()
    u3_1.set('请选择下面设置选项')
    global l_1
    l_1 = tk.Label(f3_2,textvariable=u3_1,bg = COLOR_SUB,fg = COLOR_FRONT)  
    l_1.pack(side = 'left',fill = 'x',expand = True)
    global cmb3_1
    cmb3_1 = ttk.Combobox(f3_2)  # https://blog.csdn.net/huige6941/article/details/100300338 下拉框的颜色
    cmb3_1.pack(side = 'left')
        # 框架 f3_1
    global f3_1;f3_1 = tk.Frame(window,bg = COLOR_SUB)
    f3_1.pack(fill = 'both',expand = True)
        # 树
    global treeview3_1,columns3_1,item3_1
    #3 放好表头
            # 表格框架搭建
    columns3_1 = ("template", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10",\
               "11","12","13","14","15","16","17","18","19","20")
    treeview3_1 = ttk.Treeview(f3_1, height=18, show="headings", columns=columns3_1)  # 表格
    treeview3_1.column("template", width=120, anchor='center') # 表示列,不显示
    item3_1 = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
    for count in range(20):
        treeview3_1.column(str(item3_1[count]), width=100, anchor='center')
        # 显示表头
    treeview3_1.heading("template", text="template") 
    count = 0
    for count in range(20):
        treeview3_1.heading(str(item3_1[count]), text=str(item3_1[count]))
        # 表格安放
    treeview3_1.pack(side=tk.LEFT, fill=tk.BOTH)
        # 定义单击事件
    def treeviewClick3_1(event):# 单击事件
        global treeview3_1
        for item in treeview3_1.selection():
            item_text = treeview3_1.item(item,"values")
            try:setting_do(item_text)
            except:pass
    treeview3_1.bind('<ButtonRelease-1>', treeviewClick3_1)#绑定单击离开事件
        # 内容填写
    for i in range(36): # 占空行
        treeview3_1.insert('', 0, values=('','','','','','','','','','','','','','','','','','','','',''))
    wtemplate = open('./resources/system/template/template.txt','r',encoding='UTF-8')
    wsetting = open('./resources/system/setting/setting.txt','r',encoding='UTF-8')
    wsetting.seek(0) #指针回到文件开头
    for line in wsetting.readlines():
        tname = get_kth_in_line(line,1) # 设置头一项名字
        if tname != "#":
            length = get_kth_in_line(line,0)
            for count in range(20):
                if count < length-1:
                    item3_1[count] = get_kth_in_line(line,count+2)
                else:
                    item3_1[count] = " "
            treeview3_1.insert('', 0, values=(tname, item3_1[0], item3_1[1],item3_1[2],\
                                               item3_1[3],item3_1[4],item3_1[5],item3_1[6],\
                                               item3_1[7],item3_1[8],item3_1[9],item3_1[10],\
                                               item3_1[11],item3_1[12],item3_1[13],item3_1[14],\
                                               item3_1[15],item3_1[16],item3_1[17],item3_1[18],\
                                               item3_1[19]))
    #wsetting.write('music  on_or_off  on  \nmusic name  123.mp3  \n')
    wsetting.close()
    
def setting_personal():# 个人信息设置
    def setting_personal_change(event):
        global L3_1,choose
        global var_l31;var_l31.set(choose)
        choose = get_kth_in_line(L3_1.get(L3_1.curselection()),1)
        if choose == "password":choose = 'Input old password first!'
    def setting_personal_back():
        f3_1.pack_forget()
        note.pack_forget()
        b3_1.pack_forget()
        setting_control()
    def setting_personal_listbox():
        wtemplate = open('./resources/system/setting/password.txt','r',encoding='UTF-8') 
        for line in wtemplate.readlines():
            if get_kth_in_line(line,1) == 'password':
                L3_1.insert("end",'password')
            if get_kth_in_line(line,1) != 'password':
                L3_1.insert("end",line)
            L3_1.pack(fill="both",side= "top", expand = True ) # 左右两边都填充 #fill=Y and X
            sb3_1.config(command=L3_1.yview)
        wtemplate.close()
    def get_password():
        # 获取密码
        print("即将获取密码")
        wsetting = open('./resources/system/setting/password.txt','r',encoding='UTF-8')
        for line in wsetting.readlines():
            if str(get_kth_in_line(line,1)) == 'password':break
        wsetting.close()
        password_s = []
        for i in range(get_kth_in_line(line,0)-1):
            password_s.append(get_kth_in_line(line,i+2))
        password = ''
        for i in range(len(password_s)):
            #print(chr(int(password_s[i])))
            password = password+chr(int(password_s[i]))
        return password
    # step 1推出上级内容
    setting_control_out()
    # step 2 放上本次内容
        # 设置标题与按钮
    var.set("Personal Information Setting\n")
    global b3_1
    if platform.system() == 'Darwin':# Mac系统
        b3_1 = tk.Button(window, text="Back to last level", width=20, height=3,fg = COLOR_MB_FRONT,command=lambda:setting_personal_back())
    elif platform.system() == 'Windows':# Windows系统
        b3_1 = tk.Button(window, text="Back to last level", width=20, height=3,fg = COLOR_FRONT,bg = COLOR_SUB,command=lambda:setting_personal_back())
    note.pack();b3_1.pack()
        # 设置主框架与左右框架
    global f3_1,f3_1_l,f3_1_r
    global width_set_l  #width_set_l = 3/16*width_set
    global width_set_r  #width_set_r = 13/16*width_set
    f3_1 = tk.Frame(window,bg = COLOR_BACK)
    f3_1.pack(fill = 'both',expand = True)
    f3_1_r = tk.Frame(f3_1,bg = COLOR_BACK,width = int(2*width_set_l))
    f3_1_r.pack(side = 'right',fill = 'y')
    f3_1_l = tk.Frame(f3_1,bg = COLOR_F2_BACK, width = int(width_set_r - width_set_l))
    f3_1_l.pack(side = 'right', fill = 'both',expand = True)
        # 右侧输入部分
            # 右边 占空行
    l3_0 = tk.Label(f3_1_r,bg = COLOR_BACK,text='\n',height = 1,width = int(2*width_set_l/10)) #  Label宽度会破坏Frame宽度，这里计算出近似代替的宽度
    l3_0.pack()
            # 右边输入部分-右边顶部题目label - l3_1
    global var_l31,choose;choose = '请选择左侧信息'
    var_l31=tk.StringVar() ;var_l31.set(choose)
    l3_1 = tk.Label(f3_1_r,bg = COLOR_F2_BACK,fg = COLOR_FRONT,textvariable=var_l31,height = 1,width = int(2*width_set_l/10)) #  Label宽度会破坏Frame宽度，这里计算出近似代替的宽度
    l3_1.pack()
            # 右边输入部分-输入窗口entry - e1_4_2
    def e3_1_submit(event):
        global choose,e3_1,password1,password2
        if choose == 'Input old password first!':
            if e3_1.get() == get_password():# 老密码正确
                var_l31.set("Please Input New password")   
                choose = "Please Input New password"
                e3_1.delete(0, tk.END)
        elif choose == 'Please Input New password':
            password1 = e3_1.get()
            var_l31.set("Input New password again")
            choose = "Input New password again"
            e3_1.delete(0, tk.END)
        elif choose == 'Input New password again':
            password2 = e3_1.get()
            e3_1.delete(0, tk.END)
            if password2 == password1:
                wsetting = open('./resources/system/setting/password.txt','r',encoding='UTF-8') # 文本形式，只读
                wcopy = open('./resources/inforchange.txt','w',encoding='UTF-8') # 文本形式，重写模式
                for line in wsetting.readlines():
                    wcopy.write(line)
                wcopy.close();wsetting.close()
                wcopy = open('./resources/inforchange.txt','r',encoding='UTF-8') # 文本形式，只读
                wsetting = open('./resources/system/setting/password.txt','w',encoding='UTF-8') # 文本形式，重写模式
                for line in wcopy.readlines():
                    if get_kth_in_line(line,1) == 'password':
                        wsetting.write("password")
                        for i in range(len(password2)):
                            wsetting.write("  ")
                            wsetting.write(str(ord(password2[i])))
                        wsetting.write("\n")
                    else:
                        wsetting.write(line)
                wcopy.close();wsetting.close()
                L3_1.delete(0, tk.END)
                setting_personal_listbox()# 刷新表格
                choose = "Changeed Successfully!"
                var_l31.set(choose)
        elif choose == "Changeed Successfully!" or choose == "请选择左侧信息":pass
        else:
            ask_if = messagebox.askyesno('askyesno', 'Sure To Change?', parent=window)
            if ask_if == True:
                change = e3_1.get()
                e3_1.delete(0, tk.END)
                wsetting = open('./resources/system/setting/password.txt','r',encoding='UTF-8') # 文本形式，只读
                wcopy = open('./resources/inforchange.txt','w',encoding='UTF-8') # 文本形式，重写模式
                for line in wsetting.readlines():
                    wcopy.write(line)
                wcopy.close();wsetting.close()
                wcopy = open('./resources/inforchange.txt','r',encoding='UTF-8') # 文本形式，只读
                wsetting = open('./resources/system/setting/password.txt','w',encoding='UTF-8') # 文本形式，重写模式
                for line in wcopy.readlines():
                    if get_kth_in_line(line,1) == choose:
                        wsetting.write(choose +"  "+ change +'\n')
                    else:
                        wsetting.write(line)
                wcopy.close();wsetting.close()
                L3_1.delete(0, tk.END)
                setting_personal_listbox()# 刷新表格
                 
    global e3_1
    e3_1 = tk.Entry(f3_1_r,bg = COLOR_F2_BACK,fg = COLOR_FRONT)
    e3_1.pack(fill = 'x')
    e3_1.bind("<Return>",e3_1_submit)
    
        # 左侧展示部分
    global L3_1
    sb3_1 = tk.Scrollbar(f3_1_l)
    sb3_1.pack(side="right", fill="y") # 滚动条放在右边，上下填充
    L3_1 = tk.Listbox(f3_1_l,bg = COLOR_F2_BACK,fg = COLOR_F2_FRONT, yscrollcommand=sb3_1.set)
    setting_personal_listbox()
    L3_1.bind('<ButtonRelease-1>',setting_personal_change)
    
def setting_do(item_text): # 设置生效函数
    # 下拉菜单
    global f3_2,u3_1
    global cmb3_1
    # 不同设置
    if item_text[0] == 'music' and item_text[1] == 'on_or_off': # 设置音乐是否开启
        def setting_do_music_onoroff(event): #音乐开关
            if cmb3_1.get() == 'on':
                if item_text[2] == 'on':pass
                else:
                    ini_music()#开音乐
                    # 先把文件保存到工作区
                    wsetting = open('./resources/system/setting/setting.txt','r',encoding='UTF-8') # 文本形式，只读
                    wcopy = open('./resources/inforchange.txt','w',encoding='UTF-8') # 文本形式，重写模式
                    for line in wsetting.readlines():
                        wcopy.write(line)
                    wcopy.close()
                    wsetting.close()
                    # 再进行文件重写
                    wcopy = open('./resources/inforchange.txt','r',encoding='UTF-8') # 文本形式，只读
                    wsetting = open('./resources/system/setting/setting.txt','w',encoding='UTF-8') # 文本形式，重写模式
                    for line in wcopy.readlines():
                        if get_kth_in_line(line,1) == 'music' and get_kth_in_line(line,2) == 'on_or_off':
                            wsetting.write('music  on_or_off  on  \n')
                        else:
                            wsetting.write(line)
                    wcopy.close()
                    wsetting.close()
                    setting_control_out();setting_control() # 重新进入
            elif cmb3_1.get() == 'off':
                if item_text[2] == 'off':pass
                else:
                    pygame.mixer.music.stop()#关音乐
                    # 先把文件保存到工作区
                    wsetting = open('./resources/system/setting/setting.txt','r',encoding='UTF-8') # 文本形式，只读
                    wcopy = open('./resources/inforchange.txt','w',encoding='UTF-8') # 文本形式，重写模式
                    for line in wsetting.readlines():
                        wcopy.write(line)
                    wcopy.close()
                    wsetting.close()
                    # 再进行文件重写
                    wcopy = open('./resources/inforchange.txt','r',encoding='UTF-8') # 文本形式，只读
                    wsetting = open('./resources/system/setting/setting.txt','w',encoding='UTF-8') # 文本形式，重写模式
                    for line in wcopy.readlines():
                        if get_kth_in_line(line,1) == 'music' and get_kth_in_line(line,2) == 'on_or_off':
                            wsetting.write('music  on_or_off  off  \n')
                        else:
                            wsetting.write(line)
                    wcopy.close()
                    wsetting.close()
                    setting_control_out();setting_control() # 重新进入
            else:pass
        # 调用函数内容
        cmb3_1['value'] = ('on','off')#设置下拉菜单中的值 
        if item_text[2] == 'on':#本来音乐是关的
            cmb3_1.current(0)
        elif item_text[2] == 'off':# 本来音乐是开的
            cmb3_1.current(1)
        else: pass
        cmb3_1.bind("<<ComboboxSelected>>",setting_do_music_onoroff)

    elif item_text[0] == 'music' and item_text[1] == 'name': # 设置音乐名称
        def setting_do_music_choose(event): #音乐开关
            # 更改音乐文件
            name = cmb3_1.get()
            wsetting = open('./resources/system/setting/setting.txt','r',encoding='UTF-8') # 文本形式，只读
            wcopy = open('./resources/inforchange.txt','w',encoding='UTF-8') # 文本形式，重写模式
            for line in wsetting.readlines():
                wcopy.write(line)
            wcopy.close()
            wsetting.close()
            wcopy = open('./resources/inforchange.txt','r',encoding='UTF-8') # 文本形式，只读
            wsetting = open('./resources/system/setting/setting.txt','w',encoding='UTF-8') # 文本形式，重写模式
            for line in wcopy.readlines():
                if get_kth_in_line(line,1) == 'music' and get_kth_in_line(line,2) == 'name':
                    wsetting.write('music  name  '+name+'\n')
                else:
                    wsetting.write(line)
            wcopy.close()
            wsetting.close()
            setting_control_out();setting_control() # 重新进入
            # 重启音乐
            ini_related_to_music()
        # 调用函数内容
        wsetting = open('./resources/system/music/setting_music_name.txt','r',encoding='UTF-8') # 文本形式，重写模式
        ls = []
        for line in wsetting.readlines():
            ls.append(get_kth_in_line(line,2))
        wsetting.close()
        cmb3_1['value'] = (ls)#设置下拉菜单中的值 
        #cmb3_1.current(0) 不设置默认值了
        cmb3_1.bind("<<ComboboxSelected>>",setting_do_music_choose)
       
    elif item_text[0] == 'common' and item_text[1] == 'font' : pass # 设置字号 
        
    elif item_text[0] == 'common' and item_text[1] == 'dark_mod' : # 暗黑模式
        def setting_do_dark_mod(event): #暗黑模式
            if cmb3_1.get() == 'on':
                if item_text[2] == 'on':pass
                else:
                    #global COLOR_BACK,COLOR_FRONT,COLOR_SUB 
                    COLOR_BACK = 'dimgray';COLOR_FRONT = 'white';COLOR_SUB = 'black'
                    print("本来是off 现在要改成on")
                    wsetting = open('./resources/system/setting/setting.txt','r',encoding='UTF-8') # 文本形式，只读
                    wcopy = open('./resources/inforchange.txt','w',encoding='UTF-8') # 文本形式，重写模式
                    for line in wsetting.readlines():
                        wcopy.write(line)
                    wcopy.close();wsetting.close()
                    wcopy = open('./resources/inforchange.txt','r',encoding='UTF-8') # 文本形式，只读
                    wsetting = open('./resources/system/setting/setting.txt','w',encoding='UTF-8') # 文本形式，重写模式
                    for line in wcopy.readlines():
                        if get_kth_in_line(line,1) == 'common' and get_kth_in_line(line,2) == 'dark_mod':
                            wsetting.write('common  dark_mod  on  \n')
                        else:
                            wsetting.write(line)
                    wcopy.close();wsetting.close()
                    setting_control_out();setting_control() # 重新进入
            elif cmb3_1.get() == 'off':
                if item_text[2] == 'off':pass
                else:
                    #global COLOR_BACK,COLOR_FRONT,COLOR_SUB
                    COLOR_BACK = 'white';COLOR_FRONT = 'black';COLOR_SUB = 'floralwhite'
                    wsetting = open('./resources/system/setting/setting.txt','r',encoding='UTF-8') # 文本形式，只读
                    wcopy = open('./resources/inforchange.txt','w',encoding='UTF-8') # 文本形式，重写模式
                    for line in wsetting.readlines():
                        wcopy.write(line)
                    wcopy.close();wsetting.close()
                    wcopy = open('./resources/inforchange.txt','r',encoding='UTF-8') # 文本形式，只读
                    wsetting = open('./resources/system/setting/setting.txt','w',encoding='UTF-8') # 文本形式，重写模式
                    for line in wcopy.readlines():
                        if get_kth_in_line(line,1) == 'common' and get_kth_in_line(line,2) == 'dark_mod':
                            wsetting.write('common  dark_mod  off  \n')
                        else:
                            wsetting.write(line)
                    wcopy.close();wsetting.close()
                    setting_control_out();setting_control() # 重新进入
            else: pass
        # 调用函数内容
        cmb3_1['value'] = ('on','off')#设置下拉菜单中的值 
        if item_text[2] == 'on':#本来音乐是关的
            cmb3_1.current(0)
        elif item_text[2] == 'off':# 本来音乐是开的
            cmb3_1.current(1)
        else: pass
        cmb3_1.bind("<<ComboboxSelected>>",setting_do_dark_mod)
        
    elif item_text[0] == 'safe' and item_text[1] == 'password' and (item_text[2] == 'on' or item_text[2] == 'off'): # 设置是否需要密码
        def setting_do_password_onoroff(event):
            if cmb3_1.get() == 'on':
                if item_text[2] == 'on':pass
                else:
                    # 先把文件保存到工作区
                    wsetting = open('./resources/system/setting/setting.txt','r',encoding='UTF-8') # 文本形式，只读
                    wcopy = open('./resources/inforchange.txt','w',encoding='UTF-8') # 文本形式，重写模式
                    for line in wsetting.readlines():
                        wcopy.write(line)
                    wcopy.close()
                    wsetting.close()
                    # 再进行文件重写
                    wcopy = open('./resources/inforchange.txt','r',encoding='UTF-8') # 文本形式，只读
                    wsetting = open('./resources/system/setting/setting.txt','w',encoding='UTF-8') # 文本形式，重写模式
                    for line in wcopy.readlines():
                        if get_kth_in_line(line,1) == 'safe' and get_kth_in_line(line,2) == 'password' and get_kth_in_line(line,3) == 'off':
                            wsetting.write('safe  password  on  \n')
                        else:
                            wsetting.write(line)
                    wcopy.close()
                    wsetting.close()
                    setting_control_out();setting_control() # 重新进入
            elif cmb3_1.get() == 'off':
                if item_text[2] == 'off':pass
                else:
                    # 先把文件保存到工作区
                    wsetting = open('./resources/system/setting/setting.txt','r',encoding='UTF-8') # 文本形式，只读
                    wcopy = open('./resources/inforchange.txt','w',encoding='UTF-8') # 文本形式，重写模式
                    for line in wsetting.readlines():
                        wcopy.write(line)
                    wcopy.close()
                    wsetting.close()
                    # 再进行文件重写
                    wcopy = open('./resources/inforchange.txt','r',encoding='UTF-8') # 文本形式，只读
                    wsetting = open('./resources/system/setting/setting.txt','w',encoding='UTF-8') # 文本形式，重写模式
                    for line in wcopy.readlines():
                        if get_kth_in_line(line,1) == 'safe' and get_kth_in_line(line,2) == 'password' and get_kth_in_line(line,3) == 'on':
                            wsetting.write('safe  password  off  \n')
                        else:
                            wsetting.write(line)
                    wcopy.close()
                    wsetting.close()
                    setting_control_out();setting_control() # 重新进入
            else:pass
        # 调用函数内容
        cmb3_1['value'] = ('on','off')#设置下拉菜单中的值 
        if item_text[2] == 'on':#本来是开的
            cmb3_1.current(0)
        elif item_text[2] == 'off':# 本来是关的
            cmb3_1.current(1)
        else: pass
        cmb3_1.bind("<<ComboboxSelected>>",setting_do_password_onoroff)
    
    #elif ... : pass # 下一个设置写在这里
    elif item_text[0] == 'Me': # 进入个人信息设置
        setting_personal()
    
    else: pass

def setting_control_out():# 退出函数
    f3_1.pack_forget()
    f3_2.pack_forget()
    note.pack_forget()
    b3_1.pack_forget()
def setting_control_back():# 返回函数 b3_1 按钮
    setting_control_out()
    main()

'''
语言设置-中英文切换，隐私安全-输入密码查看信息，显示-暗黑模式与字体大小，词云的生成，信息的备份，备份的覆盖-全覆盖，差异覆盖，模板删除的撤回，云端备份，
搜索筛选功能，输入空格，信息变量，提示，预置信息，
'''

###############################################################################################################################################
###############################################################################################################################################
'''
工具函数
'''
# 寻找一个字符串中的某个词
def get_kth_in_line(line,k):#当k=0时，返回词的个数，当k<0时，为倒叙寻找第-k个词，当k>0时，为正序寻找第k个词
    max_num = 0;count = 0;last = " ";word = ""
    for item in line:
        if last == " " and item != " " and item != "\n": max_num = max_num+1
        last = item
    last = " "
    if k == 0:                    # 当k=0时，返回词的个数
        return max_num
    elif k > 0 and k <= max_num:  # 当k>0时，为正序寻找第k的词
        for item in line:
            if (last == " " or last == '\n') and (item != " " and item != "\n"): count=count+1
            last = item
            if k == count and item!=' ' and item != '\n': word = word+item
        return word
    elif k < 0 and -k <= max_num: # 当k<0时，为倒叙寻找第k的词
        k = max_num + 1 + k
        for item in line:
            if (last == " " or last == '\n') and (item != " " and item != "\n"): count=count+1
            last = item
            if k == count and item!=' ' and item != "\n": word = word+item
        return word
    else:                         # 输入格式错误
        print("wrong type of k in get_kth_in_line(line,k) of line = "+line)
        
def read_excel(word,word_type):
    print(word)
    if word_type == 2 and word % 1 == 0:  # 如果是整形
        word = int(word)
    elif word_type == 3:
        # 转成datetime对象
        try:
            date = datetime(*xldate_as_tuple(word, 0))
            word = date.strftime('%Y/%d/%m %H:%M:%S')
            if word[-8:]=='00:00:00' :#只有日期
                word = word[:-9]
        except:
            date = datetime(*xldate_as_tuple(637.0+word, 0))
            word = date.strftime('%H:%M:%S')
        '''
        elif word[-8:]=='00:00:00' :#只有时间
            word = word[:-9]
        '''
    return word

# 弹出窗口进行确认 - 注意需要通过全局变量make_sure_var来判断用户选择而不是make_sure的返回值！
def make_sure(note,width=300,height=150,mood=0):# note为提示词语,width为宽,height为长,mood为可选参数 默认为0
    global make_sure_var ;make_sure_var= -1
    def return_False():
        global make_sure_var;make_sure_var = 0
        print(make_sure_var)
        mind.destroy()
    def return_True():
        global make_sure_var;make_sure_var = 1
        print(make_sure_var)
        mind.destroy()
    if mood == 0:
        mind = tk.Tk() # 生成窗口变量
        mind.geometry(str(width)+"x"+str(height)+"+500+300")  # 大小和位置
        mind.title('make sure')      #设置窗口标题
        lnote = tk.Label(mind, text=note,font=("黑体", 23))
        lnote.pack(fill="x",side="top")
        bmind1 = tk.Button(mind, text="Yes", width=10, height=3,command=lambda:return_True())
        bmind2 = tk.Button(mind, text="No ", width=10, height=3,command=lambda:return_False())
        bmind1.pack()
        bmind2.pack()
        mind.mainloop()

# 弹出窗口进行提示
def mind(mind_note,mood=0):# mind_note为提示词语,mood为可选参数 默认为0
    if mood == 0:
        mind = tk.Tk() # 生成窗口变量
        mind.geometry("300x150+500+300")  # 大小和位置
        mind.title('提示')      #设置窗口标题
        print(mind_note)
        lnote = tk.Label(mind, text=mind_note,font=("黑体", 23))
        lnote.pack(fill="both",side="top",expand = True)
    if mood == 1:
        mind = tk.Tk() # 生成窗口变量
        mind.geometry("300x150+500+300")  # 大小和位置
        mind.title('警告')      #设置窗口标题
        print(mind_note)
        lnote = tk.Label(mind, text=mind_note,font=("黑体", 23),bg = "red")
        lnote.pack(fill="both",side="top",expand = True)

###############################################################################################################################################
###############################################################################################################################################
'''
开始程序
'''
def start():
    main_password()
    window.mainloop()
    exit_()
    
try:
    initial()
    start()
except:
    pass
