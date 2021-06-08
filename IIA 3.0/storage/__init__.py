import os
import json

# 检查路径
if os.path.exists('./storage/resources') == False:
	os.makedirs('./storage/resources')

if os.path.exists('./storage/resources/repo_info.json') == False:
	with open('./storage/resources/repo_info.json'\
		, 'w', encoding='utf-8') as f:
		content = {
			'repo_id': []
		}
		f.write(json.dumps(content, indent=4, ensure_ascii=False))
