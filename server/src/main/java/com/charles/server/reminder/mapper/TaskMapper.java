package com.charles.server.reminder.mapper;

import com.charles.server.reminder.entity.Task;
import org.apache.ibatis.annotations.*;
import java.util.List;

@Mapper
public interface TaskMapper {
    
    // 插入新任务
    @Insert("INSERT INTO reminder_task(user_id, project_id, title, category, status, parent_task_id, "+
            "sort_order, due_date, start_date, completed_at, reminder_sent_at, priority) "+
            "VALUES(#{userId}, #{projectId}, #{title}, #{category}, #{status}, #{parentTaskId}, "+
            "#{sortOrder}, #{dueDate}, #{startDate}, #{completedAt}, #{reminderSentAt}, #{priority})")
    @Options(useGeneratedKeys = true, keyProperty = "taskId", keyColumn = "task_id")
    int insert(Task task);
    
    // 根据ID查询任务
    @Select("SELECT * FROM reminder_task WHERE task_id = #{taskId}")
    Task findById(Long taskId);
    
    // 查询用户的所有任务
    @Select("SELECT * FROM reminder_task WHERE user_id = #{userId}")
    List<Task> findByUserId(Long userId);
    
    // 查询用户的任务（按状态筛选）
    @Select("SELECT * FROM reminder_task WHERE user_id = #{userId} AND status = #{status}")
    List<Task> findByUserIdAndStatus(@Param("userId") Long userId, @Param("status") String status);
    
    // 查询用户的任务（按项目筛选）
    @Select("SELECT * FROM reminder_task WHERE user_id = #{userId} AND project_id = #{projectId}")
    List<Task> findByUserIdAndProjectId(@Param("userId") Long userId, @Param("projectId") Long projectId);
    
    // 查询用户的子任务
    @Select("SELECT * FROM reminder_task WHERE user_id = #{userId} AND parent_task_id = #{parentTaskId}")
    List<Task> findSubTasks(@Param("userId") Long userId, @Param("parentTaskId") Long parentTaskId);
    
    // 更新任务信息
    @Update("UPDATE reminder_task SET project_id = #{projectId}, title = #{title}, category = #{category}, "+
            "status = #{status}, parent_task_id = #{parentTaskId}, sort_order = #{sortOrder}, "+
            "due_date = #{dueDate}, start_date = #{startDate}, completed_at = #{completedAt}, "+
            "reminder_sent_at = #{reminderSentAt}, priority = #{priority} "+
            "WHERE task_id = #{taskId}")
    int update(Task task);
    
    // 更新任务状态
    @Update("UPDATE reminder_task SET status = #{status} WHERE task_id = #{taskId}")
    int updateStatus(@Param("taskId") Long taskId, @Param("status") String status);
    
    // 查询截止日期前的任务
    @Select("SELECT * FROM reminder_task WHERE user_id = #{userId} AND due_date <= #{dueDate}")
    List<Task> findUpcomingTasks(@Param("userId") Long userId, @Param("dueDate") java.time.LocalDateTime dueDate);
}