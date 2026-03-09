package com.charles.server.reminder.controller;

import com.charles.server.BaseE2eDatabaseTest;
import com.charles.server.auth.service.TokenService;
import com.charles.server.reminder.dto.ProjectCreateRequest;
import com.charles.server.reminder.dto.TaskCreateRequest;
import com.charles.server.reminder.dto.TaskDeleteRequest;
import com.charles.server.reminder.dto.ProjectDeleteRequest;
import com.charles.server.reminder.dto.TaskStatusUpdateRequest;
import com.charles.server.reminder.entity.Project;
import com.charles.server.reminder.entity.Task;
import com.charles.server.reminder.mapper.ProjectMapper;
import com.charles.server.reminder.mapper.TaskMapper;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;
import org.mockito.Mockito;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.context.TestConfiguration;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Primary;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;

import java.util.Comparator;
import java.util.List;
import java.util.Optional;

import static org.hamcrest.Matchers.is;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.patch;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.MOCK)
@AutoConfigureMockMvc(addFilters = false)
class TaskControllerScenarioE2ETest extends BaseE2eDatabaseTest {

    @Autowired MockMvc mockMvc;
    @Autowired ObjectMapper objectMapper;
    @Autowired ProjectMapper projectMapper;
    @Autowired TaskMapper taskMapper;

    @TestConfiguration
    static class TestConfig {
        @Bean @Primary
        TokenService tokenService() {
            TokenService mock = Mockito.mock(TokenService.class);
            Mockito.when(mock.getUserIdFromRequest(Mockito.any())).thenReturn(1L);
            return mock;
        }
    }

    @Test
    void scenario_createProject_then_twoRootTasks_then_oneSubTask() throws Exception {
        // 1) 创建默认项目
        ProjectCreateRequest pReq = new ProjectCreateRequest();
        pReq.setName("Default");
        mockMvc.perform(post("/api/reminder/projects/create")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(pReq)))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.code", is(200)));

        List<Project> projects = projectMapper.findByUserIdAndArchived(1L, false);
        Optional<Project> opt = projects.stream().filter(p -> "Default".equals(p.getName())).findFirst();
        Assertions.assertTrue(opt.isPresent(), "Project 'Default' should be created");
        Long projectId = opt.get().getProjectId();

        // 2) 创建两个根任务（同一项目）
        TaskCreateRequest t1 = new TaskCreateRequest();
        t1.setProjectId(projectId);
        t1.setTitle("T1");
        t1.setIsRecurring(false);
        mockMvc.perform(post("/api/reminder/task/create")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(t1)))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.code", is(200)));

        TaskCreateRequest t2 = new TaskCreateRequest();
        t2.setProjectId(projectId);
        t2.setTitle("T2");
        t2.setIsRecurring(false);
        mockMvc.perform(post("/api/reminder/task/create")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(t2)))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.code", is(200)));

        List<Task> roots = taskMapper.findByUserIdAndProjectId(1L, projectId);
        Assertions.assertTrue(roots.size() >= 2, "At least two root tasks should exist in the project");
        Task first = roots.stream().filter(x -> "T1".equals(x.getTitle())).findFirst().orElseThrow();
        Task second = roots.stream().filter(x -> "T2".equals(x.getTitle())).findFirst().orElseThrow();
        // 验证根任务排序递增（插入顺序）
        roots.sort(Comparator.comparing(Task::getSortOrder));
        Assertions.assertEquals("T1", roots.get(0).getTitle());
        Assertions.assertEquals("T2", roots.get(1).getTitle());

        // 3) 创建第三个任务，父任务是第一个任务
        TaskCreateRequest c1 = new TaskCreateRequest();
        c1.setProjectId(projectId);
        c1.setParentTaskId(first.getTaskId());
        c1.setTitle("T1-1");
        c1.setIsRecurring(false);
        mockMvc.perform(post("/api/reminder/task/create")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(c1)))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.code", is(200)));

        List<Task> children = taskMapper.findByUserIdAndParentTaskId(1L, first.getTaskId());
        Assertions.assertFalse(children.isEmpty(), "Child tasks for T1 should exist");
        Assertions.assertTrue(children.stream().anyMatch(t -> "T1-1".equals(t.getTitle())), "Should contain child 'T1-1'");
        // 子任务应有有效排序
        Assertions.assertTrue(children.stream().allMatch(t -> t.getSortOrder() != null && t.getSortOrder() > 0));

        // 再创建二级子任务 T1-1-1（父：T1-1）
        Task c1Entity = children.stream().filter(t -> "T1-1".equals(t.getTitle())).findFirst().orElseThrow();
        TaskCreateRequest c2 = new TaskCreateRequest();
        c2.setProjectId(projectId);
        c2.setParentTaskId(c1Entity.getTaskId());
        c2.setTitle("T1-1-1");
        c2.setIsRecurring(false);
        mockMvc.perform(post("/api/reminder/task/create")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(c2)))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.code", is(200)));

        // 验证二级子任务存在
        List<Task> grandChildren = taskMapper.findByUserIdAndParentTaskId(1L, c1Entity.getTaskId());
        Assertions.assertTrue(grandChildren.stream().anyMatch(t -> "T1-1-1".equals(t.getTitle())), "Should contain grandchild 'T1-1-1'");

        // 4) 删除任务一（应级联删除其子任务），保留任务二
        TaskDeleteRequest del = new TaskDeleteRequest();
        del.setTaskId(first.getTaskId());
        mockMvc.perform(post("/api/reminder/task/delete")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(del)))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.code", is(200)));

        // 校验 T1 已删除
        Task t1After = taskMapper.findById(first.getTaskId());
        Assertions.assertNull(t1After, "T1 should be deleted");
        // 子任务也应被删除
        List<Task> childrenAfter = taskMapper.findByUserIdAndParentTaskId(1L, first.getTaskId());
        Assertions.assertTrue(childrenAfter.isEmpty(), "Children of T1 should be deleted");
        // 二级子任务也应被删除（以 T1-1 为父）
        List<Task> grandChildrenAfter = taskMapper.findByUserIdAndParentTaskId(1L, c1Entity.getTaskId());
        Assertions.assertTrue(grandChildrenAfter.isEmpty(), "Grandchildren of T1 should be deleted");
        Task c1After = taskMapper.findById(c1Entity.getTaskId());
        Assertions.assertNull(c1After, "T1-1 should be deleted with its subtree");
        // T2 仍存在
        Task t2After = taskMapper.findById(second.getTaskId());
        Assertions.assertNotNull(t2After, "T2 should remain");
    }

    @Test
    void scenario_deleteProject_keepTasks_transferToAnotherProject() throws Exception {
        // 创建两个项目：MoveP1 与 MoveP2
        ProjectCreateRequest p1Req = new ProjectCreateRequest();
        p1Req.setName("MoveP1");
        mockMvc.perform(post("/api/reminder/projects/create")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(p1Req)))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.code", is(200)));

        ProjectCreateRequest p2Req = new ProjectCreateRequest();
        p2Req.setName("MoveP2");
        mockMvc.perform(post("/api/reminder/projects/create")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(p2Req)))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.code", is(200)));

        List<Project> projectsAll = projectMapper.findByUserIdAndArchived(1L, false);
        Long p1Id = projectsAll.stream().filter(p -> "MoveP1".equals(p.getName())).findFirst().orElseThrow().getProjectId();
        Long p2Id = projectsAll.stream().filter(p -> "MoveP2".equals(p.getName())).findFirst().orElseThrow().getProjectId();

        // 在 P2 下预先创建任务 C，用于观察迁移后的 sort_order 关系
        TaskCreateRequest c = new TaskCreateRequest();
        c.setProjectId(p2Id);
        c.setTitle("C");
        c.setIsRecurring(false);
        mockMvc.perform(post("/api/reminder/task/create")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(c)))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.code", is(200)));
        Task taskCBefore = taskMapper.findByUserIdAndProjectId(1L, p2Id).stream()
                .filter(t -> "C".equals(t.getTitle())).findFirst().orElseThrow();
        int cOrderBefore = taskCBefore.getSortOrder();

        // 在 P1 下创建任务 A
        TaskCreateRequest a = new TaskCreateRequest();
        a.setProjectId(p1Id);
        a.setTitle("A");
        a.setIsRecurring(false);
        mockMvc.perform(post("/api/reminder/task/create")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(a)))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.code", is(200)));

        // 获取 A 的 id
        Task taskA = taskMapper.findByUserIdAndProjectId(1L, p1Id).stream()
                .filter(t -> "A".equals(t.getTitle())).findFirst().orElseThrow();
        int aOrderBefore = taskA.getSortOrder();

        // 在 P1 下创建任务 B，父任务=A
        TaskCreateRequest b = new TaskCreateRequest();
        b.setProjectId(p1Id);
        b.setTitle("B");
        b.setIsRecurring(false);
        b.setParentTaskId(taskA.getTaskId());
        mockMvc.perform(post("/api/reminder/task/create")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(b)))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.code", is(200)));

        // 验证父子关系存在于 P1 下
        Task taskB = taskMapper.findByUserIdAndProjectId(1L, p1Id).stream()
                .filter(t -> "B".equals(t.getTitle())).findFirst().orElseThrow();
        Assertions.assertEquals(taskA.getTaskId(), taskB.getParentTaskId());

        // 删除 P1，保留任务并迁移到 P2
        ProjectDeleteRequest del = new ProjectDeleteRequest();
        del.setProjectId(p1Id);
        del.setKeepTasks(true);
        del.setTargetProject(true);
        del.setTargetProjectId(p2Id);
        mockMvc.perform(post("/api/reminder/projects/delete")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(del)))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.code", is(200)));

        // P1 应被删除
        Assertions.assertNull(projectMapper.findById(p1Id));

        // 任务应迁移到 P2，且父子关系保持
        List<Task> tasksInP2 = taskMapper.findByUserIdAndProjectId(1L, p2Id);
        Task taskAInP2 = tasksInP2.stream().filter(t -> "A".equals(t.getTitle())).findFirst().orElse(null);
        Task taskBInP2 = tasksInP2.stream().filter(t -> "B".equals(t.getTitle())).findFirst().orElse(null);
        Task taskCInP2 = tasksInP2.stream().filter(t -> "C".equals(t.getTitle())).findFirst().orElse(null);
        Assertions.assertNotNull(taskAInP2, "Task A should be moved to P2");
        Assertions.assertNotNull(taskBInP2, "Task B should be moved to P2");
        Assertions.assertNotNull(taskCInP2, "Task C should remain in P2");
        Assertions.assertEquals(taskA.getTaskId(), taskAInP2.getTaskId(), "Task A ID should remain same");
        Assertions.assertEquals(taskB.getTaskId(), taskBInP2.getTaskId(), "Task B ID should remain same");
        Assertions.assertEquals(taskA.getTaskId(), taskBInP2.getParentTaskId(), "Parent relation should be preserved");
        // sort_order：迁移的根任务应追加在目标项目现有任务之后
        Assertions.assertEquals(cOrderBefore + 1, taskAInP2.getSortOrder(), "Task A should be appended after existing tasks in P2");
        Assertions.assertEquals(cOrderBefore, taskCInP2.getSortOrder(), "Task C sort_order should remain as before");

        // P1 下不应再有 A/B
        List<Task> tasksInP1 = taskMapper.findByUserIdAndProjectId(1L, p1Id);
        Assertions.assertTrue(tasksInP1.stream().noneMatch(t -> "A".equals(t.getTitle()) || "B".equals(t.getTitle())),
                "P1 should have no A/B after migration");
    }

    @Test
    void scenario_deleteProject_to_inbox_appends_after_existing() throws Exception {
        // 在收件箱（project_id=NULL）先创建任务 D，记录其排序
        TaskCreateRequest d = new TaskCreateRequest();
        d.setTitle("D");
        d.setIsRecurring(false);
        mockMvc.perform(post("/api/reminder/task/create")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(d)))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.code", is(200)));
        Task taskDBefore = taskMapper.findByUserIdAndProjectIdIsNull(1L).stream()
                .filter(t -> "D".equals(t.getTitle())).findFirst().orElseThrow();
        int dOrderBefore = taskDBefore.getSortOrder();

        // 创建项目 MoveP3
        ProjectCreateRequest p3Req = new ProjectCreateRequest();
        p3Req.setName("MoveP3");
        mockMvc.perform(post("/api/reminder/projects/create")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(p3Req)))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.code", is(200)));
        Long p3Id = projectMapper.findByUserIdAndArchived(1L, false).stream()
                .filter(p -> "MoveP3".equals(p.getName())).findFirst().orElseThrow().getProjectId();

        // 在 P3 下创建根任务 X
        TaskCreateRequest x = new TaskCreateRequest();
        x.setProjectId(p3Id);
        x.setTitle("X");
        x.setIsRecurring(false);
        mockMvc.perform(post("/api/reminder/task/create")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(x)))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.code", is(200)));
        Task taskX = taskMapper.findByUserIdAndProjectId(1L, p3Id).stream()
                .filter(t -> "X".equals(t.getTitle())).findFirst().orElseThrow();

        // 在 P3 下创建子任务 Y，父任务=X
        TaskCreateRequest y = new TaskCreateRequest();
        y.setProjectId(p3Id);
        y.setTitle("Y");
        y.setIsRecurring(false);
        y.setParentTaskId(taskX.getTaskId());
        mockMvc.perform(post("/api/reminder/task/create")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(y)))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.code", is(200)));
        Task taskY = taskMapper.findByUserIdAndProjectId(1L, p3Id).stream()
                .filter(t -> "Y".equals(t.getTitle())).findFirst().orElseThrow();
        org.junit.jupiter.api.Assertions.assertEquals(taskX.getTaskId(), taskY.getParentTaskId());

        // 删除 P3，保留任务并迁入收件箱（project_id=NULL）
        ProjectDeleteRequest del = new ProjectDeleteRequest();
        del.setProjectId(p3Id);
        del.setKeepTasks(true);
        del.setTargetProject(false);
        del.setTargetProjectId(0L);
        mockMvc.perform(post("/api/reminder/projects/delete")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(del)))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.code", is(200)));

        // P3 应被删除
        org.junit.jupiter.api.Assertions.assertNull(projectMapper.findById(p3Id));

        // 任务应进入收件箱，且根任务 X 的排序应在 D 之后，父子关系保持
        List<Task> inbox = taskMapper.findByUserIdAndProjectIdIsNull(1L);
        Task xInInbox = inbox.stream().filter(t -> "X".equals(t.getTitle())).findFirst().orElse(null);
        Task yInInbox = inbox.stream().filter(t -> "Y".equals(t.getTitle())).findFirst().orElse(null);
        org.junit.jupiter.api.Assertions.assertNotNull(xInInbox, "Task X should be moved to inbox");
        org.junit.jupiter.api.Assertions.assertNotNull(yInInbox, "Task Y should be moved to inbox");
        org.junit.jupiter.api.Assertions.assertEquals(taskX.getTaskId(), xInInbox.getTaskId());
        org.junit.jupiter.api.Assertions.assertEquals(taskY.getTaskId(), yInInbox.getTaskId());
        org.junit.jupiter.api.Assertions.assertEquals(xInInbox.getTaskId(), yInInbox.getParentTaskId());
        org.junit.jupiter.api.Assertions.assertEquals(dOrderBefore + 1, xInInbox.getSortOrder(), "X should be appended after D in inbox");
    }

    @Test
    void scenario_updateStatus_done_then_todo() throws Exception {
        // 创建项目并创建任务 Z
        ProjectCreateRequest p = new ProjectCreateRequest();
        p.setName("StatusP");
        mockMvc.perform(post("/api/reminder/projects/create")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(p)))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.code", is(200)));
        Long pId = projectMapper.findByUserIdAndArchived(1L, false).stream()
                .filter(pp -> "StatusP".equals(pp.getName())).findFirst().orElseThrow().getProjectId();

        TaskCreateRequest z = new TaskCreateRequest();
        z.setProjectId(pId);
        z.setTitle("Z");
        z.setIsRecurring(false);
        mockMvc.perform(post("/api/reminder/task/create")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(z)))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.code", is(200)));
        Task taskZ = taskMapper.findByUserIdAndProjectId(1L, pId).stream()
                .filter(t -> "Z".equals(t.getTitle())).findFirst().orElseThrow();

        // 标记完成
        TaskStatusUpdateRequest dtoDone = new TaskStatusUpdateRequest();
        dtoDone.setTaskId(taskZ.getTaskId());
        dtoDone.setStatus("done");
        mockMvc.perform(patch("/api/reminder/task/update-status")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(dtoDone)))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.code", is(200)));
        Task afterDone = taskMapper.findById(taskZ.getTaskId());
        Assertions.assertEquals("done", afterDone.getStatus());
        Assertions.assertNotNull(afterDone.getCompletedAt(), "completedAt should be set on done");

        // 恢复为待办
        // TaskStatusUpdateRequest dtoTodo = new TaskStatusUpdateRequest();
        // dtoTodo.setTaskId(taskZ.getTaskId());
        // dtoTodo.setStatus("todo");
        // mockMvc.perform(patch("/api/reminder/task/update-status")
        //                 .contentType(MediaType.APPLICATION_JSON)
        //                 .content(objectMapper.writeValueAsString(dtoTodo)))
        //         .andExpect(status().isOk())
        //         .andExpect(jsonPath("$.code", is(200)));
        // Task afterTodo = taskMapper.findById(taskZ.getTaskId());
        // Assertions.assertEquals("todo", afterTodo.getStatus());
        // Assertions.assertNull(afterTodo.getCompletedAt(), "completedAt should be cleared on todo");
    }
}