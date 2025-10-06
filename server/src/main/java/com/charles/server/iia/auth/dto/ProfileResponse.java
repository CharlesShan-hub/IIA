package com.charles.server.iia.auth.dto;

import lombok.Data;

@Data
public class ProfileResponse {
    private Long userId;
    private String email;
    private String userName;
}