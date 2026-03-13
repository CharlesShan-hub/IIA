package com.charles.server.reminder.testutils;

import com.charles.server.BaseE2eDatabaseTest;
import com.charles.server.reminder.dto.ProjectCreateRequest;
import com.charles.server.reminder.dto.TaskCreateRequest;
import com.charles.server.reminder.dto.TaskUpdateCompletedRequest;
import com.charles.server.reminder.dto.TaskUpdateAbandonedRequest;
import com.charles.server.reminder.entity.Project;
import com.charles.server.reminder.entity.Task;
import com.charles.server.reminder.mapper.ProjectMapper;
import com.charles.server.reminder.mapper.TaskMapper;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.ResultActions;

import java.util.Comparator;
import java.util.List;
import java.util.Optional;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

/**
 * 测试工具类，封装常用的测试操作
 */
@AutoConfigureMockMvc(addFilters = false)
public class TaskTestUtils extends BaseE2eDatabaseTest {
    
    @Autowired
    protected MockMvc mockMvc;
    
    @Autowired
    protected ObjectMapper objectMapper;
    
    @Autowired
    protected ProjectMapper projectMapper;
    
    @Autowired
    protected TaskMapper taskMapper;
    
    /**
     * 创建项目
     * @param projectName 项目名称
     * @return 项目ID
     */
    public Long createProject(String projectName) throws Exception {
        ProjectCreateRequest request = new ProjectCreateRequest();
        request.setName(projectName);
        
        mockMvc.perform(post("/api/reminder/projects/create")
                .contentType(MediaType.APPLICATION_JSON)
                .content(objectMapper.writeValueAsString(request)))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.code").value(200));
        
        List<Project> projects = projectMapper.findByUserIdAndArchived(1L, false);
        Optional<Project> project = projects.stream()
                .filter(p -> projectName.equals(p.getName()))
                .findFirst();
        
        if (!project.isPresent()) {
            throw new RuntimeException("Project '" + projectName + "' not found after creation");
        }
        
        return project.get().getProjectId();
    }
    
    /**
     * 创建根任务
     * @param projectId 项目ID
     * @param title 任务标题
     * @return 任务ID
     */
    public Long createRootTask(Long projectId, String title) throws Exception {
        TaskCreateRequest request = new TaskCreateRequest();
        request.setProjectId(projectId);
        request.setTitle(title);
        request.setIsRecurring(false);
        
        mockMvc.perform(post("/api/reminder/task/create")
                .contentType(MediaType.APPLICATION_JSON)
                .content(objectMapper.writeValueAsString(request)))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.code").value(200));
        
        List<Task> tasks = taskMapper.findByUserIdAndProjectId(1L, projectId);
        Optional<Task> task = tasks.stream()
                .filter(t -> title.equals(t.getTitle()))
                .findFirst();
        
        if (!task.isPresent()) {
            throw new RuntimeException("Task '" + title + "' not found after creation");
        }
        
        return task.get().getTaskId();
    }
    
    /**
     * 创建子任务
     * @param projectId 项目ID
     * @param parentTaskId 父任务ID
     * @param title 任务标题
     * @return 任务ID
     */
    public Long createSubTask(Long projectId, Long parentTaskId, String title) throws Exception {
        TaskCreateRequest request = new TaskCreateRequest();
        request.setProjectId(projectId);
        request.setParentTaskId(parentTaskId);
        request.setTitle(title);
        request.setIsRecurring(false);
        
        mockMvc.perform(post("/api/reminder/task/create")
                .contentType(MediaType.APPLICATION_JSON)
                .content(objectMapper.writeValueAsString(request)))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.code").value(200));
        
        List<Task> tasks = taskMapper.findByUserIdAndProjectId(1L, projectId);
        Optional<Task> task = tasks.stream()
                .filter(t -> title.equals(t.getTitle()) && parentTaskId.equals(t.getParentTaskId()))
                .findFirst();
        
        if (!task.isPresent()) {
            throw new RuntimeException("Subtask '" + title + "' not found after creation");
        }
        
        return task.get().getTaskId();
    }
    
    /**
     * 更新任务完成状态
     * @param taskId 任务ID
     * @param isCompleted 是否完成
     */
    public void updateTaskCompletedStatus(Long taskId, Boolean isCompleted) throws Exception {
        TaskUpdateCompletedRequest request = new TaskUpdateCompletedRequest();
        request.setTaskId(taskId);
        request.setIsCompleted(isCompleted);
        
        mockMvc.perform(patch("/api/reminder/task/update/completed")
                .contentType(MediaType.APPLICATION_JSON)
                .content(objectMapper.writeValueAsString(request)))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.code").value(200));
    }
    
    /**
     * 更新任务废弃状态
     * @param taskId 任务ID
     * @param isAbandoned 是否废弃
     */
    public void updateTaskAbandonedStatus(Long taskId, Boolean isAbandoned) throws Exception {
        TaskUpdateAbandonedRequest request = new TaskUpdateAbandonedRequest();
        request.setTaskId(taskId);
        request.setIsAbandoned(isAbandoned);
        
        mockMvc.perform(patch("/api/reminder/task/update/abandoned")
                .contentType(MediaType.APPLICATION_JSON)
                .content(objectMapper.writeValueAsString(request)))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.code").value(200));
    }
    
    /**
     * 获取任务
     * @param taskId 任务ID
     * @return 任务对象
     */
    public Task getTask(Long taskId) {
        return taskMapper.findById(taskId);
    }
    
    /**
     * 获取项目中的所有任务
     * @param projectId 项目ID
     * @return 任务列表
     */
    public List<Task> getTasksInProject(Long projectId) {
        return taskMapper.findByUserIdAndProjectId(1L, projectId);
    }
    
    /**
     * 获取任务的子任务
     * @param parentTaskId 父任务ID
     * @return 子任务列表
     */
    public List<Task> getChildTasks(Long parentTaskId) {
        return taskMapper.findByUserIdAndParentTaskId(1L, parentTaskId);
    }
    
    /**
     * 验证任务状态
     * @param taskId 任务ID
     * @param expectedCompleted 期望的完成状态
     * @param expectedAbandoned 期望的废弃状态
     */
    public void assertTaskStatus(Long taskId, Boolean expectedCompleted, Boolean expectedAbandoned) {
        Task task = getTask(taskId);
        if (expectedCompleted != null) {
            org.junit.jupiter.api.Assertions.assertEquals(expectedCompleted, task.getIsCompleted(),
                    "Task " + taskId + " completed status mismatch");
        }
        if (expectedAbandoned != null) {
            org.junit.jupiter.api.Assertions.assertEquals(expectedAbandoned, task.getIsAbandoned(),
                    "Task " + taskId + " abandoned status mismatch");
        }
    }
    
    /**
     * 验证任务排序
     * @param projectId 项目ID
     * @param expectedTitles 期望的任务标题顺序
     */
    public void assertTaskOrder(Long projectId, String... expectedTitles) {
        List<Task> tasks = getTasksInProject(projectId);
        tasks.sort(Comparator.comparing(Task::getSortOrder));
        
        org.junit.jupiter.api.Assertions.assertEquals(expectedTitles.length, tasks.size(),
                "Number of tasks mismatch");
        
        for (int i = 0; i < expectedTitles.length; i++) {
            org.junit.jupiter.api.Assertions.assertEquals(expectedTitles[i], tasks.get(i).getTitle(),
                    "Task order mismatch at position " + i);
        }
    }
    
    /**
     * 创建测试场景：父任务和子任务
     * @param projectName 项目名称
     * @param parentTitle 父任务标题
     * @param childTitle 子任务标题
     * @return 包含项目ID、父任务ID、子任务ID的数组
     */
    public Long[] createParentChildScenario(String projectName, String parentTitle, String childTitle) throws Exception {
        Long projectId = createProject(projectName);
        Long parentTaskId = createRootTask(projectId, parentTitle);
        Long childTaskId = createSubTask(projectId, parentTaskId, childTitle);
        
        return new Long[]{projectId, parentTaskId, childTaskId};
    }
}