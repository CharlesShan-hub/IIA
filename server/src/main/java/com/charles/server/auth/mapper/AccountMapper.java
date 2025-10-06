package com.charles.server.auth.mapper;

import com.charles.server.auth.entity.Account;
import org.apache.ibatis.annotations.Insert;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Options;
import org.apache.ibatis.annotations.Select;
import org.apache.ibatis.annotations.Update;

@Mapper
public interface AccountMapper {
    @Insert("INSERT INTO iia_auth(password_hash) VALUES(#{passwordHash})")
    @Options(useGeneratedKeys = true, keyProperty = "userId", keyColumn = "user_id")
    void insert(Account account); // 插入新的认证信息

    @Select("SELECT * FROM iia_auth WHERE user_id = #{userId}")
    Account findById(Long userId); // 通过id查找认证信息

    @Update("UPDATE iia_auth SET password_hash = #{passwordHash} WHERE user_id = #{userId}")
    void updateById(Account account); // 更新认证信息（密码）
}