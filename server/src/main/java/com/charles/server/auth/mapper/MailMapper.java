package com.charles.server.auth.mapper;

import com.charles.server.auth.entity.Mail;
import org.apache.ibatis.annotations.Insert;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Select;

@Mapper
public interface MailMapper {
    @Select("SELECT COUNT(*) FROM iia_mail WHERE email = #{email}")
    boolean existsByEmail(String email);

    @Select("SELECT * FROM iia_mail WHERE email = #{email}")
    Mail findByEmail(String email);

    @Select("SELECT * FROM iia_mail WHERE user_id = #{userId}")
    Mail findByAuthId(Long userId);

    @Insert("INSERT INTO iia_mail(email, user_id) VALUES(#{email}, #{userId})")
    int insert(Mail mail);
}