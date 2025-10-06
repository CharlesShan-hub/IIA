-- 项目表
CREATE TABLE projects (
    project_id BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '项目ID',
    user_id BIGINT NOT NULL COMMENT '用户ID',
    name VARCHAR(255) NOT NULL COMMENT '项目名称',
    description TEXT COMMENT '项目描述',
    color VARCHAR(20) COMMENT '项目颜色',
    icon VARCHAR(50) COMMENT '项目图标',
    sort_order INT DEFAULT 0 COMMENT '排序顺序',
    is_archived TINYINT(1) DEFAULT 0 COMMENT '0:未归档,1:已归档',
    FOREIGN KEY (user_id) REFERENCES iia_auth(user_id) ON DELETE CASCADE
) ENGINE=InnoDB COMMENT='项目表';

CREATE INDEX idx_projects_user_id ON projects(user_id);


-- 任务表
CREATE TABLE tasks (
    task_id BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '任务ID',
    user_id BIGINT NOT NULL COMMENT '用户ID',
    project_id BIGINT NULL COMMENT '项目ID',
    
    -- 核心元数据
    title TEXT NOT NULL COMMENT '任务标题',
    task_type TINYINT NOT NULL DEFAULT 1 COMMENT '1:task, 2:note',
    status TINYINT NOT NULL DEFAULT 1 COMMENT '1:inbox, 2:todo, 3:in_progress, 4:completed, 5:archived',
    
    -- 层级结构
    parent_task_id BIGINT NULL COMMENT '父任务ID',
    sort_order DOUBLE DEFAULT 0 COMMENT '排序顺序',

    -- 时间信息
    due_date DATETIME NULL COMMENT '任务截止日期',
    start_date DATETIME NULL COMMENT '任务开始日期',
    completed_at DATETIME NULL COMMENT '任务完成日期',
    reminder_sent_at DATETIME NULL COMMENT '提醒已发送时间',
    
    -- 优先级
    priority TINYINT DEFAULT 0 COMMENT '0:无,1:低,2:中,3:高',
    
    FOREIGN KEY (user_id) REFERENCES iia_auth(user_id) ON DELETE CASCADE,
    FOREIGN KEY (parent_task_id) REFERENCES tasks(task_id) ON DELETE CASCADE,
    FOREIGN KEY (project_id) REFERENCES projects(project_id) ON DELETE SET NULL
) ENGINE=InnoDB COMMENT='任务表';

CREATE INDEX idx_tasks_user_id ON tasks(user_id);
CREATE INDEX idx_tasks_parent_id ON tasks(parent_task_id);
CREATE INDEX idx_tasks_project_id ON tasks(project_id);
CREATE INDEX idx_tasks_due_date ON tasks(due_date);
CREATE INDEX idx_tasks_status ON tasks(status);
CREATE INDEX idx_tasks_type ON tasks(task_type);


-- 标签表
CREATE TABLE tags (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT NOT NULL COMMENT '关联的认证ID',
    name VARCHAR(100) NOT NULL,
    color VARCHAR(20),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (user_id) REFERENCES iia_auth(id) ON DELETE CASCADE,
    UNIQUE KEY uk_tags_auth_name (user_id, name)
) ENGINE=InnoDB COMMENT='标签表';

CREATE INDEX idx_tags_user_id ON tags(user_id);
CREATE INDEX idx_tags_name ON tags(name);


-- 任务-标签关联表
CREATE TABLE task_tags (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    task_id BIGINT NOT NULL,
    tag_id BIGINT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    UNIQUE KEY uk_task_tag_unique (task_id, tag_id),
    FOREIGN KEY (task_id) REFERENCES tasks(id) ON DELETE CASCADE,
    FOREIGN KEY (tag_id) REFERENCES tags(id) ON DELETE CASCADE
) ENGINE=InnoDB COMMENT='任务与标签的多对多关联表';

CREATE INDEX idx_task_tags_task_id ON task_tags(task_id);
CREATE INDEX idx_task_tags_tag_id ON task_tags(tag_id);
CREATE INDEX idx_task_tags_created_at ON task_tags(created_at);


CREATE TABLE recurrence_task (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    task_id BIGINT NOT NULL UNIQUE,
    
    -- 重复类型：weekly(每周), monthly(每月), yearly(每年), days(每隔N天), weeks(每隔N周), ebinghaus(艾宾浩斯)
    repeat_type ENUM('weekly', 'monthly', 'yearly', 'days', 'weeks', 'ebinghaus') NOT NULL,
    
    -- 间隔数值（对days/weeks类型有效）
    interval_value INT DEFAULT 1 COMMENT '间隔数值',
    
    -- 每周重复：存储周几（1-7表示周一到周日）
    weekly_days JSON COMMENT '[1,3,5] 表示周一、三、五',
    
    -- 每月重复：存储哪几天（1-31）
    monthly_days JSON COMMENT '[1,15] 表示每月1号和15号',
    
    -- 每年重复：存储月份和日期
    yearly_months JSON COMMENT '[1,7,12] 表示1月、7月、12月',
    yearly_days JSON COMMENT '[1,15] 表示1号和15号',
    
    -- 结束条件
    end_type ENUM('after_occurrences', 'on_date') DEFAULT 'after_occurrences',
    end_after_occurrences INT,
    end_on_date DATETIME,
    
    FOREIGN KEY (task_id) REFERENCES tasks(id) ON DELETE CASCADE
) COMMENT '重复规则表';

CREATE INDEX idx_recurrence_task_id ON recurrence_task(task_id);
CREATE INDEX idx_recurrence_type ON recurrence_task(repeat_type);


