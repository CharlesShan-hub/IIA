package com.charles.server.reminder.service.impl;

import com.charles.server.reminder.entity.TaskTag;
import com.charles.server.reminder.entity.Task;
import com.charles.server.reminder.entity.Tag;
import com.charles.server.reminder.mapper.TaskTagMapper;
import com.charles.server.reminder.mapper.TaskMapper;
import com.charles.server.reminder.mapper.TagMapper;
import com.charles.server.reminder.service.TaskTagService;
import com.charles.server.reminder.dto.TaskTagCreateRequest;
import com.charles.server.reminder.dto.TaskTagDeleteRequest;
import com.charles.server.reminder.dto.TaskTagBatchCreateRequest;
import com.charles.server.reminder.dto.TaskTagBatchDeleteRequest;
import com.charles.server.reminder.exception.TagException;
import com.charles.server.reminder.exception.TaskAccessException;
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
    private final TagMapper tagMapper;

    private TaskTag convertToEntity(TaskTagCreateRequest dto) {
        return TaskTag.builder()
                .taskId(dto.getTaskId())
                .tagId(dto.getTagId())
                .build();
    }

    private void validatedFindTaskById(Long userId, Long taskId) {
        Task task = taskMapper.findById(taskId);
        if (task == null) {
            throw TaskAccessException.notFound(taskId);
        }
        if (!task.getUserId().equals(userId)) {
            throw TaskAccessException.permissionDenied(userId, taskId);
        }
    }

    private void validatedFindTagById(Long userId, Long tagId) {
        Tag tag = tagMapper.findById(tagId);
        if (tag == null) {
            throw TagException.notFound(tagId);
        }
        if (!tag.getUserId().equals(userId)) {
            throw TagException.permissionDenied(userId, tagId);
        }
    }

    private List<Task> getSubTasks(Long userId, Long parentTaskId) {
        return taskMapper.findByUserIdAndParentTaskId(userId, parentTaskId);
    }

    @Transactional
    @Override
    public void create(Long userId, TaskTagCreateRequest dto) {
        try{
            validatedFindTagById(userId, dto.getTagId());
            validatedFindTaskById(userId, dto.getTaskId());
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
    public void createBatch(Long userId, TaskTagBatchCreateRequest dto) {
        for (Long tagId : dto.getTagIds()) {
            TaskTagCreateRequest single = new TaskTagCreateRequest();
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
    public void delete(Long userId, TaskTagDeleteRequest dto) {
        try{
            validatedFindTagById(userId, dto.getTagId());
            validatedFindTaskById(userId, dto.getTaskId());
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
    public void deleteBatch(Long userId, TaskTagBatchDeleteRequest dto) {
        for (Long tagId : dto.getTagIds()) {
            TaskTagDeleteRequest single = new TaskTagDeleteRequest();
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

    // @Override
    // public int createBatch(List<TaskTag> taskTagList) {
    //     log.info("Creating batch task-tag associations, size: {}", taskTagList.size());
    //     int result = taskTagMapper.insertBatch(taskTagList);
    //     log.info("Created {} task-tag associations in batch", result);
    //     return result;
    // }

    // @Override
    // public TaskTag getById(Long id) {
    //     log.info("Getting task-tag association by id: {}", id);
    //     return taskTagMapper.findById(id);
    // }

    // @Override
    // public TaskTag getByTaskIdAndTagId(Long taskId, Long tagId) {
    //     log.info("Getting task-tag association by taskId: {} and tagId: {}", taskId, tagId);
    //     return taskTagMapper.findByTaskIdAndTagId(taskId, tagId);
    // }

    // @Override
    // public List<TaskTag> getByTaskId(Long taskId) {
    //     log.info("Getting all task-tag associations by taskId: {}", taskId);
    //     return taskTagMapper.findByTaskId(taskId);
    // }

    // @Override
    // public List<TaskTag> getByTagId(Long tagId) {
    //     log.info("Getting all task-tag associations by tagId: {}", tagId);
    //     return taskTagMapper.findByTagId(tagId);
    // }

    // @Override
    // public int deleteByTaskId(Long taskId) {
    //     log.info("Deleting all task-tag associations by taskId: {}", taskId);
    //     int result = taskTagMapper.deleteByTaskId(taskId);
    //     log.info("Deleted {} task-tag associations by taskId", result);
    //     return result;
    // }

    // @Override
    // public int deleteByTagId(Long tagId) {
    //     log.info("Deleting all task-tag associations by tagId: {}", tagId);
    //     int result = taskTagMapper.deleteByTagId(tagId);
    //     log.info("Deleted {} task-tag associations by tagId", result);
    //     return result;
    // }

    // @Override
    // public int deleteByTaskIdAndTagId(Long taskId, Long tagId) {
    //     log.info("Deleting task-tag association by taskId: {} and tagId: {}", taskId, tagId);
    //     int result = taskTagMapper.deleteByTaskIdAndTagId(taskId, tagId);
    //     log.info("Delete task-tag association result: {}", result > 0 ? "success" : "failed");
    //     return result;
    // }

    // @Override
    // public int deleteBatchByTaskIdAndTagIds(Long taskId, List<Long> tagIds) {
    //     log.info("Deleting batch task-tag associations by taskId: {} and tagIds size: {}", taskId, tagIds.size());
    //     int result = taskTagMapper.deleteBatchByTaskIdAndTagIds(taskId, tagIds);
    //     log.info("Deleted {} task-tag associations in batch", result);
    //     return result;
    // }
}


// select task.title, tag.name from reminder_task_tag tt join reminder_tag tag on tt.tag_id = tag.tag_id join reminder_task task on task.task_id = tt.task_id;