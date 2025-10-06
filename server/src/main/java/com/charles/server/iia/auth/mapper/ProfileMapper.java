package com.charles.server.iia.auth.mapper;

import com.charles.server.iia.auth.entity.Profile;
import org.apache.ibatis.annotations.Insert;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Select;

@Mapper
public interface ProfileMapper {
    @Insert("INSERT INTO iia_profile(id, username) VALUES(#{id}, #{username})")
    int insert(Profile profile); // 插入新的用户基本信息
    
    @Select("SELECT * FROM iia_profile WHERE id = #{id}")
    Profile findById(Long id); // 通过id查找用户基本信息
}