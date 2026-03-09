package com.charles.server.reminder.service.impl;

import com.charles.server.reminder.dto.TaskCreateRequest;
import com.charles.server.reminder.dto.TaskUpdateRequest;
import com.charles.server.reminder.entity.Recurrence;
import com.charles.server.reminder.mapper.RecurrenceMapper;
import com.charles.server.reminder.service.RecurrenceService;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

@Service
@RequiredArgsConstructor
@Slf4j
public class RecurrenceServiceImpl implements RecurrenceService {
    
    private final RecurrenceMapper recurrenceMapper;
    // private final TaskMapper taskMapper;

    /**************************************************************************************/
    /*                                      Utils                                         */
    /**************************************************************************************/

    private Recurrence convertToEntity(Long taskId, TaskCreateRequest dto) {
        Recurrence r = new Recurrence();
        r.setTaskId(taskId);
        r.setCategory(dto.getRecurrenceCategory());
        r.setInterval(dto.getRecurrenceInterval());
        r.setCount(dto.getRecurrenceCount());
        r.setNextTime(dto.getRecurrenceNextTime());
        r.setSchedule(dto.getRecurrenceSchedule());
        return r;
    }

    private Recurrence convertToEntity(Long taskId, TaskUpdateRequest dto) {
        Recurrence r = new Recurrence();
        r.setTaskId(taskId);
        r.setCategory(dto.getRecurrenceCategory());
        r.setInterval(dto.getRecurrenceInterval());
        r.setCount(dto.getRecurrenceCount());
        r.setNextTime(dto.getRecurrenceNextTime());
        r.setSchedule(dto.getRecurrenceSchedule());
        return r;
    }

    // private void validateTaskOwnership(Long userId, Long taskId) {
    //     com.charles.server.reminder.entity.Task task = taskMapper.findById(taskId);
    //     if (task == null) {
    //         throw com.charles.server.reminder.exception.TaskAccessException.notFound(taskId);
    //     }
    //     if (!task.getUserId().equals(userId)) {
    //         throw com.charles.server.reminder.exception.TaskAccessException.permissionDenied(userId, taskId);
    //     }
    // }

    // private Recurrence validatedFindByTaskId(Long userId, Long taskId) {
    //     validateTaskOwnership(userId, taskId);
    //     return recurrenceMapper.findByTaskId(taskId);
    // }

    /**************************************************************************************/
    /*                                    Basic CRUD                                      */
    /**************************************************************************************/

    private void create(Long taskId, Recurrence recurrence) {
        try {
            log.info("Creating recurrence config for taskId={}", taskId);
            Recurrence existing = recurrenceMapper.findByTaskId(taskId);
            if (existing == null) {
                recurrenceMapper.insert(recurrence);
            } else {
                recurrenceMapper.update(recurrence);
            }
        } catch (Exception e) {
            log.error("Create recurrence config failed: {}", e.getMessage(), e);
            throw e;
        }
    }

    @Override
    public void create(Long taskId, TaskCreateRequest dto) {
        create(taskId, convertToEntity(taskId, dto));
    }

    @Override
    public void create(Long taskId, TaskUpdateRequest dto) {
        create(taskId, convertToEntity(taskId, dto));
    }

    @Override
    public void deleteByTaskId(Long taskId) {
        try {
            log.info("Deleting recurrence config for taskId={}", taskId);
            recurrenceMapper.deleteByTaskId(taskId);
        } catch (Exception e) {
            log.error("Delete recurrence config failed: {}", e.getMessage(), e);
            throw e;
        }
    }
    
    // @Override
    // public Recurrence getByTaskId(Long taskId) {
    //     try {
    //         log.info("根据任务ID查询循环配置: taskId={}", taskId);
    //         return recurrenceMapper.findByTaskId(taskId);
    //     } catch (Exception e) {
    //         log.error("根据任务ID查询循环配置失败: taskId={}, error={}", taskId, e.getMessage(), e);
    //         throw e;
    //     }
    // }
    
    // @Override
    // public int update(Recurrence recurrence) {
    //     try {
    //         log.info("更新循环任务配置: {}", recurrence);
    //         return recurrenceMapper.update(recurrence);
    //     } catch (Exception e) {
    //         log.error("更新循环任务配置失败: {}", e.getMessage(), e);
    //         throw e;
    //     }
    // }
    
    // @Override
    // public int updateNextTime(Long taskId, LocalDateTime nextTime) {
    //     try {
    //         log.info("更新循环任务下一次发生时间: taskId={}, nextTime={}", taskId, nextTime);
    //         return recurrenceMapper.updateNextTime(taskId, nextTime);
    //     } catch (Exception e) {
    //         log.error("更新循环任务下一次发生时间失败: taskId={}, error={}", taskId, e.getMessage(), e);
    //         throw e;
    //     }
    // }
    
    // @Override
    // public int updateCount(Long taskId, Integer count) {
    //     try {
    //         log.info("更新循环任务重复次数: taskId={}, count={}", taskId, count);
    //         return recurrenceMapper.updateCount(taskId, count);
    //     } catch (Exception e) {
    //         log.error("更新循环任务重复次数失败: taskId={}, error={}", taskId, e.getMessage(), e);
    //         throw e;
    //     }
    // }
    
    // @Override
    // public int deleteByTaskId(Long taskId) {
    //     try {
    //         log.info("删除循环任务配置: taskId={}", taskId);
    //         return recurrenceMapper.deleteByTaskId(taskId);
    //     } catch (Exception e) {
    //         log.error("删除循环任务配置失败: taskId={}, error={}", taskId, e.getMessage(), e);
    //         throw e;
    //     }
    // }
    
    // @Override
    // public List<Recurrence> getUpcomingByUserId(Long userId, LocalDateTime deadline) {
    //     try {
    //         log.info("查询用户即将发生的循环任务: userId={}, deadline={}", userId, deadline);
    //         return recurrenceMapper.findUpcomingByUserId(userId, deadline);
    //     } catch (Exception e) {
    //         log.error("查询用户即将发生的循环任务失败: userId={}, error={}", userId, e.getMessage(), e);
    //         throw e;
    //     }
    // }
}