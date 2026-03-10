package com.charles.server.reminder.entity;

import lombok.Data;
import lombok.Builder;

@Data
@Builder
public class TaskTag {
    private Long id; // 关联ID
    private Long taskId; // 任务ID
    private Long tagId; // 标签ID
}