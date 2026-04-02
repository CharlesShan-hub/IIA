package com.charles.server.debug.mapper;

import org.apache.ibatis.annotations.Delete;
import org.apache.ibatis.annotations.Mapper;

@Mapper
public interface DebugTagMapper {
    @Delete("DELETE FROM reminder_tag")
    void drop();
}
