import csv
import sys
import os

def loadDataset(path,encoding='UTF-8'):
    ''' 获取数据
    :param path: 数据集路径
    :return data: 获取的数据
    '''
    data = []
    with open(path, 'r', encoding=encoding) as f:
        for line in csv.reader(f):
            data.append(line)
    return data

def csvWriter(thing,path,mode='a+',encoding='utf-8'):
    ''' csv文件数据添加
        将一行数据添加到csv格式的文件中, 注意thing的类型为列表
    '''
    try:
        f = open(path, mode, encoding=encoding)
        if thing != None:
            csv_writer = csv.writer(f)
            csv_writer.writerow(thing)
        f.close()
        return True
    except:
        print('csvWriter Failed!')
        return False

def csvWriterLines(data,path,mode='w',encoding='utf-8'):
    ''' 将多行写入CSV中
    '''
    if mode == 'w':
        #os.remove(path) # 不知道为啥'w'不会覆盖写， 出此下策
        if data == None:
            csvWriter(None,path,'a+',encoding=encoding)
            return True
        for count in range(len(data)):
            if count:
                csvWriter(data[count],path,'a+',encoding=encoding)
            else: #第一行
                csvWriter(data[count],path,'w',encoding=encoding)
    elif mode == 'a+':
        if data == None:
            csvWriter(None,path,'a+',encoding=encoding)
            return True
        for count in range(len(data)):
            csvWriter(data[count],path,'a+',encoding=encoding)

def listToList(origin):
    '''
    '''
    for count in range(len(origin)):
        origin[count] = [origin[count]]
    return origin

def changeWord(path,origin,new,encoding='utf-8',match=False):
    ''' 修改csv文件的某一行
    origin与new都需要是列表
    '''
    try:
        # 加载数据
        data = loadDataset(path)
        change = False
        # 判断是否找到对应行
        for count in range(len(data)):
            if data[count] == origin:
                data[count] = new
                change = True
                break 
            if match:
                if len(data[count]) <= len(origin): change = False
                elif data[count][:len(origin)] == origin:
                    data[count] = new
                    change = True
                    break   
        if new == None:
            del data[count]
        if change:
            f = open(path, 'w', encoding=encoding, newline="")
            csv_writer = csv.writer(f)
            for line in data:
                if line: csv_writer.writerow(line)
            f.close()
            return True
        return False
    except:
        print("保存失败")
        return False

def get_setting(items=[], default=""):
    ''' 获得设置文件中的内容
    :params items: 设置项的具体内容, 类型为列表
    :params path: (optional)设置文件的地址
    :params path: (optional)设置文件的地址
    :return : 返回一个字符串,是特定信息的设置
    '''
    path = os.getcwd()+'/resources/system/setting/setting.csv'
    # 读取信息
    if len(items): # 列表中传入了元素
        for line in loadDataset(path):
            if len(line)>=len(items):
                if line[:len(items)] == items:
                    return line[len(items)]
    return default
