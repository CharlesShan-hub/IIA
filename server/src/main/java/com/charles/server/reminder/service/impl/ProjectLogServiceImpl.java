package com.charles.server.reminder.service.impl;

import com.charles.server.reminder.entity.Project;
import com.charles.server.reminder.entity.ProjectLog;
import com.charles.server.reminder.mapper.ProjectLogMapper;
import com.charles.server.reminder.mapper.ProjectMapper;
import com.charles.server.reminder.service.ProjectLogService;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;

@Service
@RequiredArgsConstructor
@Slf4j
public class ProjectLogServiceImpl implements ProjectLogService {
    
    private final ProjectLogMapper projectLogMapper;
    private final ProjectMapper projectMapper;
    
    @Override
    public void save(Project project) {
        save(project, null);
    }
    
    @Override
    public void save(Project project, Long batchOperationId) {
        ProjectLog projectLog = ProjectLog.fromProject(project, batchOperationId);
        projectLogMapper.insert(projectLog);
        log.debug("Project log saved: projectId={}, operationId={}, batchOperationId={}", 
                project.getProjectId(), project.getOperationId(), batchOperationId);
    }
    
    @Override
    public List<ProjectLog> findByProjectId(Long projectId) {
        return projectLogMapper.findByProjectId(projectId);
    }
    
    @Override
    public List<ProjectLog> findByOperationId(Long operationId) {
        return projectLogMapper.findByOperationId(operationId);
    }
    
    @Override
    public List<ProjectLog> findByBatchOperationId(Long batchOperationId) {
        return projectLogMapper.findByBatchOperationId(batchOperationId);
    }
    
    @Override
    @Transactional
    public void revert(Long userId, Long operationId, Long previousOperationId) {
        // 处理新增操作的撤回（previousOperationId为null）
        if (previousOperationId == null || previousOperationId == 0) {
            // 新增操作：直接删除所有operationId = operationId的项目
            int deletedCount = projectMapper.deleteByOperationId(operationId);
            
            // 删除相关的日志记录
            projectLogMapper.deleteByOperationId(operationId);
            
            log.info("撤回新增操作完成: userId={}, operationId={}, deletedCount={}", 
                    userId, operationId, deletedCount);
            return;
        }
        
        // 1. 查找需要恢复的日志记录
        // 先尝试根据batch_operation_id查找（批量操作）
        List<ProjectLog> logsToRestore = projectLogMapper.findByBatchOperationId(operationId);
        
        boolean isBatchOperation = !logsToRestore.isEmpty();
        
        // 如果没有找到批量操作的日志，则根据operation_id查找（单个操作）
        if (!isBatchOperation) {
            logsToRestore = projectLogMapper.findByOperationId(previousOperationId);
        }
        
        if (logsToRestore.isEmpty()) {
            log.warn("没有找到可恢复的日志记录: userId={}, operationId={}, previousOperationId={}", 
                    userId, operationId, previousOperationId);
            return;
        }
        
        // 2. 恢复之前的记录
        int restoredCount = 0;
        for (ProjectLog log : logsToRestore) {
            // 根据project_id删除当前版本
            projectMapper.deleteByProjectIdAndOperationId(log.getProjectId(), operationId);
            
            // 使用日志中的状态恢复项目
            Project restoredProject = log.toProject(userId, log.getOperationId());
            projectMapper.insert(restoredProject);
            restoredCount++;
        }
        
        // 3. 删除相关的日志记录（撤回后不可再撤回）
        if (isBatchOperation) {
            // 批量操作：删除batch_operation_id = operationId的记录
            projectLogMapper.deleteByBatchOperationId(operationId);
        } else {
            // 单个操作：删除operation_id = previousOperationId的记录
            projectLogMapper.deleteByOperationId(previousOperationId);
        }
        
        // 4. 注意：撤回操作本身不创建新的操作记录
        // 这样设计实现了"只能撤回一次"的功能
        
        log.info("撤回操作完成（只能撤回一次）: userId={}, operationId={}, previousOperationId={}, isBatchOperation={}, restoredCount={}", 
                userId, operationId, previousOperationId, isBatchOperation, restoredCount);
    }
}