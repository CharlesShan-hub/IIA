package com.charles.server.auth.mapper;

import com.charles.server.auth.entity.Account;
import com.charles.server.auth.entity.Mail;
import com.charles.server.auth.entity.Profile;
import com.charles.server.auth.entity.UserAll;
import org.apache.ibatis.annotations.Insert;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Options;
import org.apache.ibatis.annotations.Select;
import org.apache.ibatis.annotations.Update;
import org.apache.ibatis.annotations.Result;
import org.apache.ibatis.annotations.Results;

// 用于 Mapper 内部使用的注册 DTO
class RegisterDto {
    private String email;
    private String passwordHash;
    private String username;
    
    public String getEmail() { return email; }
    public void setEmail(String email) { this.email = email; }
    
    public String getPasswordHash() { return passwordHash; }
    public void setPasswordHash(String passwordHash) { this.passwordHash = passwordHash; }
    
    public String getUsername() { return username; }
    public void setUsername(String username) { this.username = username; }
}

@Mapper
public interface UserMapper {
    // 表名常量
    String ACCOUNT_TABLE = "iia_auth";
    String PROFILE_TABLE = "iia_profile";
    String MAIL_TABLE = "iia_mail";

    // === 邮箱相关操作 ===
    
    @Select("SELECT COUNT(*) FROM " + MAIL_TABLE + " WHERE email = #{email}")
    boolean existsByEmail(String email);

    @Select("SELECT * FROM " + MAIL_TABLE + " WHERE email = #{email}")
    @Deprecated
    Mail findByEmail(String email);

    @Insert("INSERT INTO " + MAIL_TABLE + " (email, user_id) VALUES(#{email}, #{userId})")
    int insertMail(Mail mail);

    // === 账户相关操作 ===
    
    @Select("SELECT * FROM " + ACCOUNT_TABLE + " WHERE user_id = #{userId}")
    @Deprecated
    Account findAccountById(Long userId);

    @Insert("INSERT INTO " + ACCOUNT_TABLE + " (password_hash) VALUES(#{passwordHash})")
    @Options(useGeneratedKeys = true, keyProperty = "userId", keyColumn = "user_id")
    void insertAccount(Account account);

    @Update("UPDATE " + ACCOUNT_TABLE + " SET password_hash = #{passwordHash} WHERE user_id = #{userId}")
    void updateAccount(Account account);

    // === 资料相关操作 ===
    
    @Insert("INSERT INTO " + PROFILE_TABLE + " (user_id, username) VALUES(#{userId}, #{username})")
    int insertProfile(Profile profile);

    // === 根据邮箱获取完整用户信息（用于登录） ===
    
    @Select("SELECT a.user_id, a.password_hash, p.username, m.email " +
            "FROM " + ACCOUNT_TABLE + " a " +
            "JOIN " + PROFILE_TABLE + " p ON a.user_id = p.user_id " +
            "JOIN " + MAIL_TABLE + " m ON a.user_id = m.user_id " +
            "WHERE m.email = #{email}")
    @Results({
        @Result(property = "userId", column = "user_id"),
        @Result(property = "passwordHash", column = "password_hash"),
        @Result(property = "username", column = "username"),
        @Result(property = "email", column = "email")
    })
    UserAll findAllByEmail(String email);
}