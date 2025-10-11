package com.charles.server.reminder.service;

import java.util.List;

import com.charles.server.reminder.dto.CreateProjectRequest;
import com.charles.server.reminder.dto.UpdateProjectRequest;
import com.charles.server.reminder.dto.BatchUpdatePositionRequest;
import com.charles.server.reminder.entity.Project;

public interface ProjectService {
    /** 创建项目 */
    void create(Long userId, CreateProjectRequest dto);

    /** 更新项目 */
    void update(Long userId, UpdateProjectRequest dto);

    /** 更新位置 */
    void updateSortOrder(Long userId, Long projectId, Integer sortOrder);
    
    /** 获取用户所有项目 */
    List<Project> getAll(Long userId);
    
    /** 根据项目ID获取项目 */
    Project getProjectById(Long userId, Long projectId);

    /** 根据名称获取项目 */
    Project getProjectByName(Long userId, String name);

    /** 根据位置获取项目 */
    Project getProjectBySortOrder(Long userId, Integer sortOrder);

    /** 根据项目名判断项目是否存在 */
    boolean existsByName(Long userId, String name);

    /** 根据位置判断项目是否存在 */
    public boolean existsBySortOrder(Long userId, Integer sortOrder);

    /** 添加批量更新位置方法 */
    void batchUpdatePosition(Long userId, BatchUpdatePositionRequest request);
}