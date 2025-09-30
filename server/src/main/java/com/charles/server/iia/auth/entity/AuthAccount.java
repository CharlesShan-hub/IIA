package com.charles.server.iia.auth.entity;

import lombok.Data;
import java.time.LocalDateTime;

@Data
public class AuthAccount {
    private Long id;
    private String passwordHash;
    private LocalDateTime createdAt;
}