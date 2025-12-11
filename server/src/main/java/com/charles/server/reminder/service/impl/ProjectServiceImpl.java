package com.charles.server.reminder.service.impl;

import java.util.List;

import com.charles.server.reminder.dto.CreateProjectRequest;
import com.charles.server.reminder.dto.UpdateProjectRequest;
import com.charles.server.reminder.dto.BatchUpdatePositionRequest;
import com.charles.server.reminder.exception.PermissionDeniedException;
import com.charles.server.reminder.exception.ProjectNotFoundException;
import jakarta.transaction.Transactional;
import org.springframework.stereotype.Service;
import com.charles.server.reminder.entity.Project;
import com.charles.server.reminder.mapper.ProjectMapper;
import com.charles.server.reminder.service.ProjectService;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import java.util.Optional;

@Slf4j
@Service
@RequiredArgsConstructor
public class ProjectServiceImpl implements ProjectService {
    
    private final ProjectMapper projectMapper;

    private Project convertToEntity(CreateProjectRequest dto) {
        Project project = new Project();
        project.setName(dto.getName());
        project.setDescription(dto.getDescription());
        project.setColor(dto.getColor());
        project.setIcon(dto.getIcon());
        return project;
    }
    
    @Override
    public void create(Long userId, CreateProjectRequest dto) {
        if (this.existsByName(userId, dto.getName())) {
            throw new RuntimeException("Project name already exists");
        }
        Project project = convertToEntity(dto);
        project.setUserId(userId);
        project.setSortOrder(projectMapper.findActiveByUserId(userId).size() + 1);
        project.setIsArchived(false);
        projectMapper.insert(project);
        log.info("User {} create project {} successfully", userId, project.getName());
    }

    @Override
    public void update(Long userId, UpdateProjectRequest dto) {
        Project project = projectMapper.findById(dto.getProjectId());
        if (project == null) {
            throw new ProjectNotFoundException(dto.getProjectId());
        }
        if (!project.getUserId().equals(userId)) {
            throw new PermissionDeniedException(userId, project.getProjectId());
        }
        if (dto.getName() != null) project.setName(dto.getName());
        if (dto.getDescription() != null) project.setDescription(dto.getDescription());
        if (dto.getColor() != null) project.setColor(dto.getColor());
        if (dto.getIcon() != null) project.setIcon(dto.getIcon());
        projectMapper.update(project);
        log.info("User {} update project {} successfully", userId, project.getProjectId());
    }

    @Override
    public void updateSortOrder(Long userId, Long projectId, Integer sortOrder) {
        Project project = projectMapper.findById(projectId);
        if (project == null) {
            throw new ProjectNotFoundException(projectId);
        }
        if (!project.getUserId().equals(userId)) {
            throw new PermissionDeniedException(userId, projectId);
        }
        project.setSortOrder(sortOrder);
        projectMapper.update(project);
        log.info("User {} update project {} sort order to {}", userId, projectId, sortOrder);
    }
        
    @Override
    public List<Project> getAll(Long userId) {
        List<Project> projects = projectMapper.findByUserId(userId);
        log.info("User {} get all projects successfully", userId);
        return projects;
    }
    
    @Override
    public Project getProjectById(Long userId, Long projectId) {
        return Optional.ofNullable(projectMapper.findById(projectId))
                .filter(project -> project.getUserId().equals(userId))
                .orElseThrow(() -> new RuntimeException("项目不存在或无权限访问"));
    }

    @Override
    public Project getProjectByName(Long userId, String name) {
        Project project = projectMapper.findByName(userId, name);
        if (project == null) {
            throw new RuntimeException("项目不存在");
        }
        log.info("用户获取项目成功, 用户ID: {}, 项目名称: {}", userId, name);
        return project;
    }

    @Override
    public Project getProjectBySortOrder(Long userId, Integer sortOrder) {
        Project project = projectMapper.findBySortOrder(userId, sortOrder);
        if (project == null) {
            throw new RuntimeException("项目不存在");
        }
        log.info("用户获取项目成功, 用户ID: {}, 项目排序: {}", userId, sortOrder);
        return project;
    }

    @Override
    public boolean existsByName(Long userId, String name) {
        return projectMapper.findByName(userId, name) != null;
    }

    @Override
    public boolean existsBySortOrder(Long userId, Integer sortOrder) {
        return projectMapper.findBySortOrder(userId, sortOrder) != null;
    }

    @Transactional // 添加事务注解，确保操作的原子性
    @Override
    public void batchUpdatePosition(Long userId, BatchUpdatePositionRequest request) {
        // 验证每个项目是否属于当前用户
        for (BatchUpdatePositionRequest.ProjectPosition position : request.getProjects()) {
            Project project = projectMapper.findById(position.getProjectId());
            if (project == null || !project.getUserId().equals(userId)) {
                throw new RuntimeException("项目不存在或无权限访问");
            }
        }
        
        // 批量更新所有项目的位置
        for (BatchUpdatePositionRequest.ProjectPosition position : request.getProjects()) {
            Project project = new Project();
            project.setProjectId(position.getProjectId());
            project.setSortOrder(position.getSortOrder());
            projectMapper.updateSortOrder(project);
        }
        
        log.info("用户批量更新项目位置成功, 用户ID: {}, 更新项目数量: {}", 
                 userId, request.getProjects().size());
    }
}