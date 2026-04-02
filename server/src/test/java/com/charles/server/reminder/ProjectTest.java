package com.charles.server.reminder;

import com.charles.server.BaseE2eDatabaseTest;
import com.charles.server.reminder.dto.ProjectDeleteDTO;
import com.charles.server.reminder.dto.ProjectUpdateDTO;
import com.charles.server.reminder.dto.BatchUpdatePositionDTO;
import com.charles.server.reminder.entity.Position;
import com.charles.server.reminder.entity.Project;
import com.charles.server.reminder.entity.Task;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import lombok.extern.slf4j.Slf4j;

import java.util.List;

import static org.junit.jupiter.api.Assertions.*;

@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.MOCK)
@AutoConfigureMockMvc(addFilters = false)
@Slf4j
class ProjectTest extends BaseE2eDatabaseTest {

    @BeforeEach
    void clean() {
        recreateDatabase();
        executeSqlFiles(dataSource);
        seedBaseUser(jdbc, passwordEncoder);
        afterSchemaInitialized(jdbc);
    }

    @Test
    void create() throws Exception {
        Long projectId = createProject("P1", 200);
        assertNotNull(projectId);

        Project p = projectMapper.findById(projectId);
        assertNotNull(p);
        assertEquals("P1", p.getName());
        assertEquals(1L, p.getUserId());
    }

    @Test
    void update_name() throws Exception {
        Long projectId = createProject("P1", 200);

        ProjectUpdateDTO req = new ProjectUpdateDTO();
        req.setProjectId(projectId);
        req.setName("P1-Renamed");

        updateProject(req, 200);

        Project updated = projectMapper.findById(projectId);
        assertNotNull(updated);
        assertEquals("P1-Renamed", updated.getName());
    }

    @Test
    void update_sort_order() throws Exception {
        Long projectId1 = createProject("P1", 200);
        Long projectId2 = createProject("P2", 200);
        Long projectId3 = createProject("P3", 200);
        Long projectId4 = createProject("P4", 200);

        BatchUpdatePositionDTO req1 = new BatchUpdatePositionDTO();
        req1.setPos(List.of(
            new Position(projectId1, 400),
            new Position(projectId2, 300),
            new Position(projectId3, 200),
            new Position(projectId4, 100)
        ));
        batchUpdateProjectPosition(req1, 200);
    }

    @Test
    void delete() throws Exception {
        Long projectId = createProject("P1", 200);

        ProjectDeleteDTO del = ProjectDeleteDTO.builder()
                .projectId(projectId)
                .keepTasks(false)
                .build();

        deleteProject(del, 200);

        assertNull(projectMapper.findById(projectId));

        revertOperation();
    }

    @Test
    void update_revert_create_and_batch_update_position() throws Exception {
        Long projectId1 = createProject("P1", 200);
        Long projectId2 = createProject("P2", 200);
        Long projectId3 = createProject("P3", 200);
        Long projectId4 = createProject("P4", 200);

        BatchUpdatePositionDTO req1 = new BatchUpdatePositionDTO();
        req1.setPos(List.of(
            new Position(projectId1, 400),
            new Position(projectId2, 300),
            new Position(projectId3, 200),
            new Position(projectId4, 100)
        ));
        batchUpdateProjectPosition(req1, 200);
    }
    
    @Test
    void delete_project_keep_tasks_moves_tasks_to_default_area() throws Exception {
        Long projectId = createProject("P1", 200);
        Long taskId = createRootTask(projectId, "T1");

        ProjectDeleteDTO del = new ProjectDeleteDTO();
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

        ProjectDeleteDTO del = new ProjectDeleteDTO();
        del.setProjectId(projectId);
        del.setKeepTasks(false);
        del.setTargetProject(false);
        del.setTargetProjectId(0L);

        deleteProject(del, 200);

        assertNull(projectMapper.findById(projectId));
        assertNull(taskMapper.findById(taskId));
    }
}