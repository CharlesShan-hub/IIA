package com.charles.server.reminder.controller;

import java.util.List;
import java.util.Map;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.charles.server.auth.service.TokenService;
import com.charles.server.reminder.entity.Project;
import com.charles.server.reminder.service.ProjectService;
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
    
    // 创建项目
    @PostMapping("create")
    public Map<String, Object> create(@RequestBody Project project, HttpServletRequest request) {
        try {
            project.setUserId(tokenService.getUserIdFromRequest(request));
            Project createdProject = projectService.create(project);
            return ResponseUtils.buildSuccessResponse(createdProject, "创建成功");
        } catch (Exception e) {
            log.error("创建项目失败: {}", e.getMessage(), e);
            return ResponseUtils.buildErrorResponse(e.getMessage());
        }
    }
    
    // 获取用户所有项目
    @GetMapping("get-all")
    public Map<String, Object> getAll(HttpServletRequest request) {
        try {
            Long userId = tokenService.getUserIdFromRequest(request);
            List<Project> projects = projectService.getAll(userId);
            return ResponseUtils.buildSuccessResponse(projects, "查询成功");
        } catch (Exception e) {
            log.error("获取项目列表失败: {}", e.getMessage(), e);
            return ResponseUtils.buildErrorResponse(e.getMessage());
        }
    }
    
    // 获取单个项目
    @GetMapping("get/{id}")
    public Map<String, Object> getById(@PathVariable("id") Long projectId, HttpServletRequest request) {
        try {
            Long userId = tokenService.getUserIdFromRequest(request);
            Project project = projectService.getProjectById(userId, projectId);
            return ResponseUtils.buildSuccessResponse(project, "查询成功");
        } catch (Exception e) {
            log.error("获取项目失败: {}", e.getMessage(), e);
            return ResponseUtils.buildErrorResponse(e.getMessage());
        }
    }
    
    // 更新项目
    @PutMapping("update/{id}")
    public Map<String, Object> updateById(@PathVariable("id") Long projectId, @RequestBody Project project, HttpServletRequest request) {
        try {
            project.setUserId(tokenService.getUserIdFromRequest(request));
            project.setProjectId(projectId);
            Project updatedProject = projectService.updateProject(project);
            return ResponseUtils.buildSuccessResponse(updatedProject, "更新成功");
        } catch (Exception e) {
            log.error("更新项目失败: {}", e.getMessage(), e);
            return ResponseUtils.buildErrorResponse(e.getMessage());
        }
    }
}