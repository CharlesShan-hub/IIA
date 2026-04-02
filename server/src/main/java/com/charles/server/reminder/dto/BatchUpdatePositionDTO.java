package com.charles.server.reminder.dto;

import io.swagger.v3.oas.annotations.media.Schema;
import lombok.Data;
import java.util.List;
import com.charles.server.reminder.entity.Position;

@Data
@Schema(description = "Batch update position request data")
public class BatchUpdatePositionDTO {
    @Schema(
        description = "Position list",
        example = "[{\"itemId\": 1, \"sortOrder\": 0}, {\"itemId\": 2, \"sortOrder\": 1}]",
        requiredMode = Schema.RequiredMode.REQUIRED
    )
    private List<Position> pos;
}