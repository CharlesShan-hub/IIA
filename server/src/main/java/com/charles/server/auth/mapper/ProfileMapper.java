package com.charles.server.auth.mapper;

import com.charles.server.auth.entity.Profile;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Select;
import org.apache.ibatis.annotations.Insert;

@Mapper
public interface ProfileMapper {
    
    String PROFILE_TABLE = "iia_profile";
    
    @Select("SELECT user_id, username FROM " + PROFILE_TABLE + " WHERE user_id = #{userId}")
    Profile findById(Long userId);

    @Insert("INSERT INTO " + PROFILE_TABLE + " (user_id, username) VALUES(#{userId}, #{username})")
    int insertProfile(Profile profile);
}