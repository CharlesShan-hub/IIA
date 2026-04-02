package com.charles.server.debug.mapper;

import org.apache.ibatis.annotations.Delete;
import org.apache.ibatis.annotations.Mapper;

@Mapper
public interface DebugTaskMapper {
    @Delete("DELETE FROM reminder_task")
    void drop();
}
