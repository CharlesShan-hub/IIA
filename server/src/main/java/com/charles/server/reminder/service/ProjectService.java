package com.charles.server.reminder.service;

import java.util.List;

import com.charles.server.reminder.dto.ProjectCreateDTO;
import com.charles.server.reminder.dto.ProjectUpdateDTO;
import com.charles.server.reminder.dto.BatchUpdatePositionDTO;
import com.charles.server.reminder.dto.ProjectDeleteDTO;
import com.charles.server.reminder.dto.ProjectGetDTO;
import com.charles.server.reminder.entity.Project;

public interface ProjectService {
    /** Create a new project
    */
    void create(Long userId, ProjectCreateDTO dto);

    /** Update an existing project
    */
    void update(Long userId, ProjectUpdateDTO dto);

    /** Delete a project
     */
    void delete(Long userId, ProjectDeleteDTO dto);

    /** Batch update the sort order of projects
     */
    void batchUpdatePosition(Long userId, BatchUpdatePositionDTO dto);

    /** Get projects by archived filter via DTO: archived or isAll
     * @return the list of projects matching the filter
     */
    List<Project> get(Long userId, ProjectGetDTO dto);
}
