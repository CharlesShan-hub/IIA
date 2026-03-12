package com.charles.server.reminder.service.impl;

import com.charles.server.reminder.dto.BatchUpdatePositionRequest;
import com.charles.server.reminder.dto.ProjectDeleteRequest;
import com.charles.server.reminder.dto.TaskCreateRequest;
import com.charles.server.reminder.dto.TaskUpdateRequest;
import com.charles.server.reminder.dto.TaskGetAllRequest;
import com.charles.server.reminder.dto.TaskUpdateCompletedRequest;
import com.charles.server.reminder.dto.TaskUpdateAbandonedRequest;
import com.charles.server.reminder.entity.Task;
import com.charles.server.reminder.entity.History;
import com.charles.server.reminder.mapper.TaskMapper;
import com.charles.server.reminder.service.TaskService;
import com.charles.server.reminder.service.HistoryService;
import com.charles.server.reminder.service.PermissionService;
import com.charles.server.reminder.service.RecurrenceService;
import com.charles.server.reminder.exception.TaskException;

import java.util.List;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.stereotype.Service;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;

@Slf4j
@Service
@RequiredArgsConstructor
public class TaskServiceImpl implements TaskService {

    private final TaskMapper taskMapper;
    private final HistoryService historyService;
    private final RecurrenceService recurrenceService;
    private final PermissionService permissionService;

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

    /**************************************************************************************/
    /*                                    Basic CRUD                                      */
    /**************************************************************************************/

    @Transactional
    @Override
    public void create(Long userId, TaskCreateRequest dto) {
        Task task = convertToEntity(userId, dto);
        task.setIsCompleted(Boolean.FALSE);
        task.setIsAbandoned(Boolean.FALSE);
        task.setIsSkipped(Boolean.FALSE);
        Long projectId = task.getProjectId();
        Long parentTaskId = task.getParentTaskId();
        task.setSortOrder(getNextSortOrder(userId, projectId, parentTaskId));
        taskMapper.insert(task);
        if (Boolean.TRUE.equals(task.getIsRecurring())) {
            recurrenceService.create(task.getTaskId(), dto);
        }
    }

    private void updateById(Task task) {
        log.info("Updating task with id: {}", task.getTaskId());
        Task existingTask = taskMapper.findById(task.getTaskId());
        if (existingTask == null) {
            throw TaskException.notFound(task.getTaskId());
        }
        if (!existingTask.getUserId().equals(task.getUserId())) {
            throw TaskException.permissionDenied(task.getUserId(), task.getTaskId());
        }
        int result = taskMapper.update(task);
        boolean success = result > 0;
        log.info("Task update {} for task id: {}", success ? "successful" : "failed", task.getTaskId());
        if (!success) {
            throw new RuntimeException("Task update failed");
        }
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
            if(dto.getIsRecurring()) recurrenceService.update(task.getTaskId(), dto);
            else recurrenceService.delete(task.getTaskId());
        }
        if (dto.getParentTaskId() != null) task.setParentTaskId(dto.getParentTaskId());
        if (dto.getDueDate() != null) task.setDueDate(dto.getDueDate());
        if (dto.getStartDate() != null) task.setStartDate(dto.getStartDate());
        if (dto.getReminderSentAt() != null) task.setReminderSentAt(dto.getReminderSentAt());
        if (dto.getPriority() != null) task.setPriority(dto.getPriority());
        updateById(task);
    }

    @Override
    public void delete(Long userId, Long taskId) {
        deleteRecursively(permissionService.getTask(userId, taskId));
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
        request.getPos().forEach(t -> permissionService.validTask(userId, t.getItemId()));
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
    @Transactional
    public void updateCompletedStatus(Long userId, TaskUpdateCompletedRequest dto) {
        Task existing = permissionService.getTask(userId, dto.getTaskId());
        // 如果任务已废弃，直接忽略
        if(Boolean.TRUE.equals(existing.getIsAbandoned())) return;
        // 如果状态没有变化，直接忽略
        if(dto.getIsCompleted().equals(existing.getIsCompleted())) return;
        // 只有激活中的任务，且状态发生变化时才处理
        java.time.LocalDateTime operationTime = java.time.LocalDateTime.now();
        Long operationId = historyService.generateNextOperationId();
        // 上次的操作ID（如果没有历史记录，则使用0L）
        History lastHistory = historyService.findLatestByTaskId(existing.getTaskId());
        Long lastOperationId = (lastHistory != null) ? lastHistory.getOperationId() : 0L;
        // 记录状态变更历史
        historyService.create(History.builder()
            .taskId(existing.getTaskId())
            .isCompleted(dto.getIsCompleted())
            .isAbandoned(existing.getIsAbandoned())
            .isSkipped(existing.getIsSkipped())
            .operationId(operationId)
            .createdAt(operationTime)
            .build());
        // 更新主任务完成状态
        // 如果任务完成，设置完成时间；如果取消完成，清空完成时间
        java.time.LocalDateTime completedAt = dto.getIsCompleted() ? operationTime : null;
        taskMapper.updateCompletedStatus(existing.getTaskId(), dto.getIsCompleted(), completedAt);
        // 递归更新子任务完成状态
        updateCompletedStatusRecursively(userId, existing.getTaskId(), dto.getIsCompleted(), operationTime, completedAt, operationId, lastOperationId);
    }

    private void updateCompletedStatusRecursively(Long userId, Long parentTaskId, Boolean isCompleted, 
                                                 java.time.LocalDateTime operationTime,java.time.LocalDateTime completedAt, Long operationId, Long parentLastOperationId) {
        List<Task> children = taskMapper.findByUserIdAndParentTaskId(userId, parentTaskId);
        for (Task child : children) {
            // 如果子任务已废弃，直接忽略
            if(Boolean.TRUE.equals(child.getIsAbandoned())) continue;
            // 只有当子任务的完成状态实际发生变化时才处理
            if(isCompleted.equals(child.getIsCompleted())) continue;
            
            // 对于取消完成，需要智能判断：
            // 只有由父任务完成操作完成的子任务才取消完成
            if(!isCompleted) {
                // parentLastOperationId应该总是有值的，因为父任务必须曾经被完成过才能取消完成
                // 检查父任务的上次完成操作ID是否在子任务的历史记录中
                // 这样可以处理：A完成时同步了B，后来B被单独操作过，现在取消A时B也应该被取消
                boolean foundInChildHistory = historyService.isOperationIdInTaskHistory(child.getTaskId(), parentLastOperationId);
                if(!foundInChildHistory) {
                    // 父任务的完成操作没有影响这个子任务，跳过
                    continue;
                }
            }
            // 记录子任务状态变更历史
            historyService.create(History.builder()
                .taskId(child.getTaskId())
                .isCompleted(isCompleted) // 子任务使用与父任务相同的完成状态
                .isAbandoned(child.getIsAbandoned()) // 保持原有废弃状态
                .isSkipped(child.getIsSkipped())     // 保持原有跳过状态
                .operationId(operationId)
                .createdAt(operationTime)
                .build());
            // 更新子任务完成状态
            taskMapper.updateCompletedStatus(child.getTaskId(), isCompleted, completedAt);
            // 递归更新孙子任务，传递当前操作ID作为parentLastOperationId
            updateCompletedStatusRecursively(userId, child.getTaskId(), isCompleted, operationTime, completedAt, operationId, operationId);
        }
    }
    
    @Override
    @Transactional
    public void updateAbandonedStatus(Long userId, TaskUpdateAbandonedRequest dto) {
        Task existing = permissionService.getTask(userId, dto.getTaskId());
        // 如果状态没有变化，直接返回
        if(dto.getIsAbandoned().equals(existing.getIsAbandoned())) return;
        // 只有当任务有父任务时，才需要检查父任务的完成状态
        if(existing.getParentTaskId() != null && Boolean.FALSE.equals(dto.getIsAbandoned())) {
            // 检查父任务是否已废弃
            Task parent = permissionService.getTask(userId, existing.getParentTaskId());
            if(Boolean.TRUE.equals(parent.getIsAbandoned())) {
                return; // 父任务已废弃，子任务也自动废弃
            }
        }
        
        java.time.LocalDateTime operationTime = java.time.LocalDateTime.now();
        Long operationId = historyService.generateNextOperationId();
        
        // 上次的操作ID（如果没有历史记录，则使用0L）
        History lastHistory = historyService.findLatestByTaskId(existing.getTaskId());
        Long lastOperationId = (lastHistory != null) ? lastHistory.getOperationId() : 0L;
        
        // 记录状态变更历史
        historyService.create(History.builder()
            .taskId(existing.getTaskId())
            .isCompleted(existing.getIsCompleted())
            .isAbandoned(dto.getIsAbandoned())
            .isSkipped(existing.getIsSkipped())
            .operationId(operationId)
            .createdAt(operationTime)
            .build());
        
        // 更新主任务废弃状态
        taskMapper.updateAbandonedStatus(existing.getTaskId(), dto.getIsAbandoned());
        
        // 递归更新子任务废弃状态
        updateAbandonedStatusRecursively(userId, existing.getTaskId(), dto.getIsAbandoned(), operationTime, operationId, lastOperationId);
    }
    
    private void updateAbandonedStatusRecursively(Long userId, Long parentTaskId, Boolean isAbandoned, 
                                                 java.time.LocalDateTime operationTime, Long operationId, Long parentLastOperationId) {
        List<Task> children = taskMapper.findByUserIdAndParentTaskId(userId, parentTaskId);
        for (Task child : children) {
            // 只有当子任务的废弃状态实际发生变化时才处理
            if(isAbandoned.equals(child.getIsAbandoned())) continue;
            
            // 对于恢复废弃状态（isAbandoned = false），需要智能判断：
            // 只有由父任务废弃操作废弃的子任务才恢复
            if(!isAbandoned) {
                // parentLastOperationId应该总是有值的，因为父任务必须曾经被废弃过才能恢复
                // 检查父任务的上次废弃操作ID是否在子任务的历史记录中
                // 这样可以处理：A废弃时同步了B，后来B被单独操作过，现在恢复A时B也应该被恢复
                boolean foundInChildHistory = historyService.isOperationIdInTaskHistory(child.getTaskId(), parentLastOperationId);
                if(!foundInChildHistory) {
                    // 父任务的废弃操作没有影响这个子任务，跳过
                    continue;
                }
            }
            
            // 记录子任务状态变更历史
            historyService.create(History.builder()
                .taskId(child.getTaskId())
                .isCompleted(child.getIsCompleted()) // 保持原有完成状态
                .isAbandoned(isAbandoned)            // 子任务使用与父任务相同的废弃状态
                .isSkipped(child.getIsSkipped())     // 保持原有跳过状态
                .operationId(operationId)
                .createdAt(operationTime)
                .build());
            
            // 更新子任务废弃状态
            taskMapper.updateAbandonedStatus(child.getTaskId(), isAbandoned);
            
            // 递归更新孙子任务，传递当前操作ID作为parentLastOperationId
            updateAbandonedStatusRecursively(userId, child.getTaskId(), isAbandoned, operationTime, operationId, operationId);
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
