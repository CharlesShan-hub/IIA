from websocket_server import WebsocketServer
import threading
import json
import socket
import os
import sys
import random
import chardet
import base64

import server.auth as auth
import server.test as test
import server.dashboard as dashboard
from server.tool import *
import storage


SERVER_WELCOME = True
FILE_CLIENT_DICT = {}
Amazing_Phenomenon_Tag = 0


class ServerProcessThread(threading.Thread):
    def __init__(self,daemon=False):
        threading.Thread.__init__(self,daemon=daemon)
    def run(self):
        process()


def process():
    while(1):
        command = input()
        if command == 'HELP':
            print(""" IIA Server Help\
                \n STOP: Stop server(all clients lose connection)\
                \n clear: Clear Console Log""")
        elif command == 'STOP':
            print("Stop server. Input `YES` to continue stopping server:")
            if input() == 'YES':
                print("请点击窗口左上角红色按钮")
        elif command == 'clear':
            import os
            import sys
            if sys.platform == 'darwin' or sys.platform == 'linux':
                os.system("clear")
            else:
                os.system("cls")

class ServerThread(threading.Thread):
    def __init__(self,daemon=False):
        threading.Thread.__init__(self,daemon=daemon)
    def run(self):
        _run()


# 当新的客户端连接时会提示
def new_client(client, server):
    print("New connection:%s" % client['id'])
    #server.send_message_to_all("Hey all, a new client has joined us")


# 当旧的客户端离开
def client_left(client, server):
    print("Connection %s interrupt" % client['id'])


def change_unicode_to_str(message):
    temp=''
    for item in message.split(','):
        temp+=(chr(eval(item)))
    return temp

# 接收客户端的信息
def message_received(client, server, message):
    # 判断消息类型(文件,命令,错误)
    if(type(message)!=str):
        return
    if(message[0]!='{'):
        try:
            message=change_unicode_to_str(message)
        except:
            return

    try:#试试能不能找到type选项
        if("type" not in json.loads(message)):
            return # 错误格式的命令
    except:
        return

    message = json.loads(message)
    receive_command(message,client,server)


def receive_command(message,client,server):
    """ 接受命令
    """
    if message["type"] == "auth":
        ''' 身份验证部分
        * 登陆: 输入邮箱与密码, 判断是否对应
        * 注册: 输入邮箱与密码, 如果已有邮箱, 则注册失败
        * 找回密码: 第一次输入邮箱,验证码填"request"; 第二次输入邮箱与验证码
        * 修改密码: 第一次输入邮箱,验证码填"request"; 第二次输入邮箱与验证码与新密码
        '''
        do_auth(message,client,server)

    elif message["type"] == "dashboard":
        ''' 数据看板部分
        * 获取看板布局
        * 设置看板布局
        '''
        do_dashboard(message,client,server)

    elif message["type"] == "mission":
        ''' 任务部分
        * 创建任务
        '''
        pass

    elif message["type"] == "test":
        ''' 测试部分
        '''
        do_test(message,client,server)

    #添加数据仓库
    #elif message["type"] == "creat_repository":
    #    storage.creat_repository(name=message['repo_name'],user_id=message['mail'])
    

def do_auth(message,client,server):
    """ 进行身份验证相关操作
    """
    # 登陆
    if message["operate"] == "login":
        code = auth.login(message['mail'],message['password'])
        server.send_message(client,reply_maker(code))
    # 注册
    elif message["operate"] == "regist":
        code = auth.regist(message['mail'],message['password'],message['name'],message['code'])
        server.send_message(client,reply_maker(code))
    # 找回密码
    elif message["operate"] == "find password":
        code = auth.find_password(message['mail'],message['code'])
        server.send_message(client,reply_maker(code))
    # 修改密码
    elif message["operate"] == "change password":
        code = auth.change_password(message['mail'],message['code'],message['password'])
        server.send_message(client,reply_maker(code))
    # 记住身份
    elif message["operate"] == "remember":
        auth.remember_user(message['mail'])


def do_dashboard(message,client,server):
    """ 进行数据展板相关操作
    """
    # 获取数据展板模板
    if message["operate"] == "init":
        server.send_message(client,str(dashboard.get_layout(message["mail"])))
    elif message["operate"] == "set":
        dashboard.set_layout(message["mail"],message["layout"])


def do_test(message,client,server):
    """ 进行测试相关操作
    """
    # ping
    if message["operate"] == "ping":
        code = test.ping(int(message["param"]))
        server.send_message(client,reply_maker(code))
    # 接收上传文件 - 客户端:请求发送文件,文件内容,报告发送完毕
    if message["operate"] == "upload file":
        if message["state"] == "start":
            key = client['address'][0]+str(client['address'][1])
            if(key in FILE_CLIENT_DICT):
                server.send_message(client,reply_maker(403))
            else:
                file = open("./test/"+message['name'],'wb')
                FILE_CLIENT_DICT[key]={
                    'temp':"",
                    'content':b"",
                    'len':message['len'],
                    'file':file
                }
        elif message["state"] == "end":
            key = client['address'][0]+str(client['address'][1])
            print("CLOSE!!!!")
            FILE_CLIENT_DICT[key]['file'].close()
            del FILE_CLIENT_DICT[key]
        elif message["state"] == "send":
            key = client['address'][0]+str(client['address'][1])
            try:
                message["content"] = message["content"].split(',',1)[1]
            except:
                pass
            if("tag" in message):# 分片不完整
                if(message["tag"]==0): # 不是最后一片
                    FILE_CLIENT_DICT[key]['temp']+=message["content"]
                elif(message["tag"]==1): # 是最后一片
                    temp=bytes.decode(str.encode(FILE_CLIENT_DICT[key]['temp']))
                    print(temp[-50:],len(temp))
                    try:
                        content = base64.b64decode(str.encode(temp))
                    except:
                        #print(temp)
                        #print("1Wrong!!!!!!")
                        FILE_CLIENT_DICT[key]['file'].close()
                        return
                    FILE_CLIENT_DICT[key]['file'].write(content)
            else: # 分片完整
                temp=bytes.decode(str.encode(message["content"]))
                #print(message["sequence"],'/',FILE_CLIENT_DICT[key]['len'],temp[-50:],len(temp))
                try:
                    content = base64.b64decode(str.encode(temp))
                except:
                    print(temp)
                    print("2Wrong!!!!!!")
                    FILE_CLIENT_DICT[key]['file'].close()
                    content = base64.b64decode(str.encode(temp))
                    return
                FILE_CLIENT_DICT[key]['file'].write(content)
                #FILE_CLIENT_DICT[key]['content']+=content

    # 发送下载文件
    #if message["operate"] == "download file":
    #    pass
    #server.send_message(client,reply_maker(code))


def _run():
    # Server welcome info
    if SERVER_WELCOME == True:
        print(" ---------------------------------------\n")
        print(" Welcome to IIA Server!")
        print("""
      ___________ 
     /  _/  _/   |
     / / / // /| |
   _/ /_/ // ___ |
  /___/___/_/  |_|
                
""")
        print(" Author: Charles Shan")
        print(" Mail: charles.shht@gmail.com")
        print("\n---------------------------------------\n")

        print(" Input 'HELP' to see what IIA Sever can do!\n")
        #print("Input 'STOP' to shut down the sever safely!")
        #print("Input 'STOP_FORCED' to shut down the sever directly!\n")
        
    # 获取目前运行的ip与port
    IP = get_host_ip()
    port = get_host_port()
    
    # 将ip与port写入文件(ui模块需要)
    write_json('./server/setting.json',
        {'ip': IP,
        'port': port})
    f = open("./server/setting.json","r")
    setting = f.read()
    f.close()
    f = open("./server/setting.json","w")
    f.write("setting="+setting)
    f.close()

    # 启动服务器处理进程 - ServerProcess
    server_process_thread = ServerProcessThread(daemon=True)
    server_process_thread.start()

    # 启动连接服务器 - WebsocketServer
    #print(type(port),type(IP))
    server = WebsocketServer(port, IP)
    server.set_fn_new_client(new_client)
    server.set_fn_client_left(client_left)
    server.set_fn_message_received(message_received)
    print("The Node Server log:")
    server.run_forever()