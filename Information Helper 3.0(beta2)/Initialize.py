import os
import sys
import pygame
import jieba
from tool.CSVTool import *
from tool.Path import *
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import font

# 文件初始化
def ini_check(base_path):
    ''' Check file configuration 检查文件配置
    Called by the function initial(). It checks the file system level by level 
    from the initial() function and creates it if it does not exist.
    由initial()函数调用, 进行文件系统的逐级检查,如果不存在则创建之.

    ini_check_creat_folders()  - Check or Create folders 检查或创建文件夹
    ini_check_creat_files()   - ini_check_creat_files   检查或创建文件
    '''
    
    def ini_check_creat_folders(pathList):
        ''' Check or Create folders 检查或创建文件夹
        It checks for a specific folder, or creates a folder if it doesn't exist.
        实现特定文件夹的检查, 如果文件夹不存在则创建之.
        :param pathList: 列表类型, The path to the folder to check 待检查文件夹的路径的列表
        '''
        for path in pathList:
            if os.path.exists(path) != True:
                os.mkdir(base_path+path) 

    def ini_check_creat_files(path,word=None):
        ''' Check or Create a file 检查或创建文件
        It checks for a specific file, or creates a file if it doesn't exist.
        特定文件的检查, 如果文件不存在则创建之.
        :param path: The path to the file to check 待检查文件的路径
        :param word: (optional) What to fill in when creating a file 创建文件时填入的内容
        '''
        if os.path.exists(path): # 判断存在
            print(os.path.split(path)[1]+" checked successfully!")
        else: # 创建
            if os.path.splitext(path)[1] == '.txt':
                if word == None: word = ''
                fcreator = open(path,'a', encoding='UTF-8')
                fcreator.write(word)
                fcreator.close()
            elif os.path.splitext(path)[1] == '.csv':
                if word == None: word = None
                csvWriterLines(word,path,'w')
            print(os.path.split(path)[1]+" created successfully!")

    # 进行文件夹的检查(或创建)
    pathList=[r'resources',r'resources/system',r'resources/system/setting',r'resources/system/music',\
    r'resources/system/template',r'resources/user',r'resources/input box',r'resources/picture',\
    r'resources/time',r'resources/time/single',r'resources/time/period',r'resources/database']
    ini_check_creat_folders(pathList=pathList)

    # 进行文件的检查(或创建)
    dict_txt = \
    '!!! Attention !!!\
    \nThe [dict.txt] is missing. You need to download the dict.txt and replace this file with the downloaded one.\n\
    \n!!! 注意 !!!\
    \ndict文件缺失! 您需要通过百度网盘下载dict文件并用下载的文件代替本文件\n\
    \n链接:https://pan.baidu.com/s/1G6XmJQZfHANsCZXO6R14XQ  密码:67w0'
    ini_check_creat_files(path='./resources/system/dict.txt',word=dict_txt)
    setting_txt = [['Me','password'],
                   ['Me','mail',None],
                   ['music','on_or_off','off'],
                   ['music','name','未设置'],
                   ['common','dark_mod','off'],
                   ['common','palette','Autumn'],
                   ['common','font','Times'],
                   ['common','size','18'],
                   ['common','language','English'],
                   ['safe','password','off'],
                   ['plot','mode','散点图'],
                   ['info','search','time_event','off'],
                   ['info','search','mode','Search All'],
                   ['info','add','mode','Item']]
    ini_check_creat_files(path=base_path+'/resources/system/setting/setting.csv',word=setting_txt)  
    ini_check_creat_files(path=base_path+'/resources/system/music/setting_music_name.csv')
    ini_check_creat_files(path=base_path+'/resources/system/template/template.csv')   
    ini_check_creat_files(path=base_path+'/resources/system/template/infor_path.csv')
    ini_check_creat_files(path=base_path+'/resources/system/music/setting_music_name.csv') 
    ini_check_creat_files(path=base_path+'/resources/time/single/single.csv')    
    ini_check_creat_files(path=base_path+'/resources/time/period/period.csv')
    ini_check_creat_files(path=base_path+'/resources/database/default.csv',word=[[0]])

    # 更新信息路径文件
    update_infor_path(base_path)

# 音乐初始化
def ini_music(base_path,ini=True):
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
    ini_music_once()  - Initialize the music directory 进行音乐目录的初始化
    ini_music_ifplay()- Determine if music is needed   判断是否需要播放音乐
    ini_music_play()  - Open the music                 打开音乐
    '''
    def ini_music_once():
        ''' Initialize the music directory 进行音乐目录的初始化
        Called by the function ini_music(), Complete the first step
        of ini_music() - initialize the music directory.
        
        该函数由ini_music()调用.完成ini_music的第一步,进行音乐目录的初始化.
        '''
        ls = [] ; list_dir(base_path+'/resources/system/music',ls,'.mp3')
        for count in range(len(ls)):
            ls[count] = os.path.basename(ls[count])
        csvWriterLines(listToList(ls),base_path+'/resources/system/music/setting_music_name.csv','w')
        pygame.mixer.init()
    
    def ini_music_ifplay():
        ''' Determine if music is needed 判断是否需要播放音乐
        '''
        return get_setting(items=['music', 'on_or_off'], default='off') == 'on'
    
    def ini_music_play():
        ''' Open the music 打开音乐
        Open the selected music in the Settings file. 
        Open successfully and play the music in the single loop mode.
        
        打开设置文件中选择的音乐.打开成功即播放音乐,播放模式为单曲循环
        '''
        print("Play music!")

        music_name = get_setting(items=['music', 'name'])
        music_mode = get_setting(items=['music', 'mode'], default='single')
        if ini == False:
            pygame.mixer.init()

        if music_mode == 'single': # 单曲循环
            print("music mode: single")
            try:
                file=base_path+'/resources/system/music/'+music_name
                pygame.mixer.music.load(file)
                pygame.mixer.music.play(-1)
                print("Staring play music "+music_name)
            except:
                print("Error! Fail to play music! "+music_name)
        '''
        elif music_mode == 'random': #随机播放 # 有问题
            print("music mode: random")
            clock = pygame.time.Clock()
            song_idx = 0  # The index of the current song.
            done = False
            name_list = []; list_dir('./resources/system/music',name_list,'.mp3')
            #print(name_list) # testing
            play_list = [];
            for name in name_list:
                play_list.append('./resources/system/music/'+name)
        '''
    
    # 如果是第一次打开, 则进行音乐目录更新的操作 (进行音乐目录的初始化)
    if ini:
        ini_music_once()
    
    # 如果未设置过音乐名称, 不进行播放
    if get_setting(items=['music', 'name']) == '未设置':
        return False

    # 进行播放特定音乐
    if ini_music_ifplay():
    	ini_music_play()

# 变量初始化
def ini_setting(base_path):
    ''' 变量初始化
    '''
    setting_dict = {}
    # 暗黑模式
    setting_dict['dark_mod'] = get_setting(items=['common','dark_mod'], default='off')
    # 调色板
    setting_dict['palette'] = get_setting(items=['common','palette'], default='Autumn')
    # 语言
    setting_dict['language'] = get_setting(items=['common','language'], default='English')
    # 信息默认插入方式
    setting_dict['info_insert_way'] = get_setting(items=['info','add','mode'], default='item')
    # 信息默认查询方式
    setting_dict['info_search_way'] = get_setting(items=['search','mode'], default='Search All')
    # 信息搜索是否将提醒事项列出
    setting_dict['info_search_time'] = get_setting(items=['search','time_event'], default='off')
    # 所有的绘图模式
    setting_dict['all_plot_mode'] = ['散点图','线图','分布散点图1', '分布散点图2', '分类分布图1', \
                 '分类分布图2', '分类分布图3', '分类估计图1', '分类估计图2', \
                 '分类估计图3', '单变量分布','二元分布图','成对关系图']
    # 默认绘图模式
    setting_dict['default_plot'] = get_setting(items=['plot','mode'], default='散点图')
    if setting_dict['default_plot'] not in setting_dict['all_plot_mode']:
        setting_dict['default_plot'] = '散点图'
    # 是否开启密码
    setting_dict['need_password'] = get_setting(items=['safe','password'], default='off')
    # 用户邮箱
    setting_dict['mail'] = get_setting(items=['Me','mail'],default=None)
    # 所有的字体
    temp_window = tk.Tk()#temp_window.alpha = 0
    setting_dict['all_font'] = font.families()
    temp_window.destroy()
    # 获取当前字体
    setting_dict['font'] = get_setting(items=['common','font'], default='Times')
    if setting_dict['font'] not in setting_dict['all_font']:
        setting_dict['font'] = setting_dict['all_font'][0]
    # 字体大小
    setting_dict['size'] = int(get_setting(items=['common','size'], default='16'))
    # 标题字体大小
    setting_dict['tsize'] = setting_dict['size'] + 6
    # 获取系统类型
    if sys.platform == 'darwin':
        setting_dict['system'] = 'Mac'
    elif sys.platform == 'win32' or sys.platform == 'cygwin' or sys.platform == 'linux':
        setting_dict['system'] = 'else'
    # 窗口宽度
    setting_dict['window_width'] = 1000
    # 窗口高度
    setting_dict['window_height'] = 618
    # 右侧界面宽度(通过功能窗宽度比例计算)
    setting_dict['rwidth'] = int(setting_dict['window_width']*eval(get_setting(items=['common','toolbox','size'], default='0.25')))
    # 左侧界面宽度
    setting_dict['lwidth'] = setting_dict['window_width'] - setting_dict['rwidth']
    # 获取左右界面容纳字数
    def get_size(family,size):
        text = '1'#"█"
        temp_window = tk.Tk()#temp_window.alpha = 0
        _font = font.Font(temp_window,family=family, size=size)
        (w,h) = (_font.measure(text),_font.metrics("linespace"))
        temp_window.destroy()
        return w,h
    max_size = get_size(setting_dict['font'],setting_dict['size'])
    setting_dict['rletter'] = setting_dict['rwidth'] / max_size[0]
    setting_dict['lletter'] = setting_dict['lwidth'] / max_size[0]
    # 获取表格需要的最小数据项数据(最小5)
    setting_dict['min_table'] = tabel_max_length(base_path)
    # 用于设置模块检查的设置参数字典
    setting_dict['settingDict'] = {'Me - password':[''],
                   'Me - mail':[''],
                   'music - on_or_off':['on','off'],
                   'music - name':[],
                   'common - dark_mod':['on','off'],
                   'safe - password':['on','off'],
                   'plot - mode':setting_dict['all_plot_mode'],
                   'common - insert_way':['item','file'],
                   'info - add - mode':['item','outer','inner'],
                   'search - time_event':['on','off'],
                   'search - mode':['Search All','Search Template','Keywords'],
                   'common - palette':['Snow','Autumn','Warm Winter','Psychedelic','Strawberry','Jasmine','Mint','Jade-like stone white','Stock','Watercolor Painting','Chocolate'],
                   'common - language':['English','简体中文']}
    # 语言序号
    setting_dict['language_id'] = setting_dict['settingDict']['common - language'].index(setting_dict['language'])

    return setting_dict

def ini_palette(palette='Autumn',dark_mod='off'):
    ''' 页面颜色
    '''
    if dark_mod == 'on':
        # 暗黑模式
        COLOR_BACK = 'dimgray';COLOR_FRONT = 'white';COLOR_SUB = 'black';COLOR_MB_FRONT = 'black'
        COLOR_F1_BACK = 'black';COLOR_F2_BACK = "#383838";COLOR_F2_FRONT = "white"
    else: 
        # 非暗黑模式
        if palette == 'Snow':
            COLOR_BACK = '#F2F2F2';COLOR_FRONT = 'black';COLOR_SUB = '#F2F2F2';COLOR_MB_FRONT = 'black'
            COLOR_F1_BACK = '#F2F2F2';COLOR_F2_BACK = "#EDEDED";COLOR_F2_FRONT = "black"
        elif palette == 'Autumn':
            COLOR_BACK = 'floralwhite';COLOR_FRONT = 'black';COLOR_SUB = 'floralwhite';COLOR_MB_FRONT = 'black'
            COLOR_F1_BACK = 'floralwhite';COLOR_F2_BACK = "#FFF5EE";COLOR_F2_FRONT = "black"
        elif palette ==  'Warm Winter':
            COLOR_BACK = 'oldlace';COLOR_FRONT = 'black';COLOR_SUB = 'oldlace';COLOR_MB_FRONT = 'black'
            COLOR_F1_BACK = 'oldlace';COLOR_F2_BACK = "floralwhite";COLOR_F2_FRONT = "black"
        elif palette == 'Psychedelic':
            COLOR_BACK = 'aliceblue';COLOR_FRONT = 'black';COLOR_SUB = 'aliceblue';COLOR_MB_FRONT = 'black'
            COLOR_F1_BACK = 'aliceblue';COLOR_F2_BACK = "ghostwhite";COLOR_F2_FRONT = "black"
        elif palette == 'Strawberry':
            COLOR_BACK = '#e4c6d0';COLOR_FRONT = 'black';COLOR_SUB = '#e4c6d0';COLOR_MB_FRONT = 'black'
            COLOR_F1_BACK = '#e4c6d0';COLOR_F2_BACK = "#edd1d8";COLOR_F2_FRONT = "black"
        elif palette == 'Jasmine':
            COLOR_BACK = 'lavenderblush';COLOR_FRONT = 'black';COLOR_SUB = 'lavenderblush';COLOR_MB_FRONT = 'black'
            COLOR_F1_BACK = 'lavenderblush';COLOR_F2_BACK = "#fff0f1";COLOR_F2_FRONT = "black"
        elif palette == 'Mint':
            COLOR_BACK = '#F5FFFA';COLOR_FRONT = 'black';COLOR_SUB = '#F5FFFA';COLOR_MB_FRONT = 'black'
            COLOR_F1_BACK = '#F5FFFA';COLOR_F2_BACK = "#F1FFF0";COLOR_F2_FRONT = "black"
        elif palette == 'Jade-like stone white':
            COLOR_BACK = '#d6ecf0';COLOR_FRONT = 'black';COLOR_SUB = '#d6ecf0';COLOR_MB_FRONT = 'black'
            COLOR_F1_BACK = '#d6ecf0';COLOR_F2_BACK = "#f0fcff";COLOR_F2_FRONT = "black"
        elif palette == 'Stock':
            COLOR_BACK = '#F4DAB0';COLOR_FRONT = 'black';COLOR_SUB = '#F4DAB0';COLOR_MB_FRONT = 'black'
            COLOR_F1_BACK = '#F4DAB0';COLOR_F2_BACK = "bisque";COLOR_F2_FRONT = "black"
        elif palette == 'Watercolor Painting':
            COLOR_BACK = '#424c50';COLOR_FRONT = 'white';COLOR_SUB = '#424c50';COLOR_MB_FRONT = 'black'
            COLOR_F1_BACK = '#424c50';COLOR_F2_BACK = "#41555f";COLOR_F2_FRONT = "white"
        elif palette == 'Chocolate':
            COLOR_BACK = '#312520';COLOR_FRONT = 'white';COLOR_SUB = '#312520';COLOR_MB_FRONT = 'black'
            COLOR_F1_BACK = '#312520';COLOR_F2_BACK = "#4c221f";COLOR_F2_FRONT = "white"  
        else: # 按Warm Winter
            COLOR_BACK = 'oldlace';COLOR_FRONT = 'black';COLOR_SUB = 'oldlace';COLOR_MB_FRONT = 'black'
            COLOR_F1_BACK = 'oldlace';COLOR_F2_BACK = "floralwhite";COLOR_F2_FRONT = "black" 

        color_dict = {}
        color_dict["back"] = COLOR_BACK       # 背景颜色
        color_dict["front"] = COLOR_FRONT        # 字体颜色
        color_dict["cback"] = COLOR_SUB      # 组件背景颜色
        color_dict["mcfront"] = COLOR_MB_FRONT      # Mac系统按钮字体颜色  -- 对Mac按钮做出的适配
        color_dict["tback1"] = COLOR_F1_BACK     # 表格背景色1
        color_dict["tback2"] = COLOR_F2_BACK # 表格背景色2
        color_dict["tfront"] = COLOR_F2_FRONT       # 表格字体颜色

        '''
        # 设置表格颜色
        ttk.Style().configure("Treeview", background=color_dict["tback2"], foreground=color_dict["tfront"])

        # 设置下拉菜单颜色
        ttk.Style().configure("TCombobox", background=color_dict["tback2"], foreground=color_dict["tfront"])
        '''

        return color_dict

def ini_jieba(window,base_path):
    ''' jieba字典配置
    '''
    # 进行jiaba库字典的设置
    try:
        jieba.set_dictionary(base_path+"/resources/system/dict.txt")
        jieba.load_userdict(base_path+'/resources/system/dict.txt')
        jieba.initialize() # 这两步是为了打包 #http://blog.csdn.net/qq_26376175/article/details/69680992
    except:
        print("未进行jiaba库dict设置")
        messagebox.showinfo(parent=window,message='文件缺失! 无法进行任何内容的模糊搜索!\n请按照system文件夹中dict.txt中的提示进行操作')

def tabel_max_length(base_path):
    """ 计算数据表最大长度 """
    size = 8
    for item in loadDataset(base_path+'/resources/system/template/template.csv'):
        if len(item) > size:
            size = len(item)
    return size


