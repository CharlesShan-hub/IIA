package com.charles.server.reminder.dto;

import lombok.Data;
import java.util.List;

@Data
public class BatchUpdatePositionRequest {
    private List<ProjectPosition> projects;
    
    @Data
    public static class ProjectPosition {
        private Long projectId;
        private Integer sortOrder;
    }
}