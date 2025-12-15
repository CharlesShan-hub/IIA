package com.charles.server.reminder.service.impl;

import java.util.List;
import org.springframework.stereotype.Service;
import com.charles.server.reminder.entity.Tag;
import com.charles.server.reminder.mapper.TagMapper;
import com.charles.server.reminder.service.TagService;
import com.charles.server.reminder.dto.CreateTagRequest;
import com.charles.server.reminder.dto.UpdateTagRequest;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;

@Slf4j
@Service
@RequiredArgsConstructor
public class TagServiceImpl implements TagService {
    
    private final TagMapper tagMapper;

    private Tag convertToEntity(Long userId, CreateTagRequest dto) {
        Tag tag = new Tag();
        tag.setUserId(userId);
        tag.setName(dto.getName());
        tag.setColor(dto.getColor());
        return tag;
    }

    private boolean existsByName(Long userId, String name) {
        return tagMapper.findByName(userId, name) != null;
    }
    
    private Tag validatedFindTagById(Long userId, Long tagId) {
        Tag tag = tagMapper.findById(tagId);
        if (tag == null) {
            throw new RuntimeException("Tag not found");
        }
        if (!tag.getUserId().equals(userId)) {
            throw new RuntimeException("No permission to access this tag");
        }
        return tag;
    }
    
    @Override
    public Tag create(Long userId, CreateTagRequest dto) {
        if (existsByName(userId, dto.getName())) {
            throw new RuntimeException("Tag name " + dto.getName() + " already exists");
        }
        Tag tag = convertToEntity(userId, dto);
        tagMapper.insert(tag);
        log.info("User {} create tag {}: {}", userId, tag.getTagId(), tag.getName());
        return tag;
    }

    @Override
    public void updateById(Long userId, UpdateTagRequest dto) {
        Tag tag = validatedFindTagById(userId, dto.getTagId());
        tag.setName(dto.getName());
        tag.setColor(dto.getColor());
        tagMapper.update(tag);
        log.info("User {} update tag {}: {}", userId, dto.getTagId(), dto.getName());
    }
    
    @Override
    public List<Tag> getAll(Long userId) {
        List<Tag> tags = tagMapper.findByUserId(userId);
        log.info("User {} get tag list {}", userId, tags);
        return tags;
    }
}