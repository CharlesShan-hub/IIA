package com.charles.server.reminder.entity;

import java.time.LocalDateTime;
import lombok.Data;

@Data
public class Recurrence {
    private Long taskId; // 与Task实体一对一关联
    private String category; // 'weekly', 'monthly', 'yearly', 'days', 'weeks', 'ebinghaus'
    private Integer interval; // 间隔数值 - days/weeks类型使用
    private Integer count; // 总重复次数
    private LocalDateTime nextTime; // 下一次发生时间
    private Boolean isPaused; // 是否暂停循环
    private Boolean isSkipOverdue; // 完成后是否跳过已过期实例
    private Boolean isRepeatFromDue; // 按计划日期+周期(true)还是完成日期+周期(false)
    private String schedule; // 要注意services需要转换string和json
}
