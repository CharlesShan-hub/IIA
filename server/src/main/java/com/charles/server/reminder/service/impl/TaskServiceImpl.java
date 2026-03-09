package com.charles.server.reminder.service.impl;

import java.time.LocalDateTime;
import java.util.List;
import org.springframework.transaction.annotation.Transactional;

import com.charles.server.reminder.dto.BatchUpdatePositionRequest;
import com.charles.server.reminder.dto.ProjectDeleteRequest;
import com.charles.server.reminder.dto.TaskCreateRequest;
import com.charles.server.reminder.dto.TaskUpdateRequest;
import com.charles.server.reminder.dto.TaskGetAllRequest;
import com.charles.server.reminder.dto.TaskStatusUpdateRequest;

import org.springframework.stereotype.Service;

import com.charles.server.reminder.entity.Task;
import com.charles.server.reminder.mapper.TaskMapper;
import com.charles.server.reminder.service.TaskService;
import com.charles.server.reminder.exception.TaskAccessException;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;

@Slf4j
@Service
@RequiredArgsConstructor
public class TaskServiceImpl implements TaskService {

    private final TaskMapper taskMapper;

    private Task convertToEntity(Long userId, TaskCreateRequest dto) {
        Task task = new Task();
        task.setUserId(userId);
        task.setProjectId(dto.getProjectId());
        task.setTitle(dto.getTitle());
        task.setCategory(dto.getCategory());
        task.setParentTaskId(dto.getParentTaskId());
        task.setDueDate(dto.getDueDate());
        task.setStartDate(dto.getStartDate());
        task.setReminderSentAt(dto.getReminderSentAt());
        task.setPriority(dto.getPriority());
        return task;
    }

    private int getNextSortOrder(Long userId, Long projectId, Long parentTaskId) {
        if (parentTaskId == null) {
            if (projectId == null) {
                Integer max = taskMapper.findMaxSortOrderOfRootTasksByUserIdAndProjectIdIsNull(userId);
                return (max == null ? 0 : max) + 1;
            } else {
                Integer max = taskMapper.findMaxSortOrderOfRootTasksByUserIdAndProjectId(userId, projectId);
                return (max == null ? 0 : max) + 1;
            }
        } else {
            Integer max = taskMapper.findMaxSortOrderByUserIdAndParentTaskId(userId, parentTaskId);
            return (max == 0 ? 0 : max) + 1;
        }
    }

    private Task validatedFindTaskById(Long userId, Long taskId) {
        Task task = taskMapper.findById(taskId);
        if (task == null) {
            throw TaskAccessException.notFound(taskId);
        }
        if (!task.getUserId().equals(userId)) {
            throw TaskAccessException.permissionDenied(userId, taskId);
        }
        return task;
    }

    @Override
    public void create(Long userId, TaskCreateRequest dto) {
        Task task = convertToEntity(userId, dto);
        task.setStatus("todo");
        Long projectId = task.getProjectId();
        Long parentTaskId = task.getParentTaskId();
        task.setSortOrder(getNextSortOrder(userId, projectId, parentTaskId));
        taskMapper.insert(task);
    }

    @Override
    public void update(Long userId, TaskUpdateRequest dto) {
        Task task = new Task();
        task.setTaskId(dto.getTaskId());
        task.setUserId(userId);
        if (dto.getProjectId() != null) task.setProjectId(dto.getProjectId());
        if (dto.getTitle() != null) task.setTitle(dto.getTitle());
        if (dto.getCategory() != null) task.setCategory(dto.getCategory());
        if (dto.getParentTaskId() != null) task.setParentTaskId(dto.getParentTaskId());
        if (dto.getDueDate() != null) task.setDueDate(dto.getDueDate());
        if (dto.getStartDate() != null) task.setStartDate(dto.getStartDate());
        if (dto.getReminderSentAt() != null) task.setReminderSentAt(dto.getReminderSentAt());
        if (dto.getPriority() != null) task.setPriority(dto.getPriority());
        if (!updateById(task)) {
            throw new RuntimeException("Task update failed or no permission");
        }
    }

    @Override
    public void delete(Long userId, Long taskId) {
        deleteById(validatedFindTaskById(userId, taskId));
    }

    private void deleteById(Task task){
        // 1. Recursively delete all subtasks
        List<Task> subTasks = taskMapper.findByUserIdAndParentTaskId(task.getUserId(), task.getTaskId());
        subTasks.forEach(this::deleteById);
        // 2. Delete current task (task-tag relations are cascade-deleted by DB)
        // 3. No sort order adjustment needed due to max()+1 insertion strategy
        // 4. Delete current task
        taskMapper.deleteById(task.getTaskId());
    }

    @Transactional
    @Override
    public void batchUpdatePosition(Long userId, BatchUpdatePositionRequest request) {
        request.getPos().forEach(t -> validatedFindTaskById(userId, t.getItemId()));
        request.getPos().forEach(t -> {
            Task task = new Task();
            task.setTaskId(t.getItemId());
            task.setSortOrder(t.getSortOrder());
            taskMapper.updateSortOrder(task);
        });
    }

    @Override
    public List<Task> getAll(Long userId, TaskGetAllRequest dto) {
        if (Boolean.TRUE.equals(dto.getIsAll())) {
            return taskMapper.findByUserId(userId);
        }
        if (dto.getProjectId() == null) {
            return taskMapper.findByUserIdAndProjectIdIsNull(userId);
        }
        return taskMapper.findByUserIdAndProjectId(userId, dto.getProjectId());
    }

    @Override
    public void batchUpdateProjectId(Long userId, ProjectDeleteRequest dto) {
        if (dto == null || dto.getProjectId() == null) return;
        Long fromProjectId = dto.getProjectId();
        // Capture source root tasks (for order preservation)
        List<Task> sourceTasks = taskMapper.findByUserIdAndProjectId(userId, fromProjectId);
        java.util.List<Task> sourceRoot = new java.util.ArrayList<>();
        for (Task t : sourceTasks) {
            if (t.getParentTaskId() == null) sourceRoot.add(t);
        }
        sourceRoot.sort(java.util.Comparator.comparing(Task::getSortOrder)
                .thenComparing(Task::getTaskId));

        if (Boolean.TRUE.equals(dto.getTargetProject())) {
            // Move to target project
            // target project_id has been validated in ProjectDeleteRequest!
            Long toProjectId = dto.getTargetProjectId();
            Integer max = taskMapper.findMaxSortOrderOfRootTasksByUserIdAndProjectId(userId, toProjectId);
            int next = (max == null ? 0 : max) + 1;
            // Move tasks
            taskMapper.updateProjectIdByUserId(userId, fromProjectId, toProjectId);
            // Append moved roots after existing ones in target project
            for (Task rt : sourceRoot) {
                Task update = new Task();
                update.setTaskId(rt.getTaskId());
                update.setSortOrder(next++);
                taskMapper.updateSortOrder(update);
            }
        } else {
            // Move to inbox (project_id = NULL), append after existing inbox roots
            Integer maxInbox = taskMapper.findMaxSortOrderOfRootTasksByUserIdAndProjectIdIsNull(userId);
            int next = (maxInbox == null ? 0 : maxInbox) + 1;
            taskMapper.clearProjectIdByUserId(userId, fromProjectId);
            for (Task rt : sourceRoot) {
                Task update = new Task();
                update.setTaskId(rt.getTaskId());
                update.setSortOrder(next++);
                taskMapper.updateSortOrder(update);
            }
        }
    }

    @Override
    public void deleteByProjectId(Long userId, Long projectId) {
        taskMapper.deleteByUserIdAndProjectId(userId, projectId);
    }

    @Override
    public Task getById(Long taskId) { return taskMapper.findById(taskId);}

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
        log.info("Task update {}{} for task id: {}", success ? "successful" : "failed", success ? "successful" : "failed", task.getTaskId());
        return success;
    }

    @Override
    public void updateStatus(Long userId, TaskStatusUpdateRequest dto) {
        Task task = validatedFindTaskById(userId, dto.getTaskId());
        taskMapper.updateStatus(task.getTaskId(), dto.getStatus());
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
        return taskMapper.findByUserIdAndParentTaskId(userId, parentTaskId);
    }

    @Override
    public List<Task> getUpcomingTasks(Long userId, LocalDateTime dueDate) {
        log.info("Getting upcoming tasks for user: {} until: {}", userId, dueDate);
        return taskMapper.findUpcomingTasks(userId, dueDate);
    }
}
