package com.charles.server.auth.mapper;

import com.charles.server.auth.entity.Account;
import com.charles.server.auth.entity.UserAll;
import org.apache.ibatis.annotations.Insert;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Options;
import org.apache.ibatis.annotations.Select;
import org.apache.ibatis.annotations.Update;
import org.apache.ibatis.annotations.Result;
import org.apache.ibatis.annotations.Results;

@Mapper
public interface AuthMapper {
    String ACCOUNT_TABLE = "iia_auth";
    String PROFILE_TABLE = "iia_profile";
    String MAIL_TABLE = "iia_mail";

    @Select("SELECT * FROM " + ACCOUNT_TABLE + " WHERE user_id = #{userId}")
    @Deprecated
    Account findAccountById(Long userId);

    @Insert("INSERT INTO " + ACCOUNT_TABLE + " (password_hash) VALUES(#{passwordHash})")
    @Options(useGeneratedKeys = true, keyProperty = "userId", keyColumn = "user_id")
    void insertAccount(Account account);

    @Update("UPDATE " + ACCOUNT_TABLE + " SET password_hash = #{passwordHash} WHERE user_id = #{userId}")
    void updateAccount(Account account);

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