package com.charles.server.iia.auth.entity;

import lombok.Data;
import java.time.LocalDateTime;

@Data
public class Profile {
    private Long id; // 关联的认证ID
    private String nickname;
    private LocalDateTime createdAt;
}