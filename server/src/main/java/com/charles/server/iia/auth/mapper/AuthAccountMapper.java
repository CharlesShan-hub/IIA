package com.charles.server.iia.auth.mapper;

import com.charles.server.iia.auth.entity.AuthAccount;
import org.apache.ibatis.annotations.Insert;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Options;
import org.apache.ibatis.annotations.Select;
import org.apache.ibatis.annotations.Update;

@Mapper
public interface AuthAccountMapper {
    @Insert("INSERT INTO iia_auth(password_hash) VALUES(#{passwordHash})")
    @Options(useGeneratedKeys = true, keyProperty = "id")
    int insert(AuthAccount account); // 插入新的认证信息
    
    @Select("SELECT * FROM iia_auth WHERE id = #{id}")
    AuthAccount findById(Long id); // 通过id查找认证信息
    
    @Update("UPDATE iia_auth SET password_hash = #{passwordHash} WHERE id = #{id}")
    int updateById(AuthAccount account); // 更新认证信息（密码）
}