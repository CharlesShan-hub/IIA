package com.charles.server.debug.service.impl;

import com.charles.server.debug.mapper.*;
import com.charles.server.debug.service.DebugService;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Slf4j
@Service
@RequiredArgsConstructor
public class DebugServiceImpl implements DebugService {
    private final DebugAuthMapper authMapper;
    private final DebugProfileMapper profileMapper;
    private final DebugMailMapper mailMapper;
    private final DebugProjectMapper projectMapper;
    private final DebugTaskMapper taskMapper;
    private final DebugTagMapper tagMapper;
    private final DebugTaskTagMapper taskTagMapper;
    private final DebugHistoryMapper historyMapper;
    private final DebugOperationMapper operationMapper;
    private final DebugProjectLogMapper projectLogMapper;
    private final DebugRecurrenceMapper recurrenceMapper;

    @Override
    @Transactional
    public void dropUnauthTables() {
        log.warn("Debug: Performing unauthenticated data reset (TRUNCATE)...");
        // Delete in order to handle potential dependencies (if any)
        recurrenceMapper.drop();
        projectLogMapper.drop();
        historyMapper.drop();
        taskTagMapper.drop();
        tagMapper.drop();
        taskMapper.drop();
        projectMapper.drop();
        operationMapper.drop();
        
        log.info("Debug: Unauthenticated data reset successful.");
    }

    @Override
    @Transactional
    public void dropAllTables() {
        log.warn("Debug: Performing full system data reset (TRUNCATE)...");
        
        // Delete in order to handle potential dependencies (if any)
        recurrenceMapper.drop();
        projectLogMapper.drop();
        historyMapper.drop();
        taskTagMapper.drop();
        tagMapper.drop();
        taskMapper.drop();
        projectMapper.drop();
        operationMapper.drop();
        
        mailMapper.drop();
        profileMapper.drop();
        authMapper.drop();
        
        log.info("Debug: Full system data reset successful.");
    }
}