package com.charles.server.reminder;

import com.charles.server.BaseE2eDatabaseTest;
import com.charles.server.reminder.dto.ProjectDeleteRequest;
import com.charles.server.reminder.dto.ProjectUpdateRequest;
import com.charles.server.reminder.entity.Operation;
import com.charles.server.reminder.entity.Project;
import com.charles.server.reminder.entity.Task;
import com.charles.server.reminder.mapper.OperationMapper;
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
    
    @Autowired
    private OperationMapper operationMapper;

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

    @Test
    void revert_scenario_create_update_revert_twice() throws Exception {
        // 1. 创建项目
        Long projectId = createProject("Init Project", 200);
        assertNotNull(projectId);
        
        Project initialProject = projectMapper.findById(projectId);
        assertNotNull(initialProject);
        assertEquals("Init Project", initialProject.getName());
        Long initialOperationId = initialProject.getOperationId();
        assertNotNull(initialOperationId);
        
        // 验证初始操作记录存在
        Operation initialOperation = operationMapper.findByIdAndUserId(initialOperationId, 1L);
        assertNotNull(initialOperation, "初始操作记录应该存在");
        assertEquals(initialOperationId, initialOperation.getOperationId());
        
        // 2. 修改：重命名
        ProjectUpdateRequest updateRequest = new ProjectUpdateRequest();
        updateRequest.setProjectId(projectId);
        updateRequest.setName("First Update Project");
        
        updateProject(updateRequest, 200);
        
        Project afterUpdate = projectMapper.findById(projectId);
        assertNotNull(afterUpdate);
        assertEquals("First Update Project", afterUpdate.getName());
        Long updateOperationId = afterUpdate.getOperationId();
        assertNotNull(updateOperationId);
        assertNotEquals(initialOperationId, updateOperationId);
        
        // 验证修改操作记录存在
        Operation updateOperation = operationMapper.findByIdAndUserId(updateOperationId, 1L);
        assertNotNull(updateOperation, "修改操作记录应该存在");
        assertEquals(updateOperationId, updateOperation.getOperationId());
        
        // 3. 第一次撤回：撤回修改
        operationService.revert(1L); // userId = 1L
        
        Project afterFirstRevert = projectMapper.findById(projectId);
        assertNotNull(afterFirstRevert);
        assertEquals("Init Project", afterFirstRevert.getName());
        assertEquals(initialOperationId, afterFirstRevert.getOperationId());
        
        // 验证修改操作记录已被删除
        Operation deletedUpdateOperation = operationMapper.findByIdAndUserId(updateOperationId, 1L);
        assertNull(deletedUpdateOperation, "撤回后修改操作记录应该被删除");
        
        // 验证初始操作记录仍然存在
        Operation stillInitialOperation = operationMapper.findByIdAndUserId(initialOperationId, 1L);
        assertNotNull(stillInitialOperation, "初始操作记录应该仍然存在");
        assertEquals(initialOperationId, stillInitialOperation.getOperationId());
        
        // 4. 第二次撤回：应该失败，因为没有更早的操作了
        IllegalStateException exception = assertThrows(IllegalStateException.class, () -> {
            operationService.revert(1L);
        });
        
        assertEquals("没有可撤回的上一次操作", exception.getMessage());
        
        // 验证项目状态没有变化
        Project afterSecondRevertAttempt = projectMapper.findById(projectId);
        assertNotNull(afterSecondRevertAttempt);
        assertEquals("Init Project", afterSecondRevertAttempt.getName());
        assertEquals(initialOperationId, afterSecondRevertAttempt.getOperationId());
        
        // 验证：就像只撤回了一次一样
        assertEquals(initialProject.getName(), afterSecondRevertAttempt.getName());
        assertEquals(initialProject.getDescription(), afterSecondRevertAttempt.getDescription());
        assertEquals(initialProject.getColor(), afterSecondRevertAttempt.getColor());
        assertEquals(initialProject.getIcon(), afterSecondRevertAttempt.getIcon());
        assertEquals(initialProject.getSortOrder(), afterSecondRevertAttempt.getSortOrder());
        assertEquals(initialProject.getIsArchived(), afterSecondRevertAttempt.getIsArchived());
        assertEquals(initialProject.getOperationId(), afterSecondRevertAttempt.getOperationId());
        
        log.info("项目撤回测试完成: projectId={}, 第二次撤回按预期失败", projectId);
    }

    @Test
    void revert_scenario_create_two_delete_first_revert() throws Exception {
        Long project1Id = createProject("Project1", 200);
        Long project2Id = createProject("Project2", 200);

        assertNotNull(project1Id);
        assertNotNull(project2Id);
        assertNotEquals(project1Id, project2Id);

        Project project1BeforeDelete = projectMapper.findById(project1Id);
        Project project2BeforeDelete = projectMapper.findById(project2Id);

        assertNotNull(project1BeforeDelete);
        assertNotNull(project2BeforeDelete);
        assertEquals("Project1", project1BeforeDelete.getName());
        assertEquals("Project2", project2BeforeDelete.getName());

        ProjectDeleteRequest del = new ProjectDeleteRequest();
        del.setProjectId(project1Id);
        del.setKeepTasks(true);
        del.setTargetProject(false);
        del.setTargetProjectId(0L);

        deleteProject(del, 200);

        assertNull(projectMapper.findById(project1Id));

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
    }
}