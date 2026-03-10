package com.charles.server.reminder.service;

import com.charles.server.reminder.dto.TaskTagCreateRequest;
import com.charles.server.reminder.dto.TaskTagDeleteRequest;
import com.charles.server.reminder.dto.TaskTagBatchCreateRequest;
import com.charles.server.reminder.dto.TaskTagBatchDeleteRequest;

public interface TaskTagService {
    // 创建任务-标签关联（可选级联到子任务）
    void create(Long userId, TaskTagCreateRequest dto);

    // 批量创建任务-标签关联（可选级联到子任务）
    void createBatch(Long userId, TaskTagBatchCreateRequest dto);

    // 删除任务-标签关联（可选级联到子任务）
    void delete(Long userId, TaskTagDeleteRequest dto);
    
    // 批量删除任务-标签关联（可选级联到子任务）
    void deleteBatch(Long userId, TaskTagBatchDeleteRequest dto);

    
    // // 批量创建任务-标签关联
    // int createBatch(List<TaskTag> taskTagList);
    
    // // 根据ID获取任务-标签关联
    // TaskTag getById(Long id);
    
    // // 根据任务ID和标签ID获取关联
    // TaskTag getByTaskIdAndTagId(Long taskId, Long tagId);
    
    // // 获取任务的所有标签关联
    // List<TaskTag> getByTaskId(Long taskId);
    
    // // 获取标签的所有任务关联
    // List<TaskTag> getByTagId(Long tagId);
    
    // // 根据任务ID删除所有关联
    // int deleteByTaskId(Long taskId);
    
    // // 根据标签ID删除所有关联
    // int deleteByTagId(Long tagId);
    
    // // 删除特定的任务-标签关联
    // int deleteByTaskIdAndTagId(Long taskId, Long tagId);
    
    // // 批量删除任务-标签关联
    // int deleteBatchByTaskIdAndTagIds(Long taskId, List<Long> tagIds);
}
