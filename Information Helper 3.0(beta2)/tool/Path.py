import os
from tool.CSVTool import *

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

def update_infor_path(basename):
    ''' Update the infor_path.txt file 更新infor_path.txt文件
    To support user-defined folders, we need to get the latest location of 
    each information file before the program starts or each information-related 
    operation. This function is to iterate over all the.txt files in the user 
    directory and store the directory in infor_path.txt.
    
    为了支持用户自定义文件夹, 在程序开始或每一次与信息相关的操作前,需要获得最新的每个信息
    文件存储地址. 本函数就是遍历所有user目录下的.csv文件然后将目录存在infor_path.csv中.
    ''' 
    #print("更新信息路径文件")
    ls = [] ; list_dir(basename+'/resources/user',ls,'.csv')
    ls_write = []
    for item in ls:
        ls_item = [];ls_item.append(item);ls_write.append(ls_item)
    csvWriterLines(ls_write,basename+'/resources/system/template/infor_path.csv','w')

def find_infor_path(name,basename,update_infor_path_=False,default_home='./resources/user/',type='look path'):
    ''' Find the information file address 寻找信息文件地址
    Find the address of the information file for a particular template. 
    Take a template name, look for it in infor_path.txt, 
    return the address if found, print an error.
    
    寻找特定模板的信息文件地址.接受一个模板名称, 在infor_path.csv中进行寻找,
    如果由则返回地址,未找到则输出错误.
    
    :param name: The template name of the file to search 要搜索的文件的模板名
    :param update_infor_path_: (optional) Whether to update the address file of the infor file 是否更新信息文件的地址文件
    :param type: (optional)'look path'为找到某个地址, 'if exist'为判断是否存在
    :return line: path 地址
    '''
    if update_infor_path_: update_infor_path(basename)
    path = './resources/system/template/infor_path.csv'
    for line in loadDataset(path):
        #print('line',line)
        name_ = os.path.basename(line[0]).split('.')[0]
        #name_ = line[0].split('/')[-1].split('.')[0]
        if name_ == name: return line[0]
    #print("未找到模板:",name)
    if type=='look path':
        return default_home+name+'.csv'
    elif type=='if exist':
        return False

def getAllItem(path,_type,_from='folder'):
    ''' 获取所有某种文件名 '''
    if _from == 'folder':
        ls = [] ; list_dir(path,ls,_type)
        return ls
    elif _from == 'template':
        ls = []
        for item in loadDataset(path):
            ls.append(item[0]+'.csv')
        return ls

def un_repeat_name(name,path,_type='.csv',_from='folder'):
    ''' 获得不重复的名字
    参数说明: 
    _from: 'folder'说明获取某文件夹内的不重复得名字
           'template'说明获取的是模板名
    '''
    if len(getAllItem(path=path,_type=_type,_from=_from)) == 0: 
        return name
    loop = True
    number = 0
    while(loop):
        _checkName = getAllItem(path=path,_type=_type,_from=_from)
        for item in _checkName:
            loop = False
            if number == 0:
                if name+_type == os.path.basename(item):
                    number = number+1
                    loop = True
                    break
            if number!=0: 
                if name+str(number)+_type == os.path.basename(item):
                    number = number+1
                    loop = True
                    break
    if number!=0:
         name = name + str(number)
    return name



