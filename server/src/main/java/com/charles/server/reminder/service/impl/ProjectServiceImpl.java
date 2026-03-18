package com.charles.server.reminder.service.impl;

import java.util.List;
import java.util.ArrayList;
import java.util.Comparator;

import com.charles.server.reminder.dto.ProjectCreateRequest;
import com.charles.server.reminder.dto.ProjectUpdateRequest;
import com.charles.server.reminder.dto.ProjectGetAllRequest;
import com.charles.server.reminder.dto.ProjectDeleteRequest;
import com.charles.server.reminder.dto.BatchUpdatePositionRequest;
import com.charles.server.reminder.exception.ProjectException;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.stereotype.Service;
import com.charles.server.reminder.entity.Project;
import com.charles.server.reminder.entity.Operation;
import com.charles.server.reminder.mapper.ProjectMapper;
import com.charles.server.reminder.service.PermissionService;
import com.charles.server.reminder.service.TaskService;
import com.charles.server.reminder.service.ProjectService;
import com.charles.server.reminder.service.OperationService;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;

@Slf4j
@Service
@RequiredArgsConstructor
public class ProjectServiceImpl implements ProjectService {
    
    private final ProjectMapper projectMapper;
    private final TaskService taskService;
    private final PermissionService permissionService;
    private final OperationService operationService;

    private Project convertToEntity(ProjectCreateRequest dto) {
        Project project = new Project();
        project.setName(dto.getName());
        project.setDescription(dto.getDescription());
        project.setColor(dto.getColor());
        project.setIcon(dto.getIcon());
        return project;
    }

    private int getNextSortOrder(Long userId, boolean archived) {
        return projectMapper.findMaxSortOrderByUserIdAndArchived(userId, archived) + 1;
    }
    
    @Override
    @Transactional
    public void create(Long userId, ProjectCreateRequest dto) {
        Project existed = projectMapper.findByUserIdAndName(userId, dto.getName());
        if (existed != null) {
            throw ProjectException.nameAlreadyExists(userId, dto.getName());
        }
        
        // 生成操作ID
        Long operationId = operationService.getId(userId);
        
        // 创建操作记录
        operationService.create(Operation.builder()
                .operationId(operationId)
                .userId(userId)
                .isReminderProject(true)
                .build());
        
        // 创建项目
        Project project = convertToEntity(dto);
        project.setUserId(userId);
        project.setSortOrder(getNextSortOrder(userId, false));
        project.setIsArchived(false);
        project.setOperationId(operationId);
        
        projectMapper.insert(project);
        
        log.info("创建项目: userId={}, projectId={}, operationId={}", userId, project.getProjectId(), operationId);
    }

    @Override
    public void update(Long userId, ProjectUpdateRequest dto) {
        Project project = permissionService.getProject(userId, dto.getProjectId());
        if (dto.getName() != null) project.setName(dto.getName());
        if (dto.getDescription() != null) project.setDescription(dto.getDescription());
        if (dto.getColor() != null) project.setColor(dto.getColor());
        if (dto.getIcon() != null) project.setIcon(dto.getIcon());
        if (dto.getIsArchived() != null && !dto.getIsArchived().equals(project.getIsArchived())) {
            boolean archived = dto.getIsArchived();
            project.setIsArchived(archived);
            project.setSortOrder(getNextSortOrder(userId, archived));
        }
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
        request.getPos().forEach(p -> permissionService.validProject(userId, p.getItemId()));

        List<BatchUpdatePositionRequest.Position> sorted = new ArrayList<>(request.getPos());
        sorted.sort(Comparator.comparing(BatchUpdatePositionRequest.Position::getSortOrder)
                .thenComparing(BatchUpdatePositionRequest.Position::getItemId));

        int next = 1;
        for (BatchUpdatePositionRequest.Position p : sorted) {
            Project project = new Project();
            project.setProjectId(p.getItemId());
            project.setSortOrder(next++);
            projectMapper.updateSortOrder(project);
        }
    }

    @Override
    @Transactional
    public void delete(Long userId, ProjectDeleteRequest dto) {
        Long projectId = dto.getProjectId();
        permissionService.validProject(userId, projectId);
        if (Boolean.FALSE.equals(dto.getKeepTasks())) {
            taskService.deleteByProjectId(userId, projectId);
        } else {
            if(Boolean.TRUE.equals(dto.getTargetProject())){
                permissionService.validProject(userId, dto.getTargetProjectId());
            }
            taskService.batchUpdateProjectId(userId, dto);
        }
        projectMapper.deleteById(projectId);
    }
}
