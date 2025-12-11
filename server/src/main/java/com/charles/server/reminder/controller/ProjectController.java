package com.charles.server.reminder.controller;

import java.util.List;
import java.util.Map;

import com.charles.server.reminder.dto.*;
import jakarta.validation.Valid;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.charles.server.auth.service.TokenService;
import com.charles.server.reminder.entity.Project;
import com.charles.server.reminder.service.ProjectService;
import com.charles.server.reminder.dto.BatchUpdatePositionRequest;
import com.charles.server.utils.ResponseUtils;

import jakarta.servlet.http.HttpServletRequest;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;

@Slf4j
@RestController
@RequestMapping("/api/reminder/projects")
@RequiredArgsConstructor
public class ProjectController {
    
    private final ProjectService projectService;
    private final TokenService tokenService;
    
    // Create Project
    @PostMapping("create")
    public Map<String, Object> create(@RequestBody @Valid CreateProjectRequest dto, HttpServletRequest request) {
        try {
            Long userId = tokenService.getUserIdFromRequest(request);
            projectService.create(userId, dto);
            return ResponseUtils.buildEmptySuccessResponse("Reminder Project Created");
        } catch (Exception e) {
            log.error("Reminder Project Create Failed: {}", e.getMessage(), e);
            return ResponseUtils.buildErrorResponse(e.getMessage());
        }
    }

    // Update Project
    @PostMapping("update")
    public Map<String, Object> updateById(@RequestBody @Valid UpdateProjectRequest dto, HttpServletRequest request) {
        try {
            Long userId = tokenService.getUserIdFromRequest(request);
            projectService.update(userId, dto);
            return ResponseUtils.buildEmptySuccessResponse("Reminder Project Updated");
        } catch (Exception e) {
            log.error("Reminder Project Update Failed: {}", e.getMessage(), e);
            return ResponseUtils.buildErrorResponse(e.getMessage());
        }
    }

    // Batch Update Project Positions
    @PostMapping("batch-update-position")
    public Map<String, Object> batchUpdatePosition(@RequestBody @Valid BatchUpdatePositionRequest request, HttpServletRequest httpRequest) {
        try {
            Long userId = tokenService.getUserIdFromRequest(httpRequest);
            projectService.batchUpdatePosition(userId, request);
            return ResponseUtils.buildEmptySuccessResponse("Reminder Project Positions Updated");
        } catch (Exception e) {
            log.error("Reminder Project Batch Update Position Failed: {}", e.getMessage(), e);
            return ResponseUtils.buildErrorResponse(e.getMessage());
        }
    }
    
    // Query All Projects for User
    @GetMapping("get-all")
    public Map<String, Object> getAll(HttpServletRequest request) {
        try {
            Long userId = tokenService.getUserIdFromRequest(request);
            List<Project> projects = projectService.getAll(userId);
            return ResponseUtils.buildSuccessResponse(projects, "Reminder Projects Queried");
        } catch (Exception e) {
            log.error("Reminder Project Query Failed: {}", e.getMessage(), e);
            return ResponseUtils.buildErrorResponse(e.getMessage());
        }
    }
    
    // Query Project by ID
    @GetMapping("get/{id}")
    public Map<String, Object> getById(@PathVariable("id") Long projectId, HttpServletRequest request) {
        try {
            Long userId = tokenService.getUserIdFromRequest(request);
            Project project = projectService.getProjectById(userId, projectId);
            return ResponseUtils.buildSuccessResponse(project, "Reminder Project Queried");
        } catch (Exception e) {
            log.error("Reminder Project Query Failed: {}", e.getMessage(), e);
            return ResponseUtils.buildErrorResponse(e.getMessage());
        }
    }
}