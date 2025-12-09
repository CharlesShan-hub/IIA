package com.charles.server.auth.dto;

public class RefreshResponse {
    private String token;
    
    public RefreshResponse(String token) {
        this.token = token;
    }
    
    public String getToken() {
        return token;
    }
    
    public void setToken(String token) {
        this.token = token;
    }
}