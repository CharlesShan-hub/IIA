# Logger MODULE DOCUMENT

[返回主菜单](../README.md)

## 1. Overview

`logger`模块用于产生与显示运行记录。可以将记录进行不同层级的标注。可以根据记录等级选择性的输出到命令行中。可以记录记录产生的模块，位置与时间。另外，`logger`模块使用python3标准库`logging`进行封装，不需要下载其他依赖。

## 2. API

* __Import__  

``` Python
import logger
```

You should import `logger` module to use logger api.  

* **Init**

```python
LOG_MODULE = 'EXAMPLE'
```

在你的的模块`import logger`后，首先要声明所在模块的名称。

*  **Generate Log**

```python
# Debug Log
logger.debug("This is a debug log",LOG_MODULE)
# Info Log
logger.info("This is a info log",LOG_MODULE)
# Warning Log
logger.info("This is a warning log",LOG_MODULE)
# Enfo Log
logger.info("This is a error log",LOG_MODULE)
# Critical Log
logger.info("This is a critical log",LOG_MODULE)
```