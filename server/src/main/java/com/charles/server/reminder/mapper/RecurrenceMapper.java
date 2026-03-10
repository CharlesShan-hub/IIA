package com.charles.server.reminder.mapper;

import com.charles.server.reminder.entity.Recurrence;
import org.apache.ibatis.annotations.*;

@Mapper
public interface RecurrenceMapper {
    
    // 插入新的循环任务配置
    @Insert("INSERT INTO reminder_recurrence(task_id, category, `interval`, `count`, next_time, is_paused, is_skip_overdue, is_repeat_from_due, schedule) " +
            "VALUES(#{taskId}, #{category}, #{interval}, #{count}, #{nextTime}, #{isPaused}, #{isSkipOverdue}, #{isRepeatFromDue}, #{schedule})")
    int insert(Recurrence recurrence);
    
    // 根据任务ID查询循环配置
    @Select("SELECT * FROM reminder_recurrence WHERE task_id = #{taskId}")
    @Results(id = "RecurrenceMap", value = {
            @Result(column = "task_id", property = "taskId"),
            @Result(column = "category", property = "category"),
            @Result(column = "interval", property = "interval"),
            @Result(column = "count", property = "count"),
            @Result(column = "next_time", property = "nextTime"),
            @Result(column = "is_paused", property = "isPaused"),
            @Result(column = "is_skip_overdue", property = "isSkipOverdue"),
            @Result(column = "is_repeat_from_due", property = "isRepeatFromDue"),
            @Result(column = "schedule", property = "schedule")
    })
    Recurrence findByTaskId(Long taskId);
    
    // 更新循环任务配置
    @Update("UPDATE reminder_recurrence SET category = #{category}, `interval` = #{interval}, " +
            "`count` = #{count}, next_time = #{nextTime}, is_paused = #{isPaused}, is_skip_overdue = #{isSkipOverdue}, is_repeat_from_due = #{isRepeatFromDue}, schedule = #{schedule} " +
            "WHERE task_id = #{taskId}")
    int update(Recurrence recurrence);
    
    // 删除循环任务配置
    @Delete("DELETE FROM reminder_recurrence WHERE task_id = #{taskId}")
    void deleteByTaskId(Long taskId);
}
