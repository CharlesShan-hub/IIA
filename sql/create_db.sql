-- 如果数据库已存在则跳过创建
CREATE DATABASE IF NOT EXISTS iia
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

-- 创建测试数据库
CREATE DATABASE IF NOT EXISTS iia_test
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

-- 切换到 iia 数据库
USE iia;