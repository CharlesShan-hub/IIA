package com.charles.server.reminder.controller;

import java.util.List;
import java.util.Map;

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
    
    // 创建标签
    @PostMapping("create")
    public Map<String, Object> create(@RequestBody Tag tag, HttpServletRequest request) {
        try {
            Long userId = tokenService.getUserIdFromRequest(request);
            
            // 检查标签名是否已存在
            if (tagService.existsByName(tag.getName(), userId)) {
                return ResponseUtils.buildErrorResponse("标签名称已存在");
            }
            
            Tag createdTag = tagService.create(tag, userId);
            return ResponseUtils.buildSuccessResponse(createdTag, "创建成功");
        } catch (Exception e) {
            log.error("创建标签失败: {}", e.getMessage(), e);
            return ResponseUtils.buildErrorResponse(e.getMessage());
        }
    }
    
    // 获取用户所有标签
    @GetMapping("get-all")
    public Map<String, Object> getAll(HttpServletRequest request) {
        try {
            Long userId = tokenService.getUserIdFromRequest(request);
            List<Tag> tags = tagService.getAll(userId);
            return ResponseUtils.buildSuccessResponse(tags, "查询成功");
        } catch (Exception e) {
            log.error("获取标签列表失败: {}", e.getMessage(), e);
            return ResponseUtils.buildErrorResponse(e.getMessage());
        }
    }
    
    // 获取单个标签
    @GetMapping("get/{id}")
    public Map<String, Object> getById(@PathVariable("id") Long tagId, HttpServletRequest request) {
        try {
            Long userId = tokenService.getUserIdFromRequest(request);
            Tag tag = tagService.getById(tagId, userId);
            return ResponseUtils.buildSuccessResponse(tag, "查询成功");
        } catch (Exception e) {
            log.error("获取标签失败: {}", e.getMessage(), e);
            return ResponseUtils.buildErrorResponse(e.getMessage());
        }
    }
    
    // 更新标签
    @PutMapping("update/{id}")
    public Map<String, Object> updateById(@PathVariable("id") Long tagId, @RequestBody Tag tag, HttpServletRequest request) {
        try {
            Long userId = tokenService.getUserIdFromRequest(request);
            
            // 检查更新后的标签名是否与其他标签重复
            Tag existingTag = tagService.getById(tagId, userId);
            if (!existingTag.getName().equals(tag.getName()) && tagService.existsByName(tag.getName(), userId)) {
                return ResponseUtils.buildErrorResponse("标签名称已存在");
            }
            
            Tag updatedTag = tagService.updateById(tag, tagId, userId);
            return ResponseUtils.buildSuccessResponse(updatedTag, "更新成功");
        } catch (Exception e) {
            log.error("更新标签失败: {}", e.getMessage(), e);
            return ResponseUtils.buildErrorResponse(e.getMessage());
        }
    }
}