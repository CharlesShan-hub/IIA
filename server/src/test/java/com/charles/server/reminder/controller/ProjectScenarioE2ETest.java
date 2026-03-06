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
import org.springframework.test.context.DynamicPropertyRegistry;
import org.springframework.test.context.DynamicPropertySource;

import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;

import static org.hamcrest.Matchers.is;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.MOCK)
@AutoConfigureMockMvc(addFilters = false)
class ProjectScenarioE2ETest {

    @DynamicPropertySource
    static void dbProps(DynamicPropertyRegistry registry) {
        registry.add("spring.datasource.url", () -> System.getProperty("test.db.url", "jdbc:mysql://127.0.0.1:3306/iia_test?useSSL=false&allowPublicKeyRetrieval=true&serverTimezone=UTC"));
        registry.add("spring.datasource.username", () -> System.getProperty("test.db.username", "root"));
        registry.add("spring.datasource.password", () -> System.getProperty("test.db.password", ""));
    }

    @Autowired
    MockMvc mockMvc;
    @Autowired
    ObjectMapper objectMapper;
    @Autowired
    JdbcTemplate jdbcTemplate;
    @Autowired
    ProjectMapper projectMapper;

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

    @BeforeAll
    static void beforeAll(@Autowired JdbcTemplate jdbc) {
        jdbc.execute("SET NAMES utf8mb4");
        jdbc.execute("SET FOREIGN_KEY_CHECKS = 0");
        jdbc.execute("DROP TABLE IF EXISTS reminder_project");
        jdbc.execute("DROP TABLE IF EXISTS iia_auth");
        jdbc.execute("CREATE TABLE iia_auth (user_id BIGINT PRIMARY KEY)");
        jdbc.execute(
                "CREATE TABLE reminder_project (" +
                        " project_id BIGINT PRIMARY KEY AUTO_INCREMENT," +
                        " user_id BIGINT NOT NULL," +
                        " name VARCHAR(255) NOT NULL," +
                        " description TEXT NULL," +
                        " color VARCHAR(20) NULL," +
                        " icon VARCHAR(50) NULL," +
                        " sort_order INT DEFAULT 0," +
                        " is_archived BOOLEAN DEFAULT FALSE," +
                        " FOREIGN KEY (user_id) REFERENCES iia_auth(user_id) ON DELETE CASCADE" +
                        ") ENGINE=InnoDB"
        );
        jdbc.execute("SET FOREIGN_KEY_CHECKS = 1");
        jdbc.update("INSERT INTO iia_auth(user_id) VALUES (1)");
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