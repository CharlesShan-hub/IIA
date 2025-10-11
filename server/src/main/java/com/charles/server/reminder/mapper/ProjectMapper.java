package com.charles.server.reminder.mapper;

import com.charles.server.reminder.entity.Project;
import org.apache.ibatis.annotations.*;

import java.util.List;

@Mapper
public interface ProjectMapper {
    
    // 插入新项目
    @Insert("INSERT INTO reminder_project(user_id, name, description, color, icon, sort_order, is_archived)"+
            "VALUES(#{userId}, #{name}, #{description}, #{color}, #{icon}, #{sortOrder}, #{isArchived})")
    @Options(useGeneratedKeys = true, keyProperty = "projectId", keyColumn = "project_id")
    int insert(Project project);
    
    // 根据ID查询项目
    @Select("SELECT * FROM reminder_project WHERE project_id = #{projectId}")
    Project findById(Long projectId);

    // 根据名称查询项目
    @Select("SELECT * FROM reminder_project WHERE name = #{name} AND user_id = #{userId}")
    Project findByName(Long userId, String name);

    // 根据位置查询项目
    @Select("SELECT * FROM reminder_project WHERE user_id = #{userId} AND sort_order = #{sortOrder}")
    Project findBySortOrder(Long userId, Integer sortOrder);
    
    // 查询用户的所有项目
    @Select("SELECT * FROM reminder_project WHERE user_id = #{userId} ORDER BY sort_order")
    List<Project> findByUserId(Long userId);
    
    // 查询用户的未归档项目
    @Select("SELECT * FROM reminder_project WHERE user_id = #{userId} AND is_archived = false ORDER BY sort_order")
    List<Project> findActiveByUserId(Long userId);
    
    // 更新项目信息
    @Update("UPDATE reminder_project SET name = #{name}, description = #{description}, color = #{color}, "+
            "icon = #{icon}, sort_order = #{sortOrder}, is_archived = #{isArchived} "+
            "WHERE project_id = #{projectId}")
    int update(Project project);
    
    // 查询项目是否存在（根据用户ID和项目名称）
    @Select("SELECT COUNT(*) FROM reminder_project WHERE user_id = #{userId} AND name = #{name}")
    boolean existsByNameAndUserId(@Param("name") String name, @Param("userId") Long userId);
    
    // 更新项目排序位置
    @Update("UPDATE reminder_project SET sort_order = #{sortOrder} WHERE project_id = #{projectId}")
    int updateSortOrder(Project project);
}