# Setting MODULE DOCUMENT

[返回主菜单](../README.md)

## 1. Overview

设置模块主要负责设置IIA系统用户设置的配置，用户可以通过设置setting.json更改运行参数。不过一些系统设置比如密码，数据处理服务器端口，建议使用[storage](../storage/README.md)模块构建。

## 2. API

* __Import__  

``` Python
import setting
```

You should import `setting` module to use setting api.  

* **Init**

```python
setting.initialize()
```

* **获取设置**

```python
setting.get(path,default)
# param: (optional),`list`, 设置内容在setting.json的包含关系
# default: (optional), 设置内容查找失败默认返回的内容
# return: 获取的设置内容

# 获取全部设置
content = setting.get()

# 获取Server层级的设置
content = setting.get(['Server'])

# 获取Server中ip的参数
content = setting.get(['Server','ip'])
```

* **写入设置**

```python
setting.set(path,content)
# path: `list`, 设置内容在setting.json的包含关系
# con: (optional), 设置成的内容
# return: 设置成功(True)或失败(False)

# 设置Server中ip的参数为127.0.0.1
result = setting.set(['Server','ip'],'127.0.0.1')
```

* **删除设置**

```python
setting.del_s(path)
# path: `list`, 设置内容在setting.json的包含关系
# return: 删除成功(True)或失败(False)

# 删除Server中port的参数
result = setting.del_s(['Server','port'])

# 删除Server层级的设置
result = setting.del_s(['Server'])
```

