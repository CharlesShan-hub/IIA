package com.charles.server.utils;

import com.charles.server.auth.service.TokenService;
import org.mockito.Mockito;
import org.springframework.boot.test.context.TestConfiguration;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Primary;

@TestConfiguration
public class TestTokenServiceConfig {
    
    @Bean
    @Primary
    public TokenService tokenService() {
        TokenService mock = Mockito.mock(TokenService.class);
        Mockito.when(mock.getUserIdFromRequest(Mockito.any())).thenReturn(1L);
        return mock;
    }
}