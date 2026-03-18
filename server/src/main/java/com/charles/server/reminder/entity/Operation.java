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
public class Operation {
    private Long operationId;
    private Long userId;
    private LocalDateTime performedAt;
    
    // 表影响标识 - 默认都为false
    @Builder.Default
    private Boolean isReminderProject = false;
    @Builder.Default
    private Boolean isReminderTask = false;
    @Builder.Default
    private Boolean isReminderRecurrence = false;
    @Builder.Default
    private Boolean isReminderHistory = false;
    @Builder.Default
    private Boolean isReminderTag = false;
    @Builder.Default
    private Boolean isReminderTaskTag = false;
}