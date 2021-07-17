from websocket_server import WebsocketServer
import json
import socket
import os
import random

NAME = 'Charles'
PASSWORD = '263513'

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
    # 登陆请求
    if message["type"] == "login":
        if(message['name']==NAME and message['password']==PASSWORD):
            print("认证正确!允许登陆")
            server.send_message(client,'{"reply":"100"}')
        else:
            print("认证错误!不允许登陆")
            server.send_message(client,'{"reply":"403"}')


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
    tt= random.randint(15000,20000)
    #tt = 12345
    if tt not in procarr:
        return tt
    else:
        return get_host_port()


def load_json(path,encoding='UTF-8'):
    ''' 获取数据
    :param path: 数据集路径
    :param encoding(optional): 编码类型
    :return data: 获取的数据
    '''
    with open(path, 'r', encoding='UTF-8') as f:
        data = json.load(f)    #此时a是一个字典对象
    #logger.info("Load json - "+path)
    return data


def write_json(path, content, encoding='UTF-8'):
    ''' json写入数据
    '''
    #logger.info("Write json - "+path)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(json.dumps(content, indent=4, ensure_ascii=False))

 
def run():
    # 获取目前运行的ip与port
    ip = get_host_ip()
    port = get_host_port()
    print("ip =",ip)
    print("port =",port)

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