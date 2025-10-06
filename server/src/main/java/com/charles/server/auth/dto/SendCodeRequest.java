package com.charles.server.auth.dto;

import jakarta.validation.constraints.Email;
import lombok.Data;

@Data
public class SendCodeRequest {
    @Email(message = "邮箱格式不正确")
    private String email;
}
