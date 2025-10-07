package com.charles.server.reminder.service.impl;

import com.charles.server.reminder.entity.Recurrence;
import com.charles.server.reminder.mapper.RecurrenceMapper;
import com.charles.server.reminder.service.RecurrenceService;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

import java.time.LocalDateTime;
import java.util.List;

@Service
@RequiredArgsConstructor
@Slf4j
public class RecurrenceServiceImpl implements RecurrenceService {
    
    private final RecurrenceMapper recurrenceMapper;
    
    @Override
    public int create(Recurrence recurrence) {
        try {
            log.info("创建循环任务配置: {}", recurrence);
            return recurrenceMapper.insert(recurrence);
        } catch (Exception e) {
            log.error("创建循环任务配置失败: {}", e.getMessage(), e);
            throw e;
        }
    }
    
    @Override
    public Recurrence getByTaskId(Long taskId) {
        try {
            log.info("根据任务ID查询循环配置: taskId={}", taskId);
            return recurrenceMapper.findByTaskId(taskId);
        } catch (Exception e) {
            log.error("根据任务ID查询循环配置失败: taskId={}, error={}", taskId, e.getMessage(), e);
            throw e;
        }
    }
    
    @Override
    public int update(Recurrence recurrence) {
        try {
            log.info("更新循环任务配置: {}", recurrence);
            return recurrenceMapper.update(recurrence);
        } catch (Exception e) {
            log.error("更新循环任务配置失败: {}", e.getMessage(), e);
            throw e;
        }
    }
    
    @Override
    public int updateNextTime(Long taskId, LocalDateTime nextTime) {
        try {
            log.info("更新循环任务下一次发生时间: taskId={}, nextTime={}", taskId, nextTime);
            return recurrenceMapper.updateNextTime(taskId, nextTime);
        } catch (Exception e) {
            log.error("更新循环任务下一次发生时间失败: taskId={}, error={}", taskId, e.getMessage(), e);
            throw e;
        }
    }
    
    @Override
    public int updateCount(Long taskId, Integer count) {
        try {
            log.info("更新循环任务重复次数: taskId={}, count={}", taskId, count);
            return recurrenceMapper.updateCount(taskId, count);
        } catch (Exception e) {
            log.error("更新循环任务重复次数失败: taskId={}, error={}", taskId, e.getMessage(), e);
            throw e;
        }
    }
    
    @Override
    public int deleteByTaskId(Long taskId) {
        try {
            log.info("删除循环任务配置: taskId={}", taskId);
            return recurrenceMapper.deleteByTaskId(taskId);
        } catch (Exception e) {
            log.error("删除循环任务配置失败: taskId={}, error={}", taskId, e.getMessage(), e);
            throw e;
        }
    }
    
    @Override
    public List<Recurrence> getUpcomingByUserId(Long userId, LocalDateTime deadline) {
        try {
            log.info("查询用户即将发生的循环任务: userId={}, deadline={}", userId, deadline);
            return recurrenceMapper.findUpcomingByUserId(userId, deadline);
        } catch (Exception e) {
            log.error("查询用户即将发生的循环任务失败: userId={}, error={}", userId, e.getMessage(), e);
            throw e;
        }
    }
}