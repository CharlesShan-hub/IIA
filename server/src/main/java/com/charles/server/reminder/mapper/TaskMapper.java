package com.charles.server.reminder.mapper;

import com.charles.server.reminder.entity.Task;
import org.apache.ibatis.annotations.*;
import java.util.List;

@Mapper
public interface TaskMapper {
    
    // 插入新任务
    @Insert("INSERT INTO reminder_task(user_id, project_id, title, is_completed, is_abandoned, is_skipped, parent_task_id, "+
            "sort_order, due_date, start_date, completed_at, reminder_sent_at, priority, is_recurring) "+
            "VALUES(#{userId}, #{projectId}, #{title}, #{isCompleted}, #{isAbandoned}, #{isSkipped}, #{parentTaskId}, "+
            "#{sortOrder}, #{dueDate}, #{startDate}, #{completedAt}, #{reminderSentAt}, #{priority}, #{isRecurring})")
    @Options(useGeneratedKeys = true, keyProperty = "taskId", keyColumn = "task_id")
    int insert(Task task);
    
    // 根据ID查询任务
    @Select("SELECT * FROM reminder_task WHERE task_id = #{taskId}")
    Task findById(Long taskId);
    
    // 查询用户的所有任务
    @Select("SELECT * FROM reminder_task WHERE user_id = #{userId}")
    List<Task> findByUserId(Long userId);
    
    // 查询用户的任务（按完成状态筛选）
    @Select("SELECT * FROM reminder_task WHERE user_id = #{userId} AND is_completed = #{isCompleted}")
    List<Task> findByUserIdAndCompleted(@Param("userId") Long userId, @Param("isCompleted") Boolean isCompleted);
    
    // 查询用户的任务（按废弃状态筛选）
    @Select("SELECT * FROM reminder_task WHERE user_id = #{userId} AND is_abandoned = #{isAbandoned}")
    List<Task> findByUserIdAndAbandoned(@Param("userId") Long userId, @Param("isAbandoned") Boolean isAbandoned);
    
    // 查询用户的任务（按跳过状态筛选）
    @Select("SELECT * FROM reminder_task WHERE user_id = #{userId} AND is_skipped = #{isSkipped}")
    List<Task> findByUserIdAndSkipped(@Param("userId") Long userId, @Param("isSkipped") Boolean isSkipped);
    
    // 查询用户的任务（按项目筛选）
    @Select("SELECT * FROM reminder_task WHERE user_id = #{userId} AND project_id = #{projectId}")
    List<Task> findByUserIdAndProjectId(@Param("userId") Long userId, @Param("projectId") Long projectId);

    // 查询用户的任务（默认区：project_id IS NULL）
    @Select("SELECT * FROM reminder_task WHERE user_id = #{userId} AND project_id IS NULL")
    List<Task> findByUserIdAndProjectIdIsNull(@Param("userId") Long userId);

    // 查询用户的根任务的最大排序（按照项目筛选）
    @Select("SELECT MAX(sort_order) FROM reminder_task WHERE user_id = #{userId} AND project_id = #{projectId} AND parent_task_id IS NULL")
    Integer findMaxSortOrderOfRootTasksByUserIdAndProjectId(@Param("userId") Long userId, @Param("projectId") Long projectId);

    // 查询默认区（project_id IS NULL）的根任务最大排序
    @Select("SELECT COALESCE(MAX(sort_order), 0) FROM reminder_task WHERE user_id = #{userId} AND project_id IS NULL AND parent_task_id IS NULL")
    Integer findMaxSortOrderOfRootTasksByUserIdAndProjectIdIsNull(@Param("userId") Long userId);
    
    // 查询用户的子任务（按父任务筛选）
    @Select("SELECT * FROM reminder_task WHERE user_id = #{userId} AND parent_task_id = #{parentTaskId}")
    List<Task> findByUserIdAndParentTaskId(@Param("userId") Long userId, @Param("parentTaskId") Long parentTaskId);

    // 查询用户的某任务的子任务的最大排序
    @Select("SELECT COALESCE(MAX(sort_order), 0) FROM reminder_task WHERE user_id = #{userId} AND parent_task_id = #{parentTaskId}")
    Integer findMaxSortOrderByUserIdAndParentTaskId(@Param("userId") Long userId, @Param("parentTaskId") Long parentTaskId);
    
    // 部分更新任务信息（仅更新非空字段）
    @Update({
        "<script>",
        "UPDATE reminder_task",
        "<set>",
        "  <if test='projectId != null'>project_id = #{projectId},</if>",
        "  <if test='title != null'>title = #{title},</if>",
        "<if test='isCompleted != null'>is_completed = #{isCompleted},</if>",
        "<if test='isAbandoned != null'>is_abandoned = #{isAbandoned},</if>",
        "<if test='isSkipped != null'>is_skipped = #{isSkipped},</if>",
        "  <if test='parentTaskId != null'>parent_task_id = #{parentTaskId},</if>",
        "  <if test='sortOrder != null'>sort_order = #{sortOrder},</if>",
        "  <if test='dueDate != null'>due_date = #{dueDate},</if>",
        "  <if test='startDate != null'>start_date = #{startDate},</if>",
        "  <if test='completedAt != null'>completed_at = #{completedAt},</if>",
        "  <if test='reminderSentAt != null'>reminder_sent_at = #{reminderSentAt},</if>",
        "  <if test='priority != null'>priority = #{priority},</if>",
        "  <if test='isRecurring != null'>is_recurring = #{isRecurring},</if>",
        "</set>",
        "WHERE task_id = #{taskId}",
        "</script>"
    })
    int update(Task task);
    
    // 更新完成状态与完成时间
    @Update("UPDATE reminder_task SET is_completed = #{isCompleted}, completed_at = #{completedAt} WHERE task_id = #{taskId}")
    int updateCompletedStatus(@Param("taskId") Long taskId,
                              @Param("isCompleted") Boolean isCompleted,
                              @Param("completedAt") java.time.LocalDateTime completedAt);
    
    // 更新废弃状态
    @Update("UPDATE reminder_task SET is_abandoned = #{isAbandoned} WHERE task_id = #{taskId}")
    int updateAbandonedStatus(@Param("taskId") Long taskId,
                              @Param("isAbandoned") Boolean isAbandoned);
    
    // 更新跳过状态
    @Update("UPDATE reminder_task SET is_skipped = #{isSkipped} WHERE task_id = #{taskId}")
    int updateSkippedStatus(@Param("taskId") Long taskId,
                            @Param("isSkipped") Boolean isSkipped);

    // 更新位置
    @Update("UPDATE reminder_task SET sort_order = #{sortOrder} WHERE task_id = #{taskId}")
    void updateSortOrder(Task task);
    
    // 查询截止日期前的任务
    @Select("SELECT * FROM reminder_task WHERE user_id = #{userId} AND due_date <= #{dueDate}")
    List<Task> findUpcomingTasks(@Param("userId") Long userId, @Param("dueDate") java.time.LocalDateTime dueDate);

    // 删除任务
    @Delete("DELETE FROM reminder_task WHERE task_id = #{taskId}")
    void deleteById(Long taskId);

    @Update("UPDATE reminder_task SET project_id = #{toProjectId} WHERE user_id = #{userId} AND project_id = #{fromProjectId}")
    int updateProjectIdByUserId(@Param("userId") Long userId, @Param("fromProjectId") Long fromProjectId, @Param("toProjectId") Long toProjectId);

    @Update("UPDATE reminder_task SET project_id = NULL WHERE user_id = #{userId} AND project_id = #{fromProjectId}")
    int clearProjectIdByUserId(@Param("userId") Long userId, @Param("fromProjectId") Long fromProjectId);

    @Delete("DELETE FROM reminder_task WHERE user_id = #{userId} AND project_id = #{projectId}")
    int deleteByUserIdAndProjectId(@Param("userId") Long userId, @Param("projectId") Long projectId);

    @Update("UPDATE reminder_task SET project_id = #{projectId} WHERE task_id = #{taskId}")
    int updateProjectId(@Param("taskId") Long taskId, @Param("projectId") Long projectId);
}
