package com.charles.server.reminder.service.impl;

import com.charles.server.reminder.entity.Tag;
import com.charles.server.reminder.entity.TagLog;
import com.charles.server.reminder.mapper.TagLogMapper;
import com.charles.server.reminder.mapper.TagMapper;
import com.charles.server.reminder.service.TagLogService;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;

@Service
@RequiredArgsConstructor
@Slf4j
public class TagLogServiceImpl implements TagLogService {
    
    private final TagLogMapper tagLogMapper;
    private final TagMapper tagMapper;
    
    @Override
    public void save(Tag tag) {
        save(tag, null);
    }
    
    @Override
    public void save(Tag tag, Long batchOperationId) {
        TagLog tagLog = TagLog.fromTag(tag, batchOperationId);
        tagLogMapper.insert(tagLog);
        log.debug("Tag log saved: tagId={}, operationId={}, batchOperationId={}", 
                tag.getTagId(), tag.getOperationId(), batchOperationId);
    }
    
    @Override
    public List<TagLog> findByTagId(Long tagId) {
        return tagLogMapper.findByTagId(tagId);
    }
    
    @Override
    public List<TagLog> findByOperationId(Long operationId) {
        return tagLogMapper.findByOperationId(operationId);
    }
    
    @Override
    public List<TagLog> findByBatchOperationId(Long batchOperationId) {
        return tagLogMapper.findByBatchOperationId(batchOperationId);
    }
    
    @Override
    @Transactional
    public void revert(Long userId, Long operationId, Long previousOperationId) {
        // 1. 先尝试根据batch_operation_id查找（批量操作）
        List<TagLog> logsToRestore = tagLogMapper.findByBatchOperationId(operationId);
        
        boolean isBatchOperation = !logsToRestore.isEmpty();
        
        // 2. 如果不是批量操作，处理单个操作
        if (!isBatchOperation) {
            // 查找当前操作ID下的所有标签
            List<Tag> currentTags = tagMapper.findByOperationId(operationId);
            
            if (currentTags.isEmpty()) {
                log.warn("没有找到需要撤回的标签: userId={}, operationId={}, previousOperationId={}", 
                        userId, operationId, previousOperationId);
                return;
            }
            
            int deletedCount = 0;
            int restoredCount = 0;
            
            for (Tag currentTag : currentTags) {
                Long tagId = currentTag.getTagId();
                
                // 检查在previousOperationId下是否有该标签的日志记录
                TagLog previousLog = tagLogMapper.findByTagIdAndOperationId(tagId, previousOperationId);
                
                if (previousLog == null) {
                    // 新增操作：删除该标签
                    tagMapper.deleteByTagIdAndOperationId(tagId, operationId);
                    deletedCount++;
                } else {
                    // 更新操作：恢复之前的版本
                    // 删除当前版本
                    tagMapper.deleteByTagIdAndOperationId(tagId, operationId);
                    
                    // 使用日志中的状态恢复标签
                    Tag restoredTag = previousLog.toTag(userId, previousOperationId);
                    tagMapper.insert(restoredTag);
                    restoredCount++;
                }
            }
            
            // 删除相关的日志记录（撤回后不可再撤回）
            tagLogMapper.deleteByOperationId(operationId);
            
            log.info("撤回单个操作完成: userId={}, operationId={}, previousOperationId={}, deletedCount={}, restoredCount={}", 
                    userId, operationId, previousOperationId, deletedCount, restoredCount);
            return;
        }
        
        // 3. 处理批量操作
        int restoredCount = 0;
        
        for (TagLog logToRestore : logsToRestore) {
            Long tagId = logToRestore.getTagId();
            
            // 删除当前版本
            tagMapper.deleteByTagIdAndOperationId(tagId, operationId);
            
            // 使用日志中的状态恢复标签
            Tag restoredTag = logToRestore.toTag(userId, previousOperationId);
            tagMapper.insert(restoredTag);
            restoredCount++;
        }
        
        // 删除相关的日志记录（撤回后不可再撤回）
        tagLogMapper.deleteByBatchOperationId(operationId);
        
        log.info("撤回批量操作完成: userId={}, operationId={}, previousOperationId={}, restoredCount={}", 
                userId, operationId, previousOperationId, restoredCount);
    }
}