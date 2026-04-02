package com.charles.server.debug.mapper;

import org.apache.ibatis.annotations.Delete;
import org.apache.ibatis.annotations.Mapper;

@Mapper
public interface DebugProjectLogMapper {
    @Delete("DELETE FROM reminder_project_log")
    void drop();
}
