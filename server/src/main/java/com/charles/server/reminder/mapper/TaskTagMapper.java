package com.charles.server.reminder.mapper;

import com.charles.server.reminder.entity.TaskTag;
import org.apache.ibatis.annotations.*;
import java.util.List;

@Mapper
public interface TaskTagMapper {
    
    // 插入任务-标签关联
    @Insert("INSERT INTO reminder_task_tag(task_id, tag_id) VALUES(#{taskId}, #{tagId})")
    @Options(useGeneratedKeys = true, keyProperty = "id", keyColumn = "id")
    int insert(TaskTag taskTag);
    
    // 批量插入任务-标签关联
    @Insert("<script>" +
            "INSERT INTO reminder_task_tag(task_id, tag_id) VALUES " +
            "<foreach collection='list' item='item' separator=','>" +
            "(#{item.taskId}, #{item.tagId})" +
            "</foreach>" +
            "</script>")
    int insertBatch(@Param("list") List<TaskTag> taskTagList);
    
    // 根据ID查询关联
    @Select("SELECT * FROM reminder_task_tag WHERE id = #{id}")
    TaskTag findById(Long id);
    
    // 根据任务ID和标签ID查询关联
    @Select("SELECT * FROM reminder_task_tag WHERE task_id = #{taskId} AND tag_id = #{tagId}")
    TaskTag findByTaskIdAndTagId(@Param("taskId") Long taskId, @Param("tagId") Long tagId);
    
    // 查询任务的所有标签关联
    @Select("SELECT * FROM reminder_task_tag WHERE task_id = #{taskId}")
    List<TaskTag> findByTaskId(Long taskId);
    
    // 查询标签的所有任务关联
    @Select("SELECT * FROM reminder_task_tag WHERE tag_id = #{tagId}")
    List<TaskTag> findByTagId(Long tagId);
    
    // 根据任务ID删除所有关联
    @Delete("DELETE FROM reminder_task_tag WHERE task_id = #{taskId}")
    int deleteByTaskId(Long taskId);
    
    // 根据标签ID删除所有关联
    @Delete("DELETE FROM reminder_task_tag WHERE tag_id = #{tagId}")
    int deleteByTagId(Long tagId);
    
    // 删除特定的任务-标签关联
    @Delete("DELETE FROM reminder_task_tag WHERE task_id = #{taskId} AND tag_id = #{tagId}")
    int deleteByTaskIdAndTagId(@Param("taskId") Long taskId, @Param("tagId") Long tagId);
    
    // 批量删除任务-标签关联
    @Delete("<script>" +
            "DELETE FROM reminder_task_tag WHERE task_id = #{taskId} AND tag_id IN " +
            "<foreach collection='tagIds' item='tagId' open='(' close=')' separator=','>" +
            "#{tagId}" +
            "</foreach>" +
            "</script>")
    int deleteBatchByTaskIdAndTagIds(@Param("taskId") Long taskId, @Param("tagIds") List<Long> tagIds);
}