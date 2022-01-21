# Server Module Document

[返回主菜单](../README.md)

## Structure

* 服务器进程

  *HTTP服务器进程（虽然是）服务器进程，但任务是构建界面展示框架，所以放在了[ui模块](../ui/README.md)中*

  * 事务处理进程
    * 接收验证
    * 事务处理
    * 结果返回
  * 服务器配置进程
    * 关闭服务器（开发中）
  
* 事物处理进程的事物处理部分

  * Auth