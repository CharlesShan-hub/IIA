import setting 
#setting.initialize()
#print(setting.get())
#print(setting.get(['Server']))
#print(setting.get(['Server','ip']))
#print(setting.get(['Server','port']))

#print(setting.get(file="./ui/setting.json",js_read=True))
setting.set(['default_mail'],'shanhongtian@bupt.edu.cn',file="./ui/setting.json",js_read=True)
#print(setting.get(file="./ui/setting.json",js_read=True))

#setting.set(['Server','test'],'1')
#print(setting.get())
#setting.del_s(['Server','test'])
#print(setting.get())
#print(setting.set(['Server','1','2','3','4'],'1'))
#print(setting.set(['General'],'1'))
#print(setting.set(['Hello','new'],'1'))

