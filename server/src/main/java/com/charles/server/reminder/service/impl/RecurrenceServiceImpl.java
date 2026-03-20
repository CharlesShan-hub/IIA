package com.charles.server.reminder.service.impl;

import com.charles.server.reminder.dto.TaskCreateDTO;
import com.charles.server.reminder.dto.TaskUpdateDTO;
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

    /************************************************************************************/
    /*                                      Utils                                         */
    /**************************************************************************************/

    private Recurrence convertToEntity(Long taskId, TaskCreateDTO dto) {
        Recurrence r = new Recurrence();
        r.setTaskId(taskId);
        r.setCategory(dto.getRecurrenceCategory());
        r.setInterval(dto.getRecurrenceInterval());
        r.setCount(dto.getRecurrenceCount());
        r.setNextTime(dto.getRecurrenceNextTime());
        r.setIsPaused(dto.getRecurrenceIsPaused() != null ? dto.getRecurrenceIsPaused() : Boolean.FALSE);
        r.setIsSkipOverdue(dto.getRecurrenceIsSkipOverdue() != null ? dto.getRecurrenceIsSkipOverdue() : Boolean.TRUE);
        r.setIsRepeatFromDue(dto.getRecurrenceIsRepeatFromDue() != null ? dto.getRecurrenceIsRepeatFromDue() : Boolean.TRUE);
        r.setSchedule(dto.getRecurrenceSchedule());
        return r;
    }

    private Recurrence convertToEntity(Long taskId, TaskUpdateDTO dto) {
        Recurrence r = new Recurrence();
        r.setTaskId(taskId);
        r.setCategory(dto.getRecurrenceCategory());
        r.setInterval(dto.getRecurrenceInterval());
        r.setCount(dto.getRecurrenceCount());
        r.setNextTime(dto.getRecurrenceNextTime());
        r.setIsPaused(dto.getRecurrenceIsPaused());
        r.setIsSkipOverdue(dto.getRecurrenceIsSkipOverdue());
        r.setIsRepeatFromDue(dto.getRecurrenceIsRepeatFromDue());
        r.setSchedule(dto.getRecurrenceSchedule());
        return r;
    }

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
                Recurrence merged = new Recurrence();
                merged.setTaskId(taskId);
                merged.setCategory(recurrence.getCategory() != null ? recurrence.getCategory() : existing.getCategory());
                merged.setInterval(recurrence.getInterval() != null ? recurrence.getInterval() : existing.getInterval());
                merged.setCount(recurrence.getCount() != null ? recurrence.getCount() : existing.getCount());
                merged.setNextTime(recurrence.getNextTime() != null ? recurrence.getNextTime() : existing.getNextTime());
                merged.setIsPaused(recurrence.getIsPaused() != null ? recurrence.getIsPaused() : existing.getIsPaused());
                merged.setIsSkipOverdue(recurrence.getIsSkipOverdue() != null ? recurrence.getIsSkipOverdue() : existing.getIsSkipOverdue());
                merged.setIsRepeatFromDue(recurrence.getIsRepeatFromDue() != null ? recurrence.getIsRepeatFromDue() : existing.getIsRepeatFromDue());
                merged.setSchedule(recurrence.getSchedule() != null ? recurrence.getSchedule() : existing.getSchedule());
                recurrenceMapper.update(merged);
            }
        } catch (Exception e) {
            log.error("Create recurrence config failed: {}", e.getMessage(), e);
            throw e;
        }
    }

    @Override
    public void create(Long taskId, TaskCreateDTO dto) {
        create(taskId, convertToEntity(taskId, dto));
    }

    @Override
    public void delete(Long taskId) {
        try {
            log.info("Deleting recurrence config for taskId={}", taskId);
            recurrenceMapper.deleteByTaskId(taskId);
        } catch (Exception e) {
            log.error("Delete recurrence config failed: {}", e.getMessage(), e);
            throw e;
        }
    }
    
    @Override
    public void update(Long taskId, TaskUpdateDTO dto) {
        try {
            log.info("Updating recurrence config for taskId={}", taskId);
            
            Recurrence existing = recurrenceMapper.findByTaskId(taskId);
            Recurrence recurrence = convertToEntity(taskId, dto);
            
            if (existing == null) {
                // Not exists → Create
                log.info("Creating new recurrence config for taskId={}", taskId);
                recurrenceMapper.insert(recurrence);
            } else {
                // Exists → Update
                log.info("Recurrence config already exists for taskId={}, skipping update for now", taskId);
                // TODO
                // 现在还不支持修改已存在的循环配置
                // recurrenceMapper.update(mergeRecurrence(existing, recurrence));
            }
        } catch (Exception e) {
            log.error("Update recurrence config failed: {}", e.getMessage(), e);
            throw e;
        }
    }

    @Override
    public void complete(Long taskId) {
    }
}
