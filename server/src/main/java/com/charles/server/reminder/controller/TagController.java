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
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.responses.ApiResponse;
import io.swagger.v3.oas.annotations.responses.ApiResponses;
import io.swagger.v3.oas.annotations.security.SecurityRequirement;

@Slf4j
@RestController
@RequestMapping("/api/reminder/tag")
@RequiredArgsConstructor
@io.swagger.v3.oas.annotations.tags.Tag(name = "Tag Management", description = "Tag creation, update, deletion, and query APIs")
public class TagController {
    private final TagService tagService;
    private final TokenService tokenService;
    
    @PostMapping("create")
    @Operation(
        summary = "Create Tag",
        description = "Create a new tag with name and color"
    )
    @ApiResponses({
        @ApiResponse(responseCode = "200", description = "Tag created successfully"),
        @ApiResponse(responseCode = "400", description = "Invalid request parameters"),
        @ApiResponse(responseCode = "401", description = "Authentication required")
    })
    @SecurityRequirement(name = "bearer-jwt")
    public ResponseUtils<Void> create(@RequestBody @Valid TagCreateDTO dto, HttpServletRequest request) {
        Long userId = tokenService.getUserIdFromRequest(request);
        log.info("Create tag for user {}: {}", userId, dto);
        tagService.create(userId, dto);
        return ResponseUtils.buildEmptySuccessResponse("Tag created successfully");
    }

    @PutMapping("update")
    @Operation(
        summary = "Update Tag",
        description = "Update tag information including name and color"
    )
    @ApiResponses({
        @ApiResponse(responseCode = "200", description = "Tag updated successfully"),
        @ApiResponse(responseCode = "400", description = "Invalid request parameters"),
        @ApiResponse(responseCode = "401", description = "Authentication required"),
        @ApiResponse(responseCode = "404", description = "Tag not found")
    })
    @SecurityRequirement(name = "bearer-jwt")
    public ResponseUtils<Void> update(@RequestBody @Valid TagUpdateDTO dto, HttpServletRequest request) {
        Long userId = tokenService.getUserIdFromRequest(request);
        log.info("Update tag for user {}: {}", userId, dto);
        tagService.update(userId, dto);
        return ResponseUtils.buildEmptySuccessResponse("Tag updated successfully");
    }
    
    @PostMapping("delete")
    @Operation(
        summary = "Delete Tag",
        description = "Delete a tag by ID"
    )
    @ApiResponses({
        @ApiResponse(responseCode = "200", description = "Tag deleted successfully"),
        @ApiResponse(responseCode = "400", description = "Invalid request parameters"),
        @ApiResponse(responseCode = "401", description = "Authentication required"),
        @ApiResponse(responseCode = "404", description = "Tag not found")
    })
    @SecurityRequirement(name = "bearer-jwt")
    public ResponseUtils<Void> delete(@RequestBody @Valid TagDeleteDTO dto, HttpServletRequest request) {
        Long userId = tokenService.getUserIdFromRequest(request);
        log.info("Delete tag for user {}: {}", userId, dto);
        tagService.delete(userId, dto.getTagId());
        return ResponseUtils.buildEmptySuccessResponse("Tag deleted successfully");
    }

    @GetMapping("get-all")
    @Operation(
        summary = "Get All Tags",
        description = "Get all tags for the current user"
    )
    @ApiResponses({
        @ApiResponse(responseCode = "200", description = "Tags retrieved successfully"),
        @ApiResponse(responseCode = "401", description = "Authentication required")
    })
    @SecurityRequirement(name = "bearer-jwt")
    public ResponseUtils<List<Tag>> getAll(HttpServletRequest request) {
        Long userId = tokenService.getUserIdFromRequest(request);
        log.info("Get all tags for user {}", userId);
        List<Tag> tags = tagService.getAll(userId);
        return ResponseUtils.buildSuccessResponse(tags, "Tags retrieved successfully");
    }
}
