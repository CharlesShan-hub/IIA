# -*- coding: utf8 -*-

from tkinter import *
#####################################
###--------------tk----------------
class App:
    def __init__(self,master):
        frame = Frame(master)
        frame.pack(expand=1)
        self.e1 = Entry(frame) 
        self.e1.pack()   
        self.e2 = Entry(frame) 
        self.e2.pack()   
        
        self.e1.bind("<Return>",handlerAdaptor(focus_cg,e2=self.e2))#tk类不能直接传递参数，需要lambda

def focus_cg(event,e2):
   e2.focus_set() #焦点移到e2

def handlerAdaptor(fun, **kwds):
#事件处理函数的适配器，相当于中介，那个event是从那里来的呢，我也纳闷，这也许就是python的伟大之处吧
    return lambda event,fun=fun,kwds=kwds: fun(event, **kwds)
 

if __name__ == '__main__':
    root = Tk()
    app=App(root)
    root.mainloop()

