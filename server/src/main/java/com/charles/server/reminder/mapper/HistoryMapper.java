package com.charles.server.reminder.mapper;

import com.charles.server.reminder.entity.History;
import org.apache.ibatis.annotations.*;
import java.util.List;

@Mapper
public interface HistoryMapper {
    
    // 插入新的历史记录
    @Insert("INSERT INTO reminder_history(task_id, due_date, start_date, completed_at, " +
            "reminder_sent_at, current, status) " +
            "VALUES(#{taskId}, #{dueDate}, #{startDate}, #{completedAt}, #{reminderSentAt}, " +
            "#{current}, #{status})")
    @Options(useGeneratedKeys = true, keyProperty = "historyId", keyColumn = "history_id")
    int insert(History history);
    
    // 根据ID查询历史记录
    @Select("SELECT * FROM reminder_history WHERE history_id = #{historyId}")
    History findById(Long historyId);
    
    // 根据任务ID和当前次数查询历史记录
    @Select("SELECT * FROM reminder_history WHERE task_id = #{taskId} AND current = #{current}")
    History findByTaskIdAndCurrent(@Param("taskId") Long taskId, @Param("current") Integer current);
    
    // 查询任务的所有历史记录
    @Select("SELECT * FROM reminder_history WHERE task_id = #{taskId} ORDER BY current ASC")
    List<History> findByTaskId(Long taskId);
    
    // 查询用户的历史记录
    @Select("SELECT h.* FROM reminder_history h JOIN reminder_task t ON h.task_id = t.task_id " +
            "WHERE t.user_id = #{userId} ORDER BY h.due_date DESC")
    List<History> findByUserId(Long userId);
    
    // 查询用户特定状态的历史记录
    @Select("SELECT h.* FROM reminder_history h JOIN reminder_task t ON h.task_id = t.task_id " +
            "WHERE t.user_id = #{userId} AND h.status = #{status} ORDER BY h.due_date DESC")
    List<History> findByUserIdAndStatus(@Param("userId") Long userId, @Param("status") String status);
    
    // 更新历史记录信息
    @Update("UPDATE reminder_history SET due_date = #{dueDate}, start_date = #{startDate}, " +
            "completed_at = #{completedAt}, reminder_sent_at = #{reminderSentAt}, " +
            "status = #{status} WHERE history_id = #{historyId}")
    int update(History history);
    
    // 更新历史记录状态
    @Update("UPDATE reminder_history SET status = #{status} WHERE history_id = #{historyId}")
    int updateStatus(@Param("historyId") Long historyId, @Param("status") String status);
    
    // 查询截止日期范围内的历史记录
    @Select("SELECT h.* FROM reminder_history h JOIN reminder_task t ON h.task_id = t.task_id " +
            "WHERE t.user_id = #{userId} AND h.due_date BETWEEN #{startDate} AND #{endDate} " +
            "ORDER BY h.due_date ASC")
    List<History> findByUserIdAndDateRange(
            @Param("userId") Long userId,
            @Param("startDate") java.time.LocalDateTime startDate,
            @Param("endDate") java.time.LocalDateTime endDate);
    
    // 删除任务的所有历史记录
    @Delete("DELETE FROM reminder_history WHERE task_id = #{taskId}")
    int deleteByTaskId(Long taskId);
}