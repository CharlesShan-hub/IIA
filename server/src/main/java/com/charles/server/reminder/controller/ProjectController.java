package com.charles.server.reminder.controller;

import java.util.List;
import java.util.Map;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.web.bind.annotation.*;

import com.charles.server.auth.service.TokenService;
import com.charles.server.reminder.service.ProjectService;
import com.charles.server.reminder.entity.Project;
import com.charles.server.reminder.dto.*;
import com.charles.server.utils.ResponseUtils;

@Slf4j
@RestController
@RequestMapping("/api/reminder/project")
@RequiredArgsConstructor
public class ProjectController {
    
    private final ProjectService projectService;
    private final TokenService tokenService;
    
    // Create Project
    @PostMapping("create")
    public Map<String, Object> create(@RequestBody @Valid ProjectCreateRequest dto, HttpServletRequest request) {
        Long userId = tokenService.getUserIdFromRequest(request);
        projectService.create(userId, dto);
        log.info("User {} create project {} successfully", userId, dto.getName());
        return ResponseUtils.buildEmptySuccessResponse("Reminder Project Created");
    }

    // Delete Project
    @PostMapping("delete")
    public Map<String, Object> delete(@RequestBody @Valid ProjectDeleteRequest dto, HttpServletRequest request) {
        Long userId = tokenService.getUserIdFromRequest(request);
        projectService.delete(userId, dto);
        log.info("User {} delete project {} successfully, keepTasks: {}, targetProjectId: {}", 
                 userId, dto.getProjectId(), dto.getKeepTasks(), dto.getTargetProjectId());
        return ResponseUtils.buildEmptySuccessResponse("Reminder Project Deleted");
    }

    // Update Project
    @PostMapping("update")
    public Map<String, Object> updateById(@RequestBody @Valid ProjectUpdateRequest dto, HttpServletRequest request) {
        Long userId = tokenService.getUserIdFromRequest(request);
        projectService.update(userId, dto);
        log.info("User {} update project {} successfully", userId, dto.getProjectId());
        return ResponseUtils.buildEmptySuccessResponse("Reminder Project Updated");
    }

    // Batch Update Project Positions
    @PostMapping("batch-update-position")
    public Map<String, Object> batchUpdatePosition(@RequestBody @Valid BatchUpdatePositionRequest dto, HttpServletRequest httpRequest) {
        Long userId = tokenService.getUserIdFromRequest(httpRequest);
        projectService.batchUpdatePosition(userId, dto);
        log.info("User {} batch update project positions successfully, updated projects: {}", 
                 userId, dto.getPos());
        return ResponseUtils.buildEmptySuccessResponse("Reminder Project Positions Updated");
    }

    // Query projects by archived flag and isAll flag
    @GetMapping("get-all")
    public Map<String, Object> getAll(@RequestBody @Valid ProjectGetAllRequest dto, HttpServletRequest request) {
        Long userId = tokenService.getUserIdFromRequest(request);
        List<Project> projects = projectService.getAll(userId, dto);
        log.info("User {} query projects successfully, archived: {}, isAll: {}", userId, dto.getArchived(), dto.getIsAll());
        return ResponseUtils.buildSuccessResponse(projects, "Reminder Projects Queried");
    }
}
