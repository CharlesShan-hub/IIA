package com.charles.server.reminder.mapper;

import java.util.List;

import org.apache.ibatis.annotations.Insert;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Options;
import org.apache.ibatis.annotations.Param;
import org.apache.ibatis.annotations.Select;
import org.apache.ibatis.annotations.Update;
import org.apache.ibatis.annotations.Delete;

import com.charles.server.reminder.entity.Tag;

@Mapper
public interface TagMapper {
    
    // 插入新标签
    @Insert("INSERT INTO reminder_tag(user_id, name, color, operation_id) VALUES(#{userId}, #{name}, #{color}, #{operationId})")
    @Options(useGeneratedKeys = true, keyProperty = "tagId", keyColumn = "tag_id")
    int insert(Tag tag);
    
    // 根据ID查询标签
    @Select("SELECT * FROM reminder_tag WHERE tag_id = #{tagId}")
    Tag findById(Long tagId);
    
    // 查询用户的所有标签
    @Select("SELECT * FROM reminder_tag WHERE user_id = #{userId}")
    List<Tag> findByUserId(Long userId);
    
    // 根据操作ID查询标签
    @Select("SELECT * FROM reminder_tag WHERE operation_id = #{operationId}")
    List<Tag> findByOperationId(@Param("operationId") Long operationId);
    
    // 更新标签信息
    @Update("UPDATE reminder_tag SET name = #{name}, color = #{color} WHERE tag_id = #{tagId}")
    int update(Tag tag);

    // 删除标签
    @Delete("DELETE FROM reminder_tag WHERE tag_id = #{tagId}")
    int deleteById(@Param("tagId") Long tagId);
    
    // 根据标签ID和操作ID删除标签
    @Delete("DELETE FROM reminder_tag WHERE tag_id = #{tagId} AND operation_id = #{operationId}")
    int deleteByTagIdAndOperationId(@Param("tagId") Long tagId, @Param("operationId") Long operationId);
    
    // 查询标签是否存在（根据用户ID和标签名称）
    @Select("SELECT COUNT(*) FROM reminder_tag WHERE user_id = #{userId} AND name = #{name}")
    boolean existsByNameAndUserId(@Param("name") String name, @Param("userId") Long userId);
}