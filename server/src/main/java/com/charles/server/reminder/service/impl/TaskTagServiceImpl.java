package com.charles.server.reminder.service.impl;

import com.charles.server.reminder.entity.TaskTag;
import com.charles.server.reminder.mapper.TaskTagMapper;
import com.charles.server.reminder.service.TagService;
import com.charles.server.reminder.service.TaskService;
import com.charles.server.reminder.service.TaskTagService;
import com.charles.server.reminder.dto.CreateTaskTagRequest;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
@RequiredArgsConstructor
@Slf4j
public class TaskTagServiceImpl implements TaskTagService {

    private final TaskTagMapper taskTagMapper;

    private TaskTag convertToEntity(CreateTaskTagRequest dto) {
        TaskTag taskTag = new TaskTag();
        taskTag.setTaskId(dto.getTaskId());
        taskTag.setTagId(dto.getTagId());
        return taskTag;
    }

    @Override
    public void create(Long userId, CreateTaskTagRequest dto) {
//        validatedFindTagById(userId, dto.getTagId());
//        validatedFindTaskById(userId, dto.getTaskId());
        TaskTag taskTag = convertToEntity(dto);
        taskTagMapper.insert(taskTag);
        log.info("Created task-tag association with id: {}", taskTag.getId());
    }

    @Override
    public int createBatch(List<TaskTag> taskTagList) {
        log.info("Creating batch task-tag associations, size: {}", taskTagList.size());
        int result = taskTagMapper.insertBatch(taskTagList);
        log.info("Created {} task-tag associations in batch", result);
        return result;
    }

    @Override
    public TaskTag getById(Long id) {
        log.info("Getting task-tag association by id: {}", id);
        return taskTagMapper.findById(id);
    }

    @Override
    public TaskTag getByTaskIdAndTagId(Long taskId, Long tagId) {
        log.info("Getting task-tag association by taskId: {} and tagId: {}", taskId, tagId);
        return taskTagMapper.findByTaskIdAndTagId(taskId, tagId);
    }

    @Override
    public List<TaskTag> getByTaskId(Long taskId) {
        log.info("Getting all task-tag associations by taskId: {}", taskId);
        return taskTagMapper.findByTaskId(taskId);
    }

    @Override
    public List<TaskTag> getByTagId(Long tagId) {
        log.info("Getting all task-tag associations by tagId: {}", tagId);
        return taskTagMapper.findByTagId(tagId);
    }

    @Override
    public int deleteByTaskId(Long taskId) {
        log.info("Deleting all task-tag associations by taskId: {}", taskId);
        int result = taskTagMapper.deleteByTaskId(taskId);
        log.info("Deleted {} task-tag associations by taskId", result);
        return result;
    }

    @Override
    public int deleteByTagId(Long tagId) {
        log.info("Deleting all task-tag associations by tagId: {}", tagId);
        int result = taskTagMapper.deleteByTagId(tagId);
        log.info("Deleted {} task-tag associations by tagId", result);
        return result;
    }

    @Override
    public int deleteByTaskIdAndTagId(Long taskId, Long tagId) {
        log.info("Deleting task-tag association by taskId: {} and tagId: {}", taskId, tagId);
        int result = taskTagMapper.deleteByTaskIdAndTagId(taskId, tagId);
        log.info("Delete task-tag association result: {}", result > 0 ? "success" : "failed");
        return result;
    }

    @Override
    public int deleteBatchByTaskIdAndTagIds(Long taskId, List<Long> tagIds) {
        log.info("Deleting batch task-tag associations by taskId: {} and tagIds size: {}", taskId, tagIds.size());
        int result = taskTagMapper.deleteBatchByTaskIdAndTagIds(taskId, tagIds);
        log.info("Deleted {} task-tag associations in batch", result);
        return result;
    }
}