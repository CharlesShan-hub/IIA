package com.charles.server.reminder.controller;

import com.charles.server.BaseE2eDatabaseTest;
import com.charles.server.auth.service.TokenService;
import com.charles.server.reminder.dto.TagCreateRequest;
import com.charles.server.reminder.dto.TaskCreateRequest;
import com.charles.server.reminder.dto.TaskTagCreateRequest;
import com.charles.server.reminder.dto.TaskTagDeleteRequest;
import com.charles.server.reminder.dto.TaskTagBatchCreateRequest;
import com.charles.server.reminder.dto.TaskTagBatchDeleteRequest;
import com.charles.server.reminder.entity.Tag;
import com.charles.server.reminder.entity.Task;
import com.charles.server.reminder.mapper.TagMapper;
import com.charles.server.reminder.mapper.TaskMapper;
import com.charles.server.reminder.mapper.TaskTagMapper;
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
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.test.web.servlet.MockMvc;

import java.util.List;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.MOCK)
@AutoConfigureMockMvc(addFilters = false)
class TaskTagScenarioE2ETest extends BaseE2eDatabaseTest {

    @Autowired MockMvc mockMvc;
    @Autowired ObjectMapper objectMapper;
    @Autowired TaskMapper taskMapper;
    @Autowired TagMapper tagMapper;
    @Autowired TaskTagMapper taskTagMapper;
    @Autowired JdbcTemplate jdbc;

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
    void should_handle_task_tag_cascade_create_and_delete() throws Exception {
        // Create parent tasks 1, 2, 3, 4
        createTask("1", null);
        createTask("2", null);
        createTask("3", null);
        createTask("4", null);

        Long id1 = taskIdByTitle("1");
        Long id2 = taskIdByTitle("2");
        Long id3 = taskIdByTitle("3");
        Long id4 = taskIdByTitle("4");

        // Create child tasks 1s(child of 1), 2s(child of 2), 3s(child of 3), 4s(child of 4)
        createTask("1s", id1);
        createTask("2s", id2);
        createTask("3s", id3);
        createTask("4s", id4);

        Long id1s = taskIdByTitle("1s");
        Long id2s = taskIdByTitle("2s");
        Long id3s = taskIdByTitle("3s");
        Long id4s = taskIdByTitle("4s");

        // Create two tags: Tag-1, Tag-2
        createTag("Tag-1", "#FFAA00");
        createTag("Tag-2", "#00AAFF");
        Long tag1 = tagIdByName("Tag-1");
        Long tag2 = tagIdByName("Tag-2");

        // Task 1 add Tag-1 without cascade
        TaskTagCreateRequest add1 = new TaskTagCreateRequest();
        add1.setTaskId(id1);
        add1.setTagId(tag1);
        add1.setIncludeSubtasks(false);
        mockMvc.perform(post("/api/reminder/task-tags/create")
                        .contentType(java.util.Objects.requireNonNull(MediaType.APPLICATION_JSON))
                        .content(java.util.Objects.requireNonNull(objectMapper.writeValueAsString(add1))))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.code").value(200));

        // Task 2 add Tag-1 and Tag-2 with cascade
        TaskTagCreateRequest add31 = new TaskTagCreateRequest();
        add31.setTaskId(id2);
        add31.setTagId(tag1);
        add31.setIncludeSubtasks(true);
        mockMvc.perform(post("/api/reminder/task-tags/create")
                        .contentType(java.util.Objects.requireNonNull(MediaType.APPLICATION_JSON))
                        .content(java.util.Objects.requireNonNull(objectMapper.writeValueAsString(add31))))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.code").value(200));

        TaskTagCreateRequest add32 = new TaskTagCreateRequest();
        add32.setTaskId(id2);
        add32.setTagId(tag2);
        add32.setIncludeSubtasks(true);
        mockMvc.perform(post("/api/reminder/task-tags/create")
                        .contentType(java.util.Objects.requireNonNull(MediaType.APPLICATION_JSON))
                        .content(java.util.Objects.requireNonNull(objectMapper.writeValueAsString(add32))))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.code").value(200));

        // Task 3 and 4 add Tag-2 with cascade
        TaskTagCreateRequest add22 = new TaskTagCreateRequest();
        add22.setTaskId(id3);
        add22.setTagId(tag2);
        add22.setIncludeSubtasks(true);
        mockMvc.perform(post("/api/reminder/task-tags/create")
                        .contentType(java.util.Objects.requireNonNull(MediaType.APPLICATION_JSON))
                        .content(java.util.Objects.requireNonNull(objectMapper.writeValueAsString(add22))))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.code").value(200));

        TaskTagCreateRequest add42 = new TaskTagCreateRequest();
        add42.setTaskId(id4);
        add42.setTagId(tag2);
        add42.setIncludeSubtasks(true);
        mockMvc.perform(post("/api/reminder/task-tags/create")
                        .contentType(java.util.Objects.requireNonNull(MediaType.APPLICATION_JSON))
                        .content(java.util.Objects.requireNonNull(objectMapper.writeValueAsString(add42))))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.code").value(200));

        // Assertions before deletion
        Assertions.assertNotNull(taskTagMapper.findByTaskIdAndTagId(id1, tag1));
        Assertions.assertNull(taskTagMapper.findByTaskIdAndTagId(id1s, tag1)); // no cascade for 1

        Assertions.assertNotNull(taskTagMapper.findByTaskIdAndTagId(id2, tag1));
        Assertions.assertNotNull(taskTagMapper.findByTaskIdAndTagId(id2s, tag1));
        Assertions.assertNotNull(taskTagMapper.findByTaskIdAndTagId(id2, tag2));
        Assertions.assertNotNull(taskTagMapper.findByTaskIdAndTagId(id2s, tag2));

        Assertions.assertNotNull(taskTagMapper.findByTaskIdAndTagId(id3, tag2));
        Assertions.assertNotNull(taskTagMapper.findByTaskIdAndTagId(id3s, tag2));
        Assertions.assertNotNull(taskTagMapper.findByTaskIdAndTagId(id4, tag2));
        Assertions.assertNotNull(taskTagMapper.findByTaskIdAndTagId(id4s, tag2));

        // Delete: Task 3 remove Tag-2 without cascade (only 3)
        TaskTagDeleteRequest del3 = new TaskTagDeleteRequest();
        del3.setTaskId(id3);
        del3.setTagId(tag2);
        del3.setIncludeSubtasks(false);
        mockMvc.perform(post("/api/reminder/task-tags/delete")
                        .contentType(java.util.Objects.requireNonNull(MediaType.APPLICATION_JSON))
                        .content(java.util.Objects.requireNonNull(objectMapper.writeValueAsString(del3))))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.code").value(200));

        // Delete: Task 4 remove Tag-2 with cascade (4 and 4s)
        TaskTagDeleteRequest del4 = new TaskTagDeleteRequest();
        del4.setTaskId(id4);
        del4.setTagId(tag2);
        del4.setIncludeSubtasks(true);
        mockMvc.perform(post("/api/reminder/task-tags/delete")
                        .contentType(java.util.Objects.requireNonNull(MediaType.APPLICATION_JSON))
                        .content(java.util.Objects.requireNonNull(objectMapper.writeValueAsString(del4))))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.code").value(200));

        // Assertions after deletion
        Assertions.assertNull(taskTagMapper.findByTaskIdAndTagId(id3, tag2));
        Assertions.assertNotNull(taskTagMapper.findByTaskIdAndTagId(id3s, tag2)); // child remains

        Assertions.assertNull(taskTagMapper.findByTaskIdAndTagId(id4, tag2));
        Assertions.assertNull(taskTagMapper.findByTaskIdAndTagId(id4s, tag2)); // child removed
    }

    private void createTask(String title, Long parentId) throws Exception {
        TaskCreateRequest req = new TaskCreateRequest();
        req.setTitle(title);
        req.setIsRecurring(false);
        if (parentId != null) req.setParentTaskId(parentId);
        mockMvc.perform(post("/api/reminder/task/create")
                        .contentType(java.util.Objects.requireNonNull(MediaType.APPLICATION_JSON))
                        .content(java.util.Objects.requireNonNull(objectMapper.writeValueAsString(req))))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.code").value(200));
    }

    private void createTag(String name, String color) throws Exception {
        TagCreateRequest req = new TagCreateRequest();
        req.setName(name);
        req.setColor(color);
        mockMvc.perform(post("/api/reminder/tags/create")
                        .contentType(java.util.Objects.requireNonNull(MediaType.APPLICATION_JSON))
                        .content(java.util.Objects.requireNonNull(objectMapper.writeValueAsString(req))))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.code").value(200));
    }

    private Long taskIdByTitle(String title) {
        return taskMapper.findByUserIdAndProjectIdIsNull(1L).stream()
                .filter(t -> title.equals(t.getTitle()))
                .map(Task::getTaskId)
                .findFirst()
                .orElseThrow();
    }

    private Long tagIdByName(String name) {
        return tagMapper.findByUserId(1L).stream()
                .filter(t -> name.equals(t.getName()))
                .map(Tag::getTagId)
                .findFirst()
                .orElseThrow();
    }

    @Test
    void should_handle_batch_cascade_and_selective_deletes() throws Exception {
        createTask("A", null);
        Long idA = taskIdByTitle("A");
        createTask("B", idA);
        Long idB = taskIdByTitle("B");

        createTag("1", "#111111");
        createTag("2", "#222222");
        createTag("3", "#333333");
        createTag("4", "#444444");
        Long t1 = tagIdByName("1");
        Long t2 = tagIdByName("2");
        Long t3 = tagIdByName("3");
        Long t4 = tagIdByName("4");

        TaskTagBatchCreateRequest bc = new TaskTagBatchCreateRequest();
        bc.setTaskId(idA);
        bc.setTagIds(List.of(t1, t2, t3, t4));
        bc.setIncludeSubtasks(true);
        mockMvc.perform(post("/api/reminder/task-tags/batch-create")
                        .contentType(java.util.Objects.requireNonNull(MediaType.APPLICATION_JSON))
                        .content(java.util.Objects.requireNonNull(objectMapper.writeValueAsString(bc))))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.code").value(200));

        Assertions.assertNotNull(taskTagMapper.findByTaskIdAndTagId(idA, t1));
        Assertions.assertNotNull(taskTagMapper.findByTaskIdAndTagId(idA, t2));
        Assertions.assertNotNull(taskTagMapper.findByTaskIdAndTagId(idA, t3));
        Assertions.assertNotNull(taskTagMapper.findByTaskIdAndTagId(idA, t4));
        Assertions.assertNotNull(taskTagMapper.findByTaskIdAndTagId(idB, t1));
        Assertions.assertNotNull(taskTagMapper.findByTaskIdAndTagId(idB, t2));
        Assertions.assertNotNull(taskTagMapper.findByTaskIdAndTagId(idB, t3));
        Assertions.assertNotNull(taskTagMapper.findByTaskIdAndTagId(idB, t4));

        TaskTagBatchDeleteRequest bd = new TaskTagBatchDeleteRequest();
        bd.setTaskId(idA);
        bd.setTagIds(List.of(t1, t2));
        bd.setIncludeSubtasks(true);
        mockMvc.perform(post("/api/reminder/task-tags/batch-delete")
                        .contentType(java.util.Objects.requireNonNull(MediaType.APPLICATION_JSON))
                        .content(java.util.Objects.requireNonNull(objectMapper.writeValueAsString(bd))))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.code").value(200));

        TaskTagDeleteRequest delB3 = new TaskTagDeleteRequest();
        delB3.setTaskId(idB);
        delB3.setTagId(t3);
        delB3.setIncludeSubtasks(false);
        mockMvc.perform(post("/api/reminder/task-tags/delete")
                        .contentType(java.util.Objects.requireNonNull(MediaType.APPLICATION_JSON))
                        .content(java.util.Objects.requireNonNull(objectMapper.writeValueAsString(delB3))))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.code").value(200));

        TaskTagDeleteRequest delA4 = new TaskTagDeleteRequest();
        delA4.setTaskId(idA);
        delA4.setTagId(t4);
        delA4.setIncludeSubtasks(false);
        mockMvc.perform(post("/api/reminder/task-tags/delete")
                        .contentType(java.util.Objects.requireNonNull(MediaType.APPLICATION_JSON))
                        .content(java.util.Objects.requireNonNull(objectMapper.writeValueAsString(delA4))))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.code").value(200));

        Assertions.assertNull(taskTagMapper.findByTaskIdAndTagId(idA, t1));
        Assertions.assertNull(taskTagMapper.findByTaskIdAndTagId(idA, t2));
        Assertions.assertNotNull(taskTagMapper.findByTaskIdAndTagId(idA, t3));
        Assertions.assertNull(taskTagMapper.findByTaskIdAndTagId(idA, t4));

        Assertions.assertNull(taskTagMapper.findByTaskIdAndTagId(idB, t1));
        Assertions.assertNull(taskTagMapper.findByTaskIdAndTagId(idB, t2));
        Assertions.assertNull(taskTagMapper.findByTaskIdAndTagId(idB, t3));
        Assertions.assertNotNull(taskTagMapper.findByTaskIdAndTagId(idB, t4));
    }

    @Test
    void scenario_task_tag_error_task_not_found() throws Exception {
        createTag("E", "#EEEEEE");
        Long tagId = tagIdByName("E");

        TaskTagCreateRequest dto = new TaskTagCreateRequest();
        dto.setTaskId(999999L);
        dto.setTagId(tagId);
        dto.setIncludeSubtasks(false);
        mockMvc.perform(post("/api/reminder/task-tags/create")
                        .contentType(java.util.Objects.requireNonNull(MediaType.APPLICATION_JSON))
                        .content(java.util.Objects.requireNonNull(objectMapper.writeValueAsString(dto))))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.code").value(404));
    }

    @Test
    void scenario_task_tag_error_task_permission_denied() throws Exception {
        createTag("F", "#FFFFFF");
        Long tagId = tagIdByName("F");

        jdbc.update(
                "INSERT INTO iia_auth(user_id, password_hash) VALUES (?, ?) " +
                        "ON DUPLICATE KEY UPDATE password_hash = VALUES(password_hash)",
                2L,
                "x"
        );

        Task other = new Task();
        other.setUserId(2L);
        other.setTitle("OTHER_TASK");
        other.setIsRecurring(false);
        other.setSortOrder(1);
        other.setPriority("none");
        taskMapper.insert(other);

        TaskTagCreateRequest dto = new TaskTagCreateRequest();
        dto.setTaskId(other.getTaskId());
        dto.setTagId(tagId);
        dto.setIncludeSubtasks(false);
        mockMvc.perform(post("/api/reminder/task-tags/create")
                        .contentType(java.util.Objects.requireNonNull(MediaType.APPLICATION_JSON))
                        .content(java.util.Objects.requireNonNull(objectMapper.writeValueAsString(dto))))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.code").value(403));
    }
}

// select task.title, tag.name from reminder_task_tag tt join reminder_tag tag on tt.tag_id = tag.tag_id join reminder_task task on task.task_id = tt.task_id;
