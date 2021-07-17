# pip install websocket-server
from websocket_server import WebsocketServer

 
# 当新的客户端连接时会提示
def new_client(client, server):
    print("当新的客户端连接时会提示:%s" % client['id'])
    server.send_message_to_all("Hey all, a new client has joined us")
 
 
# 当旧的客户端离开
def client_left(client, server):
    print("客户端%s断开" % client['id'])
 
 
# 接收客户端的信息。
def message_received(client, server, message):
    print("Client(%d) said: %s" % (client['id'], message))
    server.send_message_to_all(message)
 
 
def run():
    server = WebsocketServer(12345, "127.0.0.1")
    server.set_fn_new_client(new_client)
    server.set_fn_client_left(client_left)
    server.set_fn_message_received(message_received)
    server.run_forever()