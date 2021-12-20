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
    def __init__(self,ip,port=None,daemon=False,auto=False):
        print("Preparing HTTP Server...")
        self.ip=ip
        self.auto=auto
        if port==None:
            self.port=server.get_host_port()
        else:
            self.port = port
        threading.Thread.__init__(self,daemon=daemon)
    def run(self):
        try:
            server_ = HTTPServer((self.ip, self.port), SimpleHTTPRequestHandler)
            self.server = server_
            print("HTTP Server is running at:")
            web_path = "http://"+self.ip+":"+str(self.port)
            print(web_path)
            import webbrowser
            webbrowser.open(web_path)
            print("\n---------------------------------------\n")
            server_.serve_forever()

        except:
            self.port = server.get_host_port()
            server_ = HTTPServer((self.ip, self.port), SimpleHTTPRequestHandler)
            self.server = server_
            print("HTTP Server is running at:")
            web_path = "http://"+self.ip+":"+str(self.port)
            print(web_path)
            import webbrowser
            webbrowser.open(web_path)
            print("\n---------------------------------------\n")
            server_.serve_forever()
            
    def exit(self):
        self.server.shutdown()

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
        #server.os.remove("./logger/log.txt")
        with open("./logger/log.txt",'w'):
            print("Clear log and caches!")
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
        http_thread = HTTPThread(ip=server.get_host_ip(),port=80,daemon=True,auto=False)
        http_thread.start()
        import ui
        ui.run(HTML,TEST_MODE)

    # Server Mode - Run server only
    if SERVER_MODE == 'Server':
        server_thread = ServerThread(daemon=True)
        server_thread.start()
        http_thread = HTTPThread(ip=server.get_host_ip(),port=80,daemon=True,auto=True)
        http_thread.start()
        print("【INPUT `quit` to stop the server!】")
        while(1):
            ans = input()
            if ans == 'quit':
                break
        sys.exit()
        #http_thread.exit()
        
    # Client Mode - Run client only
    if SERVER_MODE == 'Client':
        import ui
        ui.run(HTML,TEST_MODE)

    # Community Mode - Run as a community server 
    if SERVER_MODE == 'Community':
        pass
    