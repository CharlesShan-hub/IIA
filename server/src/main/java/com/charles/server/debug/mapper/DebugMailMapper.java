package com.charles.server.debug.mapper;

import org.apache.ibatis.annotations.Delete;
import org.apache.ibatis.annotations.Mapper;

@Mapper
public interface DebugMailMapper {
    @Delete("DELETE FROM iia_mail")
    void drop();
}
