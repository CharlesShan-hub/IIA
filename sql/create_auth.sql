-- 认证表（支持多邮箱）

-- 创建认证表（仅包含ID和密码哈希）
CREATE TABLE IF NOT EXISTS iia_auth (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    password_hash VARCHAR(100) NOT NULL COMMENT '密码哈希'
) COMMENT '认证信息表';

-- 创建用户基本信息表
CREATE TABLE IF NOT EXISTS iia_profile (
    id BIGINT PRIMARY KEY COMMENT '关联的认证ID',
    nickname VARCHAR(50) NOT NULL COMMENT '昵称',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    FOREIGN KEY (id) REFERENCES iia_auth(id) ON DELETE CASCADE
) ENGINE=InnoDB COMMENT='用户基本信息表';

-- 创建邮箱表（存储邮箱与用户的关联）
CREATE TABLE IF NOT EXISTS iia_mail (
    email VARCHAR(100) PRIMARY KEY COMMENT '邮箱',
    auth_id BIGINT NOT NULL COMMENT '关联的认证ID',
    is_checked BOOLEAN DEFAULT FALSE COMMENT '是否经过验证',
    FOREIGN KEY (auth_id) REFERENCES iia_auth(id) ON DELETE CASCADE
) COMMENT '邮箱信息表';
