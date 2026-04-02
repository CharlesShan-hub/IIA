package com.charles.server.debug.mapper;

import org.apache.ibatis.annotations.Delete;
import org.apache.ibatis.annotations.Mapper;

@Mapper
public interface DebugOperationMapper {
    @Delete("DELETE FROM reminder_operation")
    void drop();
}
