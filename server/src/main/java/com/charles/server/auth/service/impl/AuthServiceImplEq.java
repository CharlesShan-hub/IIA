package com.charles.server.auth.service.impl;

import com.charles.server.auth.dto.*;
import com.charles.server.auth.entity.Account;
import com.charles.server.auth.entity.Mail;
import com.charles.server.auth.entity.Profile;
import com.charles.server.auth.entity.UserAll;
import com.charles.server.auth.entity.proxy.UserAllProxy;
import com.charles.server.auth.exception.AuthException;
import com.charles.server.auth.service.AuthService;
import com.charles.server.auth.service.TokenService;
import com.charles.server.reminder.service.OperationService;
import com.easy.query.api.proxy.client.EasyEntityQuery;
import lombok.RequiredArgsConstructor;
import org.springframework.boot.autoconfigure.condition.ConditionalOnProperty;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.Map;

/**
 * easy-query 版 AuthService 实现（教学实验台）
 * 与 AuthServiceImpl（MyBatis 版）通过 app.orm 配置切换，同一接口互斥激活
 */
@Service
@RequiredArgsConstructor
@ConditionalOnProperty(name = "app.orm", havingValue = "easy-query")
public class AuthServiceImplEq implements AuthService {
    private final EasyEntityQuery easyEntityQuery;
    private final PasswordEncoder passwordEncoder;
    private final TokenService tokenService;
    private final OperationService operationService;

    @Override
    public LoginVO login(LoginDTO dto) {
        UserAll userAll = easyEntityQuery.queryable(Account.class)
                .leftJoin(Profile.class, (a, p) -> a.userId().eq(p.userId()))
                .leftJoin(Mail.class, (a, p, m) -> a.userId().eq(m.userId()))
                .where((a, p, m) -> m.email().eq(dto.getEmail()))
                .select((a, p, m) -> new UserAllProxy()
                        .userId().set(a.userId())
                        .passwordHash().set(a.passwordHash())
                        .username().set(p.username())
                        .email().set(m.email()))
                .firstOrNull();
        if (userAll == null) {
            throw AuthException.userNotFound(dto.getEmail());
        }

        if (!passwordEncoder.matches(dto.getPassword(), userAll.getPasswordHash())) {
            throw AuthException.invalidCredentials();
        }

        String userId = userAll.getUserId().toString();
        Map<String, String> tokens = tokenService.get(userId);

        LoginVO response = new LoginVO();
        response.setToken(tokens.get("accessToken"));
        response.setRefreshToken(tokens.get("refreshToken"));
        response.setUserId(userId);
        return response;
    }

    @Override
    @Transactional
    public RegisterVO register(RegisterDTO dto) {
        boolean exists = easyEntityQuery.queryable(Mail.class)
                .where(m -> m.email().eq(dto.getEmail()))
                .any();
        if (exists) {
            throw AuthException.emailAlreadyRegistered(dto.getEmail());
        }

        Account account = new Account();
        account.setPasswordHash(passwordEncoder.encode(dto.getPassword()));
        easyEntityQuery.insertable(account).executeRows(true);

        Profile profile = new Profile();
        profile.setUserId(account.getUserId());
        profile.setUsername(generateDefaultUsername(dto.getUsername(), dto.getEmail()));
        easyEntityQuery.insertable(profile).executeRows();

        Mail mail = new Mail();
        mail.setEmail(dto.getEmail());
        mail.setUserId(account.getUserId());
        easyEntityQuery.insertable(mail).executeRows();

        operationService.createZero(account.getUserId());

        Map<String, String> tokens = tokenService.get(account.getUserId().toString());

        RegisterVO response = new RegisterVO();
        response.setUserId(account.getUserId());
        response.setToken(tokens.get("accessToken"));
        response.setRefreshToken(tokens.get("refreshToken"));
        return response;
    }

    private String generateDefaultUsername(String providedUsername, String email) {
        if (providedUsername != null && !providedUsername.trim().isEmpty()) {
            return providedUsername.trim();
        }
        return email.split("@")[0];
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