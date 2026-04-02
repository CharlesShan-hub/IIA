package com.charles.server.debug.mapper;

import org.apache.ibatis.annotations.Delete;
import org.apache.ibatis.annotations.Mapper;

@Mapper
public interface DebugAuthMapper {
    @Delete("DELETE FROM iia_auth")
    void drop();
}
