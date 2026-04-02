package com.charles.server.debug.mapper;

import org.apache.ibatis.annotations.Delete;
import org.apache.ibatis.annotations.Mapper;

@Mapper
public interface DebugProjectMapper {
    @Delete("DELETE FROM reminder_project")
    void drop();
}
