-- 提醒模块

drop table if exists reminder_project;
drop table if exists reminder_task;
drop table if exists reminder_recurrence;
drop table if exists reminder_history;
drop table if exists reminder_tag;
drop table if exists reminder_task_tag;

-- 提醒模块 - 项目表
CREATE TABLE reminder_project (
    project_id BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '项目ID',
    user_id BIGINT NOT NULL COMMENT '用户ID',
    name VARCHAR(255) NOT NULL COMMENT '项目名称',
    description TEXT COMMENT '项目描述',
    color VARCHAR(20) COMMENT '项目颜色',
    icon VARCHAR(50) COMMENT '项目图标',
    sort_order INT DEFAULT 0 COMMENT '排序顺序',
    is_archived BOOLEAN DEFAULT FALSE COMMENT '是否归档',
    FOREIGN KEY (user_id) REFERENCES iia_auth(user_id) ON DELETE CASCADE
) ENGINE=InnoDB COMMENT='提醒模块 - 项目表';

CREATE INDEX idx_reminder_project_user_id ON reminder_project(user_id);

-- 提醒模块 - 任务表
CREATE TABLE reminder_task (
    task_id BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '任务ID',
    user_id BIGINT NOT NULL COMMENT '用户ID',
    project_id BIGINT NULL COMMENT '项目ID',
    
    -- 核心元数据
    title TEXT NOT NULL COMMENT '任务标题',
    category ENUM('task', 'note') NOT NULL DEFAULT 'task' COMMENT 'task:任务, note:笔记',
    status ENUM('todo','done','abandoned') NOT NULL DEFAULT 'todo' COMMENT 'todo: 待处理, done: 已完成, abandoned: 已放弃',
    is_archived BOOLEAN DEFAULT FALSE COMMENT '是否归档',
    
    -- 层级结构
    parent_task_id BIGINT NULL COMMENT '父任务ID',
    sort_order INT DEFAULT 0 COMMENT '排序顺序',

    -- 时间信息
    due_date DATETIME NULL COMMENT '任务截止日期',
    start_date DATETIME NULL COMMENT '任务开始日期',
    completed_at DATETIME NULL COMMENT '任务完成日期',
    reminder_sent_at DATETIME NULL COMMENT '提醒已发送时间',
    
    -- 优先级
    priority ENUM('none', 'low', 'medium', 'high') DEFAULT 'none' COMMENT '优先级: none, low, medium, high',
    
    FOREIGN KEY (user_id) REFERENCES iia_auth(user_id) ON DELETE CASCADE,
    FOREIGN KEY (parent_task_id) REFERENCES reminder_task(task_id) ON DELETE CASCADE,
    FOREIGN KEY (project_id) REFERENCES reminder_project(project_id) ON DELETE SET NULL
) ENGINE=InnoDB COMMENT='提醒模块 - 任务表';

CREATE INDEX idx_reminder_task_user_id ON reminder_task(user_id);
CREATE INDEX idx_reminder_task_parent_id ON reminder_task(parent_task_id);
CREATE INDEX idx_reminder_task_project_id ON reminder_task(project_id);
CREATE INDEX idx_reminder_task_due_date ON reminder_task(due_date);
CREATE INDEX idx_reminder_task_status ON reminder_task(status);
CREATE INDEX idx_reminder_task_category ON reminder_task(category);


-- 提醒模块 - 重复任务表
CREATE TABLE reminder_recurrence (
    task_id BIGINT PRIMARY KEY COMMENT '与reminder_task表一对一关联',
    category ENUM('weekly', 'monthly', 'yearly', 'days', 'weeks', 'ebinghaus') NOT NULL 
        COMMENT 'weekly:每周, monthly:每月, yearly:每年, days:隔N天, weeks:隔N周, ebinghaus:艾宾浩斯',
    interval INT DEFAULT 1 COMMENT '间隔数值 - days/weeks类型使用',
    count INT NOT NULL COMMENT '总重复次数',
    next_time DATETIME NOT NULL COMMENT '下一次发生时间',
    schedule JSON COMMENT '根据category存储规则值
        weekly: [1,3]        → 每周一、三
        monthly: [1,15]      → 每月1和15号  
        yearly: ["06-01"]    → 每年6月1日
        days/weeks:          → 无需存储
        ebbinghaus:          → 无需存储, 1,2,4,7,13,13,....
    ',
    FOREIGN KEY (task_id) REFERENCES reminder_task(task_id) ON DELETE CASCADE
) COMMENT '提醒模块 - 重复任务表';

CREATE INDEX idx_reminder_recurrence_task ON reminder_recurrence(task_id);
CREATE INDEX idx_reminder_recurrence_next ON reminder_recurrence(next_time);


-- 提醒模块 - 重复任务完成历史表
CREATE TABLE reminder_history (
    history_id BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '历史记录ID',
    task_id BIGINT NOT NULL COMMENT '任务ID',
    due_date DATETIME NULL COMMENT '任务截止日期',
    start_date DATETIME NULL COMMENT '任务开始日期',
    completed_at DATETIME NULL COMMENT '任务完成日期',
    reminder_sent_at DATETIME NULL COMMENT '提醒已发送时间',
    current INT NOT NULL COMMENT '当前重复次数, 从1开始',
    status ENUM('todo', 'done', 'skipped', 'abandoned') NOT NULL DEFAULT 'todo' COMMENT '
        todo: 待完成,
        done: 已完成,
        skipped: 已跳过,
        abandoned: 已放弃,
    ',
    
    FOREIGN KEY (task_id) REFERENCES reminder_task(task_id) ON DELETE CASCADE,
    UNIQUE KEY uk_reminder_history_task_sequence (task_id, current)
) ENGINE=InnoDB COMMENT='提醒模块 - 重复任务完成历史表';

CREATE INDEX idx_reminder_history_task_id ON reminder_history(task_id);
CREATE INDEX idx_reminder_history_status ON reminder_history(status);
CREATE INDEX idx_reminder_history_due_date ON reminder_history(due_date);

-- 提醒模块 - 标签表
CREATE TABLE reminder_tag (
    tag_id BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '标签ID',
    user_id BIGINT NOT NULL COMMENT '用户ID',
    name VARCHAR(100) NOT NULL COMMENT '标签名称',
    color VARCHAR(20) COMMENT '标签颜色',
    
    FOREIGN KEY (user_id) REFERENCES iia_auth(user_id) ON DELETE CASCADE,
    UNIQUE KEY uk_reminder_tags_auth_name (user_id, name)
) ENGINE=InnoDB COMMENT='提醒模块 - 标签表';

CREATE INDEX idx_reminder_tag_user_id ON reminder_tag(user_id);
CREATE INDEX idx_reminder_tag_name ON reminder_tag(name);

-- 提醒模块 - 任务-标签关联表
CREATE TABLE reminder_task_tag (
    id BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '关联ID',
    task_id BIGINT NOT NULL COMMENT '任务ID',
    tag_id BIGINT NOT NULL COMMENT '标签ID',
    UNIQUE KEY uk_reminder_task_tag_unique (task_id, tag_id),
    FOREIGN KEY (task_id) REFERENCES reminder_task(task_id) ON DELETE CASCADE,
    FOREIGN KEY (tag_id) REFERENCES reminder_tag(tag_id) ON DELETE CASCADE
) ENGINE=InnoDB COMMENT='提醒模块 - 任务与标签的多对多关联表';

CREATE INDEX idx_reminder_task_tag_task_id ON reminder_task_tag(task_id);
CREATE INDEX idx_reminder_task_tag_tag_id ON reminder_task_tag(tag_id);
