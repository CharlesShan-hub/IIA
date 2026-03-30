package com.charles.server.reminder.controller;

import java.util.List;

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
import com.charles.server.reminder.dto.TagCreateDTO;
import com.charles.server.reminder.dto.TagUpdateDTO;
import com.charles.server.reminder.dto.TagDeleteDTO;

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
    public ResponseUtils<Void> create(@RequestBody @Valid TagCreateDTO dto, HttpServletRequest request) {
        Long userId = tokenService.getUserIdFromRequest(request);
        log.info("Create tag for user {}: {}", userId, dto);
        tagService.create(userId, dto);
        return ResponseUtils.buildEmptySuccessResponse("Tag created successfully");
    }

    // Update Tag
    @PutMapping("update")
    public ResponseUtils<Void> update(@RequestBody @Valid TagUpdateDTO dto, HttpServletRequest request) {
        Long userId = tokenService.getUserIdFromRequest(request);
        log.info("Update tag for user {}: {}", userId, dto);
        tagService.update(userId, dto);
        return ResponseUtils.buildEmptySuccessResponse("Tag updated successfully");
    }
    
    // Delete Tag
    @PostMapping("delete")
    public ResponseUtils<Void> delete(@RequestBody @Valid TagDeleteDTO dto, HttpServletRequest request) {
        Long userId = tokenService.getUserIdFromRequest(request);
        log.info("Delete tag for user {}: {}", userId, dto);
        tagService.delete(userId, dto.getTagId());
        return ResponseUtils.buildEmptySuccessResponse("Tag deleted successfully");
    }

    // Get all tags for a user
    @GetMapping("get-all")
    public ResponseUtils<List<Tag>> getAll(HttpServletRequest request) {
        Long userId = tokenService.getUserIdFromRequest(request);
        log.info("Get all tags for user {}", userId);
        List<Tag> tags = tagService.getAll(userId);
        return ResponseUtils.buildSuccessResponse(tags, "Tags retrieved successfully");
    }
}
