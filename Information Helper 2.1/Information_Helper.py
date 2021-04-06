#!/usr/bin/env python
# -*- coding: utf-8 -*

# Author: Charles Shan <1742861545@qq.com>
#
# (c) 2020
#
# License: GLP

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
    # 数据分析
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
    # 打开图片
from PIL import Image
    # 分词库
import jieba
try:
    jieba.set_dictionary("./resources/system/dict.txt")
    jieba.load_userdict('./resources/system/dict.txt')
    jieba.initialize() # 这两步是为了打包 #http://blog.csdn.net/qq_26376175/article/details/69680992
except:
    print("未进行jiaba库dict设置")
    #make_sure('文件缺失! 无法进行任何内容的模糊搜索!\n请按照system文件夹中dict.txt中的提示进行操作',width=600,height=100,mood=0)# note为提示词语,width为宽,height为长,mood为可选参数 默认为0
    
'''
打包方法：
    第一句: pyinstaller -F Information_Helper.py --noconsole
    打包成一个文件&隐藏窗口.
    -----
    第二句: pyinstaller -F -i tubiao.ico Information_Helper.py --noconsole
    添加图标测试(先进行前边那步, 再进行这一步), 图标的名字是tubiao,类型是.ico文件,大小为16x16,在.py文件同级目录下
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
    ''' Main funtion of Initialization 初始化主函数
    By running once of the function before the program starts to initiallise.
    This is achieved by calling each initialization function sub-function 
    separately, including checking file configuration, reading system Settings, 
    initializing window Settings, loading background music,
    and establishing global variables.
    
    这个函数进行了初始化工作, 在程序开始前运行一遍. 实现的方法是分别调用各个初始化功能子函数. 
    其中包括, 检查文件配置, 对系统设置进行读取, 对窗口设置进行初始化, 加载背景音乐和建立全局变量.
    '''
    #检查文件配置
    ini_check()
    #读取系统设置
    ini_setting_var()
    # 初始化生成窗口
    ini_build_window()
    # 加载背景音乐
    ini_music()
    # 建立变量
    ini_build_var()

def ini_check():# 核查文件是否合格
    ''' Check file configuration 检查文件配置
    Called by the function initial(). It checks the file system level by level 
    from the initial() function and creates it if it does not exist.
    
    由initial()函数调用, 进行文件系统的逐级检查,如果不存在则创建之
    '''
    
    def ini_check_creat_folder(path):
        ''' Check or Create folders 检查或创建文件夹
        Called by the function ini_check(). It checks for a specific folder, 
        or creates a folder if it doesn't exist.
        由ini_check()函数调用, 特定文件夹的检查, 如果文件夹不存在则创建之
        
        :param path: The path to the folder to check 待检查文件夹的路径
        '''
        resources_check = os.path.exists(path)
        print(path+" exist: "+str(resources_check))
        if resources_check:
            pass
        else:
            print('Creating '+path)
            os.mkdir('./'+path) 
                
    def ini_check_creat_files(path,word=''):
        ''' Check or Create a file 检查或创建文件
        Called by the function ini_check(). It checks for a specific file, 
        or creates a file if it doesn't exist.
        由ini_check()函数调用, 特定文件的检查, 如果文件不存在则创建之
        
        :param path: The path to the file to check 待检查文件的路径
        :param word: (optional) What to fill in when creating a file 创建文件时填入的内容      
        '''
        try:
            wtemplate = open(path,'r', encoding='UTF-8') 
            wtemplate.close()
            print(path.split('/')[-1]+" checked successfully!")
        except:
            wtemplate = open(path,'a', encoding='UTF-8') 
            wtemplate.write(word)
            wtemplate.close()
            print(path.split('/')[-1]+" created successfully!")

    # 创建文件时填入的内容 
    setting_txt = 'music  on_or_off  off  \nmusic  name  未设置\ncommon  font  未设置\
    \ncommon  dark_mod  off\nsafe  password  off\nsafe  password  reset\nMe'
    password_txt = 'password  \nmail'
    dict_txt = '!!! Attention !!!\
    \nThe [dict.txt] is missing. You need to download the dict.txt and replace this file with the downloaded one\n\
    \n!!! 注意 !!!\
    \ndict文件缺失! 您需要通过百度网盘下载dict文件并用下载的文件代替本文件\n\
    \n链接:https://pan.baidu.com/s/1G6XmJQZfHANsCZXO6R14XQ  密码:67w0'

    # 进行文件夹与文件的检查(或创建)
    print("开始文件检查!") 
    ini_check_creat_folder(path=r'resources')
    ini_check_creat_folder(path=r'resources/system')
    ini_check_creat_folder(path=r'resources/system/setting')
    ini_check_creat_folder(path=r'resources/system/music')
    ini_check_creat_folder(path=r'resources/system/template')
    ini_check_creat_folder(path=r'resources/user')
    ini_check_creat_folder(path=r'resources/input box')
    ini_check_creat_folder(path=r'resources/picture')
    ini_check_creat_files(path='./resources/system/template/template.txt')   
    ini_check_creat_files(path='./resources/system/template/infor_path.txt')
    ini_check_creat_files(path='./resources/system/dict.txt',word=dict_txt)   
    ini_check_creat_files(path='./resources/system/setting/setting.txt',word=setting_txt)    
    ini_check_creat_files(path='./resources/system/setting/password.txt',word=password_txt)    
    
def ini_setting_var():
    ''' Read system Settings 读取系统设置
    Called by the function initial().
    This function reads sett.txt and sets global variables.
    The current function is to set the color of each component.
    该函数由initial()调用. 本函数读取setting.txt然后进行全局变量的设置.
    目前的功能是进行各个组件的颜色设置.
    
    COLOR_BACK是背景颜色      COLOR_FRONT是字体颜色
    COLOR_SUB是组建背景       COLOR_MB_FRONT是Mac系统的背景颜色
    COLOR_F1_BACK是表格背景色1 COLOR_F2_BACK是表格背景色2  注: 这些颜色的使用以后再捋捋
    COLOR_F2_FRONT表格的字体颜色
    
    功能使用小结:
        Common components :       bg = COLOR_SUB,fg = COLOR_FRONT,
        frame:                    bg = COLOR_BACK,fg = COLOR_FRONT,
        table:                    background = COLOR_F1_BACK;  treeview1_3_c1.tag_configure("ttk",background = COLOR_F1_BACK)# 设置表格颜色1/1
        table Settings in effect: ttk.Style().configure("Treeview", background=COLOR_F2_BACK, foreground=COLOR_F2_FRONT)
    '''
    global COLOR_BACK,COLOR_FRONT,COLOR_SUB# 背景颜色，字体颜色，组件背景
    global COLOR_MB_FRONT # 对Mac的按钮做出的优化
    global COLOR_F1_BACK,COLOR_F2_BACK,COLOR_F2_FRONT #表格的颜色
    
    # 根据是否开启暗黑模式进行颜色的定义
    wsetting = open('./resources/system/setting/setting.txt','r', encoding='UTF-8')
    for line in wsetting.readlines():
        if get_kth_in_line(line,1) == 'common' and get_kth_in_line(line,2) == 'dark_mod':
            if get_kth_in_line(line,3) == 'on': # 需要暗黑模式
                COLOR_BACK = 'dimgray';COLOR_FRONT = 'white';COLOR_SUB = 'black';COLOR_MB_FRONT = 'black'
                COLOR_F1_BACK = 'black';COLOR_F2_BACK = "#383838";COLOR_F2_FRONT = "white"
            else: # 不需要暗黑模式
                COLOR_BACK = 'floralwhite';COLOR_FRONT = 'black';COLOR_SUB = 'floralwhite';COLOR_MB_FRONT = 'black'
                COLOR_F1_BACK = 'floralwhite';COLOR_F2_BACK = "#FFF5EE";COLOR_F2_FRONT = "black"
            break
    wsetting.close()

def ini_build_window():
    ''' Initializes the generation window 初始化生成窗口
    Called by the function initial().This function generates the window,
    defining the window size, title, and background color.
    
    该函数由initial()调用.本函数生成了窗口, 定义了窗口大小,
    标题和背景颜色(背景颜色根据ini_setting_var()函数中获取的信息进行进一步定义)
    '''
    global window
    global width_set; width_set = 800
    window = tk.Tk()                    # 生成窗口变量
    window.geometry("800x550+400+200")  # 大小和位置
    window.title('Information Helper')  #设置窗口标题
    window["background"] = COLOR_BACK
    
def ini_help():
    ''' Guide window 引导窗口
    This function is not developed yet.
    该函数尚未进行开发
    '''
    print("该函数尚未进行开发")
    
def ini_music(ini=True):
    ''' Initialize music related content 进行音乐相关内容初始化
    Called by the function initial().This function is divided 
    into two steps, the first step is to initialize the music 
    directory, the second step is to open or close the music 
    according to the Settings file. Note that you must make 
    sure that the music switch in the Settings file is on to
    successfully turn on the music.
    
    该函数由initial()调用. 本函数分两步,第一步是进行音乐目录的初始化,
    第二步是根据设置文件来进行音乐的开或关. 注意,必须要确定设置文件中
    音乐开关为开才可以成功打开音乐
    
    :param ini:(optional) Whether to update the music catalog 是否进行音乐目录的更新 
    '''
    
    def listdir(path, list_name):
        ''' Gets all audio addresses 获取所有音频地址
        This function adds all audio names to the list recursively
        将所有的音频名称添加到列表中
        
        :param path: Root directory Settings 根目录设置
        :param list_name: The list to add 进行添加的列表
        '''
        for file in os.listdir(path):  
            file_path = os.path.join(path, file)   
            if os.path.splitext(file_path)[1]=='.mp3':  
                if platform.system() == 'Darwin':# for Mac
                    list_name.append(file_path.split('/')[-1])
                elif platform.system() == 'Windows':# for Windows
                    list_name.append(file_path.split("\\")[-1])
    
    def ini_music_once():
        ''' Initialize the music directory 进行音乐目录的初始化
        Called by the function ini_music(), Complete the first step
        of ini_music() - initialize the music directory.
        
        该函数由ini_music()调用.完成ini_music的第一步,进行音乐目录的初始化.
        '''
        print("进入音乐初始化")
        ls = [] ; listdir('./resources/system/music',ls)
        wsetting = open('./resources/system/music/setting_music_name.txt','w', encoding='UTF-8')
        for i in range(len(ls)):
            wsetting.write(ls[i]+'\n')
        wsetting.close()
    
    def ini_music_ifplay():
        ''' Determine if music is needed 判断是否需要播放音乐
        This function is a mandatory feature of the ini_music() function 
        to see if music is allowed to be turned on in the Settings file.
        
        本函数是ini_music()函数的必做功能, 功能是查看设置文件中是否允许开启音乐
        '''
        wsetting = open('./resources/system/setting/setting.txt','r', encoding='UTF-8')
        for line in wsetting.readlines():
            if get_kth_in_line(line,1) == 'music' and get_kth_in_line(line,2) == 'on_or_off' and get_kth_in_line(line,3) == 'on':return True
            else: return False
        wsetting.close()
    
    def ini_music_play():
        ''' Open the music 打开音乐
        Open the selected music in the Settings file. 
        Open successfully and play the music in the single loop mode.
        
        打开设置文件中选择的音乐.打开成功即播放音乐,播放模式为单曲循环
        '''
        print("Play music!")
        wsetting = open('./resources/system/setting/setting.txt','r',encoding='UTF-8') 
        for line in wsetting.readlines():
            if get_kth_in_line(line,1) == 'music' and get_kth_in_line(line,2) == 'name':music_name = get_kth_in_line(line,3)[:-4]+'.mp3';break
        wsetting.close()
        try:
            file=r'./resources/system/music/'+music_name
            pygame.mixer.init()
            pygame.mixer.music.load(file)
            pygame.mixer.music.play(-1)
            print("Staring play music "+music_name)
        except:
            print("Error! Fail to play music! "+music_name)
    
    # 如果是第一次打开, 则进行音乐目录更新的操作
    if ini:
        ini_music_once()
        
    # 进行播放特定音乐
    if ini_music_ifplay():
        ini_music_play()
         
def ini_build_var():
    ''' Regulation parameters and global variables 规定参数与生成全局变量
    内容包括:
        更新infor_path.txt文件
        每页的大标题与标语 var,note,window
        左右框架的宽度 width_set_l,width_set_r
        设置表格颜色 
        定义绘图marker字典与列表 markerdict,markerls
        定义绘图color字典与列表 colordict,colorls
    '''
    # 更新infor_path.txt文件
    Update_infor_path()
    # 这个是note标语和标语的变量
    global var,note,window
    var = tk.StringVar()
    note = tk.Label(window, textvariable=var ,fg = COLOR_FRONT,bg = COLOR_SUB, font=("黑体", 23), width=40, height=3, justify="left", anchor="center")
    # 左右框架的宽度
    global width_set_l;width_set_l = 3/16*width_set
    global width_set_r;width_set_r = 13/16*width_set
    ## 设置表格颜色2/2
    ttk.Style().configure("Treeview", background=COLOR_F2_BACK, foreground=COLOR_F2_FRONT)
    # 定义绘图marker字典
    global markerdict,markerls
    markerdict = {'point':'.', 'pixel':',', 'circle':'o', 'triangle_down':'v', 'triangle_up':'^', 'triangle_left':'<', 'triangle_right':'>',\
                  'tri_down':'1', 'tri_up':'2', 'tri_left':'3', 'tri_right':'4', 'octagon':'8', 'square':'s', 'pentagon':'p', 'star':'*', \
                  'hexagon1':'h', 'hexagon2':'H', 'plus':'+', 'x':'x', 'diamond':'D', 'thin_diamond':'d', 'hline':'_'}
    markerls = ['point','pixel','circle', 'triangle_down', 'triangle_up', 'triangle_left', 'triangle_right',\
                  'tri_down', 'tri_up', 'tri_left', 'tri_right', 'octagon', 'square', 'pentagon', 'star', \
                  'hexagon1', 'hexagon2', 'plus', 'x', 'diamond', 'thin_diamond', 'hline']
    # 定义绘图color字典
    global colordict,colorls
    colordict = {'aliceblue':'#F0F8FF','antiquewhite':'#FAEBD7','aqua':'#00FFFF','aquamarine':'#7FFFD4','azure':'#F0FFFF','beige':'#F5F5DC',\
                 'bisque':'#FFE4C4','black':'#000000','blanchedalmond':'#FFEBCD','blue':'#0000FF','blueviolet':'#8A2BE2','brown':'#A52A2A',\
                 'burlywood':'#DEB887','cadetblue':'#5F9EA0','chartreuse':'#7FFF00','chocolate':'#D2691E','coral':'#FF7F50','cornflowerblue':'#6495ED',\
                 'cornsilk':'#FFF8DC','crimson':'#DC143C','cyan':'#00FFFF','darkblue':'#00008B','darkcyan':'#008B8B','darkgoldenrod':'#B8860B',\
                 'darkgray':'#A9A9A9','darkgreen':'#006400','darkkhaki':'#BDB76B','darkmagenta':'#8B008B','darkolivegreen':'#556B2F',\
                 'darkorange':'#FF8C00','darkorchid':'#9932CC','darkred':'#8B0000','darksalmon':'#E9967A','darkseagreen':'#8FBC8F','darkslateblue':'#483D8B',\
                 'darkslategray':'#2F4F4F','darkturquoise':'#00CED1','darkviolet':'#9400D3','deeppink':'#FF1493','deepskyblue':'#00BFFF',\
                 'dimgray':'#696969','dodgerblue':'#1E90FF','firebrick':'#B22222','floralwhite':'#FFFAF0','forestgreen':'#228B22',\
                 'fuchsia':'#FF00FF','gainsboro':'#DCDCDC','ghostwhite':'#F8F8FF','gold':'#FFD700','goldenrod':'#DAA520','gray':'#808080',\
                 'green':'#008000','greenyellow':'#ADFF2F','honeydew':'#F0FFF0','hotpink':'#FF69B4','indianred':'#CD5C5C','indigo':'#4B0082',\
                 'ivory':'#FFFFF0','khaki':'#F0E68C','lavender':'#E6E6FA','lavenderblush':'#FFF0F5','lawngreen':'#7CFC00','lemonchiffon':'#FFFACD',\
                 'lightblue':'#ADD8E6','lightcoral':'#F08080','lightcyan':'#E0FFFF','lightgoldenrodyellow':'#FAFAD2','lightgreen':'#90EE90',\
                 'lightgray':'#D3D3D3','lightpink':'#FFB6C1','lightsalmon':'#FFA07A','lightseagreen':'#20B2AA','lightskyblue':'#87CEFA',\
                 'lightslategray':'#778899','lightsteelblue':'#B0C4DE','lightyellow':'#FFFFE0','lime':'#00FF00','limegreen':'#32CD32','linen':'#FAF0E6',\
                 'magenta':'#FF00FF','maroon':'#800000','mediumaquamarine':'#66CDAA','mediumblue':'#0000CD','mediumorchid':'#BA55D3',\
                 'mediumpurple':'#9370DB','mediumseagreen':'#3CB371','mediumslateblue':'#7B68EE','mediumspringgreen':'#00FA9A','mediumturquoise':'#48D1CC',\
                 'mediumvioletred':'#C71585','midnightblue':'#191970','mintcream':'#F5FFFA','mistyrose':'#FFE4E1','moccasin':'#FFE4B5','navajowhite':'#FFDEAD',\
                 'navy':'#000080','oldlace':'#FDF5E6','olive':'#808000','olivedrab':'#6B8E23','orange':'#FFA500','orangered':'#FF4500',\
                 'orchid':'#DA70D6','palegoldenrod':'#EEE8AA','palegreen':'#98FB98','paleturquoise':'#AFEEEE','palevioletred':'#DB7093',\
                 'papayawhip':'#FFEFD5','peachpuff':'#FFDAB9','peru':'#CD853F','pink':'#FFC0CB','plum':'#DDA0DD','powderblue':'#B0E0E6',\
                 'purple':'#800080','red':'#FF0000','rosybrown':'#BC8F8F','royalblue':'#4169E1','saddlebrown':'#8B4513','salmon':'#FA8072',\
                 'sandybrown':'#FAA460','seagreen':'#2E8B57','seashell':'#FFF5EE','sienna':'#A0522D','silver':'#C0C0C0','skyblue':'#87CEEB',\
                 'slateblue':'#6A5ACD','slategray':'#708090','snow':'#FFFAFA','springgreen':'#00FF7F','steelblue':'#4682B4','tan':'#D2B48C',\
                 'teal':'#008080','thistle':'#D8BFD8','tomato':'#FF6347','turquoise':'#40E0D0','violet':'#EE82EE','wheat':'#F5DEB3',\
                 'white':'#FFFFFF','whitesmoke':'#F5F5F5','yellow':'#FFFF00','yellowgreen':'#9ACD32'}
    colorls = ['aliceblue','antiquewhite','aqua','aquamarine','azure','beige',\
                 'bisque','black','blanchedalmond','blue','blueviolet','brown',\
                 'burlywood','cadetblue','chartreuse','chocolate','coral','cornflowerblue',\
                 'cornsilk','crimson','cyan','darkblue','darkcyan','darkgoldenrod',\
                 'darkgray','darkgreen','darkkhaki','darkmagenta','darkolivegreen',\
                 'darkorange','darkorchid','darkred','darksalmon','darkseagreen','darkslateblue',\
                 'darkslategray','darkturquoise','darkviolet','deeppink','deepskyblue',\
                 'dimgray','dodgerblue','firebrick','floralwhite','forestgreen',\
                 'fuchsia','gainsboro','ghostwhite','gold','goldenrod','gray',\
                 'green','greenyellow','honeydew','hotpink','indianred','indigo',\
                 'ivory','khaki','lavender','lavenderblush','lawngreen','lemonchiffon',\
                 'lightblue','lightcoral','lightcyan','lightgoldenrodyellow','lightgreen',\
                 'lightgray','lightpink','lightsalmon','lightseagreen','lightskyblue',\
                 'lightslategray','lightsteelblue','lightyellow','lime','limegreen','linen',\
                 'magenta','maroon','mediumaquamarine','mediumblue','mediumorchid',\
                 'mediumpurple','mediumseagreen','mediumslateblue','mediumspringgreen','mediumturquoise',\
                 'mediumvioletred','midnightblue','mintcream','mistyrose','moccasin','navajowhite',\
                 'navy','oldlace','olive','olivedrab','orange','orangered',\
                 'orchid','palegoldenrod','palegreen','paleturquoise','palevioletred',\
                 'papayawhip','peachpuff','peru','pink','plum','powderblue',\
                 'purple','red','rosybrown','royalblue','saddlebrown','salmon',\
                 'sandybrown','seagreen','seashell','sienna','silver','skyblue',\
                 'slateblue','slategray','snow','springgreen','steelblue','tan',\
                 'teal','thistle','tomato','turquoise','violet','wheat',\
                 'white','whitesmoke','yellow','yellowgreen']
    '''
    colorls = ['aliceblue','antiquewhite','aqua','aquamarine','azure','beige',\ # 0 - 5
                 'bisque','black','blanchedalmond','blue','blueviolet','brown',\ # 6 - 11
                 'burlywood','cadetblue','chartreuse','chocolate','coral','cornflowerblue',\ # 12 - 17
                 'cornsilk','crimson','cyan','darkblue','darkcyan','darkgoldenrod',\ # 18 - 23
                 'darkgray','darkgreen','darkkhaki','darkmagenta','darkolivegreen',\ # 24 - 28
                 'darkorange','darkorchid','darkred','darksalmon','darkseagreen','darkslateblue',\ # 29 - 34
                 'darkslategray','darkturquoise','darkviolet','deeppink','deepskyblue',\ # 35 - 39
                 'dimgray','dodgerblue','firebrick','floralwhite','forestgreen',\ # 40 - 44
                 'fuchsia','gainsboro','ghostwhite','gold','goldenrod','gray',\ # 45 - 50
                 'green','greenyellow','honeydew','hotpink','indianred','indigo',\ # 51 - 56
                 'ivory','khaki','lavender','lavenderblush','lawngreen','lemonchiffon',\ # 57 - 62
                 'lightblue','lightcoral','lightcyan','lightgoldenrodyellow','lightgreen',\ # 63 - 67
                 'lightgray','lightpink','lightsalmon','lightseagreen','lightskyblue',\ # 68 - 72
                 'lightslategray','lightsteelblue','lightyellow','lime','limegreen','linen',\ # 73 - 78
                 'magenta','maroon','mediumaquamarine','mediumblue','mediumorchid',\ # 79 - 83
                 'mediumpurple','mediumseagreen','mediumslateblue','mediumspringgreen','mediumturquoise',\ # 84 - 88
                 'mediumvioletred','midnightblue','mintcream','mistyrose','moccasin','navajowhite',\ # 89 - 94
                 'navy','oldlace','olive','olivedrab','orange','orangered',\ # 95 - 100
                 'orchid','palegoldenrod','palegreen','paleturquoise','palevioletred',\ # 101 - 105
                 'papayawhip','peachpuff','peru','pink','plum','powderblue',\ # 106 - 111
                 'purple','red','rosybrown','royalblue','saddlebrown','salmon',\ # 112 - 117
                 'sandybrown','seagreen','seashell','sienna','silver','skyblue',\ # 118 - 123
                 'slateblue','slategray','snow','springgreen','steelblue','tan',\ # 124 - 129
                 'teal','thistle','tomato','turquoise','violet','wheat',\ # 130 - 135
                 'white','whitesmoke','yellow','yellowgreen'] # 136 - 139
    '''
    
def exit_():
    ''' Exit 退出函数
    The main exit before the close action, currently for the close music
    主要进行退出前的关闭动作,目前为关闭音乐
    '''
    print("检查是否关闭音乐")
    wsetting = open('./resources/system/setting/setting.txt','r',encoding='UTF-8')
    for line in wsetting.readlines():
        if get_kth_in_line(line,1) == 'music' and get_kth_in_line(line,2) == 'on_or_off' and get_kth_in_line(line,3) == 'on': 
            musicon = True;break
        else:musicon = False
    wsetting.close()
    if musicon:
        pygame.mixer.music.stop()
        print("Music off")
    else: pass

###############################################################################################################################################
###############################################################################################################################################
'''
主界面
''' 
def main_password():
    ''' password 密码函数
    This function is divided into two parts. First, check whether a 
    password is needed. If so, put the contents of the password part.
    本函数分为两部分,首先检查是否需要密码,如果需要进行密码部分的内容摆放.
    '''
        
    def e0_submit(event):
        ''' Triggered by password entry box enter 由密码输入框回车触发
        First, clear the password input window, and then 
        determine the password input. If the password is
        correct, enter the main interface.
        首先清楚密码输入窗口, 然后对输入的密码进行判断, 密码正确进入主界面
        本函数由 pass_password() 调用.
        '''
        if str(e0.get()) == get_password(): 
            quit_password(); e0.delete(0, tk.END)
        e0.delete(0, tk.END)
    
    def quit_password():
        '''Exit password interface 退出密码界面
        Exit the various components of the password 
        interface and enter the main function.
        退出密码界面的各个组件, 进入到主函数中
        '''
        note.pack_forget() # 退出欢迎标语
        e0.pack_forget()   # 退出密码输入框
        l0.pack_forget()   # 退出密码输入提示
        l00.pack_forget()  # 退出占空行
        b0.pack_forget()   # 退出找回密码按钮
        b0_1.pack_forget() # 退出获取验证码按钮
        e0_1.pack_forget() # 退出输入验证码按钮
        main()
        
    def pass_password():
        ''' Whether to skip the password step 是否跳过密码步骤
        This function checks the Settings file to see if the 
        password is open. If the password is' on ', the password 
        is not skipped, otherwise the password is skipped.
        本函数检查设置文件,查看密码是否打开,如果密码为‘on’则不跳过密码,其他情况均跳过密码!
        '''
        print('进入密码检查')
        wsetting = open('./resources/system/setting/setting.txt','r',encoding='UTF-8')
        for line in wsetting.readlines():
            if get_kth_in_line(line,1) == 'safe' and get_kth_in_line(line,2) == 'password' and (get_kth_in_line(line,3) == 'on' or get_kth_in_line(line,3) == 'off'):break
        wsetting.close()
        if get_kth_in_line(line,3) == 'on': return False
        else: return True
    
    def get_mail():
        '''get mail 获取邮箱
        :return mail: 用户设置的邮箱
        '''
        wsetting = open('./resources/system/setting/password.txt','r',encoding='UTF-8')
        for mail_ in wsetting.readlines():
            if str(get_kth_in_line(mail_,1)) == 'mail' :
                if get_kth_in_line(mail_,2) == "None": mail = None;break
                else: mail = get_kth_in_line(mail_,2);break
        wsetting.close()
        return mail
    
    def find_password():
        ''' Retrieve password 找回密码
        If the user has set up a mailbox, display the 
        components that send the verification code 
        and enter the verification code.
        如果用户设置过邮箱, 显示发送验证码与输入验证码的组件.
        '''
        if get_mail() == None: print("Can‘t find your mail!")
        if get_mail() != None:
            b0_1.pack(side = "right")
            e0_1.pack(fill = 'x')
       
    def e0_1_check_CAPTCHA(event):
        ''' Verification code validates the input 验证码验证输入
        If the user verification code is correct, 
        the prompt for the password is displayed, 
        and then the main function is entered.
        如果用户验证码正确, 显示密码的提示,然后进入主函数.
        '''
        k = str(e0_1.get())
        e0_1.delete(0, tk.END)
        if str(CAPTCHA) == k:
            messagebox.showinfo(title='注意', message='您的密码为:'+get_password()+'\n别再忘了呦')
            quit_password() # 退出现在界面
    
    def pack_items_password():
        ''' Layout password interface 布置密码界面
        This function is the main part of the password section. 
        In this function, firstly, the layout of welcome slogan, 
        password prompt box, password input box and password recovery 
        button is carried out. When the password is recovered, the 
        verification code will be sent to the user's mailbox.
        
        本函数是密码部分的主要部分. 在该函数中,首先进行了欢迎标语,密码提示框,
        密码输入框与找回密码按钮的布置. 找回密码时会向用户的邮箱中发送验证码,
        在指定位置输入验证码正确即可进入程序.
        '''
        # 变量简介与声明变量
        global f0      # 获取验证码按钮的框架
        global e0      # 密码输入框
        global l0      # 密码输入提示
        global l00     # 占空行
        global b0      # 找回密码按钮
        global CAPTCHA # 验证码
        global e0_1    # 验证码输入框
        global b0_1    # 验证码获取按钮
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
        e0.bind("<Return>",e0_submit)
        # 生成验证码
        CAPTCHA = random.randint(100000,999999)
        # 找回密码按钮
        if platform.system() == 'Darwin':# Mac系统
            b0 = tk.Button(window, text='find password', width=15,height=1,fg = COLOR_MB_FRONT,command=lambda:find_password())
        elif platform.system() == 'Windows':# Windows系统
            b0 = tk.Button(window, text='find password', width=15,height=1,fg = COLOR_FRONT,bg = COLOR_SUB,command=lambda:find_password())
        b0.pack()
        # 验证码与获取验证码-按钮
        f0 = tk.Frame(window,bg = COLOR_BACK);f0.pack(fill = 'x')
        if platform.system() == 'Darwin':# Mac系统
            b0_1 = tk.Button(f0,text="获取验证码",width=20, height=1,justify="right",fg = COLOR_MB_FRONT,\
                             command=lambda:sent_message(get_mail(),"验证码为:【"+str(CAPTCHA)+'】.来自Information Helper，为您提供最精致的服务!'))
        elif platform.system() == 'Windows':# Windows系统
            b0_1 = tk.Button(f0,text="获取验证码",width=20, height=1,justify="right",bg = COLOR_SUB,fg = COLOR_FRONT,\
                             command=lambda:sent_message(get_mail(),"验证码为:【"+str(CAPTCHA)+'】.来自Information Helper，为您提供最精致的服务!'))
        e0_1 = tk.Entry(f0,bg = COLOR_F2_BACK,fg = COLOR_FRONT) 
        e0_1.bind("<Return>",e0_1_check_CAPTCHA)  
    
    # 检查是否需要密码
    if pass_password(): main() # 不需要密码
    else: pack_items_password() # 需要密码
    
def main():
    ''' main function 主操作函数
    There are three buttons in the main interface: 
    Information related, template related, and Settings.
    The program is concise and lightweight
    
    主界面中有三个按钮:信息相关,模板相关,设置. 体现了该程序简洁轻量的特点.
    '''
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
    ''' main function out function 主函数退出函数
    Each new interface has a corresponding exit function. 
    This is the exit function of the main interface.
    This function hides the contents of the next screen 
    from all components other than the specified prompt text.
    
    每一个新的界面都有一个对应的退出函数, 这个是主界面的退出函数. 
    该函数的功能是将处指定提示文本外的所有组件隐藏放上下一屏的内容.
    '''
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
    ''' main function of Information Control 信息控制主函数
    This function is a sub-function of main(). 
    It supports adding, modifying, viewing and visualizing information
    
    该函数是main()下级函数. 目前支持信息的添加,修改,查看和数据可视化功能
    '''
    main_out()
    global b1_1,b1_2,b1_3,b1_4,b1_5
    var.set("INFORMATION     SYSTEM\n")
    if platform.system() == 'Darwin':# Mac系统
        b1_1 = tk.Button(window, text="Back to last level", width=20, height=3,fg = COLOR_MB_FRONT, command=lambda:information_control_back())
        b1_2 = tk.Button(window, text="Add    information", width=20, height=3,fg = COLOR_MB_FRONT, command=lambda:information_control_add())
        b1_3 = tk.Button(window, text="Check  information", width=20, height=3,fg = COLOR_MB_FRONT, command=lambda:information_control_check())
        b1_4 = tk.Button(window, text="Change information", width=20, height=3,fg = COLOR_MB_FRONT, command=lambda:information_control_change())
        b1_5 = tk.Button(window, text="Analyse information",width=20, height=3,fg = COLOR_MB_FRONT, command=lambda:information_control_analyse())
    elif platform.system() == 'Windows':# Windows系统
        b1_1 = tk.Button(window, text="Back to last level", width=20, height=3,fg = COLOR_FRONT,bg = COLOR_SUB, command=lambda:information_control_back())
        b1_2 = tk.Button(window, text="Add    information", width=20, height=3,fg = COLOR_FRONT,bg = COLOR_SUB, command=lambda:information_control_add())
        b1_3 = tk.Button(window, text="Check  information", width=20, height=3,fg = COLOR_FRONT,bg = COLOR_SUB, command=lambda:information_control_check())
        b1_4 = tk.Button(window, text="Change information", width=20, height=3,fg = COLOR_FRONT,bg = COLOR_SUB, command=lambda:information_control_change())
        b1_5 = tk.Button(window, text="Analyse information",width=20, height=3,fg = COLOR_FRONT,bg = COLOR_SUB, command=lambda:information_control_analyse())
    note.pack()
    b1_1.pack()
    b1_2.pack()
    b1_3.pack()
    b1_4.pack()
    b1_5.pack()
def information_control_out(): # 退出函数
    ''' Information Control out function 信息主函数退出函数
    This function hides the contents of the next screen 
    from all components other than the specified prompt text.
    
    该函数的功能是将处指定提示文本外的所有组件隐藏放上下一屏的内容.
    '''
    note.pack_forget()
    b1_1.pack_forget()
    b1_2.pack_forget()
    b1_3.pack_forget()
    b1_4.pack_forget()
    b1_5.pack_forget()

#-----------------------------------------------------------------------------------------------------------------------------------------------

def information_control_back(): # 返回函数 b1_1按钮
    ''' Information Control back function 信息主函数返回函数
    This function is called for information_control(),
    The function returns the previous level information_control().
    该函数由information_control()调用,
    功能是返回上一级main().
    '''
    information_control_out()
    main()

#-----------------------------------------------------------------------------------------------------------------------------------------------

def information_control_add(): # 信息添加 b1_2 按钮
    ''' Add information 信息添加 - 逐条添加模式
    The information addition function is divided into 
    two modes: "add item by item" and "add from Excel".
    Enter the function after adding information by default.
    
    信息添加功能分为“逐条添加”与“从excel”添加两种模式,
    进入信息添加功能后默认先进入本函数. 
    '''
    # 把搜做输入框选中内容的函数
    def search(event):#定义的函数在（）内需添加event，要不会报错显示：search函数为给定赋值位置，但有一个值要赋予。
        ''' Select a template 选择模板
        The user selects templates on the left side of 
        the interface. This function can save the latest 
        selection made by the user. 
        Also, after selecting a new template, clear the 
        previous save information and set the input box 
        to the first item.
        
        用户在界面左侧进行模板的选择. 本函数可以保存用户进行的最新选择.
        同时在选择新的模板后清空上次的保存信息并将输入框设置成第一项.
        '''
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
    
    def infor_control_add_infor(n):# 进入第n项
        ''' Prompt to change the input field 改变输入区的提示
        '''
        var_l123.set(get_kth_in_line(choose,n+2))
        
    def infor_control_add_check():
        ''' Print the information used in the inspection 检查时用的信息打印
        Print the input message in a line
        将输入的一条信息在一行print出来.
        '''
        for i in range(get_kth_in_line(choose,0)-1):
            print(infor[i],end=' ')
        print('')
    
    def infor_control_add_infor_next():
        ''' go into the next term 进入下一项
        Clear the input box after saving, and then replace the 
        input box prompt with the title of the next item.
        将输入框中的内容保存后清除, 然后将输入框提示换成下一项的标题
        '''
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
    
    def infor_control_add_infor_last():
        ''' go into the last term 进入上一项
        Clear the input box after saving, and then replace the 
        input box prompt with the title of the last item.
        将输入框中的内容保存后清除, 然后将输入框提示换成上一项的标题
        '''
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
            
    def infor_control_add_infor_save():
        ''' Save the added information 保存添加的信息
        Save the information to the corresponding.txt file
        将信息保存到对应的.txt文件中
        '''
        global infor,k
        # 先把当前界面信息存起来
        infor[k] = e1_2_3.get()
        true = True
        for i in range(get_kth_in_line(choose,0)-1):
            if infor[i] == False or get_kth_in_line(infor[i],0) == 0:
                true = False
        infor_control_add_check()
        if true:
            # winfor = open('./resources/infor_'+infor[0]+'.txt','a+',encoding='UTF-8') # old edition
            winfor = open(find_infor_path(infor[0],True),'a+',encoding='UTF-8') 
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
        # step 2.4 输入区
    var_l123=tk.StringVar()
    if choose == "0:  请选择左侧模板":
        var_l123.set("")
    l1_2_3 = tk.Label(f1_2_4,bg = COLOR_SUB,fg = COLOR_FRONT,textvariable=var_l123)
    l1_2_3.pack(fill = 'x')
    e1_2_3 = tk.Entry(f1_2_4,bg = COLOR_F2_BACK,fg = COLOR_FRONT)
    e1_2_3.pack(fill = 'x')
    if platform.system() == 'Darwin':# Mac系统
        b1_2_3 = tk.Button(f1_2_4, text="Next", width=20, height=2,bg = COLOR_MB_FRONT,\
                           command=lambda:infor_control_add_infor_next())
        b1_2_4 = tk.Button(f1_2_4, text="Last", width=20, height=2,bg = COLOR_MB_FRONT,\
                           command=lambda:infor_control_add_infor_last())
        b1_2_5 = tk.Button(f1_2_4, text="Save", width=20, height=2,bg = COLOR_MB_FRONT,\
                           command=lambda:infor_control_add_infor_save())
    elif platform.system() == 'Windows':# Windows系统
        b1_2_3 = tk.Button(f1_2_4, text="Next", width=20, height=2,bg = COLOR_SUB,fg = COLOR_FRONT,\
                           command=lambda:infor_control_add_infor_next())
        b1_2_4 = tk.Button(f1_2_4, text="Last", width=20, height=2,bg = COLOR_SUB,fg = COLOR_FRONT,\
                           command=lambda:infor_control_add_infor_last())
        b1_2_5 = tk.Button(f1_2_4, text="Save", width=20, height=2,bg = COLOR_SUB,fg = COLOR_FRONT,\
                           command=lambda:infor_control_add_infor_save())
    b1_2_3.pack();b1_2_4.pack();b1_2_5.pack()
    
def information_control_add_out(): # 退出
    ''' Information Adding out function 信息添加函数退出函数
    This function hides the contents of the next screen 
    from all components other than the specified prompt text.
    
    该函数的功能是将处指定提示文本外的所有组件隐藏放上下一屏的内容.
    '''
    f1_2_1.pack_forget()
    f1_2_5.pack_forget()
    note.pack_forget()
    
def information_control_add_back(): # 返回
    ''' Information Add back function 信息主函数返回函数
    This function is called for information_control_add(),
    The function returns the previous level information_control().
    该函数由information_control_add()调用,
    功能是返回上一级information_control().
    '''
    information_control_add_out()
    information_control()

def information_control_add_excel(): # 信息添加 b1_2 按钮_按Excel导入
    ''' Add information 信息添加 - “从excel”添加模式
    The information addition function is divided into 
    two modes: "add item by item" and "add from Excel".
    Enter this mode from the add by item mode.
    
    信息添加功能分为“逐条添加”与“从excel”添加两种模式,
    从逐条添加模式中进入本模式. 
    '''
    def information_control_add_excel_help():
        ''' Make window prompts 进行窗口提示
        Tips for adding information from Excel
        从进行excel添加信息的操作步骤提示
        '''
        messagebox.showinfo(title='注意', message='从Excel添加信息步骤:\n第一步:选择左侧模板\n第二步:\
                            把Excel表格放到input box中\n第三步:输入Excel名字\n第四步:填写待添加信息的左\
                            上角与右上角\n第五步:点击Refresh进行预览\n第六步:点击Insert添加信息')
    
    def information_control_add_excel_return_item(table,row,line):
        name = table.cell_value(row, line)
        word_type = table.cell_type(row, line)
        # print(name,"  ", word_type)
        if word_type == 0:    #空0
            name = "-"
        elif word_type == 1:  #字符串1
            name = name
        elif word_type == 2 and name%1==0:  #数字2
            name = int(name)
        elif word_type == 3:  #日期3
            date_value = xlrd.xldate_as_tuple(name,0)
            try:
                name = datetime(*date_value).strftime('%Y/%m/%d %H:%M:%S')
                if(date_value[3]==0,date_value[4]==0,date_value[5]==0):
                    name = name.split(" ")[0]
            except:
                name = datetime(2000,1,1,date_value[3],date_value[4],date_value[5]).strftime('%Y/%m/%d %H:%M:%S')
                name = name.split(" ")[1]
        elif word_type == 4:  #布尔4
            name = True if name == 1 else False
        elif word_type == 5:  #error 5
            name = 'error'
        return name
    
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
        #wtemplate = open('./resources/system/template/template.txt','r',encoding='UTF-8') 
        # 填写预览表格
        excel_name = e1_2_5.get() # 表格名字
        from_row = int(e1_2_1.get());from_line = int(e1_2_2.get()) # 左上角
        to_row = int(e1_2_3.get());to_line = int(e1_2_4.get()) # 右上角
        roop1 = to_row - from_row +1
        roop2 = to_line - from_line +1
        data = xlrd.open_workbook(r'./resources/input box/'+excel_name+'.xlsx')
        table = data.sheets()[0]          #通过索引顺序获取
        #names = data.sheet_names()    #返回book中所有工作表的名字
        
        length = get_kth_in_line(choose,0)
        if length-2 == roop2:
            template = '-'
            for i in range(roop1):
                for count in range(20):
                    if count < roop2:
                        row = from_row+i-1
                        line = from_line+count-1
                        item1_3_c1_e[count] = information_control_add_excel_return_item(table,row,line)
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
        #names = data.sheet_names()    #返回book中所有工作表的名字
        #length = get_kth_in_line(choose,0)
        # 写入txt
        #winfor = open('./resources/infor_'+template_name+'.txt','a+',encoding='UTF-8') # old edition
        winfor = open(find_infor_path(template_name,True),'a+',encoding='UTF-8') 
        #if length-2 == roop2:
        for i in range(roop1):
            winfor.write(template_name+"  ")
            for j in range(roop2):
                row = from_row+i-1
                line = from_line+j-1       
                winfor.write(str(information_control_add_excel_return_item(table,row,line)) + "  ")
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
    f1_2_5_e = tk.Frame(f1_2_3_e,bg = COLOR_BACK)# 创建右侧左
    f1_2_6_e = tk.Frame(f1_2_3_e,bg = COLOR_BACK,width = int(width_set_l/2))# 创建右侧右
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
    Update_infor_path() # 更新infor_path.txt文件
    for i in range(18): # 占空行
        treeview1_3_c1.insert('', 0, values=('','','','','','','','','','','','','','','','','','','','',''))
    wtemplate = open('./resources/system/template/template.txt','r',encoding='UTF-8') 
    for line in wtemplate.readlines():
        tname = get_kth_in_line(line,1) # 模板名字
        # fname = './resources/infor_'+tname+'.txt' # 文件名字 old edition
        fname = find_infor_path(tname) # 文件名字
        length = get_kth_in_line(line,0)
        try:
            number_item = 0
            Update_infor_path()# 更新一遍 infor_path.txt
            winfor = open(fname,'r',encoding='UTF-8') 
            #winfor = open('./resources/user/日常生活/infor_名片.txt','r',encoding='UTF-8') 
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
            print ("File is not accessible.")
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
    # 计算文件名并更新infor_path.txt
    #fname1_3_2 = './resources/infor_'+tname+'.txt' # 文件名字 old edition
    fname1_3_2 = find_infor_path(tname)# 文件名字
    Update_infor_path()
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
    f1_3_c2_1 = tk.Frame(f1_3_c2,bg = COLOR_BACK,width = int(width_set_l))
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
        #global search_last
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
        # 更新infor_path.txt
        Update_infor_path()
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
        # fname = './resources/infor_'+tname+'.txt' # 文件名字 old edition
        fname = find_infor_path(tname)
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
    print(search_word)
    search_word_ls = list(jieba.lcut(search_word))
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
        # fname = './resources/infor_'+tname+'.txt' # 文件名字 old edition
        fname = find_infor_path(tname) # 文件名字
        length = get_kth_in_line(line,0)
        try:
            winfor = open(fname,'r',encoding='UTF-8') 
            number_item = 0
            if_print_all = False #是否全模板打印
            if_print_title = False#是否打印模板题目
            for i in range(length):
                for j in range(len(search_word_ls)):
                    to_be_searched_ls = list(jieba.lcut(str(get_kth_in_line(line,i+1))))
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
                            to_be_searched_ls = list(jieba.lcut(str(get_kth_in_line(fline,j+1))))
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
def information_control_check3_internet_pre(): # 联网搜索提前准备的模板
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
        if true:
            # 先把文件保存到工作区
            # winfor = open('./resources/infor_'+infor[0]+'.txt','r',encoding='UTF-8') # 文本形式，只读 old edition
            winfor = open(find_infor_path(infor[0]),'r',encoding='UTF-8') # 文本形式，只读
            wincopy = open('./resources/system/inforchange.txt','w',encoding='UTF-8') # 文本形式，重写模式
            for line in winfor.readlines():
                wincopy.write(line)
            winfor.close()
            wincopy.close()
            # 在进行文件重写
            wincopy = open('./resources/system/inforchange.txt','r',encoding='UTF-8') # 文本形式，只读
            # winfor = open('./resources/infor_'+infor[0]+'.txt','w',encoding='UTF-8') # 文本形式，重写模式 old edition
            winfor = open(find_infor_path(infor[0]),'w',encoding='UTF-8') # 文本形式，重写模式
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
        # winfor = open('./resources/infor_'+infor[0]+'.txt','r',encoding='UTF-8') # 文本形式，只读 old edition
        winfor = open(find_infor_path(infor[0]),'r',encoding='UTF-8') # 文本形式，只读
        wincopy = open('./resources/system/inforchange.txt','w',encoding='UTF-8') # 文本形式，重写模式
        for line in winfor.readlines():
            wincopy.write(line)
        winfor.close()
        wincopy.close()
        # 再进行文件重写
        wincopy = open('./resources/system/inforchange.txt','r',encoding='UTF-8') # 文本形式，只读
        # winfor = open('./resources/infor_'+infor[0]+'.txt','w',encoding='UTF-8') # 文本形式，重写模式 old edition
        winfor = open(find_infor_path(infor[0]),'w',encoding='UTF-8') # 文本形式，重写模式
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
    if platform.system() == 'Darwin':# for Mac
        b1_4_2 = tk.Button(f1_4_1_r, text=" Next ", width=15, height=2,fg = COLOR_MB_FRONT,command=lambda:infor_control_change_infor_next())
        b1_4_3 = tk.Button(f1_4_1_r, text=" Last ", width=15, height=2,fg = COLOR_MB_FRONT,command=lambda:infor_control_change_infor_last())
        b1_4_4 = tk.Button(f1_4_1_r, text=" Save ", width=15, height=2,fg = COLOR_MB_FRONT,command=lambda:infor_control_change_infor_save())
        b1_4_5 = tk.Button(f1_4_1_r, text="Delete", width=15, height=2,fg = COLOR_MB_FRONT,command=lambda:infor_control_change_infor_delete())
    elif platform.system() == 'Windows':# for Windows
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
        # 更新infor_path.txt
        Update_infor_path()
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
        # fname = './resources/infor_'+tname+'.txt' # 文件名字 old edition
        fname = find_infor_path(tname)
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
        # fname = './resources/infor_'+tname+'.txt' # 文件名字 old edition
        fname = find_infor_path(tname)
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

#-----------------------------------------------------------------------------------------------------------------------------------------------

def information_control_analyse(): # 数据分析 b1_5 按钮
    def infor_analyse_plot():
        plt.rcParams['font.sans-serif'] = ['SimHei']
        plt.rcParams['axes.unicode_minus'] = False
        #例子
        #x = np.array([137.97, 104.50, 100.00, 124.32, 79.20, 99.00, 124.00, 114.00, 106.69, 138.05, 53.75, 46.91, 68.00, 63.02, 81.26, 86.21])
        #y =  np.array([145.00, 110.00, 93.00, 116.00, 65.32, 104.00, 118.00, 91.00, 62.00, 133.00, 51.00, 45.00, 78.50, 69.65, 75.69, 95.30])
        #plt.figure()
        #plt.scatter(x,y,color='red',label="销售记录")
        #plt.xlabel('面积(平方米)',fontsize=14)
        #plt.ylabel('价格(万元)',fontsize=14)
        #plt.xlim((40,150))
        #plt.ylim((40,150))
        #plt.suptitle("商品房价格模型",fontsize=20)
        #plt.legend(loc="upper left")
        #plt.savefig('./resources/picture/test.jpg')
        #plt.show()
        #image1 = Image.open('./resources/picture/test.jpg')
        #image1.show()
        
        # y
        y_name = c1_5_9.get()
        y_type = c1_5_3.get()
        if y_type == 'int':
            try:
                # winfor = open('./resources/infor_'+choose_name+'.txt','r',encoding='UTF-8') # old edition
                winfor = open(find_infor_path(choose_name),'r',encoding='UTF-8')
                ylist = []
                yselect = c1_5_2.current()
                for readline in winfor.readlines():
                    ylist.append(int(get_kth_in_line(readline,yselect+2)))
                    print(int(get_kth_in_line(readline,yselect+2)))
                winfor.close()
                y = np.array(ylist)
            except IOError:
                pass
        if y_type == 'float':
            try:
                # winfor = open('./resources/infor_'+choose_name+'.txt','r',encoding='UTF-8') # old edition
                winfor = open(find_infor_path(choose_name),'r',encoding='UTF-8')
                ylist = []
                yselect = c1_5_2.current()
                for readline in winfor.readlines():
                    ylist.append(float(get_kth_in_line(readline,yselect+2)))
                winfor.close()
                y = np.array(ylist)
            except IOError:
                pass
        if y_type == 'String':
            try:
                # winfor = open('./resources/infor_'+choose_name+'.txt','r',encoding='UTF-8') # old edition
                winfor = open(find_infor_path(choose_name),'r',encoding='UTF-8')
                ylist = []
                yselect = c1_5_2.current()
                for readline in winfor.readlines():
                    ylist.append(get_kth_in_line(readline,yselect+2))
                winfor.close()
                y = np.array(ylist)
            except IOError:
                pass
        # x
        x_name = c1_5_a.get()
        x_type = c1_5_5.get()
        if x_type == 'int':
            try:
                # winfor = open('./resources/infor_'+choose_name+'.txt','r',encoding='UTF-8') # old edition
                winfor = open(find_infor_path(choose_name),'r',encoding='UTF-8')
                xlist = []
                xselect = c1_5_4.current()
                for readline in winfor.readlines():
                    xlist.append(int(get_kth_in_line(readline,xselect+2)))
                winfor.close()
                x = np.array(xlist)
            except IOError:
                pass
        if x_type == 'float':
            try:
                # winfor = open('./resources/infor_'+choose_name+'.txt','r',encoding='UTF-8') # old edition
                winfor = open(find_infor_path(choose_name),'r',encoding='UTF-8')
                xlist = []
                xselect = c1_5_4.current()
                for readline in winfor.readlines():
                    xlist.append(float(get_kth_in_line(readline,xselect+2)))
                winfor.close()
                x = np.array(xlist)
            except IOError:
                pass
        if x_type == 'String':
            try:
                # winfor = open('./resources/infor_'+choose_name+'.txt','r',encoding='UTF-8') # old edition
                winfor = open(find_infor_path(choose_name),'r',encoding='UTF-8')
                xlist = []
                xselect = c1_5_4.current()
                for readline in winfor.readlines():
                    xlist.append(get_kth_in_line(readline,xselect+2))
                winfor.close()
                x = np.array(xlist)
            except IOError:
                pass
        if c1_5_1.get() == '2D figure':
            # plot
            plt.figure()
            print(c1_5_c.current())
            plt.scatter(x,y,color=c1_5_i.get(),marker=markerdict[c1_5_c.get()],label="")        # 颜色 样式 以后进行用户设置
            plt.xlabel(x_name,fontsize=14)
            plt.ylabel(y_name,fontsize=14)
            #plt.xlim((40,150))
            #plt.ylim((40,150))
            suptitle_name = c1_5_8.get()
            plt.suptitle(suptitle_name,fontsize=20)           # 表格名字提供用户设置
            #plt.legend(loc="upper left")
            plt.savefig('./resources/picture/'+suptitle_name+'.jpg')
            plt.show()
            image1 = Image.open('./resources/picture/'+suptitle_name+'.jpg')
            image1.show()
        if c1_5_1.get() == '3D figure':
            # x2
            x2_name = c1_5_b.get()
            x2_type = c1_5_7.get()
            if x2_type == 'int':
                try:
                    # winfor = open('./resources/infor_'+choose_name+'.txt','r',encoding='UTF-8') # old edition
                    winfor = open(find_infor_path(choose_name),'r',encoding='UTF-8')
                    x2list = []
                    x2select = c1_5_6.current()
                    for readline in winfor.readlines():
                        x2list.append(int(get_kth_in_line(readline,x2select+2)))
                    winfor.close()
                    x2 = np.array(x2list)
                except IOError:
                    pass
            if x2_type == 'float':
                try:
                    # winfor = open('./resources/infor_'+choose_name+'.txt','r',encoding='UTF-8') # old edition
                    winfor = open(find_infor_path(choose_name),'r',encoding='UTF-8')
                    x2list = []
                    x2select = c1_5_6.current()
                    for readline in winfor.readlines():
                        x2list.append(float(get_kth_in_line(readline,x2select+2)))
                    winfor.close()
                    x2 = np.array(x2list)
                except IOError:
                    pass
            if x2_type == 'String':
                try:
                    # winfor = open('./resources/infor_'+choose_name+'.txt','r',encoding='UTF-8') # old edition
                    winfor = open(find_infor_path(choose_name),'r',encoding='UTF-8')
                    x2list = []
                    x2select = c1_5_6.current()
                    for readline in winfor.readlines():
                        x2list.append(get_kth_in_line(readline,x2select+2))
                    winfor.close()
                    x2 = np.array(x2list)
                except IOError:
                    pass
            fig = plt.figure()
            ax3d = Axes3D(fig)
            ax3d.scatter(x,x2,y,color=c1_5_i.get(),marker=markerdict[c1_5_c.get()], label='')
            ax3d.set_xlabel(x_name,color='b', fontsize=14)
            ax3d.set_ylabel(x2_name,color='b', fontsize=14)
            ax3d.set_zlabel(y_name,color='b', fontsize=14)
            ax3d.set_yticks([1,2,3])
            suptitle_name = c1_5_8.get()
            plt.suptitle(suptitle_name,fontsize=20)
            #plt.legend(loc="upper left")
            plt.savefig('./resources/picture/'+suptitle_name+'.jpg')
            plt.show()
            image1 = Image.open('./resources/picture/'+suptitle_name+'.jpg')
            image1.show()
        
    def infor_analyse_2D3D(event):
        ''' 2D3D mode layout transformation 2D3D模式布局转换
        This function changes the layout on the interface by identifying 
        whether the mode you are entering is 2D mode or 3D mode (2D mode 
        for two variables and 3D mode for three variables).
        
        该函数通过识别将要进入的模式是2D模式还是3D模式(2D模式指两个变量,
        3D模式指三个变量),来更改界面上的布局
        '''
        if(c1_5_1.get() == '2D figure'):
            f1_5_2r_r_6.pack_forget();c1_5_6.pack_forget();lc1_5_6.pack_forget()
            f1_5_2r_r_7.pack_forget();c1_5_7.pack_forget();lc1_5_7.pack_forget()
        if(c1_5_1.get() == '3D figure'):
            b1_5_3.pack_forget();b1_5_4.pack_forget()
            f1_5_2r_r_6.pack();c1_5_6.pack(side = 'right');lc1_5_6.pack(side = 'right') 
            f1_5_2r_r_7.pack();c1_5_7.pack(side = 'right');lc1_5_7.pack(side = 'right') 
            b1_5_3.pack();b1_5_4.pack()

    def infor_analyse_search(event):
        global choose
        global var_l151
        choose = L1_5_1.get(L1_5_1.curselection())
        tname = get_kth_in_line(choose,2)
        var_l151.set(tname)
        global choose_ls,choose_name
        choose_ls = []  # 被选中的模板的全部信息
        choose_name = get_kth_in_line(choose,2) # 被选中的模板的名字
        readtamplate = open('./resources/system/template/template.txt','r',encoding='UTF-8')
        for line in readtamplate.readlines():
            if get_kth_in_line(line,1) == choose_name: 
                number = get_kth_in_line(line,0);break
        readtamplate.close()
        for i in range(number):
            choose_ls.append(get_kth_in_line(line,i+1))
        c1_5_2['values'] = (choose_ls[1:])     # 设置下拉列表的值
        c1_5_2.current(0)    # 设置下拉列表默认显示的值
        c1_5_4['values'] = (choose_ls[1:])     # 设置下拉列表的值
        c1_5_4.current(0)    # 设置下拉列表默认显示的值
        c1_5_6['values'] = (choose_ls[1:])     # 设置下拉列表的值
        c1_5_6.current(0)    # 设置下拉列表默认显示的值
        # 显示当前所选模板的信息
        global treeview1_5_1
            # 删除残留的信息
        x=treeview1_5_1.get_children()
        for j in x:
            treeview1_5_1.delete(j)
            # 重新生成表头
        for count in range(number-1):
            treeview1_5_1.heading(columns1_5_1[count], text=choose_ls[count+1])
        for count in range(21-number):
            treeview1_5_1.heading(columns1_5_1[count+number-1], text=str(count+number))       
            # 填写表格内容
                # 占空行
        item = []
        for i in range(20):
            item.append('')
        for i in range(36):
            treeview1_5_1.insert('', 0, values='')
                # 填内容
        try:
            # winfor = open('./resources/infor_'+choose_name+'.txt','r',encoding='UTF-8') # old edition
            winfor = open(find_infor_path(choose_name),'r',encoding='UTF-8')
            print("打开成功")
            for readline in winfor.readlines():
                item = []
                for i in range(number-1):
                    item.append(get_kth_in_line(readline,i+2))
                treeview1_5_1.insert('', 0, values=item)
            winfor.close()
        except IOError:
            pass
        
    def infor_analyse_plot_to_setting(): # 在plot模式下, 切换到设置界面的函数
        # 首先进行输入框信息的保存
        global plot_ls; plot_ls = []
        global plot_ls_c;plot_ls_c=[]
        plot_ls.append(c1_5_1.current());plot_ls_c.append(c1_5_1.get()) # 2D/3D
        plot_ls.append(c1_5_2.current());plot_ls_c.append(c1_5_2.get()) # y
        plot_ls.append(c1_5_3.current());plot_ls_c.append(c1_5_3.get()) # y type
        plot_ls.append(c1_5_4.current());plot_ls_c.append(c1_5_4.get()) # x1
        plot_ls.append(c1_5_5.current());plot_ls_c.append(c1_5_5.get()) # x1 type
        plot_ls.append(c1_5_6.current());plot_ls_c.append(c1_5_6.get()) # x2
        plot_ls.append(c1_5_7.current());plot_ls_c.append(c1_5_7.get()) # x2 type
        print(plot_ls)
        print(plot_ls_c)
        # 进行绘图操作的隐藏
        f1_5_2r_r_1.pack_forget();c1_5_1.pack_forget();lc1_5_1.pack_forget() # 2D/3D
        f1_5_2r_r_2.pack_forget();c1_5_2.pack_forget();lc1_5_2.pack_forget() # y
        f1_5_2r_r_3.pack_forget();c1_5_3.pack_forget();lc1_5_3.pack_forget() # y type
        f1_5_2r_r_4.pack_forget();c1_5_4.pack_forget();lc1_5_4.pack_forget() # x1
        f1_5_2r_r_5.pack_forget();c1_5_5.pack_forget();lc1_5_5.pack_forget() # x1 type
        if plot_ls_c[0] == '3D figure':
            f1_5_2r_r_6.pack_forget();c1_5_6.pack_forget();lc1_5_6.pack_forget() # x2
            f1_5_2r_r_7.pack_forget();c1_5_7.pack_forget();lc1_5_7.pack_forget() # x2 type  
        b1_5_3.pack_forget();b1_5_4.pack_forget()                            # 绘图按钮与进入设置按钮
        # 进行绘图设置的摆放
        f1_5_2r_r_8.pack();c1_5_8.pack(side = 'right');lc1_5_8.pack(side = 'right')           # 大标题
        c1_5_8.delete(0,tk.END);c1_5_8.insert(0, choose_name+'信息分析')
        f1_5_2r_r_9.pack();c1_5_9.pack(side = 'right');lc1_5_9.pack(side = 'right')           # y标题
        c1_5_9.delete(0,tk.END);c1_5_9.insert(0,plot_ls_c[1])
        f1_5_2r_r_a.pack();c1_5_a.pack(side = 'right');lc1_5_a.pack(side = 'right')           # x1标题
        c1_5_a.delete(0,tk.END);c1_5_a.insert(0,plot_ls_c[3])
        if plot_ls_c[0] == '3D figure':
            f1_5_2r_r_b.pack();c1_5_b.pack(side = 'right');lc1_5_b.pack(side = 'right')       # x2标题  
            c1_5_b.delete(0,tk.END);c1_5_b.insert(0,plot_ls_c[5])
        f1_5_2r_r_c.pack();c1_5_c.pack(side = 'right');lc1_5_c.pack(side = 'right')           # marker      
        f1_5_2r_r_i.pack();c1_5_i.pack(side = 'right');lc1_5_i.pack(side = 'right')           # point color
        b1_5_5.pack()  
    
    def infor_analyse_setting_to_plot(): # 在plot模式下, 从设置界面切换回plot内容选择
        # 首先进行输入框信息的保存
        global plot_ls_set; plot_ls_set = []
        global plot_ls_c_set;plot_ls_set=[]
        #plot_ls.append(c1_5_1.current());plot_ls_c.append(c1_5_1.get()) # 2D/3D
        #plot_ls.append(c1_5_2.current());plot_ls_c.append(c1_5_2.get()) # y
        #plot_ls.append(c1_5_3.current());plot_ls_c.append(c1_5_3.get()) # y type
        #plot_ls.append(c1_5_4.current());plot_ls_c.append(c1_5_4.get()) # x1
        #plot_ls.append(c1_5_5.current());plot_ls_c.append(c1_5_5.get()) # x1 type
        #plot_ls.append(c1_5_6.current());plot_ls_c.append(c1_5_6.get()) # x2
        #plot_ls.append(c1_5_7.current());plot_ls_c.append(c1_5_7.get()) # x2 type
        #print(plot_ls)
        #print(plot_ls_c)
        # 进行绘图设置的隐藏
        f1_5_2r_r_8.pack_forget();c1_5_8.pack_forget();lc1_5_8.pack_forget() # 大标题
        f1_5_2r_r_9.pack_forget();c1_5_9.pack_forget();lc1_5_9.pack_forget() # y标题
        f1_5_2r_r_a.pack_forget();c1_5_a.pack_forget();lc1_5_a.pack_forget() # x1标题
        if plot_ls_c[0] == '3D figure':
            f1_5_2r_r_b.pack_forget();c1_5_b.pack_forget();lc1_5_b.pack_forget() # x2标题
        f1_5_2r_r_c.pack_forget();c1_5_c.pack_forget();lc1_5_c.pack_forget() # x1 marker
        f1_5_2r_r_i.pack_forget();c1_5_i.pack_forget();lc1_5_i.pack_forget() # point color
        b1_5_5.pack_forget()
        # 进行绘图设置的摆放
        f1_5_2r_r_1.pack();c1_5_1.pack(side = 'right');lc1_5_1.pack(side = 'right')
        f1_5_2r_r_2.pack();c1_5_2.pack(side = 'right');lc1_5_2.pack(side = 'right')
        f1_5_2r_r_3.pack();c1_5_3.pack(side = 'right');lc1_5_3.pack(side = 'right')
        f1_5_2r_r_4.pack();c1_5_4.pack(side = 'right');lc1_5_4.pack(side = 'right')
        f1_5_2r_r_5.pack();c1_5_5.pack(side = 'right');lc1_5_5.pack(side = 'right')
        if plot_ls_c[0] == '3D figure':
            f1_5_2r_r_6.pack();c1_5_6.pack(side = 'right');lc1_5_6.pack(side = 'right') # x2
            f1_5_2r_r_7.pack();c1_5_7.pack(side = 'right');lc1_5_7.pack(side = 'right') # x2 dtype
        b1_5_3.pack();b1_5_4.pack()

        #1 惯例操作
    information_control_out()
    var.set("INFORMATION     SYSTEM\n")
    global b1_5_1,b1_5_2,f1_5_0    
    f1_5_0 = tk.Frame(window ,width=20, height=2)
    if platform.system() == 'Darwin':# Mac系统
        b1_5_1 = tk.Button(f1_5_0, text="Back", width=10, height=2,fg = COLOR_MB_FRONT,command=lambda:information_control_analyse_back())
        b1_5_2 = tk.Button(f1_5_0, text="Predict", width=10, height=2,fg = COLOR_MB_FRONT,command=lambda:information_control_analyse_predict())
    elif platform.system() == 'Windows':# Windows系统
        b1_5_1 = tk.Button(f1_5_0, text="Back", width=10, height=2,bg = COLOR_SUB,fg = COLOR_FRONT,command=lambda:information_control_analyse_back())
        b1_5_2 = tk.Button(f1_5_0, text="Predict", width=10, height=2,fg = COLOR_FRONT,bg = COLOR_SUB,command=lambda:information_control_analyse_predict())
    note.pack();f1_5_0.pack()
    b1_5_2.pack(side='right')
    b1_5_1.pack(side='right')

        #2 框架设置
            #2.1 整体框架 f1_5_1
    global f1_5_1 
    f1_5_1 = tk.Frame(window,bg = COLOR_BACK)
    f1_5_1.pack(fill = 'both',expand = True)
            #2.2 左侧主框架 f1_5_1l
    global width_set_l,f1_5_1l
    f1_5_1l = tk.Frame(f1_5_1,bg = COLOR_BACK,width = width_set_l)
    f1_5_1l.pack(side = 'left',fill = 'y')
            #2.3 左侧滚动条与选择栏
    global sb1_5_1,L1_5_1
    sb1_5_1 = tk.Scrollbar(f1_5_1l)
    sb1_5_1.pack(side=tk.RIGHT,fill='y')
    L1_5_1 = tk.Listbox(f1_5_1l,bg = COLOR_F2_BACK,fg = COLOR_F2_FRONT, yscrollcommand=sb1_5_1.set)
    L1_5_1.bind('<ButtonRelease-1>',infor_analyse_search)
    L1_5_1.pack(side=tk.RIGHT,fill='both')
            #2.4 右侧主框架 f1_5_1r
    global f1_5_1r
    f1_5_1r = tk.Frame(f1_5_1,bg = COLOR_BACK)# 先创建右侧最大框架
    f1_5_1r.pack(expand = True,fill = 'both',side = 'left')     
            #2.5 右侧数据分析模版选择
    global choose,var_l151,l1_5_1;choose = '0:  请选择左侧模板'
    var_l151=tk.StringVar()
    var_l151.set(get_kth_in_line(choose,2))
    l1_5_1 = tk.Label(f1_5_1r,textvariable=var_l151,bg = COLOR_SUB,fg = COLOR_FRONT,justify="left", anchor="center",height = 1)
    l1_5_1.pack(fill = 'x')
            #2.6 数据分析结果-右侧次级框架 f1_5_2r, f1_5_2r_r, f1_5_2r_l
    global f1_5_2r,f1_5_2r_r,f1_5_2r_l
    f1_5_2r = tk.Frame(f1_5_1r,bg = COLOR_BACK) # 右侧最大框架
    f1_5_2r_l = tk.Frame(f1_5_2r,bg = COLOR_BACK)# 创建右侧左
    f1_5_2r_r = tk.Frame(f1_5_2r,bg = COLOR_BACK,width = int(width_set_l/2))# 创建右侧右
    f1_5_2r.pack(expand = True,fill = 'both',side = 'left') # 右侧最大框架
    f1_5_2r_r.pack(expand = True,fill = 'both',side = 'right') # 右侧左
    f1_5_2r_l.pack(expand = True,fill = 'both',side = 'right') # 右侧右

        #3 左侧模板选择内容
    L1_5_1.delete(0, tk.END)
    wtemplate = open('./resources/system/template/template.txt','r',encoding='UTF-8') 
    count = 1
    for line in wtemplate.readlines():
        L1_5_1.insert("end", str(count)+":  "+get_kth_in_line(line,1))
        L1_5_1.pack(fill="both",side= "top", expand = True )
        sb1_5_1.config(command=L1_5_1.yview)
        count = count+1
    wtemplate.close()

        #4 右侧组件
            #4.1 声明变量
    global choose_name;choose_name = ''
    global plot_ls;                   # 输入框信息的保存(在进行自定义设置时用)
    global b1_5_3                     # 生成图
    global b1_5_4                     # 更多设置
    global f1_5_2r_r_1,c1_5_1,lc1_5_1 # 设置绘图模式
    global f1_5_2r_r_2,c1_5_2,lc1_5_2 # 选择y
    global f1_5_2r_r_3,c1_5_3,lc1_5_3 # 选择y的数据类型
    global f1_5_2r_r_4,c1_5_4,lc1_5_4 # 选择x1
    global f1_5_2r_r_5,c1_5_5,lc1_5_5 # 选择x1的数据类型
    global f1_5_2r_r_6,c1_5_6,lc1_5_6 # 选择x2          # x2只在绘制3D图像时有
    global f1_5_2r_r_7,c1_5_7,lc1_5_7 # 选择x2的数据类型   
    global choose_ls; choose_ls = ['0','请选择左侧模板'] # 被选中的模板的全部信息
            #4.2 选择绘图模式
    f1_5_2r_r_1 = tk.Frame(f1_5_2r_r,bg = COLOR_BACK,width = int(width_set_l/2))# 先创建右侧右
    f1_5_2r_r_1.pack()
    c1_5_1 = ttk.Combobox(f1_5_2r_r_1, width=15)
    c1_5_1['values'] = ('2D figure','3D figure')     # 设置下拉列表的值
    c1_5_1.current(1)    # 设置下拉列表默认显示的值
    c1_5_1.configure(state="readonly") # 不可编辑
    c1_5_1.pack(side = 'right')
    lc1_5_1 = tk.Label(f1_5_2r_r_1,text='    Mood:  ',bg = COLOR_BACK,width=10)
    lc1_5_1.pack(side = 'right')
    c1_5_1.bind("<<ComboboxSelected>>",infor_analyse_2D3D)
            #4.3 选择y
    f1_5_2r_r_2 = tk.Frame(f1_5_2r_r,bg = COLOR_BACK,width = int(width_set_l/2))# 先创建右侧右
    f1_5_2r_r_2.pack()
    c1_5_2 = ttk.Combobox(f1_5_2r_r_2, width=15)
    c1_5_2['values'] = (choose_ls[1:])     # 设置下拉列表的值
    c1_5_2.current(0)    # 设置下拉列表默认显示的值
    c1_5_2.configure(state="readonly") # 不可编辑
    c1_5_2.pack(side = 'right')
    lc1_5_2 = tk.Label(f1_5_2r_r_2,text='      y:  ',bg = COLOR_BACK,width=10)
    lc1_5_2.pack(side = 'right')   
            #4.4 选择y的数据类型
    f1_5_2r_r_3 = tk.Frame(f1_5_2r_r,bg = COLOR_BACK,width = int(width_set_l/2))# 先创建右侧右
    f1_5_2r_r_3.pack()
    c1_5_3 = ttk.Combobox(f1_5_2r_r_3, width=15)
    c1_5_3['values'] = ('String','int','float')     # 设置下拉列表的值
    c1_5_3.configure(state="readonly") # 不可编辑
    c1_5_3.pack(side = 'right')
    lc1_5_3 = tk.Label(f1_5_2r_r_3,text='  y dype:  ',bg = COLOR_BACK,width=10)
    lc1_5_3.pack(side = 'right')    
            #4.5 选择x1的数据类型
    f1_5_2r_r_4 = tk.Frame(f1_5_2r_r,bg = COLOR_BACK,width = int(width_set_l/2))# 先创建右侧右
    f1_5_2r_r_4.pack()
    c1_5_4 = ttk.Combobox(f1_5_2r_r_4, width=15)
    c1_5_4['values'] = (choose_ls[1:])     # 设置下拉列表的值
    c1_5_4.current(0)    # 设置下拉列表默认显示的值
    c1_5_4.configure(state="readonly") # 不可编辑
    c1_5_4.pack(side = 'right')
    lc1_5_4 = tk.Label(f1_5_2r_r_4,text='      x:  ',bg = COLOR_BACK,width=10)
    lc1_5_4.pack(side = 'right')   
            #4.6 选择x1的数据类型
    f1_5_2r_r_5 = tk.Frame(f1_5_2r_r,bg = COLOR_BACK,width = int(width_set_l/2))# 先创建右侧右
    f1_5_2r_r_5.pack()
    c1_5_5 = ttk.Combobox(f1_5_2r_r_5, width=15)
    c1_5_5['values'] = ('String','int','float')     # 设置下拉列表的值
    c1_5_5.configure(state="readonly") # 不可编辑
    c1_5_5.pack(side = 'right')
    lc1_5_5 = tk.Label(f1_5_2r_r_5,text='  x dype:  ',bg = COLOR_BACK,width=10)
    lc1_5_5.pack(side = 'right') 
            #4.7 选择x2的数据类型
    f1_5_2r_r_6 = tk.Frame(f1_5_2r_r,bg = COLOR_BACK,width = int(width_set_l/2))# 先创建右侧右
    f1_5_2r_r_6.pack()
    c1_5_6 = ttk.Combobox(f1_5_2r_r_6, width=15)
    c1_5_6['values'] = (choose_ls[1:])     # 设置下拉列表的值
    c1_5_6.current(0)    # 设置下拉列表默认显示的值
    c1_5_6.configure(state="readonly") # 不可编辑
    c1_5_6.pack(side = 'right')
    lc1_5_6 = tk.Label(f1_5_2r_r_6,text='     x2:  ',bg = COLOR_BACK,width=10) 
    lc1_5_6.pack(side = 'right') 
            #4.8 选择x2的数据类型
    f1_5_2r_r_7 = tk.Frame(f1_5_2r_r,bg = COLOR_BACK,width = int(width_set_l/2))# 先创建右侧右
    f1_5_2r_r_7.pack()
    c1_5_7 = ttk.Combobox(f1_5_2r_r_7, width=15)
    c1_5_7['values'] = ('String','int','float')     # 设置下拉列表的值
    c1_5_7.configure(state="readonly") # 不可编辑
    c1_5_7.pack(side = 'right')
    lc1_5_7 = tk.Label(f1_5_2r_r_7,text=' x2 dype:  ',bg = COLOR_BACK,width=10)
    lc1_5_7.pack(side = 'right') 
            #4.9 进行绘图的按钮 与 进行自定义设置的按钮
    if platform.system() == 'Darwin':# Mac系统
        b1_5_3 = tk.Button(f1_5_2r_r, text="POLT", width=10, height=2,fg = COLOR_MB_FRONT,command=lambda:infor_analyse_plot())
        b1_5_4 = tk.Button(f1_5_2r_r, text="Setting", width=10, height=2,fg = COLOR_MB_FRONT,command=lambda:infor_analyse_plot_to_setting())
    elif platform.system() == 'Windows':# Windows系统
        b1_5_3 = tk.Button(f1_5_2r_r, text="PLOT", width=10, height=2,bg = COLOR_SUB,fg = COLOR_FRONT,command=lambda:infor_analyse_plot())
        b1_5_4 = tk.Button(f1_5_2r_r, text="Setting", width=20, height=2,bg = COLOR_SUB,fg = COLOR_FRONT,command=lambda:infor_analyse_plot_to_setting())
    b1_5_3.pack();b1_5_4.pack()

    # 5 显示设置的布局
        #5.1 声明变量
        # 名称
    global f1_5_2r_r_8,c1_5_8,lc1_5_8 # 自定义表格名称
    global f1_5_2r_r_9,c1_5_9,lc1_5_9 # 自定义y名称(及单位)
    global f1_5_2r_r_a,c1_5_a,lc1_5_a # 自定义x1名称(及单位)    
    global f1_5_2r_r_b,c1_5_b,lc1_5_b # 自定义x2名称(及单位) (如果是3D图的话允许设置) 
        # 显示方案
    global f1_5_2r_r_c,c1_5_c,lc1_5_c # 自定义x1-y显示方案 
    #global f1_5_2r_r_d,c1_5_d,lc1_5_d # 自定义x2-y显示方案  (如果是3D图的话允许设置) 
        # 图例
    global f1_5_2r_r_e,c1_5_e,lc1_5_e # 是否显示图例
    global f1_5_2r_r_f,c1_5_f,lc1_5_f # 图例名称- x1
    global f1_5_2r_r_g,c1_5_g,lc1_5_g # 图例名称- x2   (如果是3D图的话允许设置) 
    global f1_5_2r_r_h,c1_5_h,lc1_5_h # 图例显示位置
        # 颜色
    global f1_5_2r_r_i,c1_5_i,lc1_5_i # point color
        # 更多图
    global f1_5_2r_r_k,c1_5_k,lc1_5_k # 显示为(散点图,折线图,柱状图,棒棒糖图,饼图)(仅2D图可设置)
        # 返回绘图模式
    global b1_5_5
    
        #5.2 自定义表格名称
    f1_5_2r_r_8 = tk.Frame(f1_5_2r_r,bg = COLOR_BACK,width = int(width_set_l/2))# 先创建右侧右
    c1_5_8 = tk.Entry(f1_5_2r_r_8,bg = COLOR_F2_BACK,fg = COLOR_FRONT, width=15)
    c1_5_8.insert(0, choose_name+'信息分析')
    lc1_5_8 = tk.Label(f1_5_2r_r_8,text='figure name:  ',bg = COLOR_BACK,width=10)
        #5.3 自定义y名称(及单位)
    f1_5_2r_r_9 = tk.Frame(f1_5_2r_r,bg = COLOR_BACK,width = int(width_set_l/2))# 先创建右侧右
    c1_5_9 = tk.Entry(f1_5_2r_r_9,bg = COLOR_F2_BACK,fg = COLOR_FRONT, width=15)
    c1_5_9.insert(0, choose_name+'信息分析')
    lc1_5_9 = tk.Label(f1_5_2r_r_9,text='Y name:  ',bg = COLOR_BACK,width=10)    
        #5.4 自定义x1名称(及单位)
    f1_5_2r_r_a = tk.Frame(f1_5_2r_r,bg = COLOR_BACK,width = int(width_set_l/2))# 先创建右侧右
    c1_5_a = tk.Entry(f1_5_2r_r_a,bg = COLOR_F2_BACK,fg = COLOR_FRONT, width=15)
    c1_5_a.insert(0, choose_name+'信息分析')
    lc1_5_a = tk.Label(f1_5_2r_r_a,text='X name:  ',bg = COLOR_BACK,width=10)
        #5.5 自定义x2名称(及单位)
    f1_5_2r_r_b = tk.Frame(f1_5_2r_r,bg = COLOR_BACK,width = int(width_set_l/2))# 先创建右侧右
    c1_5_b = tk.Entry(f1_5_2r_r_b,bg = COLOR_F2_BACK,fg = COLOR_FRONT, width=15)
    lc1_5_b = tk.Label(f1_5_2r_r_b,text='X2 name:  ',bg = COLOR_BACK,width=10)
        #5.6 自定义显示方案(前面有的代码也写成x1-y style)
    f1_5_2r_r_c = tk.Frame(f1_5_2r_r,bg = COLOR_BACK,width = int(width_set_l/2))# 先创建右侧右
    c1_5_c = ttk.Combobox(f1_5_2r_r_c, width=15)
    c1_5_c['values'] = (markerls)     # 设置下拉列表的值
    c1_5_c.current(0)    # 设置下拉列表默认显示的值
    c1_5_c.configure(state="readonly") # 不可编辑
    lc1_5_c = tk.Label(f1_5_2r_r_c,text='plot style:  ',bg = COLOR_BACK,width=10) 
        #5.12 自定义显示颜色
    f1_5_2r_r_i = tk.Frame(f1_5_2r_r,bg = COLOR_BACK,width = int(width_set_l/2))# 先创建右侧右
    c1_5_i = ttk.Combobox(f1_5_2r_r_i, width=15)
    c1_5_i['values'] = (colorls)     # 设置下拉列表的值 # 113是red
    c1_5_i.current(113)    # 设置下拉列表默认显示的值
    c1_5_i.configure(state="readonly") # 不可编辑
    lc1_5_i = tk.Label(f1_5_2r_r_i,text='  color:  ',bg = COLOR_BACK,width=10) 
        #5.13
    if platform.system() == 'Darwin':# for Mac
        b1_5_5 = tk.Button(f1_5_2r_r, text="Back to plot", width=10, height=2,fg = COLOR_MB_FRONT,command=lambda:infor_analyse_setting_to_plot())
    elif platform.system() == 'Windows':# for Windows
        b1_5_5 = tk.Button(f1_5_2r_r, text="Back to plot", width=20, height=2,bg = COLOR_SUB,fg = COLOR_FRONT,command=lambda:infor_analyse_setting_to_plot())
    b1_5_5.pack();b1_5_5.pack_forget()

    # 6 选中模板的信息展示
        #6.1 表格框架搭建
    global treeview1_5_1 # 表格
    columns1_5_1 = ("1", "2", "3", "4", "5", "6", "7", "8", "9", "10",\
               "11","12","13","14","15","16","17","18","19","20")
    treeview1_5_1 = ttk.Treeview(f1_5_2r_l, show="headings", columns=columns1_5_1)  # 表格
    treeview1_5_1.tag_configure("ttk",background = COLOR_F1_BACK)# 设置表格颜色1/2
    for count in range(20):
        treeview1_5_1.column(columns1_5_1[count], width=100, anchor='center')
    for count in range(20):
        treeview1_5_1.heading(columns1_5_1[count], text=columns1_5_1[count])
    treeview1_5_1.pack(side=tk.LEFT, fill=tk.BOTH)
    item = []
    for i in range(20):
        item.append('')
    for i in range(36):
        treeview1_5_1.insert('', 0, values='')

def information_control_analyse_predict(): # 进入模型拟合模式
    # 推出上次内容
    f1_5_0.pack_forget()
    f1_5_1.pack_forget()
    # 安放本次内容
    #global f1_2_1_e,f1_2_2_e,f1_2_3_e,f1_2_4_e,f1_2_5_e,f1_2_6_e
    #global sb1_2_1_e,l1_2_1_e,L1_2_2_e,b1_2_1_e,b1_2_6_e
    global b1_5_1_p,b1_5_2_p,f1_5_0_p,f1_5_1_p    
    # 上侧
    f1_5_0_p = tk.Frame(window ,width=20, height=2)
    if platform.system() == 'Darwin':# Mac系统
        b1_5_1_p = tk.Button(f1_5_0_p, text="Back", width=10, height=2,fg = COLOR_MB_FRONT,command=lambda:information_control_analyse_predict_back())
        b1_5_2_p = tk.Button(f1_5_0_p, text="Plot", width=10, height=2,fg = COLOR_MB_FRONT,command=lambda:information_control_analyse_predict_to_plot())
    elif platform.system() == 'Windows':# Windows系统
        b1_5_1_p = tk.Button(f1_5_0_p, text="Back", width=20, height=3,bg = COLOR_SUB,fg = COLOR_FRONT,command=lambda:information_control_analyse_predict_back())
        b1_5_2_p = tk.Button(f1_5_0_p, text="Plot", width=10, height=2,fg = COLOR_FRONT,bg = COLOR_SUB,command=lambda:information_control_analyse_predict_to_plot())
    f1_5_0_p.pack()
    b1_5_2_p.pack(side='right')
    b1_5_1_p.pack(side='right')
    # 次主框架
    f1_5_1_p = tk.Frame(window,bg = COLOR_BACK)
    f1_5_1_p.pack(expand='yes', fill='both')

'''
    # 左侧
    f1_2_1_e = tk.Frame(window,bg = COLOR_BACK)# 次主框架
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
'''









def information_control_analyse_predict_back(): # 由预测模式进行的返回
    f1_5_0_p.pack_forget()
    f1_5_1_p.pack_forget()
    note.pack_forget()
    information_control()
def information_control_analyse_predict_to_plot(): # 由预测模式返回到绘图模式
    f1_5_0_p.pack_forget()
    f1_5_1_p.pack_forget()
    note.pack_forget()
    information_control_analyse()
def information_control_analyse_out(): # 退出
    f1_5_0.pack_forget()
    f1_5_1.pack_forget()
    note.pack_forget()
def information_control_analyse_back(): # 返回
    information_control_analyse_out()
    information_control()

###############################################################################################################################################
###############################################################################################################################################   
'''
模版控制函数
'''
def template_control():
    ''' main function of Template Control 模板控制主函数
    This function is a sub-function of main(). 
    It supports adding, modifying and viewing templates.
    
    该函数是main()下级函数. 目前支持模板的添加,修改,查看功能
    '''
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
    ''' Information Control out function 模板主函数退出函数
    This function hides the contents of the next screen 
    from all components other than the specified prompt text.
    
    该函数的功能是将处指定提示文本外的所有组件隐藏放上下一屏的内容.
    '''
    note.pack_forget()
    b2_1.pack_forget()
    b2_2.pack_forget()
    b2_3.pack_forget()
    b2_4.pack_forget()

#-----------------------------------------------------------------------------------------------------------------------------------------------

def template_control_back():# 返回函数 b2_1按钮
    ''' Template Control back function 模板主函数返回函数
    This function is called for template_control(),
    The function returns the previous level template_control().
    
    该函数由template_control()调用,功能是返回上一级template_control().
    '''
    template_control_out()
    main()

#-----------------------------------------------------------------------------------------------------------------------------------------------

def template_control_add(): # 模板添加 b2_2 按钮
    ''' Adding Templates 模板添加
    '''
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
      winfor = open('./resources/user/infor_'+e2_2_1.get()+'.txt','a+',encoding='UTF-8') # 文本形式，追加写模式
      winfor.close()
      Update_infor_path()
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
            wincopy = open('./resources/system/inforchange.txt','w',encoding='UTF-8') # 文本形式，重写模式
            for line in winfor.readlines():
                wincopy.write(line)
            winfor.close()
            wincopy.close()
            # 在进行文件重写
            wincopy = open('./resources/system/inforchange.txt','r',encoding='UTF-8') # 文本形式，只读
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
            wincopy = open('./resources/system/inforchange.txt','w',encoding='UTF-8') # 文本形式，重写模式
            for line in winfor.readlines():
                wincopy.write(line)
            winfor.close()
            wincopy.close()
            # 再进行文件重写
            wincopy = open('./resources/system/inforchange.txt','r',encoding='UTF-8') # 文本形式，只读
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
    cmb3_1.configure(state="readonly") # 不可编辑
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
    #wtemplate = open('./resources/system/template/template.txt','r',encoding='UTF-8')
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
        if choose == 'Input old password first!': # 确认密码是否正确
            if e3_1.get() == get_password():# 老密码正确
                var_l31.set("Please Input New password")   
                choose = "Please Input New password"
                e3_1.delete(0, tk.END)
        elif choose == 'Please Input New password': # 开始出入第一次新密码
            password1 = e3_1.get()
            var_l31.set("Input New password again")
            choose = "Input New password again"
            e3_1.delete(0, tk.END)
        elif choose == 'Input New password again': # 开始输入第二次新密码
            password2 = e3_1.get()
            e3_1.delete(0, tk.END)
            if password2 == password1:
                wsetting = open('./resources/system/setting/password.txt','r',encoding='UTF-8') # 文本形式，只读
                wcopy = open('./resources/system/inforchange.txt','w',encoding='UTF-8') # 文本形式，重写模式
                for line in wsetting.readlines():
                    wcopy.write(line)
                wcopy.close();wsetting.close()
                wcopy = open('./resources/system/inforchange.txt','r',encoding='UTF-8') # 文本形式，只读
                wsetting = open('./resources/system/setting/password.txt','w',encoding='UTF-8') # 文本形式，重写模式
                for line in wcopy.readlines():
                    if get_kth_in_line(line,1) == 'password':
                        wsetting.write("password")
                        password_ls = password_translation(password2,0)
                        for i in range(len(password_ls)):
                            wsetting.write("  ")
                            wsetting.write(password_ls[i])
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
                wcopy = open('./resources/system/inforchange.txt','w',encoding='UTF-8') # 文本形式，重写模式
                for line in wsetting.readlines():
                    wcopy.write(line)
                wcopy.close();wsetting.close()
                wcopy = open('./resources/system/inforchange.txt','r',encoding='UTF-8') # 文本形式，只读
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
                    # 先把文件保存到工作区
                    wsetting = open('./resources/system/setting/setting.txt','r',encoding='UTF-8') # 文本形式，只读
                    wcopy = open('./resources/system/inforchange.txt','w',encoding='UTF-8') # 文本形式，重写模式
                    for line in wsetting.readlines():
                        wcopy.write(line)
                    wcopy.close()
                    wsetting.close()
                    # 再进行文件重写
                    wcopy = open('./resources/system/inforchange.txt','r',encoding='UTF-8') # 文本形式，只读
                    wsetting = open('./resources/system/setting/setting.txt','w',encoding='UTF-8') # 文本形式，重写模式
                    for line in wcopy.readlines():
                        if get_kth_in_line(line,1) == 'music' and get_kth_in_line(line,2) == 'on_or_off':
                            wsetting.write('music  on_or_off  on  \n')
                        else:
                            wsetting.write(line)
                    wcopy.close()
                    wsetting.close()
                    ini_music(ini=False)#开音乐
                    setting_control_out();setting_control() # 重新进入
            elif cmb3_1.get() == 'off':
                if item_text[2] == 'off':pass
                else:
                    pygame.mixer.music.stop()#关音乐
                    # 先把文件保存到工作区
                    wsetting = open('./resources/system/setting/setting.txt','r',encoding='UTF-8') # 文本形式，只读
                    wcopy = open('./resources/system/inforchange.txt','w',encoding='UTF-8') # 文本形式，重写模式
                    for line in wsetting.readlines():
                        wcopy.write(line)
                    wcopy.close()
                    wsetting.close()
                    # 再进行文件重写
                    wcopy = open('./resources/system/inforchange.txt','r',encoding='UTF-8') # 文本形式，只读
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
            wcopy = open('./resources/system/inforchange.txt','w',encoding='UTF-8') # 文本形式，重写模式
            for line in wsetting.readlines():
                wcopy.write(line)
            wcopy.close()
            wsetting.close()
            wcopy = open('./resources/system/inforchange.txt','r',encoding='UTF-8') # 文本形式，只读
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
            ini_music(ini=False)
        # 调用函数内容
        wsetting = open('./resources/system/music/setting_music_name.txt','r',encoding='UTF-8') # 文本形式，重写模式
        ls = []
        for line in wsetting.readlines():
            ls.append(line[:-4]+'mp3')
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
                    #COLOR_BACK = 'dimgray';COLOR_FRONT = 'white';COLOR_SUB = 'black'
                    print("本来是off 现在要改成on")
                    wsetting = open('./resources/system/setting/setting.txt','r',encoding='UTF-8') # 文本形式，只读
                    wcopy = open('./resources/system/inforchange.txt','w',encoding='UTF-8') # 文本形式，重写模式
                    for line in wsetting.readlines():
                        wcopy.write(line)
                    wcopy.close();wsetting.close()
                    wcopy = open('./resources/system/inforchange.txt','r',encoding='UTF-8') # 文本形式，只读
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
                    wsetting = open('./resources/system/setting/setting.txt','r',encoding='UTF-8') # 文本形式，只读
                    wcopy = open('./resources/system/inforchange.txt','w',encoding='UTF-8') # 文本形式，重写模式
                    for line in wsetting.readlines():
                        wcopy.write(line)
                    wcopy.close();wsetting.close()
                    wcopy = open('./resources/system/inforchange.txt','r',encoding='UTF-8') # 文本形式，只读
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
                    wcopy = open('./resources/system/inforchange.txt','w',encoding='UTF-8') # 文本形式，重写模式
                    for line in wsetting.readlines():
                        wcopy.write(line)
                    wcopy.close()
                    wsetting.close()
                    # 再进行文件重写
                    wcopy = open('./resources/system/inforchange.txt','r',encoding='UTF-8') # 文本形式，只读
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
                    wcopy = open('./resources/system/inforchange.txt','w',encoding='UTF-8') # 文本形式，重写模式
                    for line in wsetting.readlines():
                        wcopy.write(line)
                    wcopy.close()
                    wsetting.close()
                    # 再进行文件重写
                    wcopy = open('./resources/system/inforchange.txt','r',encoding='UTF-8') # 文本形式，只读
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
def get_kth_in_line(line, k=0, wish=-1, split=" "):
    ''' 寻找一个字符串中的某个词或计算句子词数
    The user selects templates on the left side of the interface. 
    This function can save the latest selection made by the user.
    
    :params line: String
        One line of string to evaluate 进行计算的一行字符串
    :params k: int
        (optional) 
        When k=0, the number of words returned;
        when k<0, the -k word for flashback; 
        when k>0, the k word for positive order
        当k=0时，返回词的个数，当k<0时，为倒叙寻找第-k个词，当k>0时，为正序寻找第k个词
    :params wish: int
        (optinal) 
        The fetch operation is performed when the 
        number of words in the sentence is equal to wish. 
        If wish<=0, default does not restrict the fetch.
        当这个句话中的词数与wish相等进行取词操作. 如果wish<=0默认不进行对取词的限制.
    :params split: char
        (optional)
        The division between two words, the default is a space.
        两个词之间的分割, 默认为空格
    :return word: string or int or None
        If k is out of range or if wish is unequal to the number 
        of times, return None. If k=0, return the number of words.
        找词模式下返回寻找的那个词, k超出范围或者wish与次数不等时返回None, k=0时返回词的个数
    '''
    max_num = 0;count = 0;last = split;word = ""; wish = int(wish)
    # 计算一行有几个词
    for item in line:
        if last == split and item != split and item != "\n": max_num = max_num+1
        last = item
    last = split
    # wish有效时进行次数判断
    if wish > 0:
        if wish != max_num: print("wrong number of the line:",line); return ''
    # 根据k进入不同功能
    if k == 0:                    # 当k=0时，返回词的个数
        return max_num
    elif k > 0 and k <= max_num:  # 当k>0时，为正序寻找第k的词
        for item in line:
            if (last == split or last == '\n') and (item != split and item != "\n"): count=count+1
            last = item
            if k == count and item!=split and item != '\n': word = word+item
        return word
    elif k < 0 and -k <= max_num: # 当k<0时，为倒叙寻找第k的词
        k = max_num + 1 + k
        for item in line:
            if (last == split or last == '\n') and (item != split and item != "\n"): count=count+1
            last = item
            if k == count and item!=split and item != "\n": word = word+item
        return word
    else:                         # 输入格式错误
        print("wrong type of k in get_kth_in_line(line,k) of line = "+line)
        return ''

# old edition
#def get_kth_in_line(line, k, wish=-1, split=" "):#当k=0时，返回词的个数，当k<0时，为倒叙寻找第-k个词，当k>0时，为正序寻找第k个词
#    max_num = 0;count = 0;last = split;word = ""
#    # 计算一行有几个词
#    for item in line:
#        if last == split and item != split and item != "\n": max_num = max_num+1
#        last = item
#    last = split
#    if k == 0:                    # 当k=0时，返回词的个数
#        return max_num
#    elif k > 0 and k <= max_num:  # 当k>0时，为正序寻找第k的词
#        for item in line:
#            if (last == split or last == '\n') and (item != split and item != "\n"): count=count+1
#            last = item
#            if k == count and item!=split and item != '\n': word = word+item
#        return word
#    elif k < 0 and -k <= max_num: # 当k<0时，为倒叙寻找第k的词
#        k = max_num + 1 + k
#        for item in line:
#            if (last == split or last == '\n') and (item != split and item != "\n"): count=count+1
#            last = item
#            if k == count and item!=split and item != "\n": word = word+item
#        return word
#    else:                         # 输入格式错误
#        print("wrong type of k in get_kth_in_line(line,k) of line = "+line)

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

def list_dir(path, list_name, type_):
    ''' Gets the address of all specific files 获取所有特定文件的地址
    This function adds all audio names to the list recursively
    本函数利用递归, 将所有的特定类型文件目录添加到列表中
    
    :param path: Root directory Settings 根目录设置
    :param list_name: The list to add 进行添加的列表
    :param type_: Type of file to search 文件的类型 e.g. '.mp3','.txt'
    '''
    for file in os.listdir(path):  
        file_path = os.path.join(path, file)  
        if os.path.isdir(file_path):  
            list_dir(file_path, list_name, type_)  
        elif os.path.splitext(file_path)[1]==type_:  
            list_name.append(file_path.replace('\\', '/'))

def Update_infor_path():
    ''' Update the infor_path.txt file 更新infor_path.txt文件
    To support user-defined folders, we need to get the latest location of 
    each information file before the program starts or each information-related 
    operation. This function is to iterate over all the.txt files in the user 
    directory and store the directory in infor_path.txt.
    
    为了支持用户自定义文件夹, 在程序开始或每一次与信息相关的操作前,需要获得最新的每个信息
    文件存储地址. 本函数就是遍历所有user目录下的.txt文件然后将目录存在infor_path.txt中.
    ''' 
    print("更新信息路径文件")
    ls = [] ; list_dir('./resources/user',ls,'.txt')
    wsetting = open('./resources/system/template/infor_path.txt','w', encoding='UTF-8')
    for i in range(len(ls)):
        wsetting.write(ls[i]+'\n')
    wsetting.close()

def find_infor_path(name,update_infor_path=False):
    ''' Find the information file address 寻找信息文件地址
    Find the address of the information file for a particular template. 
    Take a template name, look for it in infor_path.txt, 
    return the address if found, print an error.
    
    寻找特定模板的信息文件地址.接受一个模板名称, 在infor_path.txt中进行寻找,
    如果由则返回地址,未找到则输出错误.
    
    :param name: The template name of the file to search 要搜索的文件的模板名
    :param update_infor_path: (optional) Whether to update the address file of the infor file 是否更新信息文件的地址文件
    :return line: path 地址
    '''
    if update_infor_path: Update_infor_path()
    winfor = open('./resources/system/template/infor_path.txt','r',encoding='UTF-8')
    for line in winfor.readlines():
        name_ = line.split('/')[-1]
        if name_[6:-5] == name: winfor.close();return str(line[:-5]+'.txt')
    print("未找到模板:",name)
    winfor.close()
    return " "

def password_translation(word,mood):
    ''' Encrypt and decrypt passwords 进行字符串的加密与解密
    You can also create your own set of encryption algorithms, just modify this function.
    你也可以自己的创建一套加密算法,只需修改本函数.
    
    :param word: The word used to encrypt and decrypt a password 进行密码的加密与解密的词
    :param mood: Mood = 0, encryption; Mood = 1, decryption    mood=0,加密;mood=1,解密
    :return password: The modified string 加密后的列表与解密后的字符串
    '''
    if mood == 0: # encryption
        password = []
        for i in range(len(word)):
            password.append(str(ord(word[i])+2*i))
        return password
    if mood == 1: # decryption 
        password = ''
        for i in range(len(word)):
            password = password+chr(int(word[i])-2*i)
        return password 

def get_password():
    ''' getpassword 获取密码
        Gets the decrypted password from the password file
        从密码文件中获取解密好的密码
        :return password: Decrypted password 解密好的密码
    '''    
    wsetting = open('./resources/system/setting/password.txt','r',encoding='UTF-8')
    for line in wsetting.readlines():
        if str(get_kth_in_line(line,1)) == 'password':break
    wsetting.close()
    password_ls = []
    for i in range(get_kth_in_line(line,0)-1):
        password_ls.append(get_kth_in_line(line,i+2))
    return password_translation(password_ls,1)

def sent_message(mail,word):
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
            msg['Subject']="Information Helper 验证码"                # 邮件的主题，也可以说是标题
        
            server=smtplib.SMTP_SSL("smtp.qq.com", 465)  # 发件人邮箱中的SMTP服务器，端口是25
            server.login(my_sender, my_pass)  # 括号中对应的是发件人邮箱账号、邮箱密码
            server.sendmail(my_sender,[my_user,],msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
            server.quit()  # 关闭连接
        except:  # 如果 try 中的语句没有执行，则会执行下面的 ret=False
            ret=False
        return ret
    ask_if_find_password = messagebox.askyesno('askyesno', 'Sure To Send ?', parent=window)
    if ask_if_find_password:
        my_sender='1742861545@qq.com'    # 发件人邮箱账号
        my_pass = 'navcurjavwtgecfg'     # 发件人邮箱密码
        my_user=mail                     # 收件人邮箱账号
        if sentmail():print("邮件发送成功")
        else: print("邮件发送失败") 
                
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
    print("程序未成功打开")
