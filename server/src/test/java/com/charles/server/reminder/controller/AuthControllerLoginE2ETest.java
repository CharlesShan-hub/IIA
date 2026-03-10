package com.charles.server.reminder.controller;

import com.charles.server.auth.dto.LoginRequest;
import com.charles.server.auth.service.TokenService;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.junit.jupiter.api.Test;
import org.mockito.Mockito;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.context.TestConfiguration;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Primary;
import org.springframework.http.MediaType;
import com.charles.server.BaseE2eDatabaseTest;
import org.springframework.test.web.servlet.MockMvc;

import java.util.HashMap;
import java.util.Map;
import java.util.Objects;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.MOCK)
@AutoConfigureMockMvc(addFilters = false)
class AuthControllerLoginE2ETest extends BaseE2eDatabaseTest {

    @Override
    protected String seedPassword() { return "123456"; }

    /* DB properties provided by BaseE2eDatabaseTest */

    @Autowired MockMvc mockMvc;
    @Autowired ObjectMapper objectMapper;

    /* Schema init handled by BaseE2eDatabaseTest */

    @TestConfiguration
    static class TestConfig {
        @Bean @Primary TokenService tokenService() {
            TokenService mock = Mockito.mock(TokenService.class);
            Map<String, String> tokens = new HashMap<>();
            tokens.put("accessToken", "test-access");
            tokens.put("refreshToken", "test-refresh");
            Mockito.when(mock.get(Mockito.anyString())).thenReturn(tokens);
            return mock;
        }
    }

    @Test
    void login_success_with_real_bcrypt() throws Exception {
        LoginRequest req = new LoginRequest();
        req.setEmail("test@example.com");
        req.setPassword("123456");

        mockMvc.perform(post("/api/auth/login")
                        .contentType(Objects.requireNonNull(MediaType.APPLICATION_JSON))
                        .content(Objects.requireNonNull(objectMapper.writeValueAsString(req))))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.code").value(200))
                .andExpect(jsonPath("$.data.token").value("test-access"))
                .andExpect(jsonPath("$.data.refreshToken").value("test-refresh"));
    }
}