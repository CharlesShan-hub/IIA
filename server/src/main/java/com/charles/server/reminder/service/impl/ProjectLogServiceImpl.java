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
        // 1. 先尝试根据batch_operation_id查找（批量操作）
        List<ProjectLog> logsToRestore = projectLogMapper.findByBatchOperationId(operationId);
        
        boolean isBatchOperation = !logsToRestore.isEmpty();
        
        // 2. 如果不是批量操作，处理单个操作
        if (!isBatchOperation) {
            // 查找当前操作ID下的所有项目
            List<Project> currentProjects = projectMapper.findByOperationId(operationId);
            
            if (currentProjects.isEmpty()) {
                log.warn("没有找到需要撤回的项目: userId={}, operationId={}, previousOperationId={}", 
                        userId, operationId, previousOperationId);
                return;
            }
            
            int deletedCount = 0;
            int restoredCount = 0;
            
            for (Project currentProject : currentProjects) {
                Long projectId = currentProject.getProjectId();
                
                // 检查在previousOperationId下是否有该项目的日志记录
                ProjectLog previousLog = projectLogMapper.findByProjectIdAndOperationId(projectId, previousOperationId);
                
                if (previousLog == null) {
                    // 新增操作：删除该项目
                    projectMapper.deleteByProjectIdAndOperationId(projectId, operationId);
                    deletedCount++;
                } else {
                    // 更新操作：恢复之前的版本
                    // 删除当前版本
                    projectMapper.deleteByProjectIdAndOperationId(projectId, operationId);
                    
                    // 使用日志中的状态恢复项目
                    Project restoredProject = previousLog.toProject(userId, previousOperationId);
                    projectMapper.insert(restoredProject);
                    restoredCount++;
                }
            }
            
            // 删除相关的日志记录（撤回后不可再撤回）
            projectLogMapper.deleteByOperationId(operationId);
            
            log.info("撤回单个操作完成: userId={}, operationId={}, previousOperationId={}, deletedCount={}, restoredCount={}", 
                    userId, operationId, previousOperationId, deletedCount, restoredCount);
            return;
        }
        
        // 3. 处理批量操作
        if (logsToRestore.isEmpty()) {
            log.warn("没有找到可恢复的批量操作日志记录: userId={}, operationId={}, previousOperationId={}", 
                    userId, operationId, previousOperationId);
            return;
        }
        
        // 恢复之前的记录
        int restoredCount = 0;
        for (ProjectLog log : logsToRestore) {
            // 根据project_id删除当前版本
            projectMapper.deleteByProjectIdAndOperationId(log.getProjectId(), operationId);
            
            // 使用日志中的状态恢复项目
            Project restoredProject = log.toProject(userId, log.getOperationId());
            projectMapper.insert(restoredProject);
            restoredCount++;
        }
        
        // 删除相关的日志记录（撤回后不可再撤回）
        projectLogMapper.deleteByBatchOperationId(operationId);
        
        log.info("撤回批量操作完成: userId={}, operationId={}, previousOperationId={}, restoredCount={}", 
                userId, operationId, previousOperationId, restoredCount);
    }
}