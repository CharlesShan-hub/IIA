import os
import random
import threading
import signal
import socket
import json

global ser
global shutdown_flag
global input_word
shutdown_flag = False
input_word = None

class Logger:                                                                      
        HEADER = '\033[95m'                                                        
        OKBLUE = '\033[94m'                                                        
        OKGREEN = '\033[92m'                                                       
        WARNING = '\033[93m'                                                       
        FAIL = '\033[91m'                                                          
        ENDC = '\033[0m'                                                           
        @staticmethod                                                              
        def log_normal(info):                                                      
                print(Logger.OKBLUE + info + Logger.ENDC)                           
        @staticmethod                                                              
        def log_high(info):                                                        
                print(Logger.HEADER + info + Logger.ENDC)                        
        @staticmethod                                                              
        def log_fail(info):                                                        
                print(Logger.FAIL + info + Logger.ENDC)

#Logger.log_normal("This is a normal message!")
#Logger.log_fail("This is a fail message!")
#Logger.log_high("This is a high-light message!")

class ListenThread(threading.Thread):
    def __init__(self,threadID):
        threading.Thread.__init__(self)
        self.threadID = threadID
    def run(self,buffer_size=512):
        global ser
        global shutdown_flag
        while 1:
            try:
                # Wait for connector
                if shutdown_flag==False:
                    print(self.threadID,"Waiting for new connector...")
                con,address=ser.accept() # 在这个位置进行等待，监听端口号 
                print(self.threadID,"get user.")
                
                # Receive the json info package
                msg = con.recv(buffer_size).decode("utf-8")
                try:
                    msg_json = eval(msg)
                except:
                    print(type(msg)) # 这两个print是测试
                    print("-----"+msg+"-----")
                    continue
                try:
                    package_type = msg_json["type"]
                except:
                    Logger.log_fail(str(self.threadID)+" get wrong type message and refused.")
                    con.send("failed: Support json package head only!".encode())
                    continue

                # Get Str
                if(msg_json["type"]=="Str"):
                    print(self.threadID,'Get Message(String): ',msg_json["content"])
                    reply_str = "send str successful"

                # Get File
                elif(msg_json["type"]=="File"):
                    filename = msg_json["name"]
                    filesize = msg_json["size"]
                    print(self.threadID,'Get Message(File): ',filename)
                    filepath = "./resources/"+filename
                    if not os.path.exists("./resources"):
                        os.makedirs("./resources")
                    recvd_size = 0  # 定义已接收文件的大小
                    fp = open(filepath, 'wb')
                    while not recvd_size == filesize:
                        if filesize - recvd_size > buffer_size:
                            data = con.recv(buffer_size)
                            recvd_size += len(data)
                        else:
                            data = con.recv(filesize - recvd_size)
                            recvd_size = filesize
                        fp.write(data)
                    fp.close()
                    reply_str = filename+" send successful"

                # Get Str reply
                elif(msg_json["type"]=="Ask"):
                    #if(msg_json["content"]=="Test"):
                    print(self.threadID,'Get Message(Ask): ',msg_json["content"])
                    # construct reply string
                    # ---
                    # ---  Type code here
                    # ---
                    reply_str = "Hello I'm "+str(self.threadID)

                # Get File by file path(wrong info return a str)
                elif (msg_json["type"]=="LoadFile"):
                    filepath = "./resources/"+msg_json["path"]
                    if os.path.isfile(filepath) == True:
                        print(self.threadID,"transmit file",msg_json["path"],"...")
                        filesize = os.stat(filepath).st_size
                        sendData = {
                            "type": "LoadFile-Reply",
                            "valid": True,
                            "name": os.path.basename(filepath),
                            "size": filesize
                        }
                        con.send(repr(sendData).encode("utf-8"))
                        # Send file
                        fo = open(filepath,'rb')
                        sendsize = filesize
                        while True:
                            #print(sendsize)
                            if(sendsize < buffer_size):
                                filedata = fo.read(sendsize)
                                con.send(filedata)
                                break
                            else:
                                filedata = fo.read(buffer_size)
                                sendsize = sendsize - buffer_size
                                con.send(filedata)
                        fo.close()
                        print('send over...')
                    else:
                        print(self.threadID,"File path",msg_json["path"],"is not aviliable!")
                        sendData = {
                            "type": "LoadFile-Reply",
                            "valid": False,
                        }
                        con.send(repr(sendData).encode("utf-8"))
                        Logger.log_fail(str(self.threadID)+" get wrong file request and refused.")
                    continue

                # Unkonw type
                else:
                    print("Unkonw type")

            except ConnectionAbortedError:
                print("Stop sever",self.threadID)
                break

            # Judge wheather is the last connection
            if shutdown_flag == False:
                con.send(reply_str.encode())
            else:
                print("Connectted sever stoped",self.threadID)
                con.send((reply_str+" (now sever shutdown)").encode())
                break


class ShutDownThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        global input_word
        while 1:
            input_word = input()
            if(input_word=='STOP'):
                # 以后要求输入账号密码
                print("starting shutdown sever safely")
                global shutdown_flag
                shutdown_flag=True
                ser.close()
                exit()
            elif(input_word=='STOP_FORCED'):
                # 以后要求输入账号密码
                print("starting shutdown sever directly")
                os._exit(0)
            elif(input_word=='HELP'):
                #Logger.log_normal("This is a normal message!")
                Logger.log_normal("\n * Info\n"\
                " - IIA-Sever can do more and more things!\n"\
                " - Receive a dict head to identify the package type.\n"\
                "\n * Receive\n"\
                " - `Str` type: Just say received successful\n"\
                " - `File` type: Save the file on the same dictionary\n"\
                "\n * Reply(`Ask` type)\n"\
                " - `Ask` type: Send a str and reply a str (like `Str`)\n"\
                " - `LoadFile` type: Get File by file path(wrong info return a str)\n"\
                "\n * Input\n"\
                " - Input `STOP`: starting shutdown sever safely, only all connection is finished, the sever closed.\n"\
                " - Input `STOP_FORCED`: shutdown the sever immediately\n")
            elif(input_word=='help'):
                Logger.log_fail("Are you going to input `HELP`?")
            else:
                Logger.log_fail("Could not find command - "+str(input_word))


def run_sever(ip_port,buffer_size=512,back_log=5,welcome_info=True):
    """
    Single User Sever function
    Version1
    """
    if welcome_info==True:
        print("---------------------------------------\n")
        print("Welcome to IIA socket function!")
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

        Logger.log_high("Input 'HELP' to see what IIA-Sever can do!")
        Logger.log_high("Input 'STOP' to shut down the sever safely!")
        Logger.log_high("Input 'STOP_FORCED' to shut down the sever directly!\n")
        
    global ser
    ser = socket.socket(socket.AF_INET,socket.SOCK_STREAM)   # 套接字类型AF_INET, socket.SOCK_STREAM   tcp协议，基于流式的协议
    ser.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)  # 对socket的配置重用ip和端口号
    # 绑定端口号
    ser.bind(ip_port)  #  写哪个ip就要运行在哪台机器上
    # 设置半连接池
    ser.listen(back_log)  # 最多可以连接n个客户端
    # 创建进程
    shut_down_listener = ShutDownThread()
    thread_listen = []
    for i in range(back_log):
        thread_listen.append(ListenThread(i))
    for item in thread_listen:
        item.start()
    shut_down_listener.start()
    for item in thread_listen:
        item.join()
    shut_down_listener.join()
    
    # 关闭服务器
    ser.close()

def get_host_ip():
    """
    get host ip
    :return: ip
    """
    try:
        s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        s.connect(('8.8.8.8',80))
        ip=s.getsockname()[0]
    finally:
        s.close()

    return ip

def get_host_port():
    pscmd = "netstat -ntl |grep -v Active| grep -v Proto|awk '{print $4}'|awk -F: '{print $NF}'"
    procs = os.popen(pscmd).read()
    procarr = procs.split("\n")
    #tt= random.randint(15000,20000)
    tt = 12345
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
    ip = get_host_ip()
    port = get_host_port()
    print("ip =",ip)
    print("port =",port)
    write_json('./server/setting.json',
        {'ip': ip,
        'port': port})
    run_sever((ip,port))
