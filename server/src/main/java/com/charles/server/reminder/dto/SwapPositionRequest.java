package com.charles.server.reminder.dto;

import com.charles.server.utils.ColorUtils;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Size;
import lombok.Data;

@Data
public class SwapPositionRequest {
    private Long projectId;
    private Integer sortOrder;
}