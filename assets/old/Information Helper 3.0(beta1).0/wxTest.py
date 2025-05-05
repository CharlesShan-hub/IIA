import wx

app = wx.App()
win = wx.Frame(None, title="随便写点东西",size=(540,335))# 窗口的长宽
win.Show()

loadBtn = wx.Button(win, label="打开", pos=(225, 5), size=(80, 25))# 设置按钮
saveBtn = wx.Button(win, label="保存", pos=(315, 5), size=(210, 25))# 设置按钮
filename = wx.TextCtrl(win,pos = (5,5),size=(210,25))

contents = wx.TextCtrl(win,pos = (5,35),size = (530,260),style=wx.TE_MULTILINE|wx.HSCROLL)

app.MainLoop()
