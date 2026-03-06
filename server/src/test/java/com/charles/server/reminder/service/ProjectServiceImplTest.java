package com.charles.server.reminder.service;

import com.charles.server.reminder.dto.*;
import com.charles.server.reminder.entity.Project;
import com.charles.server.reminder.mapper.ProjectMapper;
import com.charles.server.reminder.service.impl.ProjectServiceImpl;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.*;
import java.util.List;
import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

class ProjectServiceImplTest {

    @Mock
    private ProjectMapper projectMapper;
    @Mock
    private TaskService taskService;

    private ProjectServiceImpl service;

    @BeforeEach
    void setUp() {
        MockitoAnnotations.openMocks(this);
        service = new ProjectServiceImpl(projectMapper, taskService);
    }

    @Test
    void create_assignsNextSortOrderAndDefaults() {
        // given
        ProjectCreateRequest dto = new ProjectCreateRequest();
        dto.setName("Inbox");
        when(projectMapper.findMaxSortOrderByUserIdAndArchived(1L, false)).thenReturn(5);

        // when
        service.create(1L, dto);

        // then
        ArgumentCaptor<Project> captor = ArgumentCaptor.forClass(Project.class);
        verify(projectMapper).insert(captor.capture());
        Project inserted = captor.getValue();
        assertEquals(1L, inserted.getUserId());
        assertEquals(6, inserted.getSortOrder());
        assertFalse(Boolean.TRUE.equals(inserted.getIsArchived()));
        assertEquals("Inbox", inserted.getName());
    }

    @Test
    void update_basicFields() {
        // given
        ProjectUpdateRequest dto = new ProjectUpdateRequest();
        dto.setProjectId(100L);
        dto.setName("Renamed");
        dto.setColor("#123456");
        Project existing = new Project();
        existing.setProjectId(100L);
        existing.setUserId(1L);
        existing.setIsArchived(false);
        when(projectMapper.findById(100L)).thenReturn(existing);

        // when
        service.update(1L, dto);

        // then
        ArgumentCaptor<Project> captor = ArgumentCaptor.forClass(Project.class);
        verify(projectMapper).update(captor.capture());
        Project updated = captor.getValue();
        assertEquals("Renamed", updated.getName());
        assertEquals("#123456", updated.getColor());
        assertFalse(Boolean.TRUE.equals(updated.getIsArchived()));
    }

    @Test
    void update_toggleArchive_movesToEndOfTargetGroup() {
        // given
        ProjectUpdateRequest dto = new ProjectUpdateRequest();
        dto.setProjectId(200L);
        dto.setIsArchived(true); // 从未归档切换到已归档
        Project existing = new Project();
        existing.setProjectId(200L);
        existing.setUserId(1L);
        existing.setIsArchived(false);
        when(projectMapper.findById(200L)).thenReturn(existing);
        when(projectMapper.findMaxSortOrderByUserIdAndArchived(1L, true)).thenReturn(7);

        // when
        service.update(1L, dto);

        // then
        ArgumentCaptor<Project> captor = ArgumentCaptor.forClass(Project.class);
        verify(projectMapper).update(captor.capture());
        Project updated = captor.getValue();
        assertTrue(Boolean.TRUE.equals(updated.getIsArchived()));
        assertEquals(8, updated.getSortOrder()); // 7 + 1
    }

    @Test
    void getAll_filtersByFlags() {
        ProjectGetAllRequest dto = new ProjectGetAllRequest();
        dto.setIsAll(false);
        dto.setArchived(true);
        when(projectMapper.findByUserIdAndArchived(1L, true)).thenReturn(List.of(new Project()));
        List<Project> result = service.getAll(1L, dto);
        assertEquals(1, result.size());
    }

    @Test
    void batchUpdatePosition_normalizesGaps() {
        // given：传入存在空洞/乱序的排序
        BatchUpdatePositionRequest req = new BatchUpdatePositionRequest();
        BatchUpdatePositionRequest.Position p1 = new BatchUpdatePositionRequest.Position();
        p1.setItemId(10L); p1.setSortOrder(5);
        BatchUpdatePositionRequest.Position p2 = new BatchUpdatePositionRequest.Position();
        p2.setItemId(20L); p2.setSortOrder(100);
        BatchUpdatePositionRequest.Position p3 = new BatchUpdatePositionRequest.Position();
        p3.setItemId(30L); p3.setSortOrder(7);
        req.setPos(List.of(p1, p2, p3));

        // 所有项目都属于该用户
        when(projectMapper.findById(10L)).thenReturn(projectOf(1L, 10L));
        when(projectMapper.findById(20L)).thenReturn(projectOf(1L, 20L));
        when(projectMapper.findById(30L)).thenReturn(projectOf(1L, 30L));

        // when
        service.batchUpdatePosition(1L, req);

        // then：应重排为 1,2,3（按原 sortOrder 升序）
        ArgumentCaptor<Project> captor = ArgumentCaptor.forClass(Project.class);
        verify(projectMapper, times(3)).updateSortOrder(captor.capture());
        List<Project> updates = captor.getAllValues();
        // 更新顺序与期望一致：sort = 5 → 1, sort = 7 → 2, sort = 100 → 3
        assertEquals(10L, updates.get(0).getProjectId());
        assertEquals(1, updates.get(0).getSortOrder());
        assertEquals(30L, updates.get(1).getProjectId());
        assertEquals(2, updates.get(1).getSortOrder());
        assertEquals(20L, updates.get(2).getProjectId());
        assertEquals(3, updates.get(2).getSortOrder());
    }

    @Test
    void delete_keepTasksFalse_deletesTasksThenProject() {
        ProjectDeleteRequest dto = new ProjectDeleteRequest();
        dto.setProjectId(300L);
        dto.setKeepTasks(false);
        Project existing = projectOf(1L, 300L);
        when(projectMapper.findById(300L)).thenReturn(existing);

        service.delete(1L, dto);

        verify(taskService).deleteByProjectId(1L, 300L);
        verify(projectMapper).deleteById(300L);
    }

    @Test
    void delete_keepTasksTrue_targetProjectMovesTasks() {
        ProjectDeleteRequest dto = new ProjectDeleteRequest();
        dto.setProjectId(400L);
        dto.setKeepTasks(true);
        dto.setTargetProject(true);
        dto.setTargetProjectId(401L);

        when(projectMapper.findById(400L)).thenReturn(projectOf(1L, 400L));
        when(projectMapper.findById(401L)).thenReturn(projectOf(1L, 401L));

        service.delete(1L, dto);

        verify(taskService).batchUpdateProjectId(1L, dto);
        verify(projectMapper).deleteById(400L);
    }

    private Project projectOf(Long userId, Long projectId) {
        Project p = new Project();
        p.setUserId(userId);
        p.setProjectId(projectId);
        p.setIsArchived(false);
        return p;
    }
}