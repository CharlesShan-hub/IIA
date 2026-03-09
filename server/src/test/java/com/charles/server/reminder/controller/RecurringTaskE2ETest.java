package com.charles.server.reminder.controller;

import com.charles.server.BaseE2eDatabaseTest;
import com.charles.server.auth.service.TokenService;
import com.charles.server.reminder.dto.TaskCreateRequest;
import com.charles.server.reminder.dto.TaskUpdateRequest;
import com.charles.server.reminder.entity.Task;
import com.charles.server.reminder.entity.Recurrence;
import com.charles.server.reminder.mapper.TaskMapper;
import com.charles.server.reminder.mapper.RecurrenceMapper;
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

import java.time.LocalDateTime;

import static org.hamcrest.Matchers.is;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.MOCK)
@AutoConfigureMockMvc(addFilters = false)
class RecurringTaskE2ETest extends BaseE2eDatabaseTest {

    @Autowired MockMvc mockMvc;
    @Autowired ObjectMapper objectMapper;
    @Autowired TaskMapper taskMapper;
    @Autowired RecurrenceMapper recurrenceMapper;

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
    void should_create_monthly_recurring_task_with_schedule() throws Exception {
        LocalDateTime next = LocalDateTime.of(2026, 4, 1, 7, 0);

        TaskCreateRequest req = new TaskCreateRequest();
        req.setTitle("R-MONTHLY");
        req.setIsRecurring(true);
        req.setRecurrenceCategory("monthly");
        req.setRecurrenceInterval(1);
        req.setRecurrenceCount(6);
        req.setRecurrenceNextTime(next);
        req.setRecurrenceSchedule("[1,15]"); // 每月1号和15号

        mockMvc.perform(post("/api/reminder/task/create")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(req)))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.code", is(200)));

        Task created = taskMapper.findByUserIdAndProjectIdIsNull(1L).stream()
                .filter(t -> "R-MONTHLY".equals(t.getTitle()))
                .findFirst().orElseThrow();
        Assertions.assertEquals(Boolean.TRUE, created.getIsRecurring());

        Recurrence r = recurrenceMapper.findByTaskId(created.getTaskId());
        Assertions.assertNotNull(r);
        Assertions.assertEquals("monthly", r.getCategory());
        Assertions.assertEquals(1, r.getInterval());
        Assertions.assertEquals(6, r.getCount());
        Assertions.assertEquals(next, r.getNextTime());
        // Assertions.assertEquals("[1,15]", r.getSchedule());

        // Delete the recurring task and verify cascade deletion of recurrence
        com.charles.server.reminder.dto.TaskDeleteRequest del = new com.charles.server.reminder.dto.TaskDeleteRequest();
        del.setTaskId(created.getTaskId());
        mockMvc.perform(post("/api/reminder/task/delete")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(del)))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.code", is(200)));
        Assertions.assertNull(taskMapper.findById(created.getTaskId()));
        Assertions.assertNull(recurrenceMapper.findByTaskId(created.getTaskId()));
    }

    @Test
    void should_toggle_single_and_recurring_via_update() throws Exception {
        LocalDateTime nextA = LocalDateTime.of(2026, 4, 2, 8, 0);
        LocalDateTime nextB = LocalDateTime.of(2026, 4, 3, 9, 0);

        // Create normal task A
        TaskCreateRequest a = new TaskCreateRequest();
        a.setTitle("TASK-A");
        a.setIsRecurring(false);
        mockMvc.perform(post("/api/reminder/task/create")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(a)))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.code", is(200)));

        // Create recurring task B (daily)
        TaskCreateRequest b = new TaskCreateRequest();
        b.setTitle("TASK-B");
        b.setIsRecurring(true);
        b.setRecurrenceCategory("days");
        b.setRecurrenceInterval(1);
        b.setRecurrenceCount(5);
        b.setRecurrenceNextTime(nextB);
        mockMvc.perform(post("/api/reminder/task/create")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(b)))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.code", is(200)));

        Task taskA = taskMapper.findByUserIdAndProjectIdIsNull(1L).stream()
                .filter(t -> "TASK-A".equals(t.getTitle()))
                .findFirst().orElseThrow();
        Task taskB = taskMapper.findByUserIdAndProjectIdIsNull(1L).stream()
                .filter(t -> "TASK-B".equals(t.getTitle()))
                .findFirst().orElseThrow();
        Assertions.assertEquals(Boolean.FALSE, taskA.getIsRecurring());
        Assertions.assertEquals(Boolean.TRUE, taskB.getIsRecurring());
        Assertions.assertNotNull(recurrenceMapper.findByTaskId(taskB.getTaskId()));

        // A: single -> recurring (weekly)
        TaskUpdateRequest upA = new TaskUpdateRequest();
        upA.setTaskId(taskA.getTaskId());
        upA.setTitle("TASK-A-changed");
        upA.setIsRecurring(true);
        upA.setRecurrenceCategory("weekly");
        upA.setRecurrenceInterval(1);
        upA.setRecurrenceCount(4);
        upA.setRecurrenceNextTime(nextA);
        upA.setRecurrenceSchedule("[1,3,5]");
        mockMvc.perform(post("/api/reminder/task/update")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(upA)))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.code", is(200)));

        // B: recurring -> single
        com.charles.server.reminder.dto.TaskUpdateRequest upB = new com.charles.server.reminder.dto.TaskUpdateRequest();
        upB.setTaskId(taskB.getTaskId());
        upB.setIsRecurring(false);
        mockMvc.perform(post("/api/reminder/task/update")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(upB)))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.code", is(200)));

        // Assertions
        Task updatedA = taskMapper.findById(taskA.getTaskId());
        Task updatedB = taskMapper.findById(taskB.getTaskId());
        Assertions.assertEquals(Boolean.TRUE, updatedA.getIsRecurring());
        Assertions.assertEquals(Boolean.FALSE, updatedB.getIsRecurring());
        Recurrence aRec = recurrenceMapper.findByTaskId(taskA.getTaskId());
        Assertions.assertNotNull(aRec);
        Assertions.assertEquals("weekly", aRec.getCategory());
        Assertions.assertEquals(Integer.valueOf(1), aRec.getInterval());
        Assertions.assertEquals(Integer.valueOf(4), aRec.getCount());
        Assertions.assertEquals(nextA, aRec.getNextTime());
        Assertions.assertNull(recurrenceMapper.findByTaskId(taskB.getTaskId()));
    }

}
