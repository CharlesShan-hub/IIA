package com.charles.server.reminder.service.impl;

import java.util.List;
import org.springframework.stereotype.Service;
import com.charles.server.reminder.entity.Tag;
import com.charles.server.reminder.mapper.TagMapper;
import com.charles.server.reminder.service.TagService;
import com.charles.server.reminder.service.PermissionService;
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
    public void create(Long userId, TagCreateDTO dto) {
        if (existsByName(userId, dto.getName())) {
            throw TagException.nameAlreadyExists(userId, dto.getName());
        }
        Tag tag = convertToEntity(userId, dto);
        try {
            tagMapper.insert(tag);
        } catch (Exception e) {
            log.error("Error creating tag for user {}: {}", userId, e.getMessage(), e);
            throw TagException.createFailed(userId, e);
        }
        log.info("User {} create tag {}: {}", userId, tag.getTagId(), tag.getName());
    }

    @Override
    public void update(Long userId, TagUpdateDTO dto) {
        Tag tag = permissionService.getTag(userId, dto.getTagId());
        if (dto.getName() != null) {
            if(!dto.getName().equals(tag.getName()) && existsByName(userId, dto.getName()))
                throw TagException.nameAlreadyExists(userId, dto.getName());
            tag.setName(dto.getName());
        }
        if (dto.getColor() != null) {
            tag.setColor(dto.getColor());
        }
        try {
            tagMapper.update(tag);
        } catch (Exception e) {
            log.error("Error updating tag for user {}: {}", userId, e.getMessage(), e);
            throw TagException.updateFailed(userId, dto.getTagId(), e);
        }
    }
    
    @Override
    public void delete(Long userId, Long tagId) {
        permissionService.validTag(userId, tagId);
        try {
            tagMapper.deleteById(tagId);
        } catch (Exception e) {
            log.error("Error deleting tag for user {}: {}", userId, e.getMessage(), e);
            throw TagException.deleteFailed(userId, tagId, e);
        }
        log.info("User {} delete tag {} successfully", userId, tagId);
    }

    @Override
    public List<Tag> getAll(Long userId) {
        List<Tag> tags = tagMapper.findByUserId(userId);
        log.info("User {} get tag list {}", userId, tags);
        return tags;
    }
}
