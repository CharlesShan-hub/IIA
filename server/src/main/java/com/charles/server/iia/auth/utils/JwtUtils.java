package com.charles.server.iia.auth.utils;

import io.jsonwebtoken.Claims;
import io.jsonwebtoken.Jwts;
import io.jsonwebtoken.SignatureAlgorithm;
import io.jsonwebtoken.security.Keys;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;

import javax.crypto.SecretKey;
import java.util.Date;

/**
 * JWT工具类，用于生成和验证Token
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
     * 生成访问Token (Access Token)
     * @param userId 用户ID
     * @return JWT Token
     */
    public String generateAccessToken(String userId) {
        SecretKey key = Keys.hmacShaKeyFor(jwtSecret.getBytes());
        return Jwts.builder()
                .setSubject(userId)
                .setIssuedAt(new Date())
                .setExpiration(new Date(System.currentTimeMillis() + jwtExpirationMs))
                .claim("type", "access")
                .signWith(key, SignatureAlgorithm.HS512)
                .compact();
    }
    
    /**
     * 生成刷新Token (Refresh Token)
     * @param userId 用户ID
     * @return JWT Refresh Token
     */
    public String generateRefreshToken(String userId) {
        SecretKey key = Keys.hmacShaKeyFor(jwtSecret.getBytes());
        return Jwts.builder()
                .setSubject(userId)
                .setIssuedAt(new Date())
                .setExpiration(new Date(System.currentTimeMillis() + jwtRefreshExpirationMs))
                .claim("type", "refresh")
                .signWith(key, SignatureAlgorithm.HS512)
                .compact();
    }
    
    /**
     * 从Token中获取用户ID
     * @param token JWT Token
     * @return 用户ID
     */
    public String getUserIdFromToken(String token) {
        SecretKey key = Keys.hmacShaKeyFor(jwtSecret.getBytes());
        return Jwts.parserBuilder()
                .setSigningKey(key)
                .build()
                .parseClaimsJws(token)
                .getBody()
                .getSubject();
    }
    
    /**
     * 获取Token类型
     * @param token JWT Token
     * @return Token类型 (access/refresh)
     */
    public String getTokenType(String token) {
        SecretKey key = Keys.hmacShaKeyFor(jwtSecret.getBytes());
        return Jwts.parserBuilder()
                .setSigningKey(key)
                .build()
                .parseClaimsJws(token)
                .getBody()
                .get("type", String.class);
    }
    
    /**
     * 验证Token是否有效
     * @param token JWT Token
     * @return 是否有效
     */
    public boolean validateToken(String token) {
        try {
            // 使用密钥解析并验证 JWT Token
            SecretKey key = Keys.hmacShaKeyFor(jwtSecret.getBytes());
            Jwts.parserBuilder()
                .setSigningKey(key)
                .build()
                .parseClaimsJws(token);
            return true;
        } catch (Exception e) {
            // Token验证失败（签名错误、过期等）
            return false;
        }
    }
    
    /**
     * 验证刷新Token是否有效
     * @param refreshToken JWT Refresh Token
     * @return 是否有效
     */
    public boolean validateRefreshToken(String refreshToken) {
        try {
            SecretKey key = Keys.hmacShaKeyFor(jwtSecret.getBytes());
            Claims claims = Jwts.parserBuilder()
                .setSigningKey(key)
                .build()
                .parseClaimsJws(refreshToken)
                .getBody();
            
            // 验证Token类型是否为refresh
            String tokenType = claims.get("type", String.class);
            return "refresh".equals(tokenType);
        } catch (Exception e) {
            // Refresh Token验证失败
            return false;
        }
    }
}