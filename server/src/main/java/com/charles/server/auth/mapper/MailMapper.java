package com.charles.server.auth.mapper;

import com.charles.server.auth.entity.Mail;
import org.apache.ibatis.annotations.Insert;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Select;

@Mapper
public interface MailMapper {
    String MAIL_TABLE = "iia_mail";

    @Select("SELECT COUNT(*) FROM " + MAIL_TABLE + " WHERE email = #{email}")
    boolean existsByEmail(String email);

    @Insert("INSERT INTO " + MAIL_TABLE + " (email, user_id) VALUES(#{email}, #{userId})")
    int insertMail(Mail mail);
}