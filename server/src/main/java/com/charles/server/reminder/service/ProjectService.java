package com.charles.server.reminder.service;

import java.util.List;

import com.charles.server.reminder.entity.Project;

public interface ProjectService {
    /**
     * 创建项目
     * @param project 项目信息
     * @param userId 用户ID
     * @return 创建后的项目
     */
    Project createProject(Project project, Long userId);
    
    /**
     * 获取用户所有项目
     * @param userId 用户ID
     * @return 项目列表
     */
    List<Project> getUserProjects(Long userId);
    
    /**
     * 根据ID获取项目
     * @param projectId 项目ID
     * @param userId 用户ID
     * @return 项目信息
     */
    Project getProjectById(Long projectId, Long userId);
    
    /**
     * 更新项目
     * @param project 项目信息
     * @param projectId 项目ID
     * @param userId 用户ID
     * @return 更新后的项目
     */
    Project updateProject(Project project, Long projectId, Long userId);
}