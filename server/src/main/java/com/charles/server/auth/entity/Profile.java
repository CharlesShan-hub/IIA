package com.charles.server.auth.entity;

import com.easy.query.core.annotation.Column;
import com.easy.query.core.annotation.EntityProxy;
import com.easy.query.core.annotation.Table;
import com.easy.query.core.proxy.ProxyEntityAvailable;

import com.charles.server.auth.entity.proxy.ProfileProxy;

import java.time.LocalDateTime;

import lombok.Data;

@Data
@Table("iia_profile")
@EntityProxy
public class Profile implements ProxyEntityAvailable<Profile, ProfileProxy> {
    @Column(primaryKey = true)
    private Long userId;
    private String username;
    private LocalDateTime createdAt;
}