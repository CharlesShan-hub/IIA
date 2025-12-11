package com.charles.server.reminder.mapper;

import com.charles.server.reminder.entity.Project;
import org.apache.ibatis.annotations.*;

import java.util.List;

@Mapper
public interface ProjectMapper {
    
    @Insert("INSERT INTO reminder_project(user_id, name, description, color, icon, sort_order, is_archived)"+
            "VALUES(#{userId}, #{name}, #{description}, #{color}, #{icon}, #{sortOrder}, #{isArchived})")
    @Options(useGeneratedKeys = true, keyProperty = "projectId", keyColumn = "project_id")
    int insert(Project project);
    
    @Select("SELECT * FROM reminder_project WHERE project_id = #{projectId}")
    Project findById(Long projectId);

    @Select("SELECT * FROM reminder_project WHERE name = #{name} AND user_id = #{userId}")
    Project findByName(Long userId, String name);

    @Select("SELECT * FROM reminder_project WHERE user_id = #{userId} AND sort_order = #{sortOrder}")
    Project findBySortOrder(Long userId, Integer sortOrder);
    
    @Select("SELECT * FROM reminder_project WHERE user_id = #{userId} ORDER BY sort_order")
    List<Project> findByUserId(Long userId);
    
    @Select("SELECT * FROM reminder_project WHERE user_id = #{userId} AND is_archived = false ORDER BY sort_order")
    List<Project> findActiveByUserId(Long userId);
    
    @Update("UPDATE reminder_project SET name = #{name}, description = #{description}, color = #{color}, "+
            "icon = #{icon}, sort_order = #{sortOrder}, is_archived = #{isArchived} "+
            "WHERE project_id = #{projectId}")
    int update(Project project);
    
    @Select("SELECT COUNT(*) FROM reminder_project WHERE user_id = #{userId} AND name = #{name}")
    boolean existsByNameAndUserId(@Param("name") String name, @Param("userId") Long userId);
    
    @Update("UPDATE reminder_project SET sort_order = #{sortOrder} WHERE project_id = #{projectId}")
    int updateSortOrder(Project project);
}