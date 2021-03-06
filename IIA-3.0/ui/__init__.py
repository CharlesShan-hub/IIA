from http.server import HTTPServer, SimpleHTTPRequestHandler
import cgi
import threading
import sys
import os

import setting
import logger

'''
    Check Path and File existence
'''
# Folders
if os.path.exists('./ui') == False:
    os.makedirs('./ui')
# Files
if os.path.exists("./ui/setting.json") == False:
    import setting
    setting.initialize("./ui/setting.json",{"default_mail":""},"local_setting")


__all__ = [
        'run',
        'test_run'
        ]

""" Init
"""
LOG_MODULE = "UI"


try:
    UI_ENGINE = 'QT'

    from PyQt5.QtCore import *
    from PyQt5.QtGui import *
    from PyQt5.QtWidgets import *
    from PyQt5.QtWebEngineWidgets import *

    class MainWindow(QMainWindow):
        def __init__(self,path):
            super(MainWindow, self).__init__()
            self.setWindowTitle('IIA')
            self.setGeometry(30,50,1000,618)
            self.browser=QWebEngineView()
            self.browser.load(QUrl(path))
            self.setCentralWidget(self.browser)
    logger.debug("Generated QT Engine",LOG_MODULE)
except:
    try:
        UI_ENGINE = 'WX'

        import wx
        from wx.html2 import WebView

        class MyHtmlFrame(wx.Frame):
            def __init__(self, parent, title,path):
                wx.Frame.__init__(self, parent, -1, title, size=(1000, 618))
                web_view =WebView.New(self)
                #web_view.LoadURL("127.0.0.1:"+str(setting.get(['Server','port'])))
                web_view.LoadURL(path)
        logger.debug("Generated WX Engine",LOG_MODULE)
    except:
        UI_ENGINE = None
        logger.error("Can't open desktop window!",LOG_MODULE)
        import sys
        sys.exit()


class FormDataReader():
    def __init__(self,data):
        temp = data.split(b'------WebKitFormBoundary')[1:-1]
        self.file=temp[-1].split(b'\r\n')[-2]

class ServerHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        SimpleHTTPRequestHandler.do_GET(self)
 
    def do_POST(self):
        content_length = int(self.headers.get('Content-Length'))
        reader = FormDataReader(self.rfile.read(content_length))
        #print(reader.file)
        with open('./test/temp','wb') as f:
            f.write(reader.file)
    #    #datas = self.rfile.read(int(self.headers['content-length']))

    #    #print('headers', self.headers)
    #    #print("do post:", self.path, self.client_address, datas)
    #    print("Do Post!!!")
    #    SimpleHTTPRequestHandler.do_POST(self)


class HTTPThread(threading.Thread):
    def __init__(self,ip,port,daemon=False,auto=False,CON_OPEN_WEB=False):
        self.ip=ip
        self.auto=auto
        self.web=CON_OPEN_WEB
        self.port = port
        threading.Thread.__init__(self,daemon=daemon)
    def run(self):
        try:
            web_path = "http://"+self.ip+":"+str(self.port)
            line = "\n\n---------------------------------------\n"
            print("HTTP Server is running at:\n",web_path,line)
            server_ = HTTPServer((self.ip, self.port), ServerHandler)#SimpleHTTPRequestHandler)
            self.server = server_
            if self.web:
                import webbrowser
                webbrowser.open(web_path)
                logger.debug("Opened WebView Page",LOG_MODULE)
            server_.serve_forever()

        except KeyboardInterrupt:
            print("Good Bye!")
            
    def exit(self):
        self.server.shutdown()


def run_qt_engine(path):
    app=QApplication(sys.argv)
    app.setWindowIcon(QIcon('./ui/html/assets/images/favicon.ico'))
    win=MainWindow(path)
    win.show()
    app.exit(app.exec_())

def run_wx_engine(path):
    app = wx.App()
    icon = wx.Icon(name="./ui/html/assets/images/favicon.ico",type=wx.BITMAP_TYPE_ICO)
    win = MyHtmlFrame(None, 'IIA',path)
    win.SetIcon(icon)
    win.Show()
    app.MainLoop()

def run_occupied():
    try:
        while 1:
            ans = input()
            if ans == 'quit':
                break
        sys.exit()
    except KeyboardInterrupt:
        print("Good Bye!")
        sys.exit()

def run(HTML_PATH,TEST_PATH,TEST_MODE,CON_OPEN_WIN,\
    CON_OPEN_WEB,CON_SHARE,CON_80_PORT):
    ''' ??????UI
    HTML_PATH??? UI?????????????????????HTML????????????
    TEST_MODE???????????????????????????
    OPEN_WIN?????????????????????????????????
    OPEN_WEB????????????????????????????????????
    SHARE????????????????????????
    80_PORT?????????????????????80??????
    '''
    if TEST_MODE==True:
        PATH="file://"+os.getcwd()+TEST_PATH
    else:
        PATH="file://"+os.getcwd()+HTML_PATH

    if CON_SHARE==False:
        http_server_ip = '127.0.0.1'
    else:
        from system.network import get_host_ip
        http_server_ip = get_host_ip()
    if CON_80_PORT:
        http_server_port=80
    else:
        from system.network import get_host_port
        http_server_port = get_host_port()
    import setting
    setting.set(['Server','ip'],http_server_ip)
    setting.set(['Server','port'],http_server_port)

    if CON_SHARE==True:
        http_thread = HTTPThread(\
            ip=http_server_ip,port=http_server_port,\
            daemon=True,auto=False,CON_OPEN_WEB=CON_OPEN_WEB)
        http_thread.start()

    if CON_OPEN_WIN==True:
        if UI_ENGINE == 'QT':
            run_qt_engine(PATH)
        elif UI_ENGINE == 'WX':
            run_wx_engine(PATH)
        else:
            run_occupied()
    else:
        run_occupied()

def test_run(HTML_PATH,TEST_PATH,TEST_MODE,CON_OPEN_WIN,\
    CON_OPEN_WEB,CON_SHARE,CON_80_PORT):
    run(HTML_PATH,TEST_PATH,TEST_MODE,CON_OPEN_WIN,\
        CON_OPEN_WEB,CON_SHARE,CON_80_PORT)
