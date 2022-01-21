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
  * 用户信息表与文档最近更新时间：2023.1.5。

## 2. API

* __Import__  

``` Python
import auth
```

You should import `auth` module to use auth api.  

*  **Add User**

```python
# In Auth Module add_user is defined as
# def add_user(mail,password,**kwg)

auth.add_user('charles@example.com','******',name='Chalres') # This's OK
# auth.add_user('charles@example.com','******','Chalres')    # Failed to run

# Maybe next version of IIA
auth.add_user('charles@example.com','******',name='Chalres',birth='2000,2,26',gender=0)
```

* **Config User**

```python
# Return all user info
# - Only used for debug!
# - Do not write this function in your code!
print(auth.config_user())
```

* **Check Password**

```python
# in server threading, you can write like this
if(auth.check_password(mail,password)):
  	# check_password return True is password match with mail
		return 100
else:
  	# check_password return False is password is wrong
		return 403
```

* **Send Check Mail**

```
该功能目前使用有故障，正在修复...
```

