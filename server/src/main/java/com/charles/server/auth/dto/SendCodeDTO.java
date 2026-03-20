package com.charles.server.auth.dto;

import jakarta.validation.constraints.Email;
import lombok.Data;

@Data
public class SendCodeDTO {
    @Email(message = "email format is incorrect")
    private String email;
}
