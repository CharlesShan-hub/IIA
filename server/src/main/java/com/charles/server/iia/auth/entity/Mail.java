package com.charles.server.iia.auth.entity;

import lombok.Data;

@Data
public class Mail {
    private String email; // 邮箱作为主键
    private Long authId; // 关联的认证ID
    private Boolean isChecked; // 是否经过验证
}