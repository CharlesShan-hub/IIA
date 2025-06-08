-- 创建数据库 iia
CREATE DATABASE IF NOT EXISTS iia;

-- 使用 iia 数据库
USE iia;

-- 创建 birthday 表
CREATE TABLE IF NOT EXISTS birthday (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    birthdate DATE NOT NULL,
    INDEX idx_name (name)
);