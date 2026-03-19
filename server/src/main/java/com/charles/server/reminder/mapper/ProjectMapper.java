package com.charles.server.reminder.mapper;

import com.charles.server.reminder.entity.Project;
import org.apache.ibatis.annotations.*;

import java.util.List;

@Mapper
public interface ProjectMapper {
    
    @Insert({
            "<script>",
            "INSERT INTO reminder_project",
            "<trim prefix='(' suffix=')' suffixOverrides=','>",
            "  <if test='projectId != null'>project_id,</if>",
            "  user_id, name, description, color, icon, sort_order, is_archived, operation_id",
            "</trim>",
            "<trim prefix='VALUES(' suffix=')' suffixOverrides=','>",
            "  <if test='projectId != null'>#{projectId},</if>",
            "  #{userId}, #{name}, #{description}, #{color}, #{icon}, #{sortOrder}, #{isArchived}, #{operationId}",
            "</trim>",
            "</script>"
    })
    @Options(useGeneratedKeys = true, keyProperty = "projectId", keyColumn = "project_id")
    int insert(Project project);

    @Update("UPDATE reminder_project SET name = #{name}, description = #{description}, color = #{color}, "+
            "icon = #{icon}, sort_order = #{sortOrder}, is_archived = #{isArchived}, operation_id = #{operationId} "+
            "WHERE project_id = #{projectId}")
    int update(Project project);
    
    @Select("SELECT * FROM reminder_project WHERE project_id = #{projectId}")
    Project findById(@Param("projectId") Long projectId);

    @Select("SELECT * FROM reminder_project WHERE user_id = #{userId} AND is_archived = #{archived} ORDER BY sort_order")
    List<Project> findByUserIdAndArchived(@Param("userId") Long userId, @Param("archived") boolean archived);

    @Select("SELECT COALESCE(MAX(sort_order), 0) FROM reminder_project WHERE user_id = #{userId} AND is_archived = #{archived}")
    Integer findMaxSortOrderByUserIdAndArchived(@Param("userId") Long userId, @Param("archived") boolean archived);

    @Update("UPDATE reminder_project SET sort_order = #{sortOrder} WHERE project_id = #{projectId}")
    int updateSortOrder(Project project);

    @Delete("DELETE FROM reminder_project WHERE project_id = #{projectId}")
    int deleteById(@Param("projectId") Long projectId);

    @Select("SELECT * FROM reminder_project WHERE user_id = #{userId} AND name = #{name} LIMIT 1")
    Project findByUserIdAndName(@Param("userId") Long userId, @Param("name") String name);
    
    /**
     * 根据操作ID查找项目
     * @param operationId 操作ID
     * @return 项目列表
     */
    @Select("SELECT * FROM reminder_project WHERE operation_id = #{operationId}")
    List<Project> findByOperationId(@Param("operationId") Long operationId);
    
    /**
     * 根据项目ID和操作ID删除项目
     * @param projectId 项目ID
     * @param operationId 操作ID
     * @return 删除的行数
     */
    @Delete("DELETE FROM reminder_project WHERE project_id = #{projectId} AND operation_id = #{operationId}")
    int deleteByProjectIdAndOperationId(@Param("projectId") Long projectId, @Param("operationId") Long operationId);
    
    /**
     * 根据操作ID删除项目
     * @param operationId 操作ID
     * @return 删除的行数
     */
    @Delete("DELETE FROM reminder_project WHERE operation_id = #{operationId}")
    int deleteByOperationId(@Param("operationId") Long operationId);
}
