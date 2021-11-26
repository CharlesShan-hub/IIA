""" 测试前端运行环境
"""

try:
    from PyQt5.QtCore import *
    from PyQt5.QtGui import *
    from PyQt5.QtWidgets import *
except:
    print("* UI - 第三方库pyqt5导入\npip install pyqt5")

try:
    from PyQt5.QtWebEngineWidgets import *
except:
    print("* UI - 第三方库pyqt5导入\npip install PyQtWebEngine")


def test_ui():
    pass


def test():
    ''' IIA-运行环境测试
    '''
    pass

if __name__ == '__main__':
    test()

"""
import threading
import sys
import server
from http.server import HTTPServer, SimpleHTTPRequestHandler

class ServerThread(threading.Thread):
    def __init__(self,daemon=False):
        print("Preparing Node Server...")
        threading.Thread.__init__(self,daemon=daemon)
    def run(self):
        server.run()

class HTTPThread(threading.Thread):
    def __init__(self,ip,port=None,daemon=False):
        print("Preparing HTTP Server...")
        self.ip=ip
        if port==None:
            self.port=server.get_host_port()
        else:
            self.port = port
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
# Related HTML file entry path
HTML = "/ui/html/login.html"

# Test Mode - Run in test mode
TEST_MODE = False

# Local Mode - Run as a Local software
SERVER_MODE = 'Local'

# Server Mode - Run server only
SERVER_MODE = 'Server'

# Client Mode - Run client only
#SERVER_MODE = 'Client'

# Community Mode - Run as a community server 
#SERVER_MODE = 'Community'

if __name__ == "__main__":
    if(len(sys.argv)>1 and sys.argv[1]=='clear'):
        print("Clear log and caches!")
        server.os.remove("./logger/log.txt")
        sys.exit()

    if(len(sys.argv)>1 and sys.argv[1]=='test'):
        print("Open Test Mode!")
        TEST_MODE = True


    if SERVER_MODE not in ['Local','Server','Client','Community']:
        exit()

    # Local Mode - Run as a Local software
    if SERVER_MODE == 'Local':
        server_thread = ServerThread(daemon=True)
        server_thread.start()
        http_thread = HTTPThread(ip=server.get_host_ip(),port=80,daemon=True)
        http_thread.start()
        import ui
        ui.run(HTML,TEST_MODE)

    # Server Mode - Run server only
    if SERVER_MODE == 'Server':
        server_thread = ServerThread()
        server_thread.start()
        http_thread = HTTPThread(ip=server.get_host_ip(),port=80,daemon=True)
        http_thread.start()
        
    # Client Mode - Run client only
    if SERVER_MODE == 'Client':
        import ui
        ui.run(HTML,TEST_MODE)

    # Community Mode - Run as a community server 
    if SERVER_MODE == 'Community':
        pass

"""
