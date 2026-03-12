package com.charles.server.reminder.controller;

import com.charles.server.BaseE2eDatabaseTest;
import com.charles.server.auth.service.TokenService;
import com.charles.server.reminder.dto.ProjectCreateRequest;
import com.charles.server.reminder.dto.TaskCreateRequest;
import com.charles.server.reminder.dto.TaskDeleteRequest;
import com.charles.server.reminder.dto.ProjectDeleteRequest;
import com.charles.server.reminder.dto.TaskUpdateCompletedRequest;
import com.charles.server.reminder.dto.TaskUpdateAbandonedRequest;
import com.charles.server.reminder.entity.History;
import com.charles.server.reminder.entity.Project;
import com.charles.server.reminder.entity.Task;
import com.charles.server.reminder.mapper.HistoryMapper;
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
import org.springframework.context.ApplicationContext;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.test.web.servlet.MockMvc;

import java.util.Comparator;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;

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
    @Autowired JdbcTemplate jdbc;
    @Autowired ApplicationContext applicationContext;

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
                        .contentType(java.util.Objects.requireNonNull(MediaType.APPLICATION_JSON))
                        .content(java.util.Objects.requireNonNull(objectMapper.writeValueAsString(pReq))))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.code").value(200));

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
                        .contentType(java.util.Objects.requireNonNull(MediaType.APPLICATION_JSON))
                        .content(java.util.Objects.requireNonNull(objectMapper.writeValueAsString(t1))))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.code").value(200));

        TaskCreateRequest t2 = new TaskCreateRequest();
        t2.setProjectId(projectId);
        t2.setTitle("T2");
        t2.setIsRecurring(false);
        mockMvc.perform(post("/api/reminder/task/create")
                        .contentType(java.util.Objects.requireNonNull(MediaType.APPLICATION_JSON))
                        .content(java.util.Objects.requireNonNull(objectMapper.writeValueAsString(t2))))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.code").value(200));

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
                        .contentType(java.util.Objects.requireNonNull(MediaType.APPLICATION_JSON))
                        .content(java.util.Objects.requireNonNull(objectMapper.writeValueAsString(c1))))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.code").value(200));

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
                        .contentType(java.util.Objects.requireNonNull(MediaType.APPLICATION_JSON))
                        .content(java.util.Objects.requireNonNull(objectMapper.writeValueAsString(c2))))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.code").value(200));

        // 验证二级子任务存在
        List<Task> grandChildren = taskMapper.findByUserIdAndParentTaskId(1L, c1Entity.getTaskId());
        Assertions.assertTrue(grandChildren.stream().anyMatch(t -> "T1-1-1".equals(t.getTitle())), "Should contain grandchild 'T1-1-1'");

        // 4) 删除任务一（应级联删除其子任务），保留任务二
        TaskDeleteRequest del = new TaskDeleteRequest();
        del.setTaskId(first.getTaskId());
        mockMvc.perform(post("/api/reminder/task/delete")
                        .contentType(java.util.Objects.requireNonNull(MediaType.APPLICATION_JSON))
                        .content(java.util.Objects.requireNonNull(objectMapper.writeValueAsString(del))))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.code").value(200));

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
                        .contentType(java.util.Objects.requireNonNull(MediaType.APPLICATION_JSON))
                        .content(java.util.Objects.requireNonNull(objectMapper.writeValueAsString(p1Req))))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.code").value(200));

        ProjectCreateRequest p2Req = new ProjectCreateRequest();
        p2Req.setName("MoveP2");
        mockMvc.perform(post("/api/reminder/projects/create")
                        .contentType(java.util.Objects.requireNonNull(MediaType.APPLICATION_JSON))
                        .content(java.util.Objects.requireNonNull(objectMapper.writeValueAsString(p2Req))))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.code").value(200));

        List<Project> projectsAll = projectMapper.findByUserIdAndArchived(1L, false);
        Long p1Id = projectsAll.stream().filter(p -> "MoveP1".equals(p.getName())).findFirst().orElseThrow().getProjectId();
        Long p2Id = projectsAll.stream().filter(p -> "MoveP2".equals(p.getName())).findFirst().orElseThrow().getProjectId();

        // 在 P2 下预先创建任务 C，用于观察迁移后的 sort_order 关系
        TaskCreateRequest c = new TaskCreateRequest();
        c.setProjectId(p2Id);
        c.setTitle("C");
        c.setIsRecurring(false);
        mockMvc.perform(post("/api/reminder/task/create")
                        .contentType(java.util.Objects.requireNonNull(MediaType.APPLICATION_JSON))
                        .content(java.util.Objects.requireNonNull(objectMapper.writeValueAsString(c))))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.code").value(200));
        Task taskCBefore = taskMapper.findByUserIdAndProjectId(1L, p2Id).stream()
                .filter(t -> "C".equals(t.getTitle())).findFirst().orElseThrow();
        int cOrderBefore = taskCBefore.getSortOrder();

        // 在 P1 下创建任务 A
        TaskCreateRequest a = new TaskCreateRequest();
        a.setProjectId(p1Id);
        a.setTitle("A");
        a.setIsRecurring(false);
        mockMvc.perform(post("/api/reminder/task/create")
                        .contentType(java.util.Objects.requireNonNull(MediaType.APPLICATION_JSON))
                        .content(java.util.Objects.requireNonNull(objectMapper.writeValueAsString(a))))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.code").value(200));

        // 获取 A 的 id
        Task taskA = taskMapper.findByUserIdAndProjectId(1L, p1Id).stream()
                .filter(t -> "A".equals(t.getTitle())).findFirst().orElseThrow();
        

        // 在 P1 下创建任务 B，父任务=A
        TaskCreateRequest b = new TaskCreateRequest();
        b.setProjectId(p1Id);
        b.setTitle("B");
        b.setIsRecurring(false);
        b.setParentTaskId(taskA.getTaskId());
        mockMvc.perform(post("/api/reminder/task/create")
                        .contentType(java.util.Objects.requireNonNull(MediaType.APPLICATION_JSON))
                        .content(java.util.Objects.requireNonNull(objectMapper.writeValueAsString(b))))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.code").value(200));

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
                        .contentType(java.util.Objects.requireNonNull(MediaType.APPLICATION_JSON))
                        .content(java.util.Objects.requireNonNull(objectMapper.writeValueAsString(del))))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.code").value(200));

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
                        .contentType(java.util.Objects.requireNonNull(MediaType.APPLICATION_JSON))
                        .content(java.util.Objects.requireNonNull(objectMapper.writeValueAsString(d))))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.code").value(200));
        Task taskDBefore = taskMapper.findByUserIdAndProjectIdIsNull(1L).stream()
                .filter(t -> "D".equals(t.getTitle())).findFirst().orElseThrow();
        int dOrderBefore = taskDBefore.getSortOrder();

        // 创建项目 MoveP3
        ProjectCreateRequest p3Req = new ProjectCreateRequest();
        p3Req.setName("MoveP3");
        mockMvc.perform(post("/api/reminder/projects/create")
                        .contentType(java.util.Objects.requireNonNull(MediaType.APPLICATION_JSON))
                        .content(java.util.Objects.requireNonNull(objectMapper.writeValueAsString(p3Req))))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.code").value(200));
        Long p3Id = projectMapper.findByUserIdAndArchived(1L, false).stream()
                .filter(p -> "MoveP3".equals(p.getName())).findFirst().orElseThrow().getProjectId();

        // 在 P3 下创建根任务 X
        TaskCreateRequest x = new TaskCreateRequest();
        x.setProjectId(p3Id);
        x.setTitle("X");
        x.setIsRecurring(false);
        mockMvc.perform(post("/api/reminder/task/create")
                        .contentType(java.util.Objects.requireNonNull(MediaType.APPLICATION_JSON))
                        .content(java.util.Objects.requireNonNull(objectMapper.writeValueAsString(x))))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.code").value(200));
        Task taskX = taskMapper.findByUserIdAndProjectId(1L, p3Id).stream()
                .filter(t -> "X".equals(t.getTitle())).findFirst().orElseThrow();

        // 在 P3 下创建子任务 Y，父任务=X
        TaskCreateRequest y = new TaskCreateRequest();
        y.setProjectId(p3Id);
        y.setTitle("Y");
        y.setIsRecurring(false);
        y.setParentTaskId(taskX.getTaskId());
        mockMvc.perform(post("/api/reminder/task/create")
                        .contentType(java.util.Objects.requireNonNull(MediaType.APPLICATION_JSON))
                        .content(java.util.Objects.requireNonNull(objectMapper.writeValueAsString(y))))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.code").value(200));
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
                        .contentType(java.util.Objects.requireNonNull(MediaType.APPLICATION_JSON))
                        .content(java.util.Objects.requireNonNull(objectMapper.writeValueAsString(del))))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.code").value(200));

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
    void scenario_parent_completion_cancellation_with_abandoned_child() throws Exception {
        // 创建默认项目
        ProjectCreateRequest pReq = new ProjectCreateRequest();
        pReq.setName("TestProject");
        mockMvc.perform(post("/api/reminder/projects/create")
                        .contentType(java.util.Objects.requireNonNull(MediaType.APPLICATION_JSON))
                        .content(java.util.Objects.requireNonNull(objectMapper.writeValueAsString(pReq))))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.code").value(200));

        List<Project> projects = projectMapper.findByUserIdAndArchived(1L, false);
        Optional<Project> opt = projects.stream().filter(p -> "TestProject".equals(p.getName())).findFirst();
        Assertions.assertTrue(opt.isPresent(), "Project 'TestProject' should be created");
        Long projectId = opt.get().getProjectId();

        // 创建父任务A
        TaskCreateRequest taskAReq = new TaskCreateRequest();
        taskAReq.setProjectId(projectId);
        taskAReq.setTitle("Task A");
        taskAReq.setIsRecurring(false);
        mockMvc.perform(post("/api/reminder/task/create")
                        .contentType(java.util.Objects.requireNonNull(MediaType.APPLICATION_JSON))
                        .content(java.util.Objects.requireNonNull(objectMapper.writeValueAsString(taskAReq))))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.code").value(200));

        // 获取父任务A
        Task taskA = taskMapper.findByUserIdAndProjectId(1L, projectId).stream()
                .filter(t -> "Task A".equals(t.getTitle())).findFirst().orElseThrow();
        Long taskAId = taskA.getTaskId();

        // 创建子任务B
        TaskCreateRequest taskBReq = new TaskCreateRequest();
        taskBReq.setProjectId(projectId);
        taskBReq.setParentTaskId(taskAId);
        taskBReq.setTitle("Task B");
        taskBReq.setIsRecurring(false);
        mockMvc.perform(post("/api/reminder/task/create")
                        .contentType(java.util.Objects.requireNonNull(MediaType.APPLICATION_JSON))
                        .content(java.util.Objects.requireNonNull(objectMapper.writeValueAsString(taskBReq))))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.code").value(200));

        // 创建子任务C
        TaskCreateRequest taskCReq = new TaskCreateRequest();
        taskCReq.setProjectId(projectId);
        taskCReq.setParentTaskId(taskAId);
        taskCReq.setTitle("Task C");
        taskCReq.setIsRecurring(false);
        mockMvc.perform(post("/api/reminder/task/create")
                        .contentType(java.util.Objects.requireNonNull(MediaType.APPLICATION_JSON))
                        .content(java.util.Objects.requireNonNull(objectMapper.writeValueAsString(taskCReq))))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.code").value(200));

        // 创建子任务D
        TaskCreateRequest taskDReq = new TaskCreateRequest();
        taskDReq.setProjectId(projectId);
        taskDReq.setParentTaskId(taskAId);
        taskDReq.setTitle("Task D");
        taskDReq.setIsRecurring(false);
        mockMvc.perform(post("/api/reminder/task/create")
                        .contentType(java.util.Objects.requireNonNull(MediaType.APPLICATION_JSON))
                        .content(java.util.Objects.requireNonNull(objectMapper.writeValueAsString(taskDReq))))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.code").value(200));

        // 获取所有子任务
        Task taskB = taskMapper.findByUserIdAndParentTaskId(1L, taskAId).stream()
                .filter(t -> "Task B".equals(t.getTitle())).findFirst().orElseThrow();
        Long taskBId = taskB.getTaskId();
        
        Task taskC = taskMapper.findByUserIdAndParentTaskId(1L, taskAId).stream()
                .filter(t -> "Task C".equals(t.getTitle())).findFirst().orElseThrow();
        Long taskCId = taskC.getTaskId();
        
        Task taskD = taskMapper.findByUserIdAndParentTaskId(1L, taskAId).stream()
                .filter(t -> "Task D".equals(t.getTitle())).findFirst().orElseThrow();
        Long taskDId = taskD.getTaskId();

        // 验证初始状态
        Assertions.assertFalse(taskA.getIsCompleted(), "任务A初始应为未完成");
        Assertions.assertFalse(taskB.getIsCompleted(), "任务B初始应为未完成");
        Assertions.assertFalse(taskC.getIsCompleted(), "任务C初始应为未完成");
        Assertions.assertFalse(taskD.getIsCompleted(), "任务D初始应为未完成");
        Assertions.assertFalse(taskD.getIsAbandoned(), "任务D初始应为未废弃");

        // 步骤1：将任务D设置为废弃
        TaskUpdateAbandonedRequest abandonD = new TaskUpdateAbandonedRequest();
        abandonD.setTaskId(taskDId);
        abandonD.setIsAbandoned(true);
        mockMvc.perform(patch("/api/reminder/task/update-abandoned")
                        .contentType(java.util.Objects.requireNonNull(MediaType.APPLICATION_JSON))
                        .content(java.util.Objects.requireNonNull(objectMapper.writeValueAsString(abandonD))))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.code").value(200));

        // 验证任务D已废弃
        Task updatedD = taskMapper.findById(taskDId);
        Assertions.assertTrue(updatedD.getIsAbandoned(), "任务D应已废弃");
        Assertions.assertFalse(updatedD.getIsCompleted(), "废弃的任务D不应是完成状态");

        // 步骤2：将任务C设置为完成
        TaskUpdateCompletedRequest completeC = new TaskUpdateCompletedRequest();
        completeC.setTaskId(taskCId);
        completeC.setIsCompleted(true);
        mockMvc.perform(patch("/api/reminder/task/update-completed")
                        .contentType(java.util.Objects.requireNonNull(MediaType.APPLICATION_JSON))
                        .content(java.util.Objects.requireNonNull(objectMapper.writeValueAsString(completeC))))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.code").value(200));

        // 验证任务C已完成
        Task updatedC = taskMapper.findById(taskCId);
        Assertions.assertTrue(updatedC.getIsCompleted(), "任务C应已完成");
        Assertions.assertNotNull(updatedC.getCompletedAt(), "任务C完成时间不应为空");

        // 步骤3：将父任务A设置为完成（应该同步B，但不会影响已废弃的D和已完成的C）
        TaskUpdateCompletedRequest completeA = new TaskUpdateCompletedRequest();
        completeA.setTaskId(taskAId);
        completeA.setIsCompleted(true);
        mockMvc.perform(patch("/api/reminder/task/update-completed")
                        .contentType(java.util.Objects.requireNonNull(MediaType.APPLICATION_JSON))
                        .content(java.util.Objects.requireNonNull(objectMapper.writeValueAsString(completeA))))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.code").value(200));

        // 验证任务A已完成
        Task updatedA = taskMapper.findById(taskAId);
        Assertions.assertTrue(updatedA.getIsCompleted(), "任务A应已完成");
        Assertions.assertNotNull(updatedA.getCompletedAt(), "任务A完成时间不应为空");

        // 验证任务B已同步完成
        Task updatedB = taskMapper.findById(taskBId);
        Assertions.assertTrue(updatedB.getIsCompleted(), "任务B应已同步完成");
        Assertions.assertNotNull(updatedB.getCompletedAt(), "任务B完成时间不应为空");

        // 验证任务C状态不变（之前已完成）
        Task recheckedC = taskMapper.findById(taskCId);
        Assertions.assertTrue(recheckedC.getIsCompleted(), "任务C应保持完成状态");

        // 验证任务D状态不变（已废弃）
        Task recheckedD = taskMapper.findById(taskDId);
        Assertions.assertTrue(recheckedD.getIsAbandoned(), "任务D应保持废弃状态");
        Assertions.assertFalse(recheckedD.getIsCompleted(), "废弃的任务D不应是完成状态");

        // 获取历史记录Mapper
        HistoryMapper historyMapper = applicationContext.getBean(HistoryMapper.class);
        
        // 获取任务A完成时的操作ID
        List<History> aHistories = historyMapper.findByTaskId(taskAId);
        Assertions.assertEquals(1, aHistories.size(), "任务A应有1条历史记录");
        Long aOperationId = aHistories.get(0).getOperationId();
        
        // 获取任务B的历史记录
        List<History> bHistories = historyMapper.findByTaskId(taskBId);
        Assertions.assertEquals(1, bHistories.size(), "任务B应有1条历史记录");
        Long bOperationId = bHistories.get(0).getOperationId();
        
        // 验证任务A和任务B使用相同的操作ID（表示是同一个操作批次）
        Assertions.assertEquals(aOperationId, bOperationId, "任务A和任务B应使用相同的操作ID");

        // 步骤4：将任务B取消完成
        TaskUpdateCompletedRequest uncompleteB = new TaskUpdateCompletedRequest();
        uncompleteB.setTaskId(taskBId);
        uncompleteB.setIsCompleted(false);
        mockMvc.perform(patch("/api/reminder/task/update-completed")
                        .contentType(java.util.Objects.requireNonNull(MediaType.APPLICATION_JSON))
                        .content(java.util.Objects.requireNonNull(objectMapper.writeValueAsString(uncompleteB))))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.code").value(200));

        // 验证任务B已取消完成
        Task uncompletedB = taskMapper.findById(taskBId);
        Assertions.assertFalse(uncompletedB.getIsCompleted(), "任务B应已取消完成");
        Assertions.assertNull(uncompletedB.getCompletedAt(), "任务B完成时间应被清空");

        // 步骤5：将任务B重新完成（单独操作）
        TaskUpdateCompletedRequest reCompleteB = new TaskUpdateCompletedRequest();
        reCompleteB.setTaskId(taskBId);
        reCompleteB.setIsCompleted(true);
        mockMvc.perform(patch("/api/reminder/task/update-completed")
                        .contentType(java.util.Objects.requireNonNull(MediaType.APPLICATION_JSON))
                        .content(java.util.Objects.requireNonNull(objectMapper.writeValueAsString(reCompleteB))))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.code").value(200));

        // 验证任务B已重新完成
        Task recompletedB = taskMapper.findById(taskBId);
        Assertions.assertTrue(recompletedB.getIsCompleted(), "任务B应已重新完成");
        Assertions.assertNotNull(recompletedB.getCompletedAt(), "任务B完成时间不应为空");

        // 步骤6：将父任务A取消完成
        TaskUpdateCompletedRequest uncompleteA = new TaskUpdateCompletedRequest();
        uncompleteA.setTaskId(taskAId);
        uncompleteA.setIsCompleted(false);
        mockMvc.perform(patch("/api/reminder/task/update-completed")
                        .contentType(java.util.Objects.requireNonNull(MediaType.APPLICATION_JSON))
                        .content(java.util.Objects.requireNonNull(objectMapper.writeValueAsString(uncompleteA))))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.code").value(200));

        // 验证任务A已取消完成
        Task uncompletedA = taskMapper.findById(taskAId);
        Assertions.assertFalse(uncompletedA.getIsCompleted(), "任务A应已取消完成");
        Assertions.assertNull(uncompletedA.getCompletedAt(), "任务A完成时间应被清空");

        // 验证任务B被再次连带取消完成
        Task finalB = taskMapper.findById(taskBId);
        Assertions.assertFalse(finalB.getIsCompleted(), "任务B应被再次连带取消完成");
        Assertions.assertNull(finalB.getCompletedAt(), "任务B完成时间应被清空");

        // 验证任务C状态不变（之前已完成）
        Task finalC = taskMapper.findById(taskCId);
        Assertions.assertTrue(finalC.getIsCompleted(), "任务C应保持完成状态");
        Assertions.assertNotNull(finalC.getCompletedAt(), "任务C完成时间不应为空");

        // 验证任务D状态不变（已废弃）
        Task finalD = taskMapper.findById(taskDId);
        Assertions.assertTrue(finalD.getIsAbandoned(), "任务D应保持废弃状态");
        Assertions.assertFalse(finalD.getIsCompleted(), "废弃的任务D不应是完成状态");

        System.out.println("测试通过！验证了：");
        System.out.println("1. 废弃的任务不会被父任务完成操作影响");
        System.out.println("2. 已单独完成的任务不会被父任务完成操作影响");
        System.out.println("3. 父任务完成时会同步未完成的子任务");
        System.out.println("4. 父任务取消完成时，只有被该父任务完成操作影响的子任务才会被取消完成");
        System.out.println("5. 操作批次跟踪正确：任务A和任务B使用相同的操作ID");
    }
}