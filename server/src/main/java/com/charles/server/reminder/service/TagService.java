package com.charles.server.reminder.service;

import java.util.List;
import com.charles.server.reminder.entity.Tag;

public interface TagService {
    /**
     * 创建标签
     * @param tag 标签信息
     * @param userId 用户ID
     * @return 创建后的标签
     */
    Tag create(Tag tag, Long userId);
    
    /**
     * 获取用户所有标签
     * @param userId 用户ID
     * @return 标签列表
     */
    List<Tag> getAll(Long userId);
    
    /**
     * 根据ID获取标签
     * @param tagId 标签ID
     * @param userId 用户ID
     * @return 标签信息
     */
    Tag getById(Long tagId, Long userId);
    
    /**
     * 更新标签
     * @param tag 标签信息
     * @param tagId 标签ID
     * @param userId 用户ID
     * @return 更新后的标签
     */
    Tag updateById(Tag tag, Long tagId, Long userId);
    
    /**
     * 检查标签是否存在
     * @param name 标签名称
     * @param userId 用户ID
     * @return 是否存在
     */
    boolean existsByName(String name, Long userId);
}