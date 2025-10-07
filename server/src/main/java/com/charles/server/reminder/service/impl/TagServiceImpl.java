package com.charles.server.reminder.service.impl;

import java.util.List;
import org.springframework.stereotype.Service;
import com.charles.server.reminder.entity.Tag;
import com.charles.server.reminder.mapper.TagMapper;
import com.charles.server.reminder.service.TagService;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;

@Slf4j
@Service
@RequiredArgsConstructor
public class TagServiceImpl implements TagService {
    
    private final TagMapper tagMapper;
    
    @Override
    public Tag create(Tag tag, Long userId) {
        tag.setUserId(userId);
        tagMapper.insert(tag);
        log.info("用户创建标签成功, 用户ID: {}, 标签名称: {}", userId, tag.getName());
        return tag;
    }
    
    @Override
    public List<Tag> getAll(Long userId) {
        List<Tag> tags = tagMapper.findByUserId(userId);
        log.info("用户获取标签列表成功, 用户ID: {}", userId);
        return tags;
    }
    
    @Override
    public Tag getById(Long tagId, Long userId) {
        Tag tag = tagMapper.findById(tagId);
        if (tag == null || !tag.getUserId().equals(userId)) {
            throw new RuntimeException("标签不存在或无权限访问");
        }
        log.info("用户获取标签成功, 用户ID: {}, 标签ID: {}", userId, tagId);
        return tag;
    }
    
    @Override
    public Tag updateById(Tag tag, Long tagId, Long userId) {
        Tag existingTag = tagMapper.findById(tagId);
        if (existingTag == null || !existingTag.getUserId().equals(userId)) {
            throw new RuntimeException("标签不存在或无权限访问");
        }
        
        tag.setTagId(tagId);
        tag.setUserId(userId);
        tagMapper.update(tag);
        log.info("用户更新标签成功, 用户ID: {}, 标签ID: {}", userId, tagId);
        return tag;
    }
    
    @Override
    public boolean existsByName(String name, Long userId) {
        return tagMapper.existsByNameAndUserId(name, userId);
    }
}