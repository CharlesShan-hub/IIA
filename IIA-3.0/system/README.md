# Setting Module Document

[返回主菜单](../README.md)

## Structure

### Mail

* 发送邮件(网页格式邮件)

网页

```
```



```python
def send_find_password(mail):
	''' 发送找回密码验证码
	'''
	from system import mail as system_mail
	with open(MAIL_FILE_PATH) as f:
		word = f.read()
		word=word.replace("IIA-Flag-Code",_generate_validation_code(mail))
		word=word.replace("IIA-Flag-Content","【IIA】您正在使用找回密码功能, 验证码可能导致IIA账号被盗, 请勿转发或泄漏。")
	system_mail.send_message(mail,word)
```



* 