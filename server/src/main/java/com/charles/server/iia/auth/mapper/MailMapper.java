package com.charles.server.iia.auth.mapper;

import com.charles.server.iia.auth.entity.Mail;
import org.apache.ibatis.annotations.Insert;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Select;

@Mapper
public interface MailMapper {
    @Select("SELECT COUNT(*) FROM iia_mail WHERE email = #{email}")
    boolean existsByEmail(String email); // 查看邮箱是否已被注册

    @Select("SELECT * FROM iia_mail WHERE email = #{email}")
    Mail findByEmail(String email); // 通过邮箱查找邮箱信息

    @Select("SELECT * FROM iia_mail WHERE auth_id = #{authId}")
    Mail findByAuthId(Long authId); // 通过认证id查找邮箱信息

    @Insert("INSERT INTO iia_mail(email, auth_id, is_checked) VALUES(#{email}, #{authId}, #{isChecked})")
    int insert(Mail mail); // 插入新的邮箱信息
}