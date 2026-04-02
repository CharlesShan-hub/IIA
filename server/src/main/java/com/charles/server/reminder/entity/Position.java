package com.charles.server.reminder.entity;

import io.swagger.v3.oas.annotations.media.Schema;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
@Schema(description = "Position information for sorting items")
public class Position {
    @Schema(
        description = "Item ID",
        example = "1",
        requiredMode = Schema.RequiredMode.REQUIRED
    )
    private Long itemId;
    
    @Schema(
        description = "Sort order",
        example = "0",
        requiredMode = Schema.RequiredMode.REQUIRED
    )
    private Integer sortOrder;
}