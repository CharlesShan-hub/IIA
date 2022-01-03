import sys
import os
import setting

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
            #加载外部的web界面
            self.browser.load(QUrl(path))
            self.setCentralWidget(self.browser)
except:
    try:
        UI_ENGINE = 'WX'
        print("QT Engine goes wrong, trying wx engine")

        import wx
        from wx.html2 import WebView

        class MyHtmlFrame(wx.Frame):
            def __init__(self, parent, title):
                wx.Frame.__init__(self, parent, -1, title, size=(1000, 618))
                web_view =WebView.New(self)
                web_view.LoadURL("127.0.0.1:"+str(setting.get(['Server','port'],)))
    except:
        UI_ENGINE = None
        print("Can't open desktop window!")
        import sys
        sys.exit()


def run_qt_engine(path):
    app=QApplication(sys.argv)
    win=MainWindow(path)
    win.show()
    app.exit(app.exec_())

def run_wx_engine(path):
    app = wx.App()
    frm = MyHtmlFrame(None, 'IIA')
    frm.Show()
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

def run(html,TEST_MODE,CON_OPEN_WIN):
    if TEST_MODE==True:
        path="file://"+os.getcwd()+"/ui/html/test.html"
    else:
        path="file://"+os.getcwd()+html

    if CON_OPEN_WIN==True:
        if UI_ENGINE == 'QT':
            run_qt_engine(path)
        elif UI_ENGINE == 'WX':
            run_wx_engine(path)
        else:
            print("Can't run window, you can try run in web!")
            run_occupied()
    else:
        run_occupied()

def test_run(html,TEST_MODE,CON_OPEN_WIN):
    run(html,TEST_MODE,CON_OPEN_WIN)
