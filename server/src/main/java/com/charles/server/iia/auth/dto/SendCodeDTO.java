package com.charles.server.iia.auth.dto;

import jakarta.validation.constraints.Email;
import lombok.Data;

@Data
public class SendCodeDTO {
    @Email(message = "邮箱格式不正确")
    private String email;
}
