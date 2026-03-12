package com.charles.server.reminder.entity;

import java.time.LocalDateTime;
import lombok.Data;
import lombok.Builder;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class History {
    // 操作追踪
    private Long operationId; // 操作批次ID
    
    // 当前任务必要信息
    private Long historyId; // 历史记录ID
    private Long taskId; // 任务ID
    private LocalDateTime createdAt; // 记录创建时间
    private Boolean isCompleted; // 是否完成
    private Boolean isAbandoned; // 是否废弃
    
    // 循环任务可选信息
    private Boolean isSkipped; // 是否跳过（仅对循环任务有效）
    @Builder.Default
    private Integer current = null; // 当前重复次数，非循环任务为null
}