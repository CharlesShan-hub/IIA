import sys
import os
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle('IIA')
        self.setGeometry(30,50,1000,618)
        self.browser=QWebEngineView()
        #加载外部的web界面
        self.browser.load(QUrl("file://"+os.getcwd()+"/ui/index.html"))
        self.setCentralWidget(self.browser)


def run():
    app=QApplication(sys.argv)
    win=MainWindow()
    win.show()
    app.exit(app.exec_())