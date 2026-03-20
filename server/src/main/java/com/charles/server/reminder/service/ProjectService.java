package com.charles.server.reminder.service;

import java.util.List;

import com.charles.server.reminder.dto.ProjectCreateDTO;
import com.charles.server.reminder.dto.ProjectUpdateDTO;
import com.charles.server.reminder.dto.BatchUpdatePositionDTO;
import com.charles.server.reminder.dto.ProjectDeleteDTO;
import com.charles.server.reminder.dto.ProjectGetAllDTO;
import com.charles.server.reminder.entity.Project;

public interface ProjectService {
    /** Create a new project 
     * @param userId
     * @param dto the project creation request
    */
    void create(Long userId, ProjectCreateDTO dto);

    /** Update an existing project
     * @param userId
     * @param dto the project update request
    */
    void update(Long userId, ProjectUpdateDTO dto);

    /** Delete a project
     * @param userId
     * @param dto the project deletion request
     */
    void delete(Long userId, ProjectDeleteDTO dto);

    /** Batch update the sort order of projects
     * @param userId
     * @param dto the batch update position request
     */
    void batchUpdatePosition(Long userId, BatchUpdatePositionDTO dto);

    /** Get projects by archived filter via DTO: archived or isAll
     * @param userId
     * @param dto query options
     * @return the list of projects matching the filter
     */
    List<Project> getAll(Long userId, ProjectGetAllDTO dto);
}
