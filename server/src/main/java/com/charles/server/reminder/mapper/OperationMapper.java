package com.charles.server.reminder.mapper;

import com.charles.server.reminder.entity.Operation;
import org.apache.ibatis.annotations.*;

@Mapper
public interface OperationMapper {
    
    @Insert("INSERT INTO reminder_operation(user_id, performed_at, " +
            "is_reminder_project, is_reminder_task, is_reminder_recurrence, " +
            "is_reminder_history, is_reminder_tag, is_reminder_task_tag) " +
            "VALUES(#{userId}, #{performedAt}, " +
            "#{isReminderProject}, #{isReminderTask}, #{isReminderRecurrence}, " +
            "#{isReminderHistory}, #{isReminderTag}, #{isReminderTaskTag})")
    @Options(useGeneratedKeys = true, keyProperty = "operationId", keyColumn = "operation_id")
    int insert(Operation operation);
    
    @Select("SELECT MAX(operation_id) FROM reminder_operation WHERE user_id = #{userId}")
    Long getMaxOperationIdByUserId(@Param("userId") Long userId);
}