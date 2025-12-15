package com.charles.server.reminder.controller;

import java.util.List;
import java.util.Map;

import jakarta.validation.Valid;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.charles.server.auth.service.TokenService;
import com.charles.server.reminder.entity.Tag;
import com.charles.server.reminder.service.TagService;
import com.charles.server.utils.ResponseUtils;
import com.charles.server.reminder.dto.CreateTagRequest;
import com.charles.server.reminder.dto.UpdateTagRequest;

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
    public Map<String, Object> create(@RequestBody @Valid CreateTagRequest dto, HttpServletRequest request) {
        try {
            Long userId = tokenService.getUserIdFromRequest(request);
            tagService.create(userId, dto);
            return ResponseUtils.buildEmptySuccessResponse("Tag created successfully");
        } catch (Exception e) {
            log.error("Failed to create tag: {}", e.getMessage(), e);
            return ResponseUtils.buildErrorResponse(e.getMessage());
        }
    }

    // Update Tag
    @PutMapping("update")
    public Map<String, Object> updateById(@RequestBody @Valid UpdateTagRequest dto, HttpServletRequest request) {
        try {
            Long userId = tokenService.getUserIdFromRequest(request);
            tagService.updateById(userId, dto);
            return ResponseUtils.buildEmptySuccessResponse("Tag updated successfully");
        } catch (Exception e) {
            log.error("更新标签失败: {}", e.getMessage(), e);
            return ResponseUtils.buildErrorResponse(e.getMessage());
        }
    }
    
    // Get all tags for a user
    @GetMapping("get-all")
    public Map<String, Object> getAll(HttpServletRequest request) {
        try {
            Long userId = tokenService.getUserIdFromRequest(request);
            List<Tag> tags = tagService.getAll(userId);
            return ResponseUtils.buildSuccessResponse(tags, "Tags retrieved successfully");
        } catch (Exception e) {
            log.error("Failed to retrieve tags: {}", e.getMessage(), e);
            return ResponseUtils.buildErrorResponse(e.getMessage());
        }
    }
}