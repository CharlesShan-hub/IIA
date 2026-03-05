package com.charles.server.auth.mapper;

import com.charles.server.auth.entity.Profile;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Select;

@Mapper
public interface ProfileMapper {
    
    String PROFILE_TABLE = "profile";
    
    @Select("SELECT user_id, username FROM " + PROFILE_TABLE + " WHERE user_id = #{userId}")
    Profile findById(Long userId);
}