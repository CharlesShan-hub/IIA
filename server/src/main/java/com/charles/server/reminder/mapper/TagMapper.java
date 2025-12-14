package com.charles.server.reminder.mapper;

import java.util.List;

import org.apache.ibatis.annotations.Insert;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Options;
import org.apache.ibatis.annotations.Param;
import org.apache.ibatis.annotations.Select;
import org.apache.ibatis.annotations.Update;

import com.charles.server.reminder.entity.Tag;

@Mapper
public interface TagMapper {
    
    // 插入新标签
    @Insert("INSERT INTO reminder_tag(user_id, name, color) VALUES(#{userId}, #{name}, #{color})")
    @Options(useGeneratedKeys = true, keyProperty = "tagId", keyColumn = "tag_id")
    int insert(Tag tag);
    
    // 根据ID查询标签
    @Select("SELECT * FROM reminder_tag WHERE tag_id = #{tagId}")
    Tag findById(Long tagId);

    // 根据标签名称查询标签
    @Select("SELECT * FROM reminder_tag WHERE name = #{name} AND user_id = #{userId}")
    Tag findByName(Long userId, String name);
    
    // 查询用户的所有标签
    @Select("SELECT * FROM reminder_tag WHERE user_id = #{userId}")
    List<Tag> findByUserId(Long userId);
    
    // 更新标签信息
    @Update("UPDATE reminder_tag SET name = #{name}, color = #{color} WHERE tag_id = #{tagId}")
    int update(Tag tag);
    
    // 查询标签是否存在（根据用户ID和标签名称）
    @Select("SELECT COUNT(*) FROM reminder_tag WHERE user_id = #{userId} AND name = #{name}")
    boolean existsByNameAndUserId(@Param("name") String name, @Param("userId") Long userId);
}