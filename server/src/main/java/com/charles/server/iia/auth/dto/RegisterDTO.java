package com.charles.server.iia.auth.dto;

import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Size;
import lombok.Data;

@Data
public class RegisterDTO {
    @Email
    private String email;

    @NotBlank @Size(min = 6, max = 20)
    private String password;

    private String username; // 用户昵称，可为空

    @NotBlank(message = "验证码不能为空")
    private String code; // 新增验证码字段
}