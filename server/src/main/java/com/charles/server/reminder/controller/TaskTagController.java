package com.charles.server.reminder.controller;

import com.charles.server.auth.service.TokenService;
import com.charles.server.reminder.dto.CreateTaskTagRequest;
import com.charles.server.reminder.entity.TaskTag;
import com.charles.server.reminder.service.TaskTagService;
import com.charles.server.utils.ResponseUtils;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.web.bind.annotation.*;

import jakarta.servlet.http.HttpServletRequest;
import java.util.List;
import java.util.Map;

@Slf4j
@RestController
@RequestMapping("/api/reminder/task-tags")
@RequiredArgsConstructor
public class TaskTagController {

    private final TaskTagService taskTagService;
    private final TokenService tokenService;

    // 创建任务-标签关联
    @PostMapping("create")
    public Map<String, Object> create(@RequestBody CreateTaskTagRequest dto, HttpServletRequest request) {
        try {
            Long userId = tokenService.getUserIdFromRequest(request);
            
            log.info("User {} creating task-tag association: taskId={}, tagId={}", userId, dto.getTaskId(), dto.getTagId());
            
            // 检查关联是否已存在
            TaskTag existing = taskTagService.getByTaskIdAndTagId(dto.getTaskId(), dto.getTagId());
            if (existing != null) {
                return ResponseUtils.buildErrorResponse("任务与标签的关联已存在");
            }
            
            taskTagService.create(userId, dto);
            return ResponseUtils.buildSuccessResponse(null, "任务-标签关联创建成功");
        } catch (Exception e) {
            log.error("创建任务-标签关联失败: {}", e.getMessage(), e);
            return ResponseUtils.buildErrorResponse(e.getMessage());
        }
    }

    // 批量创建任务-标签关联
    @PostMapping("create-batch")
    public Map<String, Object> createBatch(@RequestBody List<TaskTag> taskTagList, HttpServletRequest request) {
        try {
            Long userId = tokenService.getUserIdFromRequest(request);
            log.info("User {} creating batch task-tag associations, size: {}", userId, taskTagList.size());
            
            int result = taskTagService.createBatch(taskTagList);
            return ResponseUtils.buildSuccessResponse(result, "批量创建任务-标签关联成功");
        } catch (Exception e) {
            log.error("批量创建任务-标签关联失败: {}", e.getMessage(), e);
            return ResponseUtils.buildErrorResponse(e.getMessage());
        }
    }

    // 根据ID获取任务-标签关联
    @GetMapping("get/{id}")
    public Map<String, Object> getById(@PathVariable("id") Long id, HttpServletRequest request) {
        try {
            Long userId = tokenService.getUserIdFromRequest(request);
            log.info("User {} fetching task-tag association by ID: {}", userId, id);
            
            TaskTag taskTag = taskTagService.getById(id);
            if (taskTag == null) {
                return ResponseUtils.buildErrorResponse("任务-标签关联不存在");
            }
            return ResponseUtils.buildSuccessResponse(taskTag, "任务-标签关联获取成功");
        } catch (Exception e) {
            log.error("获取任务-标签关联失败: {}", e.getMessage(), e);
            return ResponseUtils.buildErrorResponse(e.getMessage());
        }
    }

    // 获取任务的所有标签关联
    @GetMapping("get-by-task/{taskId}")
    public Map<String, Object> getByTaskId(@PathVariable Long taskId, HttpServletRequest request) {
        try {
            Long userId = tokenService.getUserIdFromRequest(request);
            log.info("User {} fetching task-tag associations by task ID: {}", userId, taskId);
            
            List<TaskTag> taskTags = taskTagService.getByTaskId(taskId);
            return ResponseUtils.buildSuccessResponse(taskTags, "任务标签关联获取成功");
        } catch (Exception e) {
            log.error("获取任务标签关联失败: {}", e.getMessage(), e);
            return ResponseUtils.buildErrorResponse(e.getMessage());
        }
    }

    // 获取标签的所有任务关联
    @GetMapping("get-by-tag/{tagId}")
    public Map<String, Object> getByTagId(@PathVariable Long tagId, HttpServletRequest request) {
        try {
            Long userId = tokenService.getUserIdFromRequest(request);
            log.info("User {} fetching task-tag associations by tag ID: {}", userId, tagId);
            
            List<TaskTag> taskTags = taskTagService.getByTagId(tagId);
            return ResponseUtils.buildSuccessResponse(taskTags, "标签任务关联获取成功");
        } catch (Exception e) {
            log.error("获取标签任务关联失败: {}", e.getMessage(), e);
            return ResponseUtils.buildErrorResponse(e.getMessage());
        }
    }

    // 删除特定的任务-标签关联
    @DeleteMapping("delete")
    public Map<String, Object> deleteByTaskIdAndTagId(@RequestParam Long taskId, 
                                                    @RequestParam Long tagId, 
                                                    HttpServletRequest request) {
        try {
            Long userId = tokenService.getUserIdFromRequest(request);
            log.info("User {} deleting task-tag association: taskId={}, tagId={}", userId, taskId, tagId);
            
            int result = taskTagService.deleteByTaskIdAndTagId(taskId, tagId);
            if (result > 0) {
                return ResponseUtils.buildSuccessResponse("任务-标签关联删除成功");
            } else {
                return ResponseUtils.buildErrorResponse("任务-标签关联不存在");
            }
        } catch (Exception e) {
            log.error("删除任务-标签关联失败: {}", e.getMessage(), e);
            return ResponseUtils.buildErrorResponse(e.getMessage());
        }
    }

    // 批量删除任务-标签关联
    @DeleteMapping("delete-batch")
    public Map<String, Object> deleteBatchByTaskIdAndTagIds(@RequestParam Long taskId, 
                                                          @RequestBody List<Long> tagIds, 
                                                          HttpServletRequest request) {
        try {
            Long userId = tokenService.getUserIdFromRequest(request);
            log.info("User {} deleting batch task-tag associations: taskId={}, tagIds size={}", userId, taskId, tagIds.size());
            
            int result = taskTagService.deleteBatchByTaskIdAndTagIds(taskId, tagIds);
            return ResponseUtils.buildSuccessResponse(result, "批量删除任务-标签关联成功");
        } catch (Exception e) {
            log.error("批量删除任务-标签关联失败: {}", e.getMessage(), e);
            return ResponseUtils.buildErrorResponse(e.getMessage());
        }
    }

    // 根据任务ID删除所有关联
    @DeleteMapping("delete-by-task/{taskId}")
    public Map<String, Object> deleteByTaskId(@PathVariable Long taskId, HttpServletRequest request) {
        try {
            Long userId = tokenService.getUserIdFromRequest(request);
            log.info("User {} deleting all task-tag associations by task ID: {}", userId, taskId);
            
            int result = taskTagService.deleteByTaskId(taskId);
            return ResponseUtils.buildSuccessResponse(result, "删除任务所有标签关联成功");
        } catch (Exception e) {
            log.error("删除任务所有标签关联失败: {}", e.getMessage(), e);
            return ResponseUtils.buildErrorResponse(e.getMessage());
        }
    }

    // 根据标签ID删除所有关联
    @DeleteMapping("delete-by-tag/{tagId}")
    public Map<String, Object> deleteByTagId(@PathVariable Long tagId, HttpServletRequest request) {
        try {
            Long userId = tokenService.getUserIdFromRequest(request);
            log.info("User {} deleting all task-tag associations by tag ID: {}", userId, tagId);
            
            int result = taskTagService.deleteByTagId(tagId);
            return ResponseUtils.buildSuccessResponse(result, "删除标签所有任务关联成功");
        } catch (Exception e) {
            log.error("删除标签所有任务关联失败: {}", e.getMessage(), e);
            return ResponseUtils.buildErrorResponse(e.getMessage());
        }
    }
}