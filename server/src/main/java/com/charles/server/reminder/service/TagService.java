package com.charles.server.reminder.service;

import java.util.List;
import com.charles.server.reminder.entity.Tag;
import com.charles.server.reminder.dto.CreateTagRequest;
import com.charles.server.reminder.dto.UpdateTagRequest;

public interface TagService {
    /**
     * Create a new tag for the user
     * @param userId the user id
     * @param dto CreateTagRequest
     */
    void create(Long userId, CreateTagRequest dto);

    /**
     * Update a tag by its ID
     * @param tag the tag information
     * @param tagId the tag id
     * @param userId the user id
     */
    void updateById(Long userId, UpdateTagRequest dto);
    
    /**
     * Get all tags for a user
     * @param userId the user id
     * @return the list of tags
     */
    List<Tag> getAll(Long userId);
    
    /**
     * Get a tag by its ID
     * @param tagId the tag id
     * @param userId the user id
     * @return the tag information
     */
    Tag getById(Long tagId, Long userId);
}