package com.charles.server.auth.entity;

import com.easy.query.core.annotation.EntityProxy;
import com.easy.query.core.proxy.ProxyEntityAvailable;

import com.charles.server.auth.entity.proxy.UserAllProxy;

import lombok.Data;

@Data
@EntityProxy
public class UserAll implements ProxyEntityAvailable<UserAll, UserAllProxy> {
    private Long userId;
    private String passwordHash;
    private String username;
    private String email;
}