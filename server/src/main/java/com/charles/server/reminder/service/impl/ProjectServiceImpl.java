package com.charles.server.reminder.service.impl;

import java.util.List;

import com.charles.server.reminder.dto.ProjectCreateRequest;
import com.charles.server.reminder.dto.ProjectUpdateRequest;
import com.charles.server.reminder.dto.ProjectGetAllRequest;
import com.charles.server.reminder.dto.ProjectDeleteRequest;
import com.charles.server.reminder.dto.BatchUpdatePositionRequest;
import com.charles.server.reminder.exception.ProjectAccessException;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.stereotype.Service;
import com.charles.server.reminder.entity.Project;
import com.charles.server.reminder.mapper.ProjectMapper;

import com.charles.server.reminder.service.TaskService;
import com.charles.server.reminder.service.ProjectService;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;

@Slf4j
@Service
@RequiredArgsConstructor
public class ProjectServiceImpl implements ProjectService {
    
    private final ProjectMapper projectMapper;
    private final TaskService taskService;

    private Project convertToEntity(ProjectCreateRequest dto) {
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
            throw ProjectAccessException.notFound(projectId);
        }
        if (!project.getUserId().equals(userId)) {
            throw ProjectAccessException.permissionDenied(userId, projectId);
        }
        return project;
    }
    
    @Override
    public void create(Long userId, ProjectCreateRequest dto) {
        Project project = convertToEntity(dto);
        project.setUserId(userId);
        project.setSortOrder(projectMapper.findByUserIdAndArchived(userId, false).size() + 1);
        project.setIsArchived(false);
        projectMapper.insert(project);
    }

    @Override
    public void update(Long userId, ProjectUpdateRequest dto) {
        Project project = validatedFindProjectById(userId, dto.getProjectId());
        if (dto.getName() != null) project.setName(dto.getName());
        if (dto.getDescription() != null) project.setDescription(dto.getDescription());
        if (dto.getColor() != null) project.setColor(dto.getColor());
        if (dto.getIcon() != null) project.setIcon(dto.getIcon());
        projectMapper.update(project);
    }
    
    @Override
    public List<Project> getAll(Long userId, ProjectGetAllRequest dto) {
        if (Boolean.TRUE.equals(dto.getIsAll())) {
            List<Project> activeList = projectMapper.findByUserIdAndArchived(userId, false);
            List<Project> archivedList = projectMapper.findByUserIdAndArchived(userId, true);
            List<Project> all = new java.util.ArrayList<>(activeList);
            all.addAll(archivedList);
            return all;
        }
        if (Boolean.TRUE.equals(dto.getArchived())) {
            return projectMapper.findByUserIdAndArchived(userId, true);
        }
        return projectMapper.findByUserIdAndArchived(userId, false);
    }
    
    @Transactional
    @Override
    public void batchUpdatePosition(Long userId, BatchUpdatePositionRequest request) {
        // Validate each project belongs to the user
        // Must validate all projects before updating positions
        request.getPos().forEach(p -> validatedFindProjectById(userId, p.getItemId()));
        
        // Batch update positions
        request.getPos().forEach(p -> {
            Project project = new Project();
            project.setProjectId(p.getItemId());
            project.setSortOrder(p.getSortOrder());
            projectMapper.updateSortOrder(project);
        });
    }

    @Override
    @Transactional
    public void delete(Long userId, ProjectDeleteRequest dto) {
        Long projectId = dto.getProjectId();
        validatedFindProjectById(userId, projectId);
        if (Boolean.FALSE.equals(dto.getKeepTasks())) {
            taskService.deleteByProjectId(userId, projectId);
        } else {
            if(Boolean.TRUE.equals(dto.getTargetProject())){
                validatedFindProjectById(userId, dto.getTargetProjectId());
            }
            taskService.batchUpdateProjectId(userId, dto);
        }
        projectMapper.deleteById(projectId);
    }
}
