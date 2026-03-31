package com.charles.server.auth.dto;

import lombok.Data;
import lombok.AllArgsConstructor;

@Data
@AllArgsConstructor
public class SendCodeVO {
    private String code;
}
