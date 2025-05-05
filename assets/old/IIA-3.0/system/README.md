# Setting Module Document

[返回主菜单](../README.md)

## Structure

### Mail

* 发送邮件(网页格式邮件)

```python
def send_find_password(mail):
	''' 发送找回密码验证码
	'''
	from system import mail as system_mail
	with open(MAIL_FILE_PATH) as f: # 写一个验证码邮件模板
		word = f.read()
		word=word.replace("IIA-Flag-Code",generate_validation_code(mail))
		word=word.replace("IIA-Flag-Content","【IIA】您正在使用找回密码功能, 验证码可能导致IIA账号被盗, 请勿转发或泄漏。")
	system_mail.send_message(mail,word)
```

### Network

* 获取本机ip

```python
from system.network import get_host_ip
print(get_host_ip())
```

* 获取一个空闲端口

```python
from system.network import get_host_port
print(get_host_port())
```

