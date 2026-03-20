package com.charles.server.reminder.service.impl;

import java.util.List;
import java.util.ArrayList;
import java.util.Comparator;

import com.charles.server.reminder.dto.ProjectCreateDTO;
import com.charles.server.reminder.dto.ProjectUpdateDTO;
import com.charles.server.reminder.dto.ProjectGetAllDTO;
import com.charles.server.reminder.dto.ProjectDeleteDTO;
import com.charles.server.reminder.dto.BatchUpdatePositionDTO;
import com.charles.server.reminder.exception.ProjectException;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.stereotype.Service;
import com.charles.server.reminder.entity.Project;
import com.charles.server.reminder.entity.Operation;
import com.charles.server.reminder.mapper.ProjectMapper;
import com.charles.server.reminder.service.ProjectLogService;
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
    private final ProjectLogService projectLogService;
    private final TaskService taskService;
    private final PermissionService permissionService;
    private final OperationService operationService;

    private Project convertToEntity(ProjectCreateDTO dto) {
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
    public void create(Long userId, ProjectCreateDTO dto) {
        // Check if project name already exists
        Project existed = projectMapper.findByUserIdAndName(userId, dto.getName());
        if (existed != null) {
            throw ProjectException.nameAlreadyExists(userId, dto.getName());
        }
        
        // Get operation ID
        Long operationId = operationService.getId(userId);
        
        // Record operation
        operationService.create(Operation.builder()
                .operationId(operationId)
                .userId(userId)
                .isReminderProject(true)
                .build());
        
        // Create project
        Project project = convertToEntity(dto);
        project.setUserId(userId);
        project.setSortOrder(getNextSortOrder(userId, false));
        project.setIsArchived(false);
        project.setOperationId(operationId);
        projectMapper.insert(project);
        
        log.info("创建项目: userId={}, projectId={}, operationId={}", userId, project.getProjectId(), operationId);
    }

    @Override
    @Transactional
    public void update(Long userId, ProjectUpdateDTO dto) {
        // 1. 获取当前项目
        Project currentProject = permissionService.getProject(userId, dto.getProjectId());

        // 2. 保存修改前的版本到历史表
        projectLogService.save(currentProject);
        
        // 3. 生成新的操作ID
        Long newOperationId = operationService.getId(userId);
        
        // 4. 记录操作
        Operation operation = Operation.builder()
                .operationId(newOperationId)
                .userId(userId)
                .isReminderProject(true)
                .build();
        operationService.create(operation);
        
        // 5. 应用修改到当前项目
        currentProject.setOperationId(newOperationId);
        if (dto.getName() != null) currentProject.setName(dto.getName());
        if (dto.getDescription() != null) currentProject.setDescription(dto.getDescription());
        if (dto.getColor() != null) currentProject.setColor(dto.getColor());
        if (dto.getIcon() != null) currentProject.setIcon(dto.getIcon());
        if (dto.getIsArchived() != null && !dto.getIsArchived().equals(currentProject.getIsArchived())) {
            boolean archived = dto.getIsArchived();
            currentProject.setIsArchived(archived);
            currentProject.setSortOrder(getNextSortOrder(userId, archived));
        }
        
        // 6. 更新主表
        projectMapper.update(currentProject);
        
        log.info("更新项目: userId={}, projectId={}, oldOperationId={}, newOperationId={}", 
                userId, currentProject.getProjectId(), currentProject.getOperationId(), newOperationId);
    }
    
    @Override
    public List<Project> getAll(Long userId, ProjectGetAllDTO dto) {
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

        List<BatchUpdatePositionDTO.Position> sorted = new ArrayList<>(request.getPos());
        sorted.sort(Comparator.comparing(BatchUpdatePositionDTO.Position::getSortOrder)
                .thenComparing(BatchUpdatePositionDTO.Position::getItemId));

        int next = 1;
        for (BatchUpdatePositionDTO.Position p : sorted) {
            Project project = permissionService.getProject(userId, p.getItemId());

            // 保存历史版本，记录这个日志是由哪个批量操作创建的
            projectLogService.save(project, operationId);

            project.setSortOrder(next++);
            project.setOperationId(operationId);
            projectMapper.update(project);
        }

        log.info("批量更新项目位置: userId={}, operationId={}, count={}", userId, operationId, sorted.size());
    }

    @Override
    @Transactional
    public void delete(Long userId, ProjectDeleteDTO dto) {
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
