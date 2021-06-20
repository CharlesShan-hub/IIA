import sys 
sys.path.append("..")
from tool.CSVTool import *

def help_sqlite_datatype(window,path,sd,cd):
	""" 显示帮助文档-sqlite数据类型 """
	data = loadDataset(path)

	window.insert('end',["Sqlite Data Type\n\n","Sqlite数据类型介绍\n\n"][sd["language_id"]],'title1')

	for line in data[1:]:
		window.insert('end','  '+line[0]+'  --- ','title2')
		window.insert('end',line[1],'item')
		window.insert('end','\n\n'+line[2]+'\n\n','item')

	window.tag_config('title1',foreground=cd["front"],font=(sd['font'],sd['size']+5,'bold'),justify='center')
	window.tag_config('title2',foreground=cd["front"],font=(sd['font'],sd['size']+3,'bold'))
	window.tag_config('item',foreground=cd["front"],font=(sd['font'],sd['size']))
