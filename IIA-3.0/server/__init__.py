from websocket_server import WebsocketServer
import threading
import json
import socket
import os
import random

import server.auth as auth
import server.test as test
import storage

import chardet

SERVER_WELCOME = True
IP = '127.0.0.1'

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


# 接收客户端的信息
def message_received(client, server, message):
    # 获取正确格式信息
    if message_received_valid(message,client,server)!=True:
        return

    message = json.loads(message)

    if message["type"] == "auth":
        ''' 身份验证部分
        * 登陆: 输入邮箱与密码, 判断是否对应
        * 注册: 输入邮箱与密码, 如果已有邮箱, 则注册失败
        * 找回密码: 第一次输入邮箱,验证码填"request"; 第二次输入邮箱与验证码
        '''
        do_auth(message,client,server)

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


def message_received_valid(message,client,server):
    """ 验证消息格式
    """
    try:
        if("type" in json.loads(message)):pass
        return True
    except:
        server.send_message(client,'{"reply":"400"}')
        return False

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


def do_test(message,client,server):
    """ 进行测试相关操作
    """
    # ping
    if message["operate"] == "ping":
        code = test.ping(int(message["param"]))
        server.send_message(client,reply_maker(code))

def reply_maker(code):
    return '{"reply":"'+str(code)+'"}'


def get_host_ip():
    """
    get host ip
    :return: ip
    """
    try:
        s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        s.connect(('8.8.8.8',80))
        ip=s.getsockname()[0]
    except:
        ip='127.0.0.1'
    finally:
        s.close()

    return ip

def get_host_port():
    pscmd = "netstat -ntl |grep -v Active| grep -v Proto|awk '{print $4}'|awk -F: '{print $NF}'"
    procs = os.popen(pscmd).read()
    procarr = procs.split("\n")
    tt= random.randint(1024,49151)#服务端口号
    #tt = 12345
    if tt not in procarr:
        return tt
    else:
        return get_host_port()


def write_json(path, content, encoding='UTF-8'):
    ''' json写入数据
    '''
    #logger.info("Write json - "+path)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(json.dumps(content, indent=4, ensure_ascii=False))


def _run():
    # Server welcome info
    if SERVER_WELCOME == True:
        print("---------------------------------------\n")
        print("Welcome to IIA Server!")
        print("""
      ___________ 
     /  _/  _/   |
     / / / // /| |
   _/ /_/ // ___ |
  /___/___/_/  |_|
                
""")
        print("Author: Charles Shan")
        print("Mail: charles.shht@gmail.com")
        print("\n---------------------------------------\n")

        #print("Input 'HELP' to see what IIA Sever can do!")
        #print("Input 'STOP' to shut down the sever safely!")
        #print("Input 'STOP_FORCED' to shut down the sever directly!\n")
        
    # 获取目前运行的ip与port
    global IP
    IP = get_host_ip()
    port = get_host_port()
    #print("Node Server is running at:")
    #print(" ip =",IP)
    #print(" port =",port)
    #print("\n---------------------------------------\n")

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

    # 启动服务器
    #print(type(port),type(IP))
    server = WebsocketServer(port, IP)
    server.set_fn_new_client(new_client)
    server.set_fn_client_left(client_left)
    server.set_fn_message_received(message_received)
    print("The Node Server log:")
    server.run_forever()