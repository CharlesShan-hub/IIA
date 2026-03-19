package com.charles.server.reminder.mapper;

import com.charles.server.reminder.entity.ProjectLog;
import org.apache.ibatis.annotations.Insert;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Param;
import org.apache.ibatis.annotations.Select;
import org.apache.ibatis.annotations.Delete;

import java.util.List;

@Mapper
public interface ProjectLogMapper {
    
    @Insert("INSERT INTO reminder_project_log(project_id, operation_id, user_id, name, " +
            "description, color, icon, sort_order, is_archived) " +
            "VALUES(#{projectId}, #{operationId}, #{userId}, #{name}, " +
            "#{description}, #{color}, #{icon}, #{sortOrder}, #{isArchived})")
    int insert(ProjectLog projectLog);
    
    @Select("SELECT * FROM reminder_project_log WHERE project_id = #{projectId} ORDER BY created_at DESC")
    List<ProjectLog> findByProjectId(@Param("projectId") Long projectId);
    
    @Select("SELECT * FROM reminder_project_log WHERE operation_id = #{operationId}")
    List<ProjectLog> findByOperationId(@Param("operationId") Long operationId);
    
    @Select("SELECT * FROM reminder_project_log WHERE project_id = #{projectId} AND operation_id = #{operationId}")
    ProjectLog findByProjectIdAndOperationId(@Param("projectId") Long projectId, @Param("operationId") Long operationId);
    
    /**
     * 删除指定操作ID的历史记录
     * @param operationId 操作ID
     * @return 删除的行数
     */
    @Delete("DELETE FROM reminder_project_log WHERE operation_id = #{operationId}")
    int deleteByOperationId(@Param("operationId") Long operationId);
}