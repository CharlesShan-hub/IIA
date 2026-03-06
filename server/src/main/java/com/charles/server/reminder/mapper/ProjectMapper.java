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

    @Update("UPDATE reminder_project SET name = #{name}, description = #{description}, color = #{color}, "+
            "icon = #{icon}, sort_order = #{sortOrder}, is_archived = #{isArchived} "+
            "WHERE project_id = #{projectId}")
    int update(Project project);
    
    @Select("SELECT * FROM reminder_project WHERE project_id = #{projectId}")
    Project findById(@Param("projectId") Long projectId);

    @Select("SELECT * FROM reminder_project WHERE user_id = #{userId} AND is_archived = #{archived} ORDER BY sort_order")
    List<Project> findByUserIdAndArchived(@Param("userId") Long userId, @Param("archived") boolean archived);

    @Update("UPDATE reminder_project SET sort_order = #{sortOrder} WHERE project_id = #{projectId}")
    int updateSortOrder(Project project);

    @Delete("DELETE FROM reminder_project WHERE project_id = #{projectId}")
    int deleteById(@Param("projectId") Long projectId);
}