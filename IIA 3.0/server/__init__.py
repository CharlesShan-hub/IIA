import os
import json
import server.main as main


# 检查路径
if os.path.exists('./server/resources') == False:
	os.makedirs('./server/resources')

# 设置文件
if os.path.exists('./storage/resources/setting.json') == False:
	with open('./storage/resources/setting.json'\
		, 'w', encoding='utf-8') as f:
		content = {
			'ip': '',
			'port': ''
		}
		f.write(json.dumps(content, indent=4, ensure_ascii=False))

def run():
	''' 服务器运行
	'''
	main.run()