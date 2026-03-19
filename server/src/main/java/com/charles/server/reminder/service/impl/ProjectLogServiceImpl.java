package com.charles.server.reminder.service.impl;

import com.charles.server.reminder.entity.Project;
import com.charles.server.reminder.entity.ProjectLog;
import com.charles.server.reminder.mapper.ProjectLogMapper;
import com.charles.server.reminder.mapper.ProjectMapper;
import com.charles.server.reminder.service.PermissionService;
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
    private final PermissionService permissionService;
    
    @Override
    public void save(Project project) {
        ProjectLog projectLog = ProjectLog.fromProject(project);
        projectLogMapper.insert(projectLog);
        log.debug("Project log saved: projectId={}, operationId={}", 
                project.getProjectId(), project.getOperationId());
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
    @Transactional
    public void revert(Long userId, Long operationId, Long previousOperationId) {
        // 1. 删除当前版本新纪录
        projectMapper.deleteByOperationId(operationId);
        
        // 2. 得到之前的记录
        List<ProjectLog> previousProjects = projectLogMapper.findByOperationId(previousOperationId);
        
        // 3. 恢复之前的记录
        for (ProjectLog previousProject : previousProjects) {
            Project restoredProject = previousProject.toProject(userId, previousOperationId);
            projectMapper.insert(restoredProject);
        }
        
        // 4. 删除log
        projectLogMapper.deleteByOperationId(previousOperationId);
        
        log.info("撤回项目操作完成: userId={}, operationId={}, previousOperationId={}, restoredCount={}", 
                userId, operationId, previousOperationId, previousProjects.size());
    }
}