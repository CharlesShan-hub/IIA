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

    private Project validatedFindProjectById(Long userId, Long projectId) {
        Project project = projectMapper.findById(projectId);
        if (project == null) {
            throw new ProjectNotFoundException(projectId);
        }
        if (!project.getUserId().equals(userId)) {
            throw new PermissionDeniedException(userId, projectId);
        }
        return project;
    }
    
    @Override
    public void create(Long userId, CreateProjectRequest dto) {
        Project project = convertToEntity(dto);
        project.setUserId(userId);
        project.setSortOrder(projectMapper.findActiveByUserId(userId).size() + 1);
        project.setIsArchived(false);
        projectMapper.insert(project);
        log.info("User {} create project {} successfully", userId, project.getName());
    }

    @Override
    public void update(Long userId, UpdateProjectRequest dto) {
        Project project = validatedFindProjectById(userId, dto.getProjectId());
        if (dto.getName() != null) project.setName(dto.getName());
        if (dto.getDescription() != null) project.setDescription(dto.getDescription());
        if (dto.getColor() != null) project.setColor(dto.getColor());
        if (dto.getIcon() != null) project.setIcon(dto.getIcon());
        projectMapper.update(project);
        log.info("User {} update project {} successfully", userId, project.getProjectId());
    }
        
    @Override
    public List<Project> getAllArchived(Long userId) {
        List<Project> projects = projectMapper.findArchivedByUserId(userId);
        log.info("User {} get all archived projects successfully", userId);
        return projects;
    }

    @Override
    public List<Project> getAllActive(Long userId) {
        List<Project> projects = projectMapper.findActiveByUserId(userId);
        log.info("User {} get all active projects successfully", userId);
        return projects;
    }

    @Transactional
    @Override
    public void batchUpdatePosition(Long userId, BatchUpdatePositionRequest request) {
        // Validate each project belongs to the user
        // Must validate all projects before updating positions
        for (BatchUpdatePositionRequest.ProjectPosition position : request.getProjects()) {
            validatedFindProjectById(userId, position.getProjectId());
        }
        
        // Batch update positions
        for (BatchUpdatePositionRequest.ProjectPosition position : request.getProjects()) {
            Project project = new Project();
            project.setProjectId(position.getProjectId());
            project.setSortOrder(position.getSortOrder());
            projectMapper.updateSortOrder(project);
        }
        
        log.info("User {} batch update project positions successfully, updated projects: {}", 
                 userId, request.getProjects());
    }
}