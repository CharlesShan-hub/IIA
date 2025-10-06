package com.charles.server.iia.auth.mapper;

import com.charles.server.iia.auth.entity.Profile;
import org.apache.ibatis.annotations.Insert;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Select;

@Mapper
public interface ProfileMapper {
    @Insert("INSERT INTO iia_profile(user_id, username) VALUES(#{userId}, #{username})")
    int insert(Profile profile); 
    
    @Select("SELECT * FROM iia_profile WHERE user_id = #{userId}")
    Profile findById(Long userId);
}