package com.charles.server.reminder.service.impl;

import java.util.List;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import com.charles.server.reminder.entity.Tag;
import com.charles.server.reminder.entity.Operation;
import com.charles.server.reminder.mapper.TagMapper;
import com.charles.server.reminder.service.TagService;
import com.charles.server.reminder.service.PermissionService;
import com.charles.server.reminder.service.OperationService;
import com.charles.server.reminder.service.TagLogService;
import com.charles.server.reminder.exception.TagException;
import com.charles.server.reminder.dto.TagCreateDTO;
import com.charles.server.reminder.dto.TagUpdateDTO;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;

@Slf4j
@Service
@RequiredArgsConstructor
public class TagServiceImpl implements TagService {
    
    private final TagMapper tagMapper;
    private final PermissionService permissionService;
    private final OperationService operationService;
    private final TagLogService tagLogService;

    private Tag convertToEntity(Long userId, TagCreateDTO dto) {
        return Tag.builder()
                .userId(userId)
                .name(dto.getName())
                .color(dto.getColor())
                .build();
    }

    private boolean existsByName(Long userId, String name) {
        return tagMapper.existsByNameAndUserId(name, userId);
    }
    
    @Override
    @Transactional
    public void create(Long userId, TagCreateDTO dto) {
        // 1. Check if tag name already exists
        if (existsByName(userId, dto.getName())) {
            throw TagException.nameAlreadyExists(userId, dto.getName());
        }
        
        // 2. Get operation ID
        Long operationId = operationService.getId(userId);
        
        // 3. Record operation
        operationService.create(Operation.builder()
                .operationId(operationId)
                .userId(userId)
                .isReminderTag(true)
                .build());
        
        // 4. Create tag
        Tag tag = convertToEntity(userId, dto);
        tag.setOperationId(operationId);
        try {
            tagMapper.insert(tag);
        } catch (Exception e) {
            log.error("Error creating tag for user {}: {}", userId, e.getMessage(), e);
            throw TagException.createFailed(userId, e);
        }
        
        log.info("User {} create tag {}: {}, operationId={}", userId, tag.getTagId(), tag.getName(), operationId);
    }

    @Override
    @Transactional
    public void update(Long userId, TagUpdateDTO dto) {
        // 1. Get tag by ID
        Tag currentTag = permissionService.getTag(userId, dto.getTagId());
        
        // 2. Check if new name already exists (if name is being changed)
        if (dto.getName() != null && !dto.getName().equals(currentTag.getName())) {
            if (existsByName(userId, dto.getName())) {
                throw TagException.nameAlreadyExists(userId, dto.getName());
            }
        }
        
        // 3. Generate new operation ID
        Long newOperationId = operationService.getId(userId);
        
        // 4. Save the previous version to history table
        tagLogService.save(currentTag, newOperationId);
        
        // 5. Record operation
        operationService.create(Operation.builder()
                .operationId(newOperationId)
                .userId(userId)
                .isReminderTag(true)
                .build());
        
        // 6. Apply changes to current tag
        currentTag.setOperationId(newOperationId);
        if (dto.getName() != null) {
            currentTag.setName(dto.getName());
        }
        if (dto.getColor() != null) {
            currentTag.setColor(dto.getColor());
        }
        
        // 7. Update main table
        try {
            tagMapper.update(currentTag);
        } catch (Exception e) {
            log.error("Error updating tag for user {}: {}", userId, e.getMessage(), e);
            throw TagException.updateFailed(userId, dto.getTagId(), e);
        }
        
        log.info("Update tag: userId={}, tagId={}, oldOperationId={}, newOperationId={}", 
                userId, currentTag.getTagId(), currentTag.getOperationId(), newOperationId);
    }
    
    @Override
    @Transactional
    public void delete(Long userId, Long tagId) {
        // 1. Get tag by ID (verify permission)
        Tag currentTag = permissionService.getTag(userId, tagId);
        
        // 2. Generate new operation ID
        Long operationId = operationService.getId(userId);
        
        // 3. Save the current version to history table (for recovery if needed)
        tagLogService.save(currentTag, operationId);
        
        // 4. Record delete operation
        operationService.create(Operation.builder()
                .operationId(operationId)
                .userId(userId)
                .isReminderTag(true)
                .build());
        
        // 5. Delete tag from main table
        try {
            tagMapper.deleteById(tagId);
        } catch (Exception e) {
            log.error("Error deleting tag for user {}: {}", userId, e.getMessage(), e);
            throw TagException.deleteFailed(userId, tagId, e);
        }
        
        log.info("Delete tag: userId={}, tagId={}, operationId={}", 
                userId, tagId, operationId);
    }

    @Override
    public List<Tag> getAll(Long userId) {
        List<Tag> tags = tagMapper.findByUserId(userId);
        log.info("User {} get tag list {}", userId, tags);
        return tags;
    }
}
