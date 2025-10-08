package com.charles.server.reminder.service.impl;

import java.util.List;

import com.charles.server.reminder.dto.CreateProjectRequest;
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
    public void create(Long userId, CreateProjectRequest dto) {
        if (this.existsByName(userId, dto.getName())) {
            throw new RuntimeException("该项目名称已存在");
        }
        Project project = new Project(dto);
        project.setUserId(userId);
        project.setSortOrder(projectMapper.findActiveByUserId(userId).size() + 1);
        project.setIsArchived(false);
        projectMapper.insert(project);
        log.info("用户创建项目成功, 用户ID: {}, 项目名称: {}", project.getUserId(), project.getName());
    }
    
    @Override
    public List<Project> getAll(Long userId) {
        List<Project> projects = projectMapper.findByUserId(userId);
        log.info("用户获取项目列表成功, 用户ID: {}", userId);
        return projects;
    }
    
    @Override
    public Project getProjectById(Long userId, Long projectId) {
        Project project = projectMapper.findById(projectId);
        if (project == null || !project.getUserId().equals(userId)) {
            throw new RuntimeException("项目不存在或无权限访问");
        }
        log.info("用户获取项目成功, 用户ID: {}, 项目ID: {}", userId, projectId);
        return project;
    }

    @Override
    public boolean existsByName(Long userId, String name) {
        return projectMapper.findByName(userId, name) != null;
    }
    
    @Override
    public Project updateProject(Project project) {
        Project existingProject = projectMapper.findById(project.getProjectId());
        if (existingProject == null || !existingProject.getUserId().equals(project.getUserId())) {
            throw new RuntimeException("项目不存在或无权限访问");
        }
        projectMapper.update(project);
        log.info("用户更新项目成功, 用户ID: {}, 项目ID: {}", project.getUserId(), project.getProjectId());
        return project;
    }
}