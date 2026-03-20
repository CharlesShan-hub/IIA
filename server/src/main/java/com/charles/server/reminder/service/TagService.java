package com.charles.server.reminder.service;

import java.util.List;
import com.charles.server.reminder.entity.Tag;
import com.charles.server.reminder.dto.TagCreateDTO;
import com.charles.server.reminder.dto.TagUpdateDTO;

public interface TagService {
    /**
     * Create a new tag for the user
     * @param userId the user id
     * @param dto TagCreateRequest
     */
    void create(Long userId, TagCreateDTO dto);

    /**
     * Update a tag by its ID
     * @param tag the tag information
     * @param tagId the tag id
     * @param userId the user id
     */
    void update(Long userId, TagUpdateDTO dto);
    
    /**
     * Delete a tag by its ID
     * @param userId the user id
     * @param tagId the tag id
     */
    void delete(Long userId, Long tagId);

    /**
     * Get all tags for a user
     * @param userId the user id
     * @return the list of tags
     */
    List<Tag> getAll(Long userId);
}
