package com.charles.server.utils;

import io.jsonwebtoken.Claims;
import io.jsonwebtoken.Jwts;
import io.jsonwebtoken.security.Keys;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;

import javax.crypto.SecretKey;
import java.util.Date;

/**
 * JWT Utils
 * Generate and verify JWT tokens
 */
@Component
public class JwtUtils {
    @Value("${jwt.secret}")
    private String jwtSecret;
    
    @Value("${jwt.expiration}")
    private int jwtExpirationMs;
    
    @Value("${jwt.refresh-expiration}")
    private int jwtRefreshExpirationMs;
    
    /**
     * Generate access token
     * @return JWT Access Token
     */
    public String generateAccessToken(String userId) {
        SecretKey key = Keys.hmacShaKeyFor(jwtSecret.getBytes());
        return Jwts.builder()
                .subject(userId)
                .issuedAt(new Date())
                .expiration(new Date(System.currentTimeMillis() + jwtExpirationMs))
                .claim("type", "access")
                .signWith(key, Jwts.SIG.HS512)
                .compact();
    }
    
    /**
     * Generate refresh token
     * @return JWT Refresh Token
     */
    public String generateRefreshToken(String userId) {
        SecretKey key = Keys.hmacShaKeyFor(jwtSecret.getBytes());
        return Jwts.builder()
                .subject(userId)
                .issuedAt(new Date())
                .expiration(new Date(System.currentTimeMillis() + jwtRefreshExpirationMs))
                .claim("type", "refresh")
                .signWith(key, Jwts.SIG.HS512)
                .compact();
    }

    /**
     * Validate access token
     * @param accessToken JWT Token
     * @return boolean
     */
    public boolean validateAccessToken(String accessToken) {
        try {
            SecretKey key = Keys.hmacShaKeyFor(jwtSecret.getBytes());
            Claims claims = Jwts.parser()
                .verifyWith(key)
                .build()
                .parseSignedClaims(accessToken)
                .getPayload();
            String tokenType = claims.get("type", String.class);
            return "access".equals(tokenType);
        } catch (Exception e) {
            return false;
        }
    }
    
    /**
     * Validate refresh token
     * @param refreshToken JWT Refresh Token
     * @return boolean
     */
    public boolean validateRefreshToken(String refreshToken) {
        try {
            SecretKey key = Keys.hmacShaKeyFor(jwtSecret.getBytes());
            Claims claims = Jwts.parser()
                .verifyWith(key)
                .build()
                .parseSignedClaims(refreshToken)
                .getPayload();
            String tokenType = claims.get("type", String.class);
            return "refresh".equals(tokenType);
        } catch (Exception e) {
            return false;
        }
    }

    /**
     * Get User ID from JWT Token
     * @param token JWT Token
     * @return User ID
     */
    public String getUserIdFromToken(String token) {
        SecretKey key = Keys.hmacShaKeyFor(jwtSecret.getBytes());
        return Jwts.parser()
                .verifyWith(key)
                .build()
                .parseSignedClaims(token)
                .getPayload()
                .getSubject();
    }
    
    /**
     * Get Token Type from JWT Token
     * @param token JWT Token
     * @return Token Type (access/refresh)  
     */
    public String getTokenType(String token) {
        SecretKey key = Keys.hmacShaKeyFor(jwtSecret.getBytes());
        return Jwts.parser()
                .verifyWith(key)
                .build()
                .parseSignedClaims(token)
                .getPayload()
                .get("type", String.class);
    }
}