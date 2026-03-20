package com.charles.server.reminder.dto;

import lombok.Data;
import lombok.AllArgsConstructor;
import java.util.List;

@Data
public class BatchUpdatePositionDTO {
    private List<Position> pos;
    
    @Data
    @AllArgsConstructor
    public static class Position {
        private Long itemId;
        private Integer sortOrder;
    }
}