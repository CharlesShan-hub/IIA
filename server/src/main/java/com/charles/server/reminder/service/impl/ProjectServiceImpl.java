package com.charles.server.reminder.service.impl;

import java.util.List;
import org.springframework.stereotype.Service;
import com.charles.server.reminder.entity.Project;
import com.charles.server.reminder.mapper.ProjectMapper;
import com.charles.server.reminder.service.ProjectService;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;

@Slf4j
@Service
@RequiredArgsConstructor
public class ProjectServiceImpl implements ProjectService {
    
    private final ProjectMapper projectMapper;
    
    @Override
    public Project createProject(Project project, Long userId) {
        project.setUserId(userId);
        projectMapper.insert(project);
        log.info("用户创建项目成功, 用户ID: {}, 项目名称: {}", userId, project.getName());
        return project;
    }
    
    @Override
    public List<Project> getUserProjects(Long userId) {
        List<Project> projects = projectMapper.findByUserId(userId);
        log.info("用户获取项目列表成功, 用户ID: {}", userId);
        return projects;
    }
    
    @Override
    public Project getProjectById(Long projectId, Long userId) {
        Project project = projectMapper.findById(projectId);
        if (project == null || !project.getUserId().equals(userId)) {
            throw new RuntimeException("项目不存在或无权限访问");
        }
        log.info("用户获取项目成功, 用户ID: {}, 项目ID: {}", userId, projectId);
        return project;
    }
    
    @Override
    public Project updateProject(Project project, Long projectId, Long userId) {
        Project existingProject = projectMapper.findById(projectId);
        if (existingProject == null || !existingProject.getUserId().equals(userId)) {
            throw new RuntimeException("项目不存在或无权限访问");
        }
        
        project.setProjectId(projectId);
        project.setUserId(userId);
        projectMapper.update(project);
        log.info("用户更新项目成功, 用户ID: {}, 项目ID: {}", userId, projectId);
        return project;
    }
}