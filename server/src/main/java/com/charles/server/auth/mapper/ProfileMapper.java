package com.charles.server.auth.mapper;

import com.charles.server.auth.entity.Profile;
import org.apache.ibatis.annotations.Insert;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Select;

@Mapper
public interface ProfileMapper {
    String TABLE_NAME = "iia_profile";

    @Insert("INSERT INTO "+TABLE_NAME+" (user_id, username) VALUES(#{userId}, #{username})")
    int insert(Profile profile);

    @Select("SELECT * FROM "+TABLE_NAME+" WHERE user_id = #{userId}")
    Profile findById(Long userId);
}