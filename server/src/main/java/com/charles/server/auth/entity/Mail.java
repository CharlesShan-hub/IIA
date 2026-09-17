package com.charles.server.auth.entity;

import com.easy.query.core.annotation.Column;
import com.easy.query.core.annotation.EntityProxy;
import com.easy.query.core.annotation.Table;
import com.easy.query.core.proxy.ProxyEntityAvailable;

import com.charles.server.auth.entity.proxy.MailProxy;

import lombok.Data;

@Data
@Table("iia_mail")
@EntityProxy
public class Mail implements ProxyEntityAvailable<Mail, MailProxy> {
    private Long userId;
    @Column(primaryKey = true)
    private String email;
}