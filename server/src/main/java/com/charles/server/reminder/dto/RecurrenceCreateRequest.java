package com.charles.server.reminder.dto;

import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Pattern;
import java.time.LocalDateTime;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class RecurrenceCreateRequest {
    @NotNull(message = "taskId is required")
    private Long taskId;

    @NotBlank(message = "category is required")
    @Pattern(
        regexp = "^(weekly|monthly|yearly|days|weeks|ebinghaus)$",
        message = "category must be one of: weekly|monthly|yearly|days|weeks|ebinghaus"
    )
    private String category;

    @Min(1)
    private Integer interval;

    @Min(1)
    private Integer count;

    private LocalDateTime nextTime;

    private String schedule;
}