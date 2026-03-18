-- 提醒模块

USE iia;

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
    operation_id BIGINT DEFAULT 0 COMMENT '操作批次ID，用于标识创建或最后修改该记录的操作',
    FOREIGN KEY (user_id) REFERENCES iia_auth(user_id) ON DELETE CASCADE
) ENGINE=InnoDB COMMENT='提醒模块 - 项目表';

CREATE INDEX idx_reminder_project_user_id ON reminder_project(user_id);
CREATE INDEX idx_reminder_project_operation_id ON reminder_project(operation_id);

-- 提醒模块 - 任务表
CREATE TABLE reminder_task (
    task_id BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '任务ID',
    user_id BIGINT NOT NULL COMMENT '用户ID',
    project_id BIGINT NULL COMMENT '项目ID',
    
    -- 核心元数据
    title TEXT NOT NULL COMMENT '任务标题',
    is_recurring BOOLEAN DEFAULT FALSE COMMENT '是否循环任务',
    
    -- 状态字段（新设计）
    is_completed BOOLEAN DEFAULT FALSE COMMENT '是否完成',
    is_abandoned BOOLEAN DEFAULT FALSE COMMENT '是否废弃',
    is_skipped BOOLEAN DEFAULT FALSE COMMENT '是否跳过',
    
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
CREATE INDEX idx_reminder_task_is_recurring ON reminder_task(is_recurring);
CREATE INDEX idx_reminder_task_completed ON reminder_task(is_completed);
CREATE INDEX idx_reminder_task_abandoned ON reminder_task(is_abandoned);
CREATE INDEX idx_reminder_task_skipped ON reminder_task(is_skipped);


-- 提醒模块 - 重复任务表
CREATE TABLE reminder_recurrence (
    task_id BIGINT PRIMARY KEY COMMENT '与reminder_task表一对一关联',
    category ENUM('weekly', 'monthly', 'yearly', 'days', 'weeks', 'ebinghaus') NOT NULL 
        COMMENT 'weekly:每周, monthly:每月, yearly:每年, days:隔N天, weeks:隔N周, ebinghaus:艾宾浩斯',
    `interval` INT DEFAULT 1 COMMENT '间隔数值 - days/weeks类型使用',
    `count` INT NOT NULL COMMENT '总重复次数',
    next_time DATETIME NOT NULL COMMENT '下一次发生时间',
    is_paused BOOLEAN NOT NULL DEFAULT FALSE COMMENT '是否暂停循环',
    is_skip_overdue BOOLEAN NOT NULL DEFAULT TRUE COMMENT '完成后跳过已过期的排队实例',
    is_repeat_from_due BOOLEAN NOT NULL DEFAULT TRUE COMMENT '按计划日期+周期(true)还是完成日期+周期(false)',
    schedule JSON COMMENT '规则: weekly=[1,3]; monthly=[1,15]; yearly=["MM-dd"]; days/weeks=无; ebbinghaus=无',
    FOREIGN KEY (task_id) REFERENCES reminder_task(task_id) ON DELETE CASCADE
) ENGINE=InnoDB COMMENT '提醒模块 - 重复任务表';

CREATE INDEX idx_reminder_recurrence_task ON reminder_recurrence(task_id);
CREATE INDEX idx_reminder_recurrence_next ON reminder_recurrence(next_time);


-- 提醒模块 - 任务状态变更历史表
CREATE TABLE reminder_history (
    history_id BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '历史记录ID',
    
    -- 任务信息
    task_id BIGINT NOT NULL COMMENT '任务ID',
    
    -- 状态信息（核心）
    is_completed BOOLEAN DEFAULT FALSE COMMENT '是否完成',
    is_abandoned BOOLEAN DEFAULT FALSE COMMENT '是否废弃',

    -- 循环任务信息（可选）
    is_skipped BOOLEAN DEFAULT FALSE COMMENT '是否跳过',
    current INT NULL COMMENT '当前重复次数（仅循环任务使用）',
    
    -- 操作追踪（核心）
    operation_id BIGINT NOT NULL COMMENT '操作批次ID，用于标识同一操作影响的所有记录',
    
    -- 记录时间
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '记录创建时间',
    
    FOREIGN KEY (task_id) REFERENCES reminder_task(task_id) ON DELETE CASCADE,
    
    -- 约束：循环任务实例不能重复
    UNIQUE KEY uk_reminder_history_task_sequence (task_id, current),
    
    -- 索引
    INDEX idx_reminder_history_task_id (task_id),
    INDEX idx_reminder_history_operation_id (operation_id),
    INDEX idx_reminder_history_created_at (created_at)
) ENGINE=InnoDB COMMENT='提醒模块 - 任务状态变更历史表';

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

-- 提醒模块 - 操作记录表
CREATE TABLE reminder_operation (
    operation_id BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '操作ID',
    user_id BIGINT NOT NULL COMMENT '用户ID',
    performed_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '操作执行时间',
    
    -- 操作信息
    is_reminder_project BOOLEAN DEFAULT FALSE COMMENT '是否影响项目表',
    is_reminder_task BOOLEAN DEFAULT FALSE COMMENT '是否影响任务表',
    is_reminder_recurrence BOOLEAN DEFAULT FALSE COMMENT '是否影响重复任务表',
    is_reminder_history BOOLEAN DEFAULT FALSE COMMENT '是否影响任务状态变更历史表',
    is_reminder_tag BOOLEAN DEFAULT FALSE COMMENT '是否影响标签表',
    is_reminder_task_tag BOOLEAN DEFAULT FALSE COMMENT '是否影响任务-标签关联表',
    
    -- 索引
    INDEX idx_reminder_operation_user_id (user_id),
    INDEX idx_reminder_operation_performed_at (performed_at),
    
    -- 外键约束
    FOREIGN KEY (user_id) REFERENCES iia_auth(user_id) ON DELETE CASCADE
) ENGINE=InnoDB COMMENT='提醒模块 - 操作记录表，用于记录所有用户操作以便追溯和撤销';
