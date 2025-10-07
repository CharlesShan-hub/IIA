package com.charles.server.reminder.mapper;

import com.charles.server.reminder.entity.Recurrence;
import org.apache.ibatis.annotations.*;

@Mapper
public interface RecurrenceMapper {
    
    // 插入新的循环任务配置
    @Insert("INSERT INTO reminder_recurrence(task_id, category, interval, count, next_time, schedule) " +
            "VALUES(#{taskId}, #{category}, #{interval}, #{count}, #{nextTime}, #{schedule})")
    int insert(Recurrence recurrence);
    
    // 根据任务ID查询循环配置
    @Select("SELECT * FROM reminder_recurrence WHERE task_id = #{taskId}")
    Recurrence findByTaskId(Long taskId);
    
    // 更新循环任务配置
    @Update("UPDATE reminder_recurrence SET category = #{category}, interval = #{interval}, " +
            "count = #{count}, next_time = #{nextTime}, schedule = #{schedule} " +
            "WHERE task_id = #{taskId}")
    int update(Recurrence recurrence);
    
    // 更新下一次发生时间
    @Update("UPDATE reminder_recurrence SET next_time = #{nextTime} WHERE task_id = #{taskId}")
    int updateNextTime(@Param("taskId") Long taskId, @Param("nextTime") java.time.LocalDateTime nextTime);
    
    // 更新重复次数
    @Update("UPDATE reminder_recurrence SET count = #{count} WHERE task_id = #{taskId}")
    int updateCount(@Param("taskId") Long taskId, @Param("count") Integer count);
    
    // 删除循环任务配置
    @Delete("DELETE FROM reminder_recurrence WHERE task_id = #{taskId}")
    int deleteByTaskId(Long taskId);
    
    // 查询即将发生的循环任务
    @Select("SELECT r.* FROM reminder_recurrence r " +
            "JOIN reminder_task t ON r.task_id = t.task_id " +
            "WHERE t.user_id = #{userId} AND r.next_time <= #{deadline}")
    java.util.List<Recurrence> findUpcomingByUserId(
            @Param("userId") Long userId, 
            @Param("deadline") java.time.LocalDateTime deadline);
}