package com.charles.server.reminder.controller;

import com.charles.server.BaseE2eDatabaseTest;
import com.charles.server.auth.service.TokenService;
import com.charles.server.reminder.dto.TagCreateRequest;
import com.charles.server.reminder.dto.TagDeleteRequest;
import com.charles.server.reminder.dto.TagUpdateRequest;
import com.charles.server.reminder.entity.Tag;
import com.charles.server.reminder.mapper.TagMapper;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.BeforeEach;
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
import java.util.List;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.put;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.MOCK)
@AutoConfigureMockMvc(addFilters = false)
class TagControllerTest extends BaseE2eDatabaseTest {

    @Autowired MockMvc mockMvc;
    @Autowired ObjectMapper objectMapper;
    @Autowired TagMapper tagMapper;

    @TestConfiguration
    static class TestConfig {
        @Bean
        @Primary
        TokenService tokenService() {
            TokenService mock = Mockito.mock(TokenService.class);
            Mockito.when(mock.getUserIdFromRequest(Mockito.any())).thenReturn(1L);
            return mock;
        }
    }

    @BeforeEach
    void cleanupTags() {
        List<Tag> tags = tagMapper.findByUserId(1L);
        for (Tag t : tags) {
            tagMapper.deleteById(t.getTagId());
        }
    }

    @Test
    void scenario_create5_update_delete() throws Exception {
        // 1) 新建四个标签
        TagCreateRequest t1 = new TagCreateRequest();
        t1.setName("Tag1");
        t1.setColor("#111111");
        mockMvc.perform(post("/api/reminder/tags/create")
                        .contentType(java.util.Objects.requireNonNull(MediaType.APPLICATION_JSON))
                        .content(java.util.Objects.requireNonNull(objectMapper.writeValueAsString(t1))))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.code").value(200));

        TagCreateRequest t2 = new TagCreateRequest();
        t2.setName("Tag2");
        t2.setColor("#222222");
        mockMvc.perform(post("/api/reminder/tags/create")
                        .contentType(java.util.Objects.requireNonNull(MediaType.APPLICATION_JSON))
                        .content(java.util.Objects.requireNonNull(objectMapper.writeValueAsString(t2))))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.code").value(200));

        TagCreateRequest t3 = new TagCreateRequest();
        t3.setName("Tag3");
        t3.setColor("#333333");
        mockMvc.perform(post("/api/reminder/tags/create")
                        .contentType(java.util.Objects.requireNonNull(MediaType.APPLICATION_JSON))
                        .content(java.util.Objects.requireNonNull(objectMapper.writeValueAsString(t3))))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.code").value(200));

        TagCreateRequest t4 = new TagCreateRequest();
        t4.setName("Tag4");
        t4.setColor("#444444");
        mockMvc.perform(post("/api/reminder/tags/create")
                        .contentType(java.util.Objects.requireNonNull(MediaType.APPLICATION_JSON))
                        .content(java.util.Objects.requireNonNull(objectMapper.writeValueAsString(t4))))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.code").value(200));

        List<Tag> created = tagMapper.findByUserId(1L);
        Assertions.assertEquals(4, created.size());
        Tag tag1 = created.stream().filter(t -> "Tag1".equals(t.getName())).findFirst().orElseThrow();
        Tag tag2 = created.stream().filter(t -> "Tag2".equals(t.getName())).findFirst().orElseThrow();
        Tag tag3 = created.stream().filter(t -> "Tag3".equals(t.getName())).findFirst().orElseThrow();
        Tag tag4 = created.stream().filter(t -> "Tag4".equals(t.getName())).findFirst().orElseThrow();

        // 2) 第五个与第四个重名，应失败
        TagCreateRequest t5 = new TagCreateRequest();
        t5.setName("Tag4");
        t5.setColor("#555555");
        mockMvc.perform(post("/api/reminder/tags/create")
                        .contentType(java.util.Objects.requireNonNull(MediaType.APPLICATION_JSON))
                        .content(java.util.Objects.requireNonNull(objectMapper.writeValueAsString(t5))))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.code").value(400))
                .andExpect(result -> {
                    String c = result.getResponse().getContentAsString();
                    com.fasterxml.jackson.databind.JsonNode root = objectMapper.readTree(c);
                    org.junit.jupiter.api.Assertions.assertTrue(root.path("msg").asText().contains("already exists"));
                });
        Assertions.assertEquals(4, tagMapper.findByUserId(1L).size());

        // 3) 第一个只改名
        TagUpdateRequest u1 = new TagUpdateRequest();
        u1.setTagId(tag1.getTagId());
        u1.setName("Tag1-Renamed");
        mockMvc.perform(put("/api/reminder/tags/update")
                        .contentType(java.util.Objects.requireNonNull(MediaType.APPLICATION_JSON))
                        .content(java.util.Objects.requireNonNull(objectMapper.writeValueAsString(u1))))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.code").value(200))
                .andExpect(result -> {
                    String c = result.getResponse().getContentAsString();
                    com.fasterxml.jackson.databind.JsonNode root = objectMapper.readTree(c);
                    org.junit.jupiter.api.Assertions.assertTrue(root.path("msg").asText().contains("updated"));
                });
        Tag tag1After = tagMapper.findById(tag1.getTagId());
        Assertions.assertEquals("Tag1-Renamed", tag1After.getName());
        Assertions.assertEquals("#111111", tag1After.getColor());

        // 4) 第二个只改颜色
        TagUpdateRequest u2 = new TagUpdateRequest();
        u2.setTagId(tag2.getTagId());
        u2.setColor("#000000");
        mockMvc.perform(put("/api/reminder/tags/update")
                        .contentType(java.util.Objects.requireNonNull(MediaType.APPLICATION_JSON))
                        .content(java.util.Objects.requireNonNull(objectMapper.writeValueAsString(u2))))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.code").value(200));
        Tag tag2After = tagMapper.findById(tag2.getTagId());
        Assertions.assertEquals("Tag2", tag2After.getName());
        Assertions.assertEquals("#000000", tag2After.getColor());

        // 5) 第三个名和颜色都改
        TagUpdateRequest u3 = new TagUpdateRequest();
        u3.setTagId(tag3.getTagId());
        u3.setName("Tag3-Renamed");
        u3.setColor("#999999");
        mockMvc.perform(put("/api/reminder/tags/update")
                        .contentType(java.util.Objects.requireNonNull(MediaType.APPLICATION_JSON))
                        .content(java.util.Objects.requireNonNull(objectMapper.writeValueAsString(u3))))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.code").value(200));
        Tag tag3After = tagMapper.findById(tag3.getTagId());
        Assertions.assertEquals("Tag3-Renamed", tag3After.getName());
        Assertions.assertEquals("#999999", tag3After.getColor());

        // 6) 第四个删除
        TagDeleteRequest d4 = new TagDeleteRequest();
        d4.setTagId(tag4.getTagId());
        mockMvc.perform(post("/api/reminder/tags/delete")
                        .contentType(java.util.Objects.requireNonNull(MediaType.APPLICATION_JSON))
                        .content(java.util.Objects.requireNonNull(objectMapper.writeValueAsString(d4))))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.code").value(200))
                .andExpect(result -> {
                    String c = result.getResponse().getContentAsString();
                    com.fasterxml.jackson.databind.JsonNode root = objectMapper.readTree(c);
                    org.junit.jupiter.api.Assertions.assertTrue(root.path("msg").asText().contains("deleted"));
                });
        Assertions.assertNull(tagMapper.findById(tag4.getTagId()));

        // 7) 最终 get-all：应剩 3 个标签，且名称符合预期
        mockMvc.perform(get("/api/reminder/tags/get-all"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.code").value(200))
                .andExpect(result -> {
                    String c = result.getResponse().getContentAsString();
                    com.fasterxml.jackson.databind.JsonNode root = objectMapper.readTree(c);
                    org.junit.jupiter.api.Assertions.assertTrue(root.path("msg").asText().contains("retrieved"));
                })
                .andExpect(result -> {
                    String c = result.getResponse().getContentAsString();
                    com.fasterxml.jackson.databind.JsonNode root = objectMapper.readTree(c);
                    com.fasterxml.jackson.databind.JsonNode data = root.path("data");
                    org.junit.jupiter.api.Assertions.assertTrue(!data.isMissingNode() && !data.isNull());
                    org.junit.jupiter.api.Assertions.assertEquals(3, data.size());
                    java.util.Set<String> names = new java.util.HashSet<>();
                    data.forEach(n -> names.add(n.path("name").asText()));
                    org.junit.jupiter.api.Assertions.assertEquals(java.util.Set.of("Tag1-Renamed", "Tag2", "Tag3-Renamed"), names);
                });
    }
}
