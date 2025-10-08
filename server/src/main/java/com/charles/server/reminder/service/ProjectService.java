package com.charles.server.reminder.service;

import java.util.List;

import com.charles.server.reminder.dto.CreateProjectRequest;
import com.charles.server.reminder.entity.Project;

public interface ProjectService {
    /** 创建项目 */
    Project create(Long userId, CreateProjectRequest dto);
    
    /** 获取用户所有项目 */
    List<Project> getAll(Long userId);
    
    /** 根据项目ID获取项目 */
    Project getProjectById(Long userId, Long projectId);

    /** 根据项目名判断项目是否存在 */
    boolean existsByName(Long userId, String name);

    /** 更新项目 */
    Project updateProject(Project project);
}