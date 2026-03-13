package com.charles.server.reminder;

import com.charles.server.BaseE2eDatabaseTest;
import com.charles.server.reminder.dto.ProjectDeleteRequest;
import com.charles.server.reminder.dto.ProjectUpdateRequest;
import com.charles.server.reminder.entity.Project;
import com.charles.server.reminder.entity.Task;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;

import java.util.List;

import static org.junit.jupiter.api.Assertions.*;

@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.MOCK)
@AutoConfigureMockMvc(addFilters = false)
class ProjectTest extends BaseE2eDatabaseTest {

    @BeforeEach
    void clean() {
        List<Task> tasks = taskMapper.findByUserId(1L);
        for (Task t : tasks) {
            taskMapper.deleteById(t.getTaskId());
        }

        projectMapper.findByUserIdAndArchived(1L, false).forEach(p -> projectMapper.deleteById(p.getProjectId()));
        projectMapper.findByUserIdAndArchived(1L, true).forEach(p -> projectMapper.deleteById(p.getProjectId()));
    }

    @Test
    void create_project_persists_row() throws Exception {
        Long projectId = createProject("P1", 200);
        assertNotNull(projectId);

        Project p = projectMapper.findById(projectId);
        assertNotNull(p);
        assertEquals("P1", p.getName());
        assertEquals(1L, p.getUserId());
    }

    @Test
    void update_project_rename() throws Exception {
        Long projectId = createProject("P1", 200);

        ProjectUpdateRequest req = new ProjectUpdateRequest();
        req.setProjectId(projectId);
        req.setName("P1-Renamed");

        updateProject(req, 200);

        Project updated = projectMapper.findById(projectId);
        assertNotNull(updated);
        assertEquals("P1-Renamed", updated.getName());
    }

    @Test
    void delete_project_keep_tasks_moves_tasks_to_default_area() throws Exception {
        Long projectId = createProject("P1", 200);
        Long taskId = createRootTask(projectId, "T1");

        ProjectDeleteRequest del = new ProjectDeleteRequest();
        del.setProjectId(projectId);
        del.setKeepTasks(true);
        del.setTargetProject(false);
        del.setTargetProjectId(0L);

        deleteProject(del, 200);

        assertNull(projectMapper.findById(projectId));

        Task moved = taskMapper.findById(taskId);
        assertNotNull(moved);
        assertNull(moved.getProjectId());
    }

    @Test
    void delete_project_delete_tasks_deletes_tasks_in_project() throws Exception {
        Long projectId = createProject("P1", 200);
        Long taskId = createRootTask(projectId, "T1");

        ProjectDeleteRequest del = new ProjectDeleteRequest();
        del.setProjectId(projectId);
        del.setKeepTasks(false);
        del.setTargetProject(false);
        del.setTargetProjectId(0L);

        deleteProject(del, 200);

        assertNull(projectMapper.findById(projectId));
        assertNull(taskMapper.findById(taskId));
    }
}