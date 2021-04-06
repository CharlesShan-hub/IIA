# mian function

import pygame
from tkinter import ttk
import tkinter as tk
import os
import jieba

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
    # 初始化生成窗口
    ini_build_window()
    # 加载背景音乐
    # 以后用过查看配置文件是否加载音乐
    if(True):ini_music()
    # 建立变量
    ini_build_var()

def ini_check():# 核查文件是否合格
    # 查看 resources文件夹 是否存在
    resources_check = os.path.exists('resources')
    print(str(resources_check) +" - 文件夹检查中") #1
    resources_last = os.path.dirname(__file__)# 上级目录
    if resources_check == False:
        pass
        #ini_help()    这里是引导窗口
    if resources_check == False:
        try:
            os.mkdir(resources_last+'\\resources') # Windows 平台有效
        except:
            pass
    resources_check = os.path.exists('resources')
    print("For Windows : "+str(resources_check))#2
    if resources_check == False:
        try:
            os.mkdir(resources_last+'/resources') # Mac 平台有效
        except:
            pass
    resources_check = os.path.exists('resources')
    print("For Mac : "+str(resources_check))#3
    if resources_check == True:
        print("文件夹检查成功!")

    # 查看模板文件(template.txt)是否创建过
    try:
        wtemplate = open('./resources/template.txt','r') 
        wtemplate.close()
        print("文件检查成功!")
    except:
        wtemplate = open('./resources/template.txt','a') 
        wtemplate.close()
        print("文件生成成功!")
    
def ini_build_window():# 初始化生成窗口
    global window
    global width_set; width_set = 800
    window = tk.Tk() # 生成窗口变量
    window.geometry("800x550+400+200")  # 大小和位置
    window.title('个人信息管理')      #设置窗口标题
    
def ini_help(): # 引导窗口（未完成）
    global window_help
    global width_set; width_set = 800
    window_help = tk.Tk() # 生成窗口变量
    window_help.geometry("800x550+400+200")  # 大小和位置
    window_help.title('个人信息管理引导窗口')      #设置窗口标题
    
def ini_music():
    # 以后通过读取设置文件来配置music_name
    music_name = '纸短情长(小调).mp3'
    try:
        file=r'./resources/'+music_name
        pygame.mixer.init()
        pygame.mixer.music.load(file)
        pygame.mixer.music.play(-1)
        print("开始播放音乐"+music_name)
    except:
        print("未加载音乐")
    
def ini_build_var():# 初始化公共变量
    # 这个是note标语和标语的变量
    global var,note,window
    var = tk.StringVar()
    note = tk.Label(window, textvariable=var ,fg="black", font=("黑体", 23), width=40, height=3, justify="left", anchor="center")
    # 左右框架的宽度
    global width_set_l;width_set_l = 3/16*width_set
    global width_set_r;width_set_r = 13/16*width_set

###############################################################################################################################################
###############################################################################################################################################
'''
主界面
''' 
def main():
    global b1,b2,b3#,b4
    var.set("Personal Information Control System !\n")
    b1 = tk.Button(window, text='Related to Information', width=20,height=3, command=lambda:information_control())
    b2 = tk.Button(window, text='Related to Tempalte   ', width=20,height=3, command=lambda:template_control())
    b3 = tk.Button(window, text='System Setting        ', width=20,height=3, command=lambda:setting_control())
    #b4 = tk.Button(window, text='Leave Immidiately     ', width=20,height=3, command=quit)
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
    b1_1 = tk.Button(window, text="Back to last level", width=20, height=3, command=lambda:information_control_back())
    b1_2 = tk.Button(window, text="Add    information", width=20, height=3, command=lambda:information_control_add())
    b1_3 = tk.Button(window, text="Check  information", width=20, height=3, command=lambda:information_control_check())
    b1_4 = tk.Button(window, text="Change information", width=20, height=3, command=lambda:information_control_change())
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
            winfor = open('./resources/infor_'+infor[0]+'.txt','a+') # 文本形式，追加写模式
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
    # 1.2提示文字与返回按钮
    global b1_2_1 
    b1_2_1 = tk.Button(window, text="Back to last level", width=20, height=3,command=lambda:information_control_add_back())
    note.pack()
    b1_2_1.pack()
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
    f1_2_1 = tk.Frame(window)
    f1_2_1.pack(expand='yes', fill='both')
    
    # 2.2 左边选择模板部分 [左边的容器f1_2_2，滚动条，文本框]
    f1_2_2 = tk.Frame(f1_2_1,width = width_set_l)
    f1_2_2.pack(fill = 'y',side = 'left')
    l1_2_1 = tk.Label(f1_2_2,text = '已有模板',justify="left", anchor="center")
    l1_2_1.pack(fill = 'x')
    sb1_2_1 = tk.Scrollbar(f1_2_2)
    sb1_2_1.pack(side=tk.RIGHT,fill='y') # 滚动条放在右边，上下填充
    L1_2_2 = tk.Listbox(f1_2_2, yscrollcommand=sb1_2_1.set)
    L1_2_2.bind('<ButtonRelease-1>',search)
    L1_2_2.pack(side=tk.RIGHT,fill='both')
    wtemplate = open('./resources/template.txt','r') 
    count = 1
    for line in wtemplate.readlines():
        L1_2_2.insert("end", str(count)+":  "+line)
        L1_2_2.pack(fill="both",side= "top", expand = True )
        sb1_2_1.config(command=L1_2_2.yview)
        count = count+1
    wtemplate.close()
    
    # 2.3 右边信息输入部分 
        # step 2.3.1 右边的整框架
    f1_2_3 = tk.Frame(f1_2_1)# 先创建右侧最大框架
    f1_2_3.pack(expand = True,fill = 'both',side = 'left')
        # step 2.3.2 先创建题目label，并摆放在顶部
    var_l122=tk.StringVar()  
    var_l122.set(get_kth_in_line(choose,2))
    l1_2_2 = tk.Label(f1_2_3,textvariable=var_l122,justify="left", anchor="center",height = 1)
    l1_2_2.pack(fill = 'x')
        # step 2.3.3 创建右边子级frame
    f1_2_4 = tk.Frame(f1_2_3)
    f1_2_4.pack(expand = True,fill = 'both',side = 'left')
        # step 3.4 输入区
    var_l123=tk.StringVar()
    if choose == "0:  请选择左侧模板":
        var_l123.set("")
    l1_2_3 = tk.Label(f1_2_4,textvariable=var_l123)
    l1_2_3.pack(fill = 'x')
    e1_2_3 = tk.Entry(f1_2_4)
    e1_2_3.pack(fill = 'x')
    b1_2_3 = tk.Button(f1_2_4, text="Next", width=20, height=2,command=lambda:infor_control_add_infor_next())
    b1_2_3.pack()
    b1_2_4 = tk.Button(f1_2_4, text="Last", width=20, height=2,command=lambda:infor_control_add_infor_last())
    b1_2_4.pack()
    b1_2_5 = tk.Button(f1_2_4, text="Save", width=20, height=2,command=lambda:infor_control_add_infor_save())
    b1_2_5.pack()
    
def information_control_add_out(): # 退出
    f1_2_1.pack_forget()
    b1_2_1.pack_forget()
    note.pack_forget()
    
def information_control_add_back(): # 返回
    information_control_add_out()
    information_control()
    
#-----------------------------------------------------------------------------------------------------------------------------------------------

def information_control_check(): # 信息查看 b1_3 按钮
    #1 惯例操作
    information_control_out()
    var.set("INFORMATION     SYSTEM\n")
    global b1_3_1
    b1_3_1 = tk.Button(window, text="Back to last level", width=20, height=3,command=lambda:information_control_check_back())
    note.pack()
    b1_3_1.pack()
    #2 建立信息查询选择方式
        #2.1 整体框架
    global f1_3_1 
    f1_3_1 = tk.Frame(window)
    f1_3_1.pack(fill = 'both',expand = True)
        #2.2 提示栏
    global choose;choose = "请选择查询方式"
    global l1_3_1,var_l131 # 整框架中的最上边有一个提示栏
    var_l131=tk.StringVar()  
    var_l131.set(choose)
    l1_3_1 = tk.Label(f1_3_1,textvariable=var_l131,font=("黑体", 20))
    l1_3_1.pack(fill = 'x')
        #2.4 选择按钮
    choose_num = 3 # 这里设置选择按钮的数量，方便以后更改
    global f1_3_2
    f1_3_2 = tk.Frame(f1_3_1,width=int(40), height=2)
    f1_3_2.pack()
    b1_3_2 = tk.Button(f1_3_2,text="Search All",width=int(40/choose_num), height=2,justify="left",command=lambda:information_control_check1())
    b1_3_2.pack(side = "left")
    b1_3_3 = tk.Button(f1_3_2,text="Template", width=int(40/choose_num), height=2,justify="left",command=lambda:information_control_check2())
    b1_3_3.pack(side = "left") 
    b1_3_3 = tk.Button(f1_3_2,text="Key Words", width=int(40/choose_num), height=2,justify="left",command=lambda:information_control_check3())
    b1_3_3.pack(side = "left")
        #2.5 按钮的属性（important）
    global type_1_3_3; type_1_3_3 = 0
    # type_1_3_3| 0           |  1           |  2          | ...
    # 代表内容   | 第一次进入按钮 | 上次进入1按钮  | 上次进入2按钮 | ...
        #2.3 提前安放好子框架
    global f1_3_c1;f1_3_c1 = tk.Frame(f1_3_1)
    information_control_check1_pre()
    global f1_3_c2;f1_3_c2 = tk.Frame(f1_3_1)
    information_control_check2_pre()
    global f1_3_c3;f1_3_c3 = tk.Frame(f1_3_1)
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
    #填写表格内容
        # 清空表格
    x=treeview1_3_c1.get_children()
    for j in x:
        treeview1_3_c1.delete(j)
        # 填写表格
    wtemplate = open('./resources/template.txt','r') 
    for line in wtemplate.readlines():
        tname = get_kth_in_line(line,1) # 模板名字
        fname = './resources/infor_'+tname+'.txt' # 文件名字
        length = get_kth_in_line(line,0)
        try:
            number_item = 0
            winfor = open(fname,'r') 
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
    wtemplate.close()
def information_control_check1_pre(): # 信息查看的第一种选择方式-全部列出-准备函数
    global treeview1_3_c1,columns1_3_c1,item1_3_c1
    global f1_3_c1
    f1_3_c1.pack(fill = 'both',expand = True)
    # 建立表格
        # 表格框架搭建
    columns1_3_c1 = ("template", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10",\
               "11","12","13","14","15","16","17","18","19","20")
    treeview1_3_c1 = ttk.Treeview(f1_3_c1, height=18, show="headings", columns=columns1_3_c1)  # 表格
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
    wtemplate = open('./resources/template.txt','r') 
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
    wtemplate = open('./resources/template.txt','r')
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
    f1_3_c2_3.pack(fill = 'both',side = 'left',expand = True)
    # 生成表头
    treeview1_3_2 = ttk.Treeview(f1_3_c2_3, height=18, show="headings", columns=columns)
    if_treeview1_3_2 = 1
    for i in range(number):
        treeview1_3_2.column(str(columns[i]), width=100, anchor='center')
    for i in range(number):
        treeview1_3_2.heading(str(columns[i]), text=str(columns[i]))
    treeview1_3_2.pack(side=tk.LEFT, fill=tk.BOTH)
    # 填写表格内容
    if choose != '0:  请选择左侧模板':
        try:
            winfor = open(fname1_3_2,'r')
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
    f1_3_c2_1 = tk.Frame(f1_3_c2,width = width_set_l,bg = 'red')
    f1_3_c2_1.pack(side = 'left',fill = 'y')
    #3 左侧滚动条与选择栏
    global sb1_3_3_1,L1_3_3
    sb1_3_3_1 = tk.Scrollbar(f1_3_c2_1)
    sb1_3_3_1.pack(side=tk.RIGHT,fill='y')
    L1_3_3 = tk.Listbox(f1_3_c2_1, yscrollcommand=sb1_3_3_1.set)
    L1_3_3.bind('<ButtonRelease-1>',infor_search)
    L1_3_3.pack(side=tk.RIGHT,fill='both')
    #4 右侧主框架 f1_3_c2_2
    global f1_3_c2_2
    f1_3_c2_2 = tk.Frame(f1_3_c2,bg = 'green')# 先创建右侧最大框架
    f1_3_c2_2.pack(expand = True,fill = 'both',side = 'left')
    #5 右侧模板题目label，放在顶部
    global choose,var_l132,l1_3_3;choose = '0:  请选择左侧模板'
    var_l132=tk.StringVar()
    var_l132.set(get_kth_in_line(choose,2))
    l1_3_3 = tk.Label(f1_3_c2_2,textvariable=var_l132,justify="left", anchor="center",height = 1)
    l1_3_3.pack(fill = 'x')
    #6 安放搜索结果-创建右侧次级框架
    global f1_3_c2_3
    f1_3_c2_3 = tk.Frame(f1_3_c2_2)# 先创建右侧最大框架
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
def information_control_check3_pre(): #信息查看的第三种选择方式-关键字-提前准备
    #1 先安放主框架
    global f1_3_c3
    f1_3_c3.pack(fill = 'both',expand = True)
    #2 次框架1（搜索框与选择按钮的框架）
    global f1_3_c3_1
    f1_3_c3_1 = tk.Frame(f1_3_c3) 
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
    e1_3_3 = tk.Entry(f1_3_c3_1,textvariable=u1_3_3)  
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
    f1_3_c3_2 = tk.Frame(f1_3_c3,bg = 'pink')
    f1_3_c3_3 = tk.Frame(f1_3_c3,bg = 'red')
    f1_3_c3_4 = tk.Frame(f1_3_c3,bg = 'yellow')
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
    wtemplate = open('./resources/template.txt','r')
    wtemplate.seek(0) #指针回到文件开头
    for line in wtemplate.readlines():
        tname = get_kth_in_line(line,1) # 模板名字
        fname = './resources/infor_'+tname+'.txt' # 文件名字
        length = get_kth_in_line(line,0)
        try:
            number_item = 0
            winfor = open(fname,'r') 
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
    treeview1_3_c3_2 = ttk.Treeview(f1_3_c3_2, height=18, show="headings", columns=columns1_3_c3_2)  # 表格
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
        #填写表格内容
    wtemplate = open('./resources/template.txt','r')
    wtemplate.seek(0) #指针回到文件开头
    for line in wtemplate.readlines():
        tname = get_kth_in_line(line,1) # 模板名字
        fname = './resources/infor_'+tname+'.txt' # 文件名字
        length = get_kth_in_line(line,0)
        try:
            winfor = open(fname,'r') 
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
                number_item = 0
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
    treeview1_3_c3_3 = ttk.Treeview(f1_3_c3_3, height=18, show="headings", columns=columns1_3_c3_3)  # 表格
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
    b1_4_1 = tk.Button(window, text="Back to last level", width=20, height=3,command=lambda:information_control_change_back())
    note.pack()
    b1_4_1.pack()
    # 设置主框架与左右框架
    global f1_4_1,f1_4_1_l,f1_4_1_r
    global width_set_l  #width_set_l = 3/16*width_set
    global width_set_r  #width_set_r = 13/16*width_set
    f1_4_1 = tk.Frame(window)
    f1_4_1.pack(fill = 'both',expand = True)
    #print(int(2*width_set_l))
    #print(int(width_set_r - width_set_l))
    f1_4_1_r = tk.Frame(f1_4_1,bg = 'red',width = int(2*width_set_l))
    f1_4_1_r.pack(side = 'right',fill = 'y')
    f1_4_1_l = tk.Frame(f1_4_1,bg = 'green', width = int(width_set_r - width_set_l))
    f1_4_1_l.pack(side = 'right', fill = 'both',expand = True)
    # 右边输入部分-右边的整框架为f1_4_1_r
    # 右边输入部分-右边顶部题目label - l1_4_1
    global var_l141,choose;choose = '请选择左侧信息'
    var_l141=tk.StringVar() ;var_l141.set(choose)
    l1_4_1 = tk.Label(f1_4_1_r,textvariable=var_l141,height = 1,width = int(2*width_set_l/10)) #  Label宽度会破坏Frame宽度，这里计算出近似代替的宽度
    l1_4_1.pack()
    # 右边输入部分-提示窗口label - l1_4_2
    global var_l142;var_l142=tk.StringVar()  
    var_l142.set(' ')
    l1_4_2 = tk.Label(f1_4_1_r,textvariable=var_l142,height = 1,width = int(2*width_set_l/10)) #  Label宽度会破坏Frame宽度，这里计算出近似代替的宽度
    l1_4_2.pack()
    # 右边输入部分-输入窗口entry - e1_4_2
    global e1_4_2
    e1_4_2 = tk.Entry(f1_4_1_r)
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
        infor[k] = e1_4_2.get()
        true = True
        for i in range(len(infor)-1):
            if infor[i] == False or get_kth_in_line(infor[i],0) == 0:
                true = False
        print(true)
        if true:
            # 先把文件保存到工作区
            winfor = open('./resources/infor_'+infor[0]+'.txt','r') # 文本形式，只读
            wincopy = open('./resources/inforchange.txt','w') # 文本形式，重写模式
            for line in winfor.readlines():
                print(line);wincopy.write(line)
            winfor.close()
            wincopy.close()
            # 在进行文件重写
            wincopy = open('./resources/inforchange.txt','r') # 文本形式，只读
            winfor = open('./resources/infor_'+infor[0]+'.txt','w') # 文本形式，重写模式
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
            # 进入对应功能
            if search_way == '精确搜索':
                information_control_change_precise()
            if search_way == '模糊搜索':
                information_control_change_vague()
            
    # 右边输入部分-删除指定信息
    def infor_control_change_infor_delete():
        global infor,choose_ls
        # 先把文件保存到工作区
        winfor = open('./resources/infor_'+infor[0]+'.txt','r') # 文本形式，只读
        wincopy = open('./resources/inforchange.txt','w') # 文本形式，重写模式
        for line in winfor.readlines():
            print(line)
            wincopy.write(line)
        winfor.close()
        wincopy.close()
        # 再进行文件重写
        wincopy = open('./resources/inforchange.txt','r') # 文本形式，只读
        winfor = open('./resources/infor_'+infor[0]+'.txt','w') # 文本形式，重写模式
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
        # 进入对应功能
        if search_way == '精确搜索':
            information_control_change_precise()
        if search_way == '模糊搜索':
            information_control_change_vague()
        
    # 右边输入部分-按钮button
    b1_4_2 = tk.Button(f1_4_1_r, text=" Next ", width=15, height=2,command=lambda:infor_control_change_infor_next())
    b1_4_2.pack()
    b1_4_3 = tk.Button(f1_4_1_r, text=" Last ", width=15, height=2,command=lambda:infor_control_change_infor_last())
    b1_4_3.pack()
    b1_4_4 = tk.Button(f1_4_1_r, text=" Save ", width=15, height=2,command=lambda:infor_control_change_infor_save())
    b1_4_4.pack()
    b1_4_5 = tk.Button(f1_4_1_r, text="Delete", width=15, height=2,command=lambda:infor_control_change_infor_delete())
    b1_4_5.pack()
    # 左侧搜索区域-搜索框与选择按钮
    global f1_4_1_l_1
    f1_4_1_l_1 = tk.Frame(f1_4_1_l,width = int(width_set_r - width_set_l))
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
    e1_4_1 = tk.Entry(f1_4_1_l_1,textvariable=u1_4_1)  
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
    # 左侧搜索区域-子框架提前布置
    f1_4_1_l_2 = tk.Frame(f1_4_1_l);information_control_change_precise_pre() # 精确搜索和模糊搜索提前安放模板
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
    wtemplate = open('./resources/template.txt','r')
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
    wtemplate = open('./resources/template.txt','r')
    wtemplate.seek(0) #指针回到文件开头
    for line in wtemplate.readlines():
        tname = get_kth_in_line(line,1) # 模板名字
        fname = './resources/infor_'+tname+'.txt' # 文件名字
        length = get_kth_in_line(line,0)
        try:
            number_item = 0
            winfor = open(fname,'r') 
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
    wtemplate = open('./resources/template.txt','r')
    wtemplate.seek(0) #指针回到文件开头
    for line in wtemplate.readlines():
        tname = get_kth_in_line(line,1) # 模板名字
        fname = './resources/infor_'+tname+'.txt' # 文件名字
        length = get_kth_in_line(line,0)
        try:
            number_item = 0
            winfor = open(fname,'r') 
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
    treeview1_4_1_1 = ttk.Treeview(f1_4_1_l_2, height=18, show="headings", columns=columns1_4_1_1)  # 表格
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
    b2_1 = tk.Button(window, text="Back to last level", width=20, height=3,command=lambda:template_control_back())
    b2_2 = tk.Button(window, text="Add       template", width=20, height=3,command=lambda:template_control_add())
    b2_3 = tk.Button(window, text="Check     template", width=20, height=3,command=lambda:template_control_check())
    b2_4 = tk.Button(window, text="Change    template", width=20, height=3,command=lambda:template_control_change())
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
    b2_2_1  = tk.Button(window, text="Back to last level", width=20, height=3,command=lambda:template_control_add_back())
    note.pack()
    b2_2_1.pack()
    # 模板内容输入
    global entry_list; entry_list = [] # 输入框的列表
    global label_list; label_list = [] # 输入框提示符的列表
    f2_2_1 = tk.Frame(window ,width=20, height=2)
    b2_2_2 = tk.Button(f2_2_1, text='Add    Entry', width=10, height=2, command=lambda:template_control_add_Entry())
    b2_2_3 = tk.Button(f2_2_1, text='Reduce Entry', width=10, height=2, command=lambda:template_control_reduce_Entry())
    b2_2_4 = tk.Button(window, text='Save'        , width=20, height=2, command=lambda:template_control_add_save())
    l2_2_1 = tk.Label(window, text="模板名称")
    e2_2_1 = tk.Entry(window)
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
    l_add_item = tk.Label(window, text="item")
    t_add_item = tk.Entry(window)
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
      wtemplate = open('./resources/template.txt','a+') # 文本形式，追加写模式
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
        wtemplate = open('./resources/template.txt','r') 
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
    b2_3_1 = tk.Button(window, text="Back to last level", width=20, height=3,command=lambda:template_control_check_back())
    note.pack()
    b2_3_1.pack()
    # 进入查询部分
    sb2_3_1 = tk.Scrollbar(window)
    sb2_3_1.pack(side="right", fill="y") # 滚动条放在右边，上下填充
    l2_3_1 = tk.Listbox(window, yscrollcommand=sb2_3_1.set)
    wtemplate = open('./resources/template.txt','r') 
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
    template_control_out()
    var.set("TEMPLATE     SYSTEM\n")
    global b2_4_1
    b2_4_1 = tk.Button(window, text="Back to last level", width=20, height=3,command=lambda:template_control_change_back())
    note.pack()
    b2_4_1.pack()
def template_control_change_out(): # 退出
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
    main_out()
    var.set("SETTING    SYSTEM\n")
    global b3_1
    b3_1 = tk.Button(window, text="Back to last level", width=20, height=3,command=lambda:setting_control_back())
    note.pack()
    b3_1.pack()
def setting_control_out():# 退出函数
    note.pack_forget()
    b3_1.pack_forget()
def setting_control_back():# 返回函数 b3_1 按钮
    setting_control_out()
    main()

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
        print("wrong type of k in get_kth_in_line(line,k)")

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
    main()
    window.mainloop()
    pygame.mixer.music.stop()
initial()
start()
