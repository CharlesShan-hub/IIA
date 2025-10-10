package com.charles.server.reminder.service.impl;

import java.time.LocalDateTime;
import java.util.List;

import com.charles.server.reminder.dto.CreateTaskRequest;
import org.springframework.stereotype.Service;

import com.charles.server.reminder.entity.Task;
import com.charles.server.reminder.mapper.TaskMapper;
import com.charles.server.reminder.service.TaskService;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;

@Slf4j
@Service
@RequiredArgsConstructor
public class TaskServiceImpl implements TaskService {

    private final TaskMapper taskMapper;

    @Override
    public void create(Long userId, CreateTaskRequest dto) {
        log.info("Creating task for user: {}", userId);
        Task task = new Task(dto);
        dto.setUserId(userId);
        task.setStatus("todo");
        task.setIsArchived(false);
        Long projectId = task.getProjectId();
        Long parentTaskId = task.getParentTaskId();
        int count;
        if(parentTaskId == null){
            count = taskMapper.findByUserIdAndProjectId(userId, null).size();
        }else{
            assert this.getById(parentTaskId).getUserId().equals(userId);
            count = taskMapper.findSubTasks(userId, parentTaskId).size();
        }
        task.setSortOrder(count + 1);

        int result = taskMapper.insert(task);
        if (result > 0) {
            log.info("Task created successfully with id: {}", task.getTaskId());
        }
        log.error("Failed to create task");
    }

    @Override
    public List<Task> getAll(Long userId) {
        log.info("Getting all tasks for user: {}", userId);
        return taskMapper.findByUserId(userId);
    }

    @Override
    public Task getById(Long taskId) {
        log.info("Getting task by id: {}", taskId);
        return taskMapper.findById(taskId);
    }

    @Override
    public boolean updateById(Task task) {
        log.info("Updating task with id: {}", task.getTaskId());
        // 验证任务存在且属于当前用户
        Task existingTask = taskMapper.findById(task.getTaskId());
        if (existingTask == null || !existingTask.getUserId().equals(task.getUserId())) {
            log.warn("Task not found or permission denied for task id: {}", task.getTaskId());
            return false;
        }
        
        int result = taskMapper.update(task);
        boolean success = result > 0;
        log.info("Task update {}" + (success ? "successful" : "failed") + " for task id: {}", success ? "successful" : "failed", task.getTaskId());
        return success;
    }

    @Override
    public boolean updateStatus(Long taskId, String status) {
        log.info("Updating status for task id: {} to {}", taskId, status);
        // 验证任务存在
        Task existingTask = taskMapper.findById(taskId);
        if (existingTask == null) {
            log.warn("Task not found for id: {}", taskId);
            return false;
        }
        
        int result = taskMapper.updateStatus(taskId, status);
        boolean success = result > 0;
        log.info("Task status update {}" + (success ? "successful" : "failed") + " for task id: {}", success ? "successful" : "failed", taskId);
        return success;
    }

    @Override
    public List<Task> getByStatus(Long userId, String status) {
        log.info("Getting tasks for user: {} with status: {}", userId, status);
        return taskMapper.findByUserIdAndStatus(userId, status);
    }

    @Override
    public List<Task> getByProjectId(Long userId, Long projectId) {
        log.info("Getting tasks for user: {} in project: {}", userId, projectId);
        return taskMapper.findByUserIdAndProjectId(userId, projectId);
    }

    @Override
    public List<Task> getSubTasks(Long userId, Long parentTaskId) {
        log.info("Getting sub-tasks for user: {} with parent task id: {}", userId, parentTaskId);
        return taskMapper.findSubTasks(userId, parentTaskId);
    }

    @Override
    public List<Task> getUpcomingTasks(Long userId, LocalDateTime dueDate) {
        log.info("Getting upcoming tasks for user: {} until: {}", userId, dueDate);
        return taskMapper.findUpcomingTasks(userId, dueDate);
    }
}