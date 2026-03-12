package com.charles.server.reminder.mapper;

import com.charles.server.reminder.entity.History;
import org.apache.ibatis.annotations.*;
import java.util.List;

@Mapper
public interface HistoryMapper {
    // 插入新的历史记录
    @Insert("INSERT INTO reminder_history(task_id, is_completed, is_abandoned, is_skipped, current, " +
            "operation_id, created_at) " +
            "VALUES(#{taskId}, #{isCompleted}, #{isAbandoned}, #{isSkipped}, #{current}, " +
            "#{operationId}, #{createdAt})")
    @Options(useGeneratedKeys = true, keyProperty = "historyId", keyColumn = "history_id")
    int insert(History history);

    // 根据任务ID和操作ID查询历史记录
    @Select("SELECT history_id, task_id, is_completed, is_abandoned, is_skipped, current, operation_id, created_at " +
            "FROM reminder_history WHERE task_id = #{taskId} AND operation_id = #{operationId}")
    History findByTaskIdAndOperationId(@Param("taskId") Long taskId, @Param("operationId") Long operationId);

    // 查询任务的所有历史记录
    @Select("SELECT history_id, task_id, is_completed, is_abandoned, is_skipped, current, operation_id, created_at " +
            "FROM reminder_history WHERE task_id = #{taskId} ORDER BY created_at ASC")
    List<History> findByTaskId(Long taskId);

    // 查询用户的历史记录
    @Select("SELECT h.history_id, h.task_id, h.is_completed, h.is_abandoned, h.is_skipped, h.current, h.operation_id, h.created_at " +
            "FROM reminder_history h JOIN reminder_task t ON h.task_id = t.task_id " +
            "WHERE t.user_id = #{userId} ORDER BY h.created_at DESC")
    List<History> findByUserId(Long userId);

    // 查询用户特定完成状态的历史记录
    @Select("SELECT h.history_id, h.task_id, h.is_completed, h.is_abandoned, h.is_skipped, h.current, h.operation_id, h.created_at " +
            "FROM reminder_history h JOIN reminder_task t ON h.task_id = t.task_id " +
            "WHERE t.user_id = #{userId} AND h.is_completed = #{isCompleted} ORDER BY h.created_at DESC")
    List<History> findByUserIdAndCompleted(@Param("userId") Long userId, @Param("isCompleted") Boolean isCompleted);

    // 查询用户特定废弃状态的历史记录
    @Select("SELECT h.history_id, h.task_id, h.is_completed, h.is_abandoned, h.is_skipped, h.current, h.operation_id, h.created_at " +
            "FROM reminder_history h JOIN reminder_task t ON h.task_id = t.task_id " +
            "WHERE t.user_id = #{userId} AND h.is_abandoned = #{isAbandoned} ORDER BY h.created_at DESC")
    List<History> findByUserIdAndAbandoned(@Param("userId") Long userId, @Param("isAbandoned") Boolean isAbandoned);

    // 查询用户特定跳过状态的历史记录
    @Select("SELECT h.history_id, h.task_id, h.is_completed, h.is_abandoned, h.is_skipped, h.current, h.operation_id, h.created_at " +
            "FROM reminder_history h JOIN reminder_task t ON h.task_id = t.task_id " +
            "WHERE t.user_id = #{userId} AND h.is_skipped = #{isSkipped} ORDER BY h.created_at DESC")
    List<History> findByUserIdAndSkipped(@Param("userId") Long userId, @Param("isSkipped") Boolean isSkipped);

    // 更新历史记录信息
    @Update("UPDATE reminder_history SET is_completed = #{isCompleted}, is_abandoned = #{isAbandoned}, is_skipped = #{isSkipped}, " +
            "current = #{current}, operation_id = #{operationId} " +
            "WHERE history_id = #{historyId}")
    int update(History history);

    // 更新历史记录完成状态
    @Update("UPDATE reminder_history SET is_completed = #{isCompleted} WHERE history_id = #{historyId}")
    int updateCompletedStatus(@Param("historyId") Long historyId, @Param("isCompleted") Boolean isCompleted);

    // 更新历史记录废弃状态
    @Update("UPDATE reminder_history SET is_abandoned = #{isAbandoned} WHERE history_id = #{historyId}")
    int updateAbandonedStatus(@Param("historyId") Long historyId, @Param("isAbandoned") Boolean isAbandoned);

    // 更新历史记录跳过状态
    @Update("UPDATE reminder_history SET is_skipped = #{isSkipped} WHERE history_id = #{historyId}")
    int updateSkippedStatus(@Param("historyId") Long historyId, @Param("isSkipped") Boolean isSkipped);

    // 查询创建时间范围内的历史记录
    @Select("SELECT h.history_id, h.task_id, h.is_completed, h.is_abandoned, h.is_skipped, h.current, h.operation_id, h.created_at " +
            "FROM reminder_history h JOIN reminder_task t ON h.task_id = t.task_id " +
            "WHERE t.user_id = #{userId} AND h.created_at BETWEEN #{startDate} AND #{endDate} " +
            "ORDER BY h.created_at ASC")
    List<History> findByUserIdAndDateRange(
            @Param("userId") Long userId,
            @Param("startDate") java.time.LocalDateTime startDate,
            @Param("endDate") java.time.LocalDateTime endDate);

    // 根据操作ID查询历史记录
    @Select("SELECT history_id, task_id, is_completed, is_abandoned, is_skipped, current, operation_id, created_at " +
            "FROM reminder_history WHERE operation_id = #{operationId}")
    List<History> findByOperationId(Long operationId);
    
    // 查询任务的最新历史记录
    @Select("SELECT history_id, task_id, is_completed, is_abandoned, is_skipped, current, operation_id, created_at " +
            "FROM reminder_history WHERE task_id = #{taskId} ORDER BY created_at DESC LIMIT 1")
    History findLatestByTaskId(Long taskId);
    
    // 获取当前最大的操作ID
    @Select("SELECT MAX(operation_id) FROM reminder_history")
    Long getMaxOperationId();
}