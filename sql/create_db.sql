-- 如果数据库已存在则删除（谨慎使用）
DROP DATABASE IF EXISTS iia;

-- 创建数据库并设置字符集
CREATE DATABASE iia 
    CHARACTER SET utf8mb4 
    COLLATE utf8mb4_unicode_ci;

-- 切换到 iia 数据库
USE iia;