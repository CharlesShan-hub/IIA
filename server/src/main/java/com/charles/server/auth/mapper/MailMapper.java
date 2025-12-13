package com.charles.server.auth.mapper;

import com.charles.server.auth.entity.Mail;
import org.apache.ibatis.annotations.Insert;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Select;

@Mapper
public interface MailMapper {
    String TABLE_NAME = "iia_mail";

    @Select("SELECT COUNT(*) FROM "+TABLE_NAME+" WHERE email = #{email}")
    boolean existsByEmail(String email);

    @Select("SELECT * FROM "+TABLE_NAME+" WHERE email = #{email}")
    Mail findByEmail(String email);

    @Select("SELECT * FROM "+TABLE_NAME+" WHERE user_id = #{userId}")
    Mail findByAuthId(Long userId);

    @Insert("INSERT INTO "+TABLE_NAME+" (email, user_id) VALUES(#{email}, #{userId})")
    int insert(Mail mail);
}