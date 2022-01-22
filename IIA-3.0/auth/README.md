# Auth MODULE DOCUMENT

[返回主菜单](../README.md)

## 1. Overview

* `auth`模块用于进行认证工作，内容包括用户登陆注册，找回密码等功能。`auth`内部通过`storage`模块进行信息存储。`auth`模块被`server`模块所调用。

* 用户信息表目前形式为

  ```sqlite
  CREATE TABLE AUTH (
  			MAIL     TEXT PRIMARY KEY NOT NULL, 
  			PASSWORD TEXT, 
  			NAME     TEXT
  )
  ```

  * 邮箱是标识用户的唯一标志，一个邮箱只能绑定一个用户。
  * 目前只有NAME字段，以后会随着需要添加。

* 操作流程

  ```python
  # 登陆数据报格式
  {
  	"type":"auth"，      # 类型为认证信息（Server模块要求）
    "operate":"login",   # 操作为登陆（Server模块要求）
    "password":password, # 密码
    "mail":mail          # 邮箱
  }
  
  # 登陆数据报格式
  {
  	"type":"auth"，      # 类型为认证信息（Server模块要求）
    "operate":"regist",  # 操作为注册（Server模块要求）
    "password":password, # 密码
    "mail":mail,         # 邮箱
    "name":name,         # 昵称
    "code":code          # 验证码
  }
  
  # 找回密码数据报格式
  {
  	"type":"auth"，            # 类型为认证信息（Server模块要求）
    "operate":"find password", # 操作为找回密码（Server模块要求）
    "password":password,       # 密码
    "mail":mail                # 邮箱
    "code":code                # 验证码/状态码
  }
  
  # 修改密码数据报格式
  {
  	"type":"auth"，            # 类型为认证信息（Server模块要求）
    "operate":"change password", # 操作为找回密码（Server模块要求）
    "password":password,       # 密码
    "mail":mail                # 邮箱
    "code":code                # 验证码/状态码
  }
  ```

  修改/找回密码或注册用户会发送两次请求，第一次数据报中code字段填写```request```进行标识，服务器收到后发送验证码，第二次请求报文code字段填写收到的验证码。

* 文档最近更新时间：2023.1.22。

## 2. API

* __Import__  

``` Python
import auth
```

You should import `auth` module to use auth api.  

*  **Regist / Add User**

```python
'''Basic Syntax'''
auth.add_user('charles@example.com','******',name='Chalres') # This's OK
# auth.add_user('charles@example.com','******','Chalres')    # Failed to run

# Maybe next version of IIA
auth.add_user('charles@example.com','******',name='Chalres',birth='2000,2,26',gender=0)

'''Example'''
# In Auth Module add_user is defined as
# def add_user(mail,password,**kwg)
def regist(mail,password,name,code):
	''' In server threading, you can write like this
	'''
	# Request to create a new user
	if code=="request":
		auth.send_check_mail(mail)
		return 200
	# Verification code received (verification code error)
	if auth.check_validation_code(mail,code)==False:
		return 403
	# Write user name and password
	if auth.add_user(mail=mail,password=password,name=name,code=code) == True:
		return 100
```

* **Config User**

```python
# Return all user info
# - Only used for debug!
# - Do not write this function in your code!
print(auth.config_user())
```

* **Login / Check Password**

```python
def login(mail,password):
	''' In server threading, you can write like this
	'''
  # check_password return True is password match with mail
	if(auth.check_password(mail,password)):
		return 100
  # check_password return False is password is wrong
	else:
		return 403
```

* **Remember User Login**

```python
# Recently, only can remember the last user
auth.remember_user(mail)
```

* **Send Mail**

```python
# Find password Example
def find_password(mail,code):
	# Request to retrieve password
	if code=="request":
		auth.send_find_password(mail)
		return 200
	# Verification code received (verification code error)
	if auth.check_validation_code(mail,code)==False:
		return 403
	# Correct verification code
	return 100

# Reset password Example
def change_password(mail,code,password):
	# Request to retrieve password
	if code=="request":
		auth.send_change_password(mail)
		return 200
	# Verification code received (verification code error)
	if auth.check_validation_code(mail,code)==False:
		return 403
	# Correct verification code
	return 100

# Regist Example
def regist(mail,password,name,code):
	''' In server threading, you can write like this
	'''
	# Request to create a new user
	if code=="request":
		auth.send_check_mail(mail)
		return 200
	# Verification code received (verification code error)
	if auth.check_validation_code(mail,code)==False:
		return 403
	# Write user name and password
	if auth.add_user(mail=mail,password=password,name=name,code=code) == True:
		return 100

```
