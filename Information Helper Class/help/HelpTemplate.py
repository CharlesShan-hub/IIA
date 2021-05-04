import sys 
sys.path.append("..")

def help_template(window,sd,cd):
	""" 显示帮助文档-模板介绍 
	'''
	1. 简介
	  信息助手存储信息采用表格进行数据存储。尤其是“普通信息”存储方案, 程序将数据存储成数据集文件, 意在加强文件对外开放的特性, 即数据集中存储的是高度结构化的数据, 用户可以轻松的通过其他软件调用或编辑数据集。
	  “模板”就相当于表格的表头, 为了便于将数据集导入数据库, 用户可以选择每一个数据项的格式(sqlite数据类型), 详细内容可以在数据类型说明中查看。

	2. 快速开始
	  我们假设要建立一个表格储存电话号码:

	  —————————————————
	  | 名字 |           号码            |      备注     |
	  —————————————————
	  | 张三 | 12345678900  | 大学同学 |
	  | 李四 | 23456789001  | 中学同学 |
	  —————————————————

	  我们可以在右侧选择, “添加类型”为“添加模板”, “添加方式”为“逐项添加”。 我们就可以看到“添加”,“减少”与“保存”三个按钮了。 在操作区填写模板名称接着点击“添加输入框”进行数据项名称填写与类别选择。 比如名片表我们就在“模板名”输入框中填写“通讯录”, 点击三次“添加输入框”, 在第一个“项目”中填写“名字”, 在第二个“项目”中填写“号码”, 在第三个“项目”中填写“备注”。 检查无误后点击“保存”即可创建一个电话号码类。
	  在上一个例子中我们并没有填写“项目类型”, 这时保存的模板是没有限制信息类型的, 我们可以在保存前, 选择“项目类型”为“text”。 设置“项目类型”在数据为数字或日期类型时益处更大。 
	'''
	"""

	if sd['language'] == 'English':
		# 标题
		window.insert('end','Introduction to Templates\n\n','title1')
		# 简介
		window.insert('end','1. Introduction\n','title2')
		window.insert('end','  Information Assistant uses tables for data storage. ','item_bold')
		window.insert('end','In particular, "common information" storage schemes, '\
			'where programs store data as dataset files. '\
			'To enhance the open file feature, the data set stored in the data set is '\
			'highly structured, users can easily call or edit the data set through other software.\n','item')
		window.insert('end','  The "template" is the table header of the table.','item_bold')
		window.insert('end',', To facilitate the import of the data set into the database, '\
			'the user can select the format (SQLite data type) for each data item, which can '\
			'be seen in the data type description.\n\n','item')
		# 2.快速开始
		window.insert('end','2. Quick Start\n','title2')
		window.insert('end','  Suppose you want to create a table to store phone numbers:\n\n','item')
		window.insert('end','      ----------------------------------------\n','item')
		window.insert('end','      | Name |         Tel          |    Notes  |\n','item')
		window.insert('end','      ----------------------------------------\n','item')
		window.insert('end','      |  Tom  | 12345678900 |     Cat     |\n','item')
		window.insert('end','      |   Jerry| 23456789001 |  Mouse   |\n','item')
		window.insert('end','      ----------------------------------------\n\n','item')
		window.insert('end','  We can select on the right, "Add Templates" for "Add Type", '\
			'"Item Insert" for "Add Way". Ten we can see the "add", '\
			'"reduce" and "save" buttons. Fill in the template name in the operation area '\
			'and then click "Add Item" to fill in the name of the data item and select '\
			'the category.\n','item')
		window.insert('end','  For example, in the business card form, we fill in the '\
			'"address book" in the input box of "Name", click "Add Item" '\
			'three times, fill in the "Name" in the first "Item", fill in the "Tel" '\
			'in the second "Item", and fill in the "Notes" in the third "Item". '\
			'Check and click "Save" to create a phone number template.\n','item')
		window.insert('end','  In the previous example, we did not fill in "Item Type", '\
			'so the saved template has no restriction on information type. We can select '\
			'"Project Type" to "Text" before saving. Setting "Item Type" is even more '\
			'beneficial when the data is of numeric or date type.\n\n','item')
	elif sd['language'] == '简体中文':
		# 标题
		window.insert('end','“模板”是什么\n\n','title1')
		# 1. 简介
		window.insert('end','1. 简介\n','title2')
		window.insert('end','  信息助手采用表格进行数据存储。','item_bold')
		window.insert('end','尤其是“普通信息”存储方案, 程序将数据存储成数据集文件, 意在加强文件对外开放的特性, '\
			'即数据集中存储的是高度结构化的数据, 用户可以轻松的通过其他软件调用或编辑数据集。\n','item')
		window.insert('end','  “模板”就相当于表格的表头','item_bold')
		window.insert('end',', 为了便于将数据集导入数据库, 用户可以选择每一个数据项的格式(sqlite数据类型), '\
			'详细内容可以在数据类型说明中查看。\n\n','item')
		# 2.快速开始
		window.insert('end','2. 快速开始\n','title2')
		window.insert('end','  我们假设要建立一个表格储存电话号码:\n\n','item')
		window.insert('end','      ----------------------------------------\n','item')
		window.insert('end','      | 名字 |     电话号     |      简介    |\n','item')
		window.insert('end','      ----------------------------------------\n','item')
		window.insert('end','      | 张三 |12345678900| 大学同学 |\n','item')
		window.insert('end','      | 李四 |23456789001| 中学同学 |\n','item')
		window.insert('end','      ----------------------------------------\n\n','item')
		window.insert('end','  我们可以在右侧选择, “添加类型”为“添加模板”, '\
			'“添加方式”为“逐项添加”。 我们就可以看到“添加”,“减少”与“保存”三个按钮了。 '\
			'在操作区填写模板名称接着点击“添加输入框”进行数据项名称填写与类别选择。 '\
			'比如名片表我们就在“模板名”输入框中填写“通讯录”, 点击三次“添加输入框”, '\
			'在第一个“项目”中填写“名字”, 在第二个“项目”中填写“号码”, 在第三个“项目”中填写“备注”。 '\
			'检查无误后点击“保存”即可创建一个电话号码类。\n','item')
		window.insert('end','  在上一个例子中我们并没有填写“项目类型”, '\
			'这时保存的模板是没有限制信息类型的, 我们可以在保存前, 选择“项目类型”为“text”。 '\
			'设置“项目类型”在数据为数字或日期类型时益处更大。\n\n','item')

	window.tag_config('title1',foreground=cd["front"],font=(sd['font'],sd['size']+4,'bold'),justify='center')
	window.tag_config('title2',foreground=cd["front"],font=(sd['font'],sd['size']+2,'bold'))
	window.tag_config('item',foreground=cd["front"],font=(sd['font'],sd['size']))
	window.tag_config('item_bold',foreground=cd["front"],font=(sd['font'],sd['size'],'bold'))



