package com.charles.server.reminder.service.impl;

import com.charles.server.reminder.entity.TaskTag;
import com.charles.server.reminder.entity.Task;
import com.charles.server.reminder.mapper.TaskTagMapper;
import com.charles.server.reminder.mapper.TaskMapper;
import com.charles.server.reminder.service.TaskTagService;
import com.charles.server.reminder.service.PermissionService;
import com.charles.server.reminder.dto.TaskTagCreateDTO;
import com.charles.server.reminder.dto.TaskTagDeleteDTO;
import com.charles.server.reminder.dto.TaskTagBatchCreateDTO;
import com.charles.server.reminder.dto.TaskTagBatchDeleteDTO;
import lombok.RequiredArgsConstructor;
import org.springframework.transaction.annotation.Transactional;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import java.util.List;

@Service
@RequiredArgsConstructor
@Slf4j
public class TaskTagServiceImpl implements TaskTagService {

    private final TaskTagMapper taskTagMapper;
    private final TaskMapper taskMapper;
    private final PermissionService permissionService;

    private TaskTag convertToEntity(TaskTagCreateDTO dto) {
        return TaskTag.builder()
                .taskId(dto.getTaskId())
                .tagId(dto.getTagId())
                .build();
    }

    private List<Task> getSubTasks(Long userId, Long parentTaskId) {
        return taskMapper.findByUserIdAndParentTaskId(userId, parentTaskId);
    }

    @Transactional
    @Override
    public void create(Long userId, TaskTagCreateDTO dto) {
        try{
            permissionService.validTag(userId, dto.getTagId());
            permissionService.validTask(userId, dto.getTaskId());
            TaskTag taskTag = convertToEntity(dto);
            if (dto.getIncludeSubtasks())
                createRecursive(userId, taskTag);
            else
                taskTagMapper.insert(taskTag);
        }catch (Exception e){
            log.error("Error creating task-tag association: {}", e.getMessage());
            throw e;
        }
    }

    @Transactional
    @Override
    public void createBatch(Long userId, TaskTagBatchCreateDTO dto) {
        for (Long tagId : dto.getTagIds()) {
            TaskTagCreateDTO single = new TaskTagCreateDTO();
            single.setTaskId(dto.getTaskId());
            single.setTagId(tagId);
            single.setIncludeSubtasks(dto.getIncludeSubtasks());
            create(userId, single);
        }
    }

    private void createRecursive(Long userId, TaskTag taskTag) {
        List<Task> subtasks = getSubTasks(userId, taskTag.getTaskId());
        for (Task subtask : subtasks) {
            TaskTag tt = TaskTag.builder()
                    .taskId(subtask.getTaskId())
                    .tagId(taskTag.getTagId())
                    .build();
            createRecursive(userId, tt);
        }
        taskTagMapper.insert(taskTag);
    }

    @Transactional
    @Override
    public void delete(Long userId, TaskTagDeleteDTO dto) {
        try{
            permissionService.validTag(userId, dto.getTagId());
            permissionService.validTask(userId, dto.getTaskId());
            if (dto.getIncludeSubtasks())
                deleteRecursive(userId, dto.getTaskId(), dto.getTagId());
            else
                taskTagMapper.deleteByTaskIdAndTagId(dto.getTaskId(), dto.getTagId());
        }catch (Exception e){
            log.error("Error deleting task-tag association: {}", e.getMessage());
            throw e;
        }
    }

    @Transactional
    @Override
    public void deleteBatch(Long userId, TaskTagBatchDeleteDTO dto) {
        for (Long tagId : dto.getTagIds()) {
            TaskTagDeleteDTO single = new TaskTagDeleteDTO();
            single.setTaskId(dto.getTaskId());
            single.setTagId(tagId);
            single.setIncludeSubtasks(dto.getIncludeSubtasks());
            delete(userId, single);
        }
    }

    private void deleteRecursive(Long userId, Long taskId, Long tagId) {
        List<Task> subtasks = getSubTasks(userId, taskId);
        for (Task subtask : subtasks) {
            deleteRecursive(userId, subtask.getTaskId(), tagId);
        }
        if (taskTagMapper.findByTaskIdAndTagId(taskId, tagId) != null) {
            taskTagMapper.deleteByTaskIdAndTagId(taskId, tagId);
        }
    }
}