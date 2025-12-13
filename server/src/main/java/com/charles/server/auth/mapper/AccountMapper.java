package com.charles.server.auth.mapper;

import com.charles.server.auth.entity.Account;
import org.apache.ibatis.annotations.Insert;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Options;
import org.apache.ibatis.annotations.Select;
import org.apache.ibatis.annotations.Update;

@Mapper
public interface AccountMapper {
    String TABLE_NAME = "iia_auth";

    @Insert("INSERT INTO "+TABLE_NAME+" (password_hash) VALUES(#{passwordHash})")
    @Options(useGeneratedKeys = true, keyProperty = "userId", keyColumn = "user_id")
    void insert(Account account);

    @Select("SELECT * FROM "+TABLE_NAME+" WHERE user_id = #{userId}")
    Account findById(Long userId);

    @Update("UPDATE "+TABLE_NAME+" SET password_hash = #{passwordHash} WHERE user_id = #{userId}")
    void updateById(Account account);
}