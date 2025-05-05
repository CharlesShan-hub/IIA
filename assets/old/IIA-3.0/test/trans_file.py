#trans_file.py
from websocket_server import WebsocketServer
import threading
import json
import socket
import os
import sys
import random
import chardet
import base64
#from ..server.tool import *

# 获取目前运行的ip与port
IP = "192.168.1.108"
PORT = 8080

server = WebsocketServer(PORT, IP)

# 当新的客户端连接时会提示
def new_client(client, server):
    print("New connection:%s" % client['id'])
    #server.send_message_to_all("Hey all, a new client has joined us")


# 当旧的客户端离开
def client_left(client, server):
    print("Connection %s interrupt" % client['id'])


# 接收到消息
def message_received(client, server, message):
	print(len(message))
	print(message)
	with open("./temp_file",'w') as f:
		f.write(message)


server.set_fn_new_client(new_client)
server.set_fn_client_left(client_left)
server.set_fn_message_received(message_received)
server.run_forever()

