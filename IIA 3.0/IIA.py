import threading
import server
import ui
import os
import time

from http.server import HTTPServer, SimpleHTTPRequestHandler

class ServerThread(threading.Thread):
    def __init__(self,daemon=False):
        print("Preparing Node Server...")
        threading.Thread.__init__(self,daemon=daemon)
    def run(self):
        server.run()

class HTTPThread(threading.Thread):
    def __init__(self,ip,daemon=False):
        print("Preparing HTTP Server...")
        self.ip=ip
        self.port=server.get_host_port()
        threading.Thread.__init__(self,daemon=daemon)
    def run(self):
        try:
            server = HTTPServer((self.ip, self.port), SimpleHTTPRequestHandler)
            print("HTTP Server is running at:")
            print("http://"+self.ip+":"+str(self.port))
            print("\n---------------------------------------\n")
            server.serve_forever()
        except:
            server.get_host_port()
            server = HTTPServer((self.ip, self.port), SimpleHTTPRequestHandler)
            print("HTTP Server is running at:")
            print("http://"+self.ip+":"+str(self.port))
            print("\n---------------------------------------\n")
            server.serve_forever()

''' IIA - Intelligent Information Assistant
    This is the main file.
'''
# Local Mode - Run as a Local software
SERVER_MODE = 'Local'

# Server Mode - Run server only
#SERVER_MODE = 'Server'

# Client Mode - Run client only
#SERVER_MODE = 'Client'

# Community Mode - Run as a community server 
#SERVER_MODE = 'Community'

if __name__ == "__main__":
    if SERVER_MODE not in ['Local','Server','Client','Community']:
        exit()

    # Local Mode - Run as a Local software
    if SERVER_MODE == 'Local':
        server_thread = ServerThread(daemon=True)
        server_thread.start()
        http_thread = HTTPThread(ip=server.get_host_ip(),daemon=True)
        http_thread.start()
        ui.run()

    # Server Mode - Run server only
    if SERVER_MODE == 'Server':
        server_thread = ServerThread()
        server_thread.start()
        #http_thread = HTTPThread()
        #http_thread.start()
        
    # Client Mode - Run client only
    if SERVER_MODE == 'Client':
        ui.run()

    # Community Mode - Run as a community server 
    if SERVER_MODE == 'Community':
        pass

    