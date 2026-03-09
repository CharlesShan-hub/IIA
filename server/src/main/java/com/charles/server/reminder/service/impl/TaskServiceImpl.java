package com.charles.server.reminder.service.impl;

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
import com.charles.server.reminder.service.RecurrenceService;
import com.charles.server.reminder.exception.TaskAccessException;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;

@Slf4j
@Service
@RequiredArgsConstructor
public class TaskServiceImpl implements TaskService {

    private final TaskMapper taskMapper;
    private final RecurrenceService recurrenceService;

    /**************************************************************************************/
    /*                                      Utils                                         */
    /**************************************************************************************/

    private Task convertToEntity(Long userId, TaskCreateRequest dto) {
        Task task = new Task();
        task.setUserId(userId);
        task.setProjectId(dto.getProjectId());
        task.setTitle(dto.getTitle());
        task.setParentTaskId(dto.getParentTaskId());
        task.setDueDate(dto.getDueDate());
        task.setStartDate(dto.getStartDate());
        task.setReminderSentAt(dto.getReminderSentAt());
        task.setPriority(dto.getPriority());
        task.setIsRecurring(Boolean.TRUE.equals(dto.getIsRecurring()));
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
            return (max == null ? 0 : max) + 1;
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

    /**************************************************************************************/
    /*                                    Basic CRUD                                      */
    /**************************************************************************************/

    @Transactional
    @Override
    public void create(Long userId, TaskCreateRequest dto) {
        Task task = convertToEntity(userId, dto);
        task.setStatus("todo");
        Long projectId = task.getProjectId();
        Long parentTaskId = task.getParentTaskId();
        task.setSortOrder(getNextSortOrder(userId, projectId, parentTaskId));
        taskMapper.insert(task);
        if (Boolean.TRUE.equals(task.getIsRecurring())) {
            recurrenceService.create(task.getTaskId(), dto);
        }
    }

    private boolean updateById(Task task) {
        log.info("Updating task with id: {}", task.getTaskId());
        // Validate task existence and ownership
        Task existingTask = taskMapper.findById(task.getTaskId());
        if (existingTask == null || !existingTask.getUserId().equals(task.getUserId())) {
            log.warn("Task not found or permission denied for task id: {}", task.getTaskId());
            return false;
        }
        int result = taskMapper.update(task);
        boolean success = result > 0;
        log.info("Task update {} for task id: {}", success ? "successful" : "failed", task.getTaskId());
        return success;
    }

    @Transactional
    @Override
    public void update(Long userId, TaskUpdateRequest dto) {
        Task task = new Task();
        task.setTaskId(dto.getTaskId());
        task.setUserId(userId);
        if (dto.getProjectId() != null) task.setProjectId(dto.getProjectId());
        if (dto.getTitle() != null) task.setTitle(dto.getTitle());
        if (dto.getIsRecurring() != null){
            task.setIsRecurring(dto.getIsRecurring());
            if(dto.getIsRecurring()) recurrenceService.create(task.getTaskId(), dto);
            else recurrenceService.deleteByTaskId(task.getTaskId());
        }
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
        deleteRecursively(validatedFindTaskById(userId, taskId));
    }

    private void deleteRecursively(Task task){
        // 1. Recursively delete all subtasks
        List<Task> subTasks = taskMapper.findByUserIdAndParentTaskId(task.getUserId(), task.getTaskId());
        subTasks.forEach(this::deleteRecursively);
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

    /**************************************************************************************/
    /*                                   Task Status                                      */
    /**************************************************************************************/

    @Override
    public void updateStatus(Long userId, TaskStatusUpdateRequest dto) {
        Task existing = validatedFindTaskById(userId, dto.getTaskId());
        String status = dto.getStatus();
        java.time.LocalDateTime completedAt = null;
        if ("done".equals(status)) {
            completedAt = java.time.LocalDateTime.now();
        }
        taskMapper.updateStatusAndCompletedAt(existing.getTaskId(), status, completedAt);
        if (Boolean.TRUE.equals(dto.getCascade())) {
            updateStatusRecursively(userId, existing.getTaskId(), status, completedAt);
        }
    }

    private void updateStatusRecursively(Long userId, Long parentTaskId, String status, java.time.LocalDateTime completedAt) {
        List<Task> children = taskMapper.findByUserIdAndParentTaskId(userId, parentTaskId);
        for (Task child : children) {
            java.time.LocalDateTime childCompletedAt = null;  // todo | abandoned
            if ("done".equals(status)) {
                childCompletedAt = (child.getCompletedAt() != null) ? child.getCompletedAt() : completedAt;
            }
            taskMapper.updateStatusAndCompletedAt(child.getTaskId(), status, childCompletedAt);
            updateStatusRecursively(userId, child.getTaskId(), status, completedAt);
        }
    }

    /**************************************************************************************/
    /*                                   Recurrence Task                                  */
    /**************************************************************************************/


    /**************************************************************************************/
    /*                              Support Project Operation                             */
    /**************************************************************************************/

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
}
