import sys
import os
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

def run(html,TEST_MODE):
    if TEST_MODE==True:
        path="file://"+os.getcwd()+"/ui/html/test.html"
    else:
        path="file://"+os.getcwd()+html
    app=QApplication(sys.argv)
    win=MainWindow(path)
    win.show()
    app.exit(app.exec_())

def test_run(html):
    run(html)
