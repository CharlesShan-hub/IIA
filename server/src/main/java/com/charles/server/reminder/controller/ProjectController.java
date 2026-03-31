package com.charles.server.reminder.controller;

import java.util.List;
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
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import io.swagger.v3.oas.annotations.responses.ApiResponse;
import io.swagger.v3.oas.annotations.responses.ApiResponses;
import io.swagger.v3.oas.annotations.security.SecurityRequirement;

@Slf4j
@RestController
@RequestMapping("/api/reminder/project")
@RequiredArgsConstructor
@Tag(name = "Project Management", description = "Project creation, update, deletion, and query APIs")
public class ProjectController {
    
    private final ProjectService projectService;
    private final TokenService tokenService;
    
    @PostMapping("create")
    @Operation(
        summary = "Create Project",
        description = "Create a new reminder project with name, description, color, and icon"
    )
    @ApiResponses({
        @ApiResponse(responseCode = "200", description = "Project created successfully"),
        @ApiResponse(responseCode = "400", description = "Invalid request parameters"),
        @ApiResponse(responseCode = "401", description = "Authentication required")
    })
    @SecurityRequirement(name = "bearer-jwt")
    public ResponseUtils<Void> create(@RequestBody @Valid ProjectCreateDTO dto, HttpServletRequest request) {
        Long userId = tokenService.getUserIdFromRequest(request);
        projectService.create(userId, dto);
        log.info("User {} create project {} successfully", userId, dto.getName());
        return ResponseUtils.buildEmptySuccessResponse("Reminder Project Created");
    }

    @PostMapping("delete")
    @Operation(
        summary = "Delete Project",
        description = "Delete a project with options to keep tasks or move them to another project"
    )
    @ApiResponses({
        @ApiResponse(responseCode = "200", description = "Project deleted successfully"),
        @ApiResponse(responseCode = "400", description = "Invalid request parameters"),
        @ApiResponse(responseCode = "401", description = "Authentication required"),
        @ApiResponse(responseCode = "404", description = "Project not found")
    })
    @SecurityRequirement(name = "bearer-jwt")
    public ResponseUtils<Void> delete(@RequestBody @Valid ProjectDeleteDTO dto, HttpServletRequest request) {
        Long userId = tokenService.getUserIdFromRequest(request);
        projectService.delete(userId, dto);
        log.info("User {} delete project {} successfully, keepTasks: {}, targetProjectId: {}", 
                 userId, dto.getProjectId(), dto.getKeepTasks(), dto.getTargetProjectId());
        return ResponseUtils.buildEmptySuccessResponse("Reminder Project Deleted");
    }

    @PostMapping("update")
    @Operation(
        summary = "Update Project",
        description = "Update project information including name, description, color, and icon"
    )
    @ApiResponses({
        @ApiResponse(responseCode = "200", description = "Project updated successfully"),
        @ApiResponse(responseCode = "400", description = "Invalid request parameters"),
        @ApiResponse(responseCode = "401", description = "Authentication required"),
        @ApiResponse(responseCode = "404", description = "Project not found")
    })
    @SecurityRequirement(name = "bearer-jwt")
    public ResponseUtils<Void> updateById(@RequestBody @Valid ProjectUpdateDTO dto, HttpServletRequest request) {
        Long userId = tokenService.getUserIdFromRequest(request);
        projectService.update(userId, dto);
        log.info("User {} update project {} successfully", userId, dto.getProjectId());
        return ResponseUtils.buildEmptySuccessResponse("Reminder Project Updated");
    }

    @PostMapping("batch-update-position")
    @Operation(
        summary = "Batch Update Project Positions",
        description = "Update positions of multiple projects in batch"
    )
    @ApiResponses({
        @ApiResponse(responseCode = "200", description = "Project positions updated successfully"),
        @ApiResponse(responseCode = "400", description = "Invalid request parameters"),
        @ApiResponse(responseCode = "401", description = "Authentication required")
    })
    @SecurityRequirement(name = "bearer-jwt")
    public ResponseUtils<Void> batchUpdatePosition(@RequestBody @Valid BatchUpdatePositionDTO dto, HttpServletRequest httpRequest) {
        Long userId = tokenService.getUserIdFromRequest(httpRequest);
        projectService.batchUpdatePosition(userId, dto);
        log.info("User {} batch update project positions successfully, updated projects: {}", 
                 userId, dto.getPos());
        return ResponseUtils.buildEmptySuccessResponse("Reminder Project Positions Updated");
    }

    @PostMapping("get")
    @Operation(
        summary = "Query Projects",
        description = "Query projects by archived flag and isAll flag"
    )
    @ApiResponses({
        @ApiResponse(responseCode = "200", description = "Projects queried successfully"),
        @ApiResponse(responseCode = "400", description = "Invalid request parameters"),
        @ApiResponse(responseCode = "401", description = "Authentication required")
    })
    @SecurityRequirement(name = "bearer-jwt")
    public ResponseUtils<List<Project>> get(@RequestBody @Valid ProjectGetDTO dto, HttpServletRequest request) {
        Long userId = tokenService.getUserIdFromRequest(request);
        List<Project> projects = projectService.get(userId, dto);
        log.info("User {} query projects successfully, archived: {}, isAll: {}", userId, dto.getArchived(), dto.getIsAll());
        return ResponseUtils.buildSuccessResponse(projects, "Reminder Projects Queried");
    }
}
