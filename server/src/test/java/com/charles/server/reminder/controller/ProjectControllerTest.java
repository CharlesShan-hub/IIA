package com.charles.server.reminder.controller;

import com.charles.server.auth.service.TokenService;
import com.charles.server.reminder.dto.*;
import com.charles.server.reminder.entity.Project;
import com.charles.server.reminder.service.ProjectService;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.ArgumentCaptor;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.context.annotation.Import;
import org.springframework.boot.test.context.TestConfiguration;
import org.springframework.context.annotation.Bean;
import org.mockito.Mockito;

import java.util.List;

import static org.mockito.ArgumentMatchers.*;
import static org.mockito.Mockito.*;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;
import java.util.Objects;

@WebMvcTest(ProjectController.class)
@AutoConfigureMockMvc(addFilters = false)
@Import(ProjectControllerTest.TestConfig.class)
class ProjectControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @Autowired
    private ProjectService projectService;

    @Autowired
    private TokenService tokenService;

    @TestConfiguration
    static class TestConfig {
        @Bean ProjectService projectService() { return Mockito.mock(ProjectService.class); }
        @Bean TokenService tokenService() { return Mockito.mock(TokenService.class); }
    }

    @Autowired
    private ObjectMapper objectMapper;

    @BeforeEach
    void setup() {
        when(tokenService.getUserIdFromRequest(any())).thenReturn(1L);
    }

    @Test
    void create_ok() throws Exception {
        ProjectCreateDTO dto = new ProjectCreateDTO();
        dto.setName("Inbox");
        dto.setColor("#409EFF");

        mockMvc.perform(post("/api/reminder/projects/create")
                        .contentType(MediaType.APPLICATION_JSON_VALUE)
                        .content(Objects.requireNonNull(objectMapper.writeValueAsString(dto))))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.code").value(200))
                .andExpect(result -> {
                    String c = result.getResponse().getContentAsString();
                    com.fasterxml.jackson.databind.JsonNode root = objectMapper.readTree(c);
                    org.junit.jupiter.api.Assertions.assertTrue(root.path("msg").asText().contains("Created"));
                });

        ArgumentCaptor<ProjectCreateDTO> captor = ArgumentCaptor.forClass(ProjectCreateDTO.class);
        verify(projectService).create(eq(1L), captor.capture());
        assert(captor.getValue().getName().equals("Inbox"));
    }

    @Test
    void update_ok() throws Exception {
        ProjectUpdateDTO dto = new ProjectUpdateDTO();
        dto.setProjectId(100L);
        dto.setName("Renamed");
        dto.setIsArchived(Boolean.TRUE);

        mockMvc.perform(post("/api/reminder/projects/update")
                        .contentType(MediaType.APPLICATION_JSON_VALUE)
                        .content(Objects.requireNonNull(objectMapper.writeValueAsString(dto))))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.code").value(200));

        verify(projectService).update(eq(1L), any(ProjectUpdateDTO.class));
    }

    @Test
    void delete_ok() throws Exception {
        ProjectDeleteDTO dto = new ProjectDeleteDTO();
        dto.setProjectId(200L);
        dto.setKeepTasks(false);
        dto.setTargetProject(false);
        dto.setTargetProjectId(0L);

        mockMvc.perform(post("/api/reminder/projects/delete")
                        .contentType(java.util.Objects.requireNonNull(MediaType.APPLICATION_JSON))
                        .content(java.util.Objects.requireNonNull(objectMapper.writeValueAsString(dto))))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.code").value(200));

        verify(projectService).delete(eq(1L), any(ProjectDeleteDTO.class));
    }

    @Test
    void batchUpdatePosition_ok() throws Exception {
        BatchUpdatePositionDTO.Position p1 = new BatchUpdatePositionDTO.Position(10L, 3);
        BatchUpdatePositionDTO.Position p2 = new BatchUpdatePositionDTO.Position(20L, 7);
        BatchUpdatePositionDTO req = new BatchUpdatePositionDTO();
        req.setPos(List.of(p1, p2));

        mockMvc.perform(post("/api/reminder/projects/batch-update-position")
                        .contentType(java.util.Objects.requireNonNull(MediaType.APPLICATION_JSON))
                        .content(java.util.Objects.requireNonNull(objectMapper.writeValueAsString(req))))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.code").value(200));

        verify(projectService).batchUpdatePosition(eq(1L), any(BatchUpdatePositionDTO.class));
    }

    @Test
    void get_true_ok() throws Exception {
        ProjectGetDTO dto = new ProjectGetDTO();
        dto.setIsAll(true);
        dto.setArchived(false);

        when(projectService.get(eq(1L), any(ProjectGetDTO.class)))
                .thenReturn(List.of(new Project()));

        mockMvc.perform(get("/api/reminder/projects/get-all")
                        .contentType(java.util.Objects.requireNonNull(MediaType.APPLICATION_JSON))
                        .content(java.util.Objects.requireNonNull(objectMapper.writeValueAsString(dto))))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.code").value(200))
                .andExpect(result -> {
                    String c = result.getResponse().getContentAsString();
                    com.fasterxml.jackson.databind.JsonNode root = objectMapper.readTree(c);
                    org.junit.jupiter.api.Assertions.assertFalse(root.path("data").isMissingNode() || root.path("data").isNull());
                });

        verify(projectService).get(eq(1L), any(ProjectGetDTO.class));
    }
}
