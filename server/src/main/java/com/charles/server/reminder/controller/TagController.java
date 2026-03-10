package com.charles.server.reminder.controller;

import java.util.List;
import java.util.Map;

import jakarta.validation.Valid;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.charles.server.auth.service.TokenService;
import com.charles.server.reminder.entity.Tag;
import com.charles.server.reminder.service.TagService;
import com.charles.server.utils.ResponseUtils;
import com.charles.server.reminder.dto.TagCreateRequest;
import com.charles.server.reminder.dto.TagUpdateRequest;
import com.charles.server.reminder.dto.TagDeleteRequest;

import jakarta.servlet.http.HttpServletRequest;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;

@Slf4j
@RestController
@RequestMapping("/api/reminder/tags")
@RequiredArgsConstructor
public class TagController {
    private final TagService tagService;
    private final TokenService tokenService;
    
    // Create Tag
    @PostMapping("create")
    public Map<String, Object> create(@RequestBody @Valid TagCreateRequest dto, HttpServletRequest request) {
        Long userId = tokenService.getUserIdFromRequest(request);
        log.info("Create tag for user {}: {}", userId, dto);
        tagService.create(userId, dto);
        return ResponseUtils.buildEmptySuccessResponse("Tag created successfully");
    }

    // Update Tag
    @PutMapping("update")
    public Map<String, Object> update(@RequestBody @Valid TagUpdateRequest dto, HttpServletRequest request) {
        Long userId = tokenService.getUserIdFromRequest(request);
        log.info("Update tag for user {}: {}", userId, dto);
        tagService.update(userId, dto);
        return ResponseUtils.buildEmptySuccessResponse("Tag updated successfully");
    }
    
    // Delete Tag
    @PostMapping("delete")
    public Map<String, Object> delete(@RequestBody @Valid TagDeleteRequest dto, HttpServletRequest request) {
        Long userId = tokenService.getUserIdFromRequest(request);
        log.info("Delete tag for user {}: {}", userId, dto);
        tagService.delete(userId, dto.getTagId());
        return ResponseUtils.buildEmptySuccessResponse("Tag deleted successfully");
    }

    // Get all tags for a user
    @GetMapping("get-all")
    public Map<String, Object> getAll(HttpServletRequest request) {
        Long userId = tokenService.getUserIdFromRequest(request);
        log.info("Get all tags for user {}", userId);
        List<Tag> tags = tagService.getAll(userId);
        return ResponseUtils.buildSuccessResponse(tags, "Tags retrieved successfully");
    }
}
