package com.charles.server.reminder.mapper;

import com.charles.server.reminder.entity.TagLog;
import org.apache.ibatis.annotations.Insert;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Param;
import org.apache.ibatis.annotations.Select;
import org.apache.ibatis.annotations.Delete;

import java.util.List;

@Mapper
public interface TagLogMapper {
    
    @Insert("INSERT INTO reminder_tag_log(tag_id, operation_id, batch_operation_id, user_id, name, color) " +
            "VALUES(#{tagId}, #{operationId}, #{batchOperationId}, #{userId}, #{name}, #{color})")
    int insert(TagLog tagLog);
    
    @Select("SELECT * FROM reminder_tag_log WHERE tag_id = #{tagId} ORDER BY created_at DESC")
    List<TagLog> findByTagId(@Param("tagId") Long tagId);
    
    @Select("SELECT * FROM reminder_tag_log WHERE operation_id = #{operationId}")
    List<TagLog> findByOperationId(@Param("operationId") Long operationId);
    
    @Select("SELECT * FROM reminder_tag_log WHERE batch_operation_id = #{batchOperationId}")
    List<TagLog> findByBatchOperationId(@Param("batchOperationId") Long batchOperationId);
    
    @Select("SELECT * FROM reminder_tag_log WHERE tag_id = #{tagId} AND operation_id = #{operationId}")
    TagLog findByTagIdAndOperationId(@Param("tagId") Long tagId, @Param("operationId") Long operationId);
    
    @Delete("DELETE FROM reminder_tag_log WHERE operation_id = #{operationId}")
    int deleteByOperationId(@Param("operationId") Long operationId);

    @Delete("DELETE FROM reminder_tag_log WHERE batch_operation_id = #{batchOperationId}")
    int deleteByBatchOperationId(@Param("batchOperationId") Long batchOperationId);
}