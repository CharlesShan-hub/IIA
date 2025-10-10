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
    public Map<String, Object> create(@RequestBody @Valid CreateProjectRequest dto, HttpServletRequest request) {
        try {
            Long userId = tokenService.getUserIdFromRequest(request);
            projectService.create(userId, dto);
            return ResponseUtils.buildSuccessResponse(null, "创建成功");
        } catch (Exception e) {
            log.error("创建项目失败: {}", e.getMessage(), e);
            return ResponseUtils.buildErrorResponse(e.getMessage());
        }
    }

    // 更新项目
    @PostMapping("update")
    public Map<String, Object> updateById(@RequestBody @Valid UpdateProjectRequest dto, HttpServletRequest request) {
        try {
            Long userId = tokenService.getUserIdFromRequest(request);
            projectService.update(userId, dto);
            return ResponseUtils.buildSuccessResponse(null, "更新成功");
        } catch (Exception e) {
            log.error("更新项目失败: {}", e.getMessage(), e);
            return ResponseUtils.buildErrorResponse(e.getMessage());
        }
    }

    // 交换项目位置
    @PostMapping("swap-position")
    public Map<String, Object> swapPosition(@RequestBody @Valid SwapPositionRequest dto, HttpServletRequest request) {
        try {
            Long userId = tokenService.getUserIdFromRequest(request);
            Project src = projectService.getProjectById(userId, dto.getProjectId());
            Project des = projectService.getProjectBySortOrder(userId, dto.getSortOrder());
            if(des == null || src == null) {
                return ResponseUtils.buildErrorResponse("项目不存在");
            }
            if(!src.equals(des)) {
                projectService.updateSortOrder(userId, des.getProjectId(), src.getSortOrder());
                projectService.updateSortOrder(userId, src.getProjectId(), dto.getSortOrder());
            }
            return ResponseUtils.buildSuccessResponse(null, "交换成功");
        } catch (Exception e) {
            log.error("交换项目位置失败: {}", e.getMessage(), e);
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
}