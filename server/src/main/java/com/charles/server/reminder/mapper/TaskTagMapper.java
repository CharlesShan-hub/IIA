package com.charles.server.reminder.mapper;

import com.charles.server.reminder.entity.TaskTag;
import org.apache.ibatis.annotations.*;

@Mapper
public interface TaskTagMapper {
    
    // 插入任务-标签关联
    @Insert("INSERT INTO reminder_task_tag(task_id, tag_id) VALUES(#{taskId}, #{tagId})")
    @Options(useGeneratedKeys = true, keyProperty = "id", keyColumn = "id")
    int insert(TaskTag taskTag);
    
    // 根据ID查询关联
    @Select("SELECT * FROM reminder_task_tag WHERE id = #{id}")
    TaskTag findById(Long id);
    
    // 根据任务ID和标签ID查询关联
    @Select("SELECT * FROM reminder_task_tag WHERE task_id = #{taskId} AND tag_id = #{tagId}")
    TaskTag findByTaskIdAndTagId(@Param("taskId") Long taskId, @Param("tagId") Long tagId);
    
    // 删除特定的任务-标签关联
    @Delete("DELETE FROM reminder_task_tag WHERE task_id = #{taskId} AND tag_id = #{tagId}")
    int deleteByTaskIdAndTagId(@Param("taskId") Long taskId, @Param("tagId") Long tagId);
}