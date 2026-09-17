package com.charles.server.auth.entity;

import com.easy.query.core.annotation.Column;
import com.easy.query.core.annotation.EntityProxy;
import com.easy.query.core.annotation.Table;
import com.easy.query.core.proxy.ProxyEntityAvailable;

import com.charles.server.auth.entity.proxy.AccountProxy;

import lombok.Data;

@Data
@Table("iia_auth")
@EntityProxy
public class Account implements ProxyEntityAvailable<Account, AccountProxy> {
    @Column(primaryKey = true)
    private Long userId;
    private String passwordHash;
}