package com.charles.server.reminder.service;

import java.util.List;

import com.charles.server.reminder.dto.ProjectCreateRequest;
import com.charles.server.reminder.dto.ProjectUpdateRequest;
import com.charles.server.reminder.dto.BatchUpdatePositionRequest;
import com.charles.server.reminder.dto.ProjectDeleteRequest;
import com.charles.server.reminder.dto.ProjectGetAllRequest;
import com.charles.server.reminder.entity.Project;

public interface ProjectService {
    /** Create a new project 
     * @param userId
     * @param dto the project creation request
    */
    void create(Long userId, ProjectCreateRequest dto);

    /** Update an existing project
     * @param userId
     * @param dto the project update request
    */
    void update(Long userId, ProjectUpdateRequest dto);

    /** Delete a project
     * @param userId
     * @param dto the project deletion request
     */
    void delete(Long userId, ProjectDeleteRequest dto);

    /** Batch update the sort order of projects
     * @param userId
     * @param dto the batch update position request
     */
    void batchUpdatePosition(Long userId, BatchUpdatePositionRequest dto);

    /** Get projects by archived filter via DTO: archived or isAll
     * @param userId
     * @param dto query options
     * @return the list of projects matching the filter
     */
    List<Project> getAll(Long userId, ProjectGetAllRequest dto);
}
