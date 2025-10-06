package com.charles.server.auth.entity;

import lombok.Data;

@Data
public class Mail {
    private String email; // 邮箱作为主键
    private Long userId; // 关联的认证ID
}