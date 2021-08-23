from websocket_server import WebsocketServer
import json
import socket
import os
import random

import server.password as password
import storage

import chardet

SERVER_WELCOME = True

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
    try:
        message = json.loads(message)
        if("type" in message):pass
    except:
        server.send_message(client,'{"reply":"400"}')
        return

    ''' 登陆
    接收用户名与密码. 如果用户名对应的密码为传入密码则允许登陆, 否则不允许登陆
    '''
    if message["type"] == "login":
        code = password.login(message['mail'],message['password'])
        server.send_message(client,reply_maker(code))

    #找回密码
    elif message["type"] == "find password":
        pass
    #注册新用户
    elif message["type"] == "regist":
        code = password.regist(message['mail'],message['password'])
        server.send_message(client,reply_maker(code))

    #添加数据仓库
    elif message["type"] == "creat_repository":
        storage.creat_repository(name=message['repo_name'],user_id=message['mail'])


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


def run():
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
    ip = get_host_ip()
    port = get_host_port()
    print("The server is run at:")
    print(" ip =",ip)
    print(" port =",port)
    print("\n---------------------------------------\n")

    # 将ip与port写入文件(ui模块需要)
    write_json('./server/setting.json',
        {'ip': ip,
        'port': port})
    f = open("./server/setting.json","r")
    setting = f.read()
    f.close()
    f = open("./server/setting.json","w")
    f.write("setting="+setting)
    f.close()

    # 启动服务器
    server = WebsocketServer(port, ip)
    server.set_fn_new_client(new_client)
    server.set_fn_client_left(client_left)
    server.set_fn_message_received(message_received)
    server.run_forever()