from http.server import HTTPServer, SimpleHTTPRequestHandler
import threading
import sys
import os

import setting
import logger

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
            server_ = HTTPServer((self.ip, self.port), SimpleHTTPRequestHandler)
            self.server = server_
            if self.web:
                import webbrowser
                webbrowser.open(web_path)
            server_.serve_forever()

        except KeyboardInterrupt:
            print("Good Bye!")
            
    def exit(self):
        self.server.shutdown()


def run_qt_engine(path):
    app=QApplication(sys.argv)
    win=MainWindow(path)
    win.show()
    app.exit(app.exec_())

def run_wx_engine(path):
    app = wx.App()
    win = MyHtmlFrame(None, 'IIA',path)
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
    ''' 运行UI
    HTML_PATH： UI模块默认打开的HTML文件路径
    TEST_MODE：是否进入测试模式
    OPEN_WIN：是否通过桌面应用打开
    OPEN_WEB：是否通过默认浏览器打开
    SHARE：是否开放局域网
    80_PORT：是否默认使用80端口
    '''
    if TEST_MODE==True:
        PATH="file://"+os.getcwd()+TEST_PATH
    else:
        PATH="file://"+os.getcwd()+HTML_PATH

    if CON_SHARE==False:
        http_server_ip = '127.0.0.1'
    else:
        from server import get_host_ip
        http_server_ip = get_host_ip()
    if CON_80_PORT:
        http_server_port=80
    else:
        from server import get_host_port
        http_server_port = get_host_port()
    import setting
    setting.set(['Server','ip'],http_server_ip)
    setting.set(['Server','port'],http_server_port)

    if CON_OPEN_WEB==True:
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
