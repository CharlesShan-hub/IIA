package com.charles.server.iia.config;

import com.charles.server.iia.security.JwtAuthenticationFilter;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.security.web.SecurityFilterChain;
import org.springframework.security.web.authentication.UsernamePasswordAuthenticationFilter;

@Configuration
@EnableWebSecurity
public class SecurityConfig {

    @Autowired
    private JwtAuthenticationFilter jwtAuthFilter;
    
    /**
     * 配置密码加密器
     * 会被自动注入到需要PasswordEncoder的地方
     */
    @Bean
    public PasswordEncoder passwordEncoder() {
        return new BCryptPasswordEncoder();
        // 默认强度10（推荐），如需调整可传参：new BCryptPasswordEncoder(12)
    }
    
    /**
     * 配置Spring Security过滤器链
     */
    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        http
            // 禁用CSRF保护（对于API通常不需要）
            .csrf(csrf -> csrf.disable())
            
            // 添加JWT过滤器
            .addFilterBefore(jwtAuthFilter, UsernamePasswordAuthenticationFilter.class)
            
            // 配置URL访问权限
            .authorizeHttpRequests(auth -> auth
                // 允许所有用户访问认证端点
                .requestMatchers("/api/auth/**").permitAll()
                // 其他所有请求都需要认证
                .anyRequest().authenticated()
            );
        
        return http.build();
    }
}