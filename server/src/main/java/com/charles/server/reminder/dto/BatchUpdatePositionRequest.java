package com.charles.server.reminder.dto;

import lombok.Data;
import lombok.AllArgsConstructor;
import java.util.List;

@Data
public class BatchUpdatePositionRequest {
    private List<Position> pos;
    
    @Data
    @AllArgsConstructor
    public static class Position {
        private Long itemId;
        private Integer sortOrder;
    }
}