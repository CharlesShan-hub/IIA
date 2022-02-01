import setting 
#setting.initialize()
#print(setting.get())
#print(setting.get(['Server']))
#print(setting.get(['Server','ip']))
#print(setting.get(['Server','port']))

#print(setting.get(file="./ui/setting.json",js_read=True))
#setting.set(['default_mail'],'shanhongtian@bupt.edu.cn',file="./ui/setting.json",js_read=True)

'''setting.set(['shanhongtian@bupt.edu.cn','dashboard'],{
	'obj1':{'class':1},
	'obj2':{'class':1},
	'obj3':{'class':1},
	'obj4':{'class':1},
	'obj5':{'class':3},
	'obj6':{'class':4},
})'''

print(setting.get(['1742861545@qq.com'],default={}))
#print(setting.get(file="./ui/setting.json",js_read=True))

#setting.set(['Server','test'],'1')
#print(setting.get())
#setting.del_s(['Server','test'])
#print(setting.get())
#print(setting.set(['Server','1','2','3','4'],'1'))
#print(setting.set(['General'],'1'))
#print(setting.set(['Hello','new'],'1'))

