package com.charles.server.reminder.service.impl;

import java.util.List;
import java.util.ArrayList;
import java.util.Comparator;

import com.charles.server.reminder.dto.ProjectCreateDTO;
import com.charles.server.reminder.dto.ProjectUpdateDTO;
import com.charles.server.reminder.dto.ProjectGetDTO;
import com.charles.server.reminder.dto.ProjectDeleteDTO;
import com.charles.server.reminder.dto.BatchUpdatePositionDTO;
import com.charles.server.reminder.exception.ProjectException;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.stereotype.Service;
import com.charles.server.reminder.entity.Project;
import com.charles.server.reminder.entity.Operation;
import com.charles.server.reminder.entity.Position;
import com.charles.server.reminder.mapper.ProjectMapper;
import com.charles.server.reminder.service.ProjectLogService;
import com.charles.server.reminder.service.PermissionService;
import com.charles.server.reminder.service.OperationService;
import com.charles.server.reminder.service.TaskService;
import com.charles.server.reminder.service.ProjectService;
import com.charles.server.config.ColorConfig;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;

@Slf4j
@Service
@RequiredArgsConstructor
public class ProjectServiceImpl implements ProjectService {
    
    private final ProjectMapper projectMapper;
    private final ProjectLogService projectLogService;
    private final TaskService taskService;
    private final PermissionService permissionService;
    private final OperationService operationService;
    private final ColorConfig colorConfig;

    private int getNextSortOrder(Long userId, boolean archived) {
        return projectMapper.findMaxSortOrderByUserIdAndArchived(userId, archived) + 1;
    }
    
    @Override
    @Transactional
    public Project create(Long userId, ProjectCreateDTO dto) {
        // 1.Check if project name already exists
        if (projectMapper.findByUserIdAndName(userId, dto.getName()) != null) {
            throw ProjectException.nameAlreadyExists(userId, dto.getName());
        }
        
        // 2.Record operation
        Long operationId = operationService.create(Operation.builder()
                .userId(userId)
                .isReminderProject(true)
                .build());
        
        // 3.Create project with color processing
        Project project = Project.builder()
                .userId(userId)
                .name(dto.getName())
                .description(dto.getDescription())
                .color(colorConfig.getProjectColor(dto.getColor()))
                .icon(dto.getIcon())
                .sortOrder(getNextSortOrder(userId, false))
                .isArchived(false)
                .operationId(operationId)
                .build();
        projectMapper.insert(project);
        
        log.info("Create project: userId={}, projectId={}, operationId={}", userId, project.getProjectId(), operationId);
        return project;
    }

    @Override
    @Transactional
    public Project update(Long userId, ProjectUpdateDTO dto) {
        // 1. Get project by ID
        Project project = permissionService.getProject(userId, dto.getProjectId());

        // 2. Record operation (operationId will be auto-generated)
        Long operationId = operationService.create(Operation.builder()
                .userId(userId)
                .isReminderProject(true)
                .build());
        
        // 3. Save the previous version to history table
        projectLogService.save(project, operationId);
        
        // 4. Apply changes to current project
        project.setOperationId(operationId);
        if (dto.getName() != null) project.setName(dto.getName());
        if (dto.getDescription() != null) project.setDescription(dto.getDescription());
        if (dto.getColor() != null) project.setColor(dto.getColor());
        if (dto.getIcon() != null) project.setIcon(dto.getIcon());
        
        // 5. Update main table
        projectMapper.update(project);
        
        log.info("Update project: userId={}, projectId={}, operationId={}", 
                userId, project.getProjectId(), operationId);
        return project;
    }

    @Override
    @Transactional
    public Project archive(Long userId, ProjectUpdateDTO dto) {
        // 1. Get project by ID
        Project project = permissionService.getProject(userId, dto.getProjectId());
        
        // 2. Check if already in target state
        if (dto.getIsArchived().equals(project.getIsArchived()))
            return project; // already archived
        Boolean archive = dto.getIsArchived();

        // 3. Record operation (operationId will be auto-generated)
        Long operationId = operationService.create(Operation.builder()
                .userId(userId)
                .isReminderProject(true)
                .isReminderTask(true)
                .build());
        
        // 4. Save the previous version to history table
        projectLogService.save(project, operationId);
        
        // 5. Apply changes to current project
        project.setOperationId(operationId);
        project.setIsArchived(archive);
        project.setSortOrder(getNextSortOrder(userId, archive));
        
        // 6. Apply basic info from DTO (if any)
        if (dto.getName() != null) project.setName(dto.getName());
        if (dto.getDescription() != null) project.setDescription(dto.getDescription());
        if (dto.getColor() != null) project.setColor(dto.getColor());
        if (dto.getIcon() != null) project.setIcon(dto.getIcon());
        
        // 7. Update project
        projectMapper.update(project);

        // 8. Update tasks status based on archive flag
        if (archive) {
            taskService.archiveByProjectId(userId, project.getProjectId(), operationId);
        } else {
            //taskService.unarchiveByProjectId(userId, project.getProjectId(), operationId);
        }
        
        log.info("Set project archive status: userId={}, projectId={}, archive={}, operationId={}", 
                userId, project.getProjectId(), archive, operationId);
        return project;
    }
    
    @Override
    public List<Project> get(Long userId, ProjectGetDTO dto) {
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
    public void batchUpdatePosition(Long userId, BatchUpdatePositionDTO request) {
        Long operationId = operationService.getId(userId);
        operationService.create(Operation.builder()
                .operationId(operationId)
                .userId(userId)
                .isReminderProject(true)
                .build());

        List<Position> sorted = new ArrayList<>(request.getPos());
        sorted.sort(Comparator.comparing(Position::getSortOrder)
                .thenComparing(Position::getItemId));

        int next = 1;
        for (Position p : sorted) {
            Project project = permissionService.getProject(userId, p.getItemId());
            projectLogService.save(project, operationId);
            project.setSortOrder(next++);
            project.setOperationId(operationId);
            projectMapper.update(project);
        }

        log.info("Update Project Position: userId={}, operationId={}, count={}", userId, operationId, sorted.size());
    }

    @Override
    @Transactional
    public void delete(Long userId, ProjectDeleteDTO dto) {
        // 1. Get project by ID (verify permission)
        Long projectId = dto.getProjectId();
        Project currentProject = permissionService.getProject(userId, projectId);
        
        // 2. Record delete operation (operationId will be auto-generated)
        Long operationId = operationService.create(Operation.builder()
                .userId(userId)
                .isReminderTask(true)
                .isReminderProject(true)
                .build());
        
        // 3. Save the current version to history table (for recovery if needed)
        projectLogService.save(currentProject, operationId);
        
        // 4. Handle tasks (based on keepTasks)
        // TODO: Whether to record operation when handling tasks?
        if (Boolean.FALSE.equals(dto.getKeepTasks())) {
            taskService.deleteByProjectId(userId, projectId, operationId);
        } else {
            if(Boolean.TRUE.equals(dto.getTargetProject())){
                permissionService.validProject(userId, dto.getTargetProjectId());
            }
            taskService.batchUpdateProjectId(userId, dto, operationId);
        }
        
        // 5. Delete project from main table
        projectMapper.deleteById(projectId);
        
        log.info("Delete project: userId={}, projectId={}, operationId={}, keepTasks={}", 
                userId, projectId, operationId, dto.getKeepTasks());
    }
}
