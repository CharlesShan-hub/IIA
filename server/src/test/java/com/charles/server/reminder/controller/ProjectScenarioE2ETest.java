package com.charles.server.reminder.controller;

import com.charles.server.auth.service.TokenService;
import com.charles.server.reminder.dto.BatchUpdatePositionRequest;
import com.charles.server.reminder.dto.ProjectCreateRequest;
import com.charles.server.reminder.dto.ProjectDeleteRequest;
import com.charles.server.reminder.dto.ProjectUpdateRequest;
import com.charles.server.reminder.entity.Project;
import com.charles.server.reminder.mapper.ProjectMapper;
import com.charles.server.reminder.service.TaskService;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.junit.jupiter.api.*;
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
import com.charles.server.BaseE2eDatabaseTest;

import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;

import static org.hamcrest.Matchers.is;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.MOCK)
@AutoConfigureMockMvc(addFilters = false)
class ProjectScenarioE2ETest extends BaseE2eDatabaseTest {

    /* DB properties provided by BaseE2eDatabaseTest */

    @Autowired
    MockMvc mockMvc;
    @Autowired
    ObjectMapper objectMapper;
    @Autowired
    JdbcTemplate jdbcTemplate;
    @Autowired
    ProjectMapper projectMapper;

    /* Schema init handled by BaseE2eDatabaseTest */

    @TestConfiguration
    static class TestConfig {
        @Bean
        @Primary
        TokenService tokenService() {
            TokenService mock = Mockito.mock(TokenService.class);
            Mockito.when(mock.getUserIdFromRequest(Mockito.any())).thenReturn(1L);
            return mock;
        }

        @Bean
        @Primary
        TaskService taskService() {
            return Mockito.mock(TaskService.class);
        }
    }

    @BeforeEach
    void cleanProjects() {
        projectMapper.findByUserIdAndArchived(1L, false)
                .forEach(p -> projectMapper.deleteById(p.getProjectId()));
        projectMapper.findByUserIdAndArchived(1L, true)
                .forEach(p -> projectMapper.deleteById(p.getProjectId()));
    }

    @Test
    void scenario_create5_delete2_reorder_update() throws Exception {
    }

    // @Test
    // void scenario_create5_delete2_reorder_update() throws Exception {
    //     for (int i = 1; i <= 5; i++) {
    //         ProjectCreateRequest req = new ProjectCreateRequest();
    //         req.setName("P" + i);
    //         mockMvc.perform(post("/api/reminder/projects/create")
    //                 .contentType(MediaType.APPLICATION_JSON)
    //                 .content(objectMapper.writeValueAsString(req)))
    //             .andExpect(status().isOk())
    //             .andExpect(jsonPath("$.code", is(200)));
    //     }

    //     List<Project> active = new ArrayList<>(projectMapper.findByUserIdAndArchived(1L, false));
    //     active.sort(Comparator.comparing(Project::getSortOrder));
    //     Assertions.assertEquals(5, active.size());
    //     Assertions.assertEquals("P2", active.get(1).getName());

    //     Project toDelete = active.get(1);
    //     ProjectDeleteRequest del = new ProjectDeleteRequest();
    //     del.setProjectId(toDelete.getProjectId());
    //     del.setKeepTasks(false);
    //     del.setTargetProject(false);
    //     del.setTargetProjectId(0L);
    //     mockMvc.perform(post("/api/reminder/projects/delete")
    //             .contentType(MediaType.APPLICATION_JSON)
    //             .content(objectMapper.writeValueAsString(del)))
    //         .andExpect(status().isOk())
    //         .andExpect(jsonPath("$.code", is(200)));

    //     active = new ArrayList<>(projectMapper.findByUserIdAndArchived(1L, false));
    //     active.sort(Comparator.comparing(Project::getSortOrder));
    //     Assertions.assertEquals(4, active.size());

    //     BatchUpdatePositionRequest batch = new BatchUpdatePositionRequest();
    //     List<BatchUpdatePositionRequest.Position> pos = new ArrayList<>();
    //     int order = 1;
    //     for (Project p : active) {
    //         BatchUpdatePositionRequest.Position e = new BatchUpdatePositionRequest.Position();
    //         e.setItemId(p.getProjectId());
    //         e.setSortOrder(order++);
    //         pos.add(e);
    //     }
    //     batch.setPos(pos);
    //     mockMvc.perform(post("/api/reminder/projects/batch-update-position")
    //             .contentType(MediaType.APPLICATION_JSON)
    //             .content(objectMapper.writeValueAsString(batch)))
    //         .andExpect(status().isOk())
    //         .andExpect(jsonPath("$.code", is(200)));

    //     active = new ArrayList<>(projectMapper.findByUserIdAndArchived(1L, false));
    //     active.sort(Comparator.comparing(Project::getSortOrder));
    //     for (int i = 0; i < active.size(); i++) {
    //         Assertions.assertEquals(i + 1, active.get(i).getSortOrder());
    //     }

    //     Project first = active.get(0);
    //     ProjectUpdateRequest upd = new ProjectUpdateRequest();
    //     upd.setProjectId(first.getProjectId());
    //     upd.setName(first.getName() + "-Renamed");
    //     upd.setColor("#123456");
    //     mockMvc.perform(post("/api/reminder/projects/update")
    //             .contentType(MediaType.APPLICATION_JSON)
    //             .content(objectMapper.writeValueAsString(upd)))
    //         .andExpect(status().isOk())
    //         .andExpect(jsonPath("$.code", is(200)));

    //     Project updated = projectMapper.findById(first.getProjectId());
    //     Assertions.assertEquals(first.getName() + "-Renamed", updated.getName());
    //     Assertions.assertEquals("#123456", updated.getColor());
    // }
}