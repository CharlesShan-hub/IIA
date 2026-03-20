package com.charles.server.reminder;

import com.charles.server.BaseE2eDatabaseTest;
import com.charles.server.reminder.dto.ProjectDeleteRequest;
import com.charles.server.reminder.dto.ProjectUpdateRequest;
import com.charles.server.reminder.dto.BatchUpdatePositionRequest;
import com.charles.server.reminder.entity.Project;
import com.charles.server.reminder.entity.Task;
import com.charles.server.reminder.service.OperationService;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import lombok.extern.slf4j.Slf4j;

import java.util.List;

import static org.junit.jupiter.api.Assertions.*;

@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.MOCK)
@AutoConfigureMockMvc(addFilters = false)
@Slf4j
class ProjectTest extends BaseE2eDatabaseTest {

    @Autowired
    private OperationService operationService;

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

        ProjectUpdateRequest req = new ProjectUpdateRequest();
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

        BatchUpdatePositionRequest req1 = new BatchUpdatePositionRequest();
        req1.setPos(List.of(
            new BatchUpdatePositionRequest.Position(projectId1, 400),
            new BatchUpdatePositionRequest.Position(projectId2, 300),
            new BatchUpdatePositionRequest.Position(projectId3, 200),
            new BatchUpdatePositionRequest.Position(projectId4, 100)
        ));
        batchUpdateProjectPosition(req1, 200);
    }

    @Test
    void update_revert_create_and_batch_update_position() throws Exception {
        Long projectId1 = createProject("P1", 200);
        Long projectId2 = createProject("P2", 200);
        Long projectId3 = createProject("P3", 200);
        Long projectId4 = createProject("P4", 200);

        BatchUpdatePositionRequest req1 = new BatchUpdatePositionRequest();
        req1.setPos(List.of(
            new BatchUpdatePositionRequest.Position(projectId1, 400),
            new BatchUpdatePositionRequest.Position(projectId2, 300),
            new BatchUpdatePositionRequest.Position(projectId3, 200),
            new BatchUpdatePositionRequest.Position(projectId4, 100)
        ));
        batchUpdateProjectPosition(req1, 200);

        ProjectUpdateRequest req = new ProjectUpdateRequest();
        req.setProjectId(projectId1);
        req.setName("P1-Renamed");
        updateProject(req, 200);

        operationService.revert(1L);
        operationService.revert(1L);
        operationService.revert(1L);

        // 验证第一次撤销：撤销批量更新操作
        // 验证第二次撤销：撤销P4的创建
        Project p1 = projectMapper.findById(projectId1);
        Project p2 = projectMapper.findById(projectId2);
        Project p3 = projectMapper.findById(projectId3);
        Project p4 = projectMapper.findById(projectId4);
        
        assertNotNull(p1);
        assertNotNull(p2);
        assertNotNull(p3);
        assertNull(p4); // P4应该被撤销（删除）
        
        // 验证排序顺序恢复到初始状态（都是200）
        assertEquals(1, p1.getSortOrder());
        assertEquals(2, p2.getSortOrder());
        assertEquals(3, p3.getSortOrder());
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

    // @Test
    // void revert_scenario_create_two_delete_first_revert() throws Exception {
    //     Long project1Id = createProject("Project1", 200);
    //     Long project2Id = createProject("Project2", 200);

    //     assertNotNull(project1Id);
    //     assertNotNull(project2Id);
    //     assertNotEquals(project1Id, project2Id);

    //     Project project1BeforeDelete = projectMapper.findById(project1Id);
    //     Project project2BeforeDelete = projectMapper.findById(project2Id);

    //     assertNotNull(project1BeforeDelete);
    //     assertNotNull(project2BeforeDelete);
    //     assertEquals("Project1", project1BeforeDelete.getName());
    //     assertEquals("Project2", project2BeforeDelete.getName());

    //     ProjectDeleteRequest del = new ProjectDeleteRequest();
    //     del.setProjectId(project1Id);
    //     del.setKeepTasks(true);
    //     del.setTargetProject(false);
    //     del.setTargetProjectId(0L);

    //     deleteProject(del, 200);

    //     assertNull(projectMapper.findById(project1Id));

        // Project project2AfterDelete = projectMapper.findById(project2Id);
        // assertNotNull(project2AfterDelete);
        // assertEquals("Project2", project2AfterDelete.getName());
        // assertEquals(project2BeforeDelete.getOperationId(), project2AfterDelete.getOperationId());

        // Long deleteOperationId = operationMapper.getLatestOperationIdByUserId(1L);
        // assertNotNull(deleteOperationId);

        // operationService.revert(1L);

        // Project project1AfterRevert = projectMapper.findById(project1Id);
        // assertNotNull(project1AfterRevert);
        // assertEquals("Project1", project1AfterRevert.getName());
        // assertEquals(project1BeforeDelete.getOperationId(), project1AfterRevert.getOperationId());

        // Project project2AfterRevert = projectMapper.findById(project2Id);
        // assertNotNull(project2AfterRevert);
        // assertEquals("Project2", project2AfterRevert.getName());
        // assertEquals(project2BeforeDelete.getOperationId(), project2AfterRevert.getOperationId());

        // Operation deletedOperation = operationMapper.findByIdAndUserId(deleteOperationId, 1L);
        // assertNull(deletedOperation);
    // }
}