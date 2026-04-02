package com.charles.server.reminder.entity;

import lombok.Data;
import java.time.LocalDateTime;

@Data
public class TagLog {
    private Long logId;
    private Long tagId;
    private Long operationId;
    private Long batchOperationId;
    private Long userId;
    private String name;
    private String color;
    private LocalDateTime createdAt;
    
    /**
     * 从Tag实体创建TagLog
     * @param tag 标签实体
     * @return 标签日志实体
     */
    public static TagLog fromTag(Tag tag) {
        return fromTag(tag, null);
    }
    
    /**
     * 从Tag实体创建TagLog（带批量操作ID）
     * @param tag 标签实体
     * @param batchOperationId 批量操作ID
     * @return 标签日志实体
     */
    public static TagLog fromTag(Tag tag, Long batchOperationId) {
        TagLog log = new TagLog();
        log.setTagId(tag.getTagId());
        log.setOperationId(tag.getOperationId());
        log.setBatchOperationId(batchOperationId);
        log.setUserId(tag.getUserId());
        log.setName(tag.getName());
        log.setColor(tag.getColor());
        return log;
    }
    
    /**
     * 从TagLog创建Tag实体
     * @param userId 用户ID（因为log中可能没有userId）
     * @param operationId 操作ID（要设置的新操作ID）
     * @return 标签实体
     */
    public Tag toTag(Long userId, Long operationId) {
        return Tag.builder()
                .tagId(this.tagId)
                .userId(userId)
                .name(this.name)
                .color(this.color)
                .operationId(operationId)
                .build();
    }
    
    /**
     * 从TagLog创建Tag实体（使用log中的operationId）
     * @param userId 用户ID
     * @return 标签实体
     */
    public Tag toTag(Long userId) {
        return toTag(userId, this.operationId);
    }
}