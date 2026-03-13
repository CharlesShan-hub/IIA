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

    /**
     * Update completed status of a task and its child tasks recursively.
     * 1. If the task is abandoned, do nothing.
     * 2. If the status has not changed, do nothing.
     * 3. Recursively update completed status of child tasks.
     * 3.1 If the child task is abandoned, do nothing.
     * 3.2 If the status has not changed, do nothing.
     * 3.3 Child tasks are synchronized with the parent task.
     * 3.3.1 If a task is completed, all child tasks are completed.
     * 3.3.2 If a task is cancelled, all child tasks are cancelled if they were completed by the parent task.
     * 3.3.3 If a task is cancelled, its parent task is cancelled.
     * 
     * @param userId the user ID
     * @param dto the task update completed request
     */
    @Override
    @Transactional
    public void updateCompletedStatus(Long userId, TaskUpdateCompletedRequest dto) {
        Task existing = permissionService.getTask(userId, dto.getTaskId());
        // if task is abandoned, do nothing
        if(Boolean.TRUE.equals(existing.getIsAbandoned())) return;
        // if status has not changed, do nothing
        if(dto.getIsCompleted().equals(existing.getIsCompleted())) return;
        // only update active tasks
        java.time.LocalDateTime operationTime = java.time.LocalDateTime.now();
        Long operationId = historyService.generateNextOperationId();
        // last operation id of the task, if no history, use 0L
        History lastHistory = historyService.findLatestByTaskId(existing.getTaskId());
        Long lastOperationId = (lastHistory != null) ? lastHistory.getOperationId() : 0L;
        // record status change history
        historyService.create(History.builder()
            .taskId(existing.getTaskId())
            .isCompleted(dto.getIsCompleted())
            .isAbandoned(existing.getIsAbandoned())
            .isSkipped(existing.getIsSkipped())
            .operationId(operationId)
            .createdAt(operationTime)
            .build());
        // update task status
        // if task is completed, set completed time; if cancelled, clear completed time
        java.time.LocalDateTime completedAt = dto.getIsCompleted() ? operationTime : null;
        taskMapper.updateCompletedStatus(existing.getTaskId(), dto.getIsCompleted(), completedAt);
        
        // recursively update completed status of child tasks
        updateChildCompletedStatusRecursively(userId, existing, dto.getIsCompleted(), operationTime, completedAt, operationId, lastOperationId);
        
        // recursively update completed status of parent tasks
        updateParentCompletedStatusRecursively(userId, existing, dto.getIsCompleted(), operationTime, completedAt, operationId, lastOperationId);
    }

    private void updateChildCompletedStatusRecursively(
        Long userId, Task parentTask, Boolean isCompleted, 
        java.time.LocalDateTime operationTime,java.time.LocalDateTime completedAt, 
        Long operationId, Long parentLastOperationId
    ){
        List<Task> children = taskMapper.findByUserIdAndParentTaskId(userId, parentTask.getTaskId());
        for (Task child : children) {
            // if child task is abandoned, do nothing
            if(Boolean.TRUE.equals(child.getIsAbandoned())) continue;
            // only update child task if its completed status has changed
            if(isCompleted.equals(child.getIsCompleted())) continue;
            
            // For cancellation, need smart judgment:
            // only cancel child task if its completed status has changed
            if(!isCompleted) {
                // parentLastOperationId should always have a value, because parent task must have been completed once to cancel
                // check if parent task's last completed operation id is in child task's history
                // Example: A completed, B is completed and synchronized with A, then B is cancelled, B should be cancelled as well
                boolean foundInChildHistory = historyService.isOperationIdInTaskHistory(child.getTaskId(), parentLastOperationId);
                if(!foundInChildHistory) {
                    // parent task's completed operation has no effect on this child task, skip
                    continue;
                }
            }
            // record child task status change history
            historyService.create(History.builder()
                .taskId(child.getTaskId())
                .isCompleted(isCompleted) // child task uses the same completed status as parent task
                .isAbandoned(child.getIsAbandoned()) // keep original abandoned status
                .isSkipped(child.getIsSkipped())     // keep original skipped status
                .operationId(operationId)
                .createdAt(operationTime)
                .build());
            // update child task completed status
            taskMapper.updateCompletedStatus(child.getTaskId(), isCompleted, completedAt);
            // recursively update completed status of grandchild tasks, pass current operation ID as parentLastOperationId
            updateChildCompletedStatusRecursively(userId, child, isCompleted, operationTime, completedAt, operationId, operationId);
        }
    }
    
    /**
     * Recursively cancel parent task's completed status when a child task is cancelled.
     * Only cancel parent task if:
     * 1. Parent task is completed
     * 2. Parent task was completed by the same operation that completed this child task
     * 3. Parent task is not abandoned
     */
    private void updateParentCompletedStatusRecursively(
        Long userId, Task currentTask, Boolean isCompleted, 
        java.time.LocalDateTime operationTime, java.time.LocalDateTime completionTime, 
        Long operationId, Long childLastOperationId
    ){
        // No parent task, return
        Task parentTask = permissionService.getTask(userId, currentTask.getParentTaskId());
        if(parentTask == null) return;
        // If parent task is abandoned, do nothing
        if (Boolean.TRUE.equals(parentTask.getIsAbandoned())) return;
        // only update parent task if its completed status has changed
        if(isCompleted.equals(parentTask.getIsCompleted())) return;

        // For completion, need smart judgment:
        // only complete parent task if its completed status has changed
        if(isCompleted) {
            boolean foundInParentHistory = historyService.isOperationIdInTaskHistory(parentTask.getTaskId(), childLastOperationId);
            if(!foundInParentHistory) return;
        }
        // record parent task status change history
        historyService.create(History.builder()
                .taskId(parentTask.getTaskId())
                .isCompleted(isCompleted) // parent task uses the same completed status as child task
                .isAbandoned(parentTask.getIsAbandoned()) // keep original abandoned status
                .isSkipped(parentTask.getIsSkipped())     // keep original skipped status
                .operationId(operationId)
                .createdAt(operationTime)
                .build());
        // update parent task completed status
        taskMapper.updateCompletedStatus(parentTask.getTaskId(), isCompleted, completionTime);
        // recursively update completed status of grandparent tasks, pass current operation ID as childLastOperationId
        updateParentCompletedStatusRecursively(userId, parentTask, isCompleted, operationTime, completionTime, operationId, operationId);
    }
    
    @Override
    @Transactional
    public void updateAbandonedStatus(Long userId, TaskUpdateAbandonedRequest dto) {
        Task existing = permissionService.getTask(userId, dto.getTaskId());
        // if status has not changed, do nothing
        if(dto.getIsAbandoned().equals(existing.getIsAbandoned())) return;
        // only update active tasks
        // only need to check parent task's completed status when task has a parent
        if(existing.getParentTaskId() != null && Boolean.FALSE.equals(dto.getIsAbandoned())) {
            // check if parent task is abandoned
            Task parent = permissionService.getTask(userId, existing.getParentTaskId());
            if(Boolean.TRUE.equals(parent.getIsAbandoned())) {
                return; // parent task is abandoned, child task is automatically abandoned
            }
        }
        
        java.time.LocalDateTime operationTime = java.time.LocalDateTime.now();
        Long operationId = historyService.generateNextOperationId();
        
        // check if last operation ID is in task history
        // if not, it means this task was never abandoned, so it cannot be recovered
        History lastHistory = historyService.findLatestByTaskId(existing.getTaskId());
        Long lastOperationId = (lastHistory != null) ? lastHistory.getOperationId() : 0L;
        if(!historyService.isOperationIdInTaskHistory(existing.getTaskId(), lastOperationId)) {
            return; // last operation ID is not in history, this task was never abandoned, so it cannot be recovered
        }
        
        // record status change history
        historyService.create(History.builder()
            .taskId(existing.getTaskId())
            .isCompleted(existing.getIsCompleted())
            .isAbandoned(dto.getIsAbandoned())
            .isSkipped(existing.getIsSkipped())
            .operationId(operationId)
            .createdAt(operationTime)
            .build());
        
        // update main task abandoned status
        taskMapper.updateAbandonedStatus(existing.getTaskId(), dto.getIsAbandoned());
        
        // recursively update abandoned status of child tasks
        updateAbandonedStatusRecursively(userId, existing.getTaskId(), dto.getIsAbandoned(), operationTime, operationId, lastOperationId);
    }
    
    private void updateAbandonedStatusRecursively(Long userId, Long parentTaskId, Boolean isAbandoned, 
                                                 java.time.LocalDateTime operationTime, Long operationId, Long parentLastOperationId) {
        List<Task> children = taskMapper.findByUserIdAndParentTaskId(userId, parentTaskId);
        for (Task child : children) {
            // only handle when child task's abandoned status actually changes
            if(isAbandoned.equals(child.getIsAbandoned())) continue;
            
            // For recovering abandoned status (isAbandoned = false), need smart judgment:
            // Only the child tasks that were abandoned by the parent task can be recovered
            if(!isAbandoned) {
                // parentLastOperationId should always have a value, because parent task must have been abandoned to recover
                // check if parent task's last abandoned operation ID is in child task's history
                // this can handle: when A is abandoned and synchronized with B, later B is independently operated, now recovering A should also recover B
                boolean foundInChildHistory = historyService.isOperationIdInTaskHistory(child.getTaskId(), parentLastOperationId);
                if(!foundInChildHistory) {
                    // parent task's last abandoned operation ID is not in child task's history,
                    // which means this child task was not abandoned by the parent task,
                    // so it cannot be recovered, skip it
                    continue;
                }
            }
            
            // record child task status change history
            historyService.create(History.builder()
                .taskId(child.getTaskId())
                .isCompleted(child.getIsCompleted()) // keep original completed status
                .isAbandoned(isAbandoned)            // child task uses the same abandoned status as parent task
                .isSkipped(child.getIsSkipped())     // keep original skipped status
                .operationId(operationId)
                .createdAt(operationTime)
                .build());
            
            // update child task abandoned status
            taskMapper.updateAbandonedStatus(child.getTaskId(), isAbandoned);
            
            // recursively update abandoned status of grandchild tasks, pass current operation ID as parentLastOperationId
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
