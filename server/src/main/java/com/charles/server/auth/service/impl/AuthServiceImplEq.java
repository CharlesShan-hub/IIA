package com.charles.server.auth.service.impl;

import com.charles.server.auth.dto.*;
import com.charles.server.auth.entity.Profile;
import com.charles.server.auth.exception.AuthException;
import com.charles.server.auth.service.AuthService;
import com.easy.query.api.proxy.client.EasyEntityQuery;
import lombok.RequiredArgsConstructor;
import org.springframework.boot.autoconfigure.condition.ConditionalOnProperty;
import org.springframework.stereotype.Service;

/**
 * easy-query 版 AuthService 实现（教学实验台）
 * 与 AuthServiceImpl（MyBatis 版）通过 app.orm 配置切换，同一接口互斥激活
 */
@Service
@RequiredArgsConstructor
@ConditionalOnProperty(name = "app.orm", havingValue = "easy-query")
public class AuthServiceImplEq implements AuthService {
    private final EasyEntityQuery easyEntityQuery;

    @Override
    public LoginVO login(LoginDTO dto) {
        // TODO: easy-query 联表查询（Account + Profile + Mail 三表），替换 authMapper.findAllByEmail
        // 思路: easyEntityQuery.queryable(Account.class).leftJoin(Profile.class,...)...
        throw new UnsupportedOperationException("easy-query 版 login 待实现，参考 AuthServiceImpl.login 的业务逻辑");
    }

    @Override
    public RegisterVO register(RegisterDTO dto) {
        // TODO: easy-query insertable 批量插入 Account / Profile / Mail，替换 authMapper.insertAccount 等
        // 思路: easyEntityQuery.insertable(account).executeRows(true) 会回填自增主键
        throw new UnsupportedOperationException("easy-query 版 register 待实现，参考 AuthServiceImpl.register 的业务逻辑");
    }

    @Override
    public ProfileVO profile(String userId) {
        // ✅ 第一个完整实现：单表查询，类型安全写法
        Profile profile = easyEntityQuery.queryable(Profile.class)
                .where(p -> p.userId().eq(Long.valueOf(userId)))
                .firstOrNull();
        if (profile == null) {
            throw AuthException.userNotFound(userId);
        }

        ProfileVO response = new ProfileVO();
        response.setUserName(profile.getUsername());
        response.setUserId(profile.getUserId());
        return response;
    }

    @Override
    public void resetPassword(ResetPasswordDTO dto) {
        // TODO: easy-query updatable 更新密码，替换 authMapper.updateAccount
        // 思路: easyEntityQuery.updatable(Account.class).where(...).setColumns(...)
        throw new UnsupportedOperationException("easy-query 版 resetPassword 待实现，参考 AuthServiceImpl.resetPassword 的业务逻辑");
    }
}