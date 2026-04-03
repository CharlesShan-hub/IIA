package com.charles.server.reminder.entity;

import lombok.Data;
import java.time.LocalDateTime;

@Data
public class ProjectLog {
    private Long logId;
    private Long projectId;
    private Long operationId;
    private Long batchOperationId;
    private Long userId;
    private String name;
    private String description;
    private String color;
    private String icon;
    private Integer sortOrder;
    private Boolean isArchived;
    private LocalDateTime createdAt;
    
    /**
     * 从Project实体创建ProjectLog
     * @param project 项目实体
     * @return 项目日志实体
     */
    public static ProjectLog fromProject(Project project) {
        return fromProject(project, null);
    }
    
    /**
     * 从Project实体创建ProjectLog（带批量操作ID）
     * @param project 项目实体
     * @param batchOperationId 批量操作ID
     * @return 项目日志实体
     */
    public static ProjectLog fromProject(Project project, Long batchOperationId) {
        ProjectLog log = new ProjectLog();
        log.setProjectId(project.getProjectId());
        log.setOperationId(project.getOperationId());
        log.setBatchOperationId(batchOperationId);
        log.setUserId(project.getUserId());
        log.setName(project.getName());
        log.setDescription(project.getDescription());
        log.setColor(project.getColor());
        log.setIcon(project.getIcon());
        log.setSortOrder(project.getSortOrder());
        log.setIsArchived(project.getIsArchived());
        return log;
    }
    
    /**
     * 从ProjectLog创建Project实体
     * @param userId 用户ID（因为log中可能没有userId）
     * @param operationId 操作ID（要设置的新操作ID）
     * @return 项目实体
     */
    public Project toProject(Long userId, Long operationId) {
        return Project.builder()
                .projectId(this.projectId)
                .userId(userId)
                .name(this.name)
                .description(this.description)
                .color(this.color)
                .icon(this.icon)
                .sortOrder(this.sortOrder)
                .isArchived(this.isArchived)
                .operationId(operationId)
                .build();
    }
    
    /**
     * 从ProjectLog创建Project实体（使用log中的operationId）
     * @param userId 用户ID
     * @return 项目实体
     */
    public Project toProject(Long userId) {
        return toProject(userId, this.operationId);
    }
}