-- 用户认证部分

-- 删除旧的表
drop table if exists iia_mail;
drop table if exists iia_profile;
drop table if exists reminder_project;
drop table if exists reminder_task;
drop table if exists reminder_recurrence;
drop table if exists reminder_history;
drop table if exists reminder_tag;
drop table if exists reminder_task_tag;
drop table if exists iia_auth;

-- 用户密码表
CREATE TABLE IF NOT EXISTS iia_auth (
    user_id BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '用户ID',
    password_hash VARCHAR(100) NOT NULL COMMENT '密码哈希'
) COMMENT '用户密码表';

-- 用户信息表
CREATE TABLE IF NOT EXISTS iia_profile (
    user_id BIGINT PRIMARY KEY COMMENT '用户ID',
    username VARCHAR(50) NOT NULL COMMENT '用户名',
    FOREIGN KEY (user_id) REFERENCES iia_auth(user_id) ON DELETE CASCADE
) ENGINE=InnoDB COMMENT='用户信息表';

-- 用户邮箱表
CREATE TABLE IF NOT EXISTS iia_mail (
    user_id BIGINT NOT NULL COMMENT '用户ID',
    email VARCHAR(100) PRIMARY KEY COMMENT '邮箱',
    FOREIGN KEY (user_id) REFERENCES iia_auth(user_id) ON DELETE CASCADE
) COMMENT '用户邮箱表';
