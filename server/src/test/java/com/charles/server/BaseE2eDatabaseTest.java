package com.charles.server;

import com.charles.server.reminder.dto.ProjectCreateRequest;
import com.charles.server.reminder.dto.ProjectDeleteRequest;
import com.charles.server.reminder.dto.ProjectUpdateRequest;
import com.charles.server.reminder.dto.TaskCreateRequest;
import com.charles.server.reminder.dto.TaskUpdateCompletedRequest;
import com.charles.server.reminder.dto.TaskUpdateAbandonedRequest;
import com.charles.server.reminder.entity.Project;
import com.charles.server.reminder.entity.Task;
import com.charles.server.reminder.mapper.ProjectMapper;
import com.charles.server.reminder.mapper.TaskMapper;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.TestInstance;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import com.charles.server.utils.TestTokenServiceConfig;
import org.springframework.context.annotation.Import;
import org.springframework.http.MediaType;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.test.context.DynamicPropertyRegistry;
import org.springframework.test.web.servlet.MockMvc;

import javax.sql.DataSource;
import java.nio.charset.StandardCharsets;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.sql.Connection;
import java.sql.Statement;
import java.util.List;
import java.util.Optional;
import java.util.function.Function;
import java.util.regex.Pattern;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;
import org.springframework.boot.test.context.SpringBootTest;

@TestInstance(TestInstance.Lifecycle.PER_CLASS)
@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.MOCK)
@AutoConfigureMockMvc(addFilters = false)
@Import(TestTokenServiceConfig.class)
public abstract class BaseE2eDatabaseTest {

    @Autowired
    private javax.sql.DataSource dataSource;
    @Autowired
    private JdbcTemplate jdbc;
    @Autowired
    private PasswordEncoder passwordEncoder;
    
    @Autowired
    protected MockMvc mockMvc;
    @Autowired
    protected ObjectMapper objectMapper;
    @Autowired
    protected ProjectMapper projectMapper;
    @Autowired
    protected TaskMapper taskMapper;

    @org.springframework.test.context.DynamicPropertySource
    static void dbProps(DynamicPropertyRegistry registry) {
        registry.add("spring.datasource.url", () -> System.getProperty(
                "test.db.url",
                "jdbc:mysql://127.0.0.1:3306/iia_test?createDatabaseIfNotExist=true&useSSL=false&allowPublicKeyRetrieval=true&serverTimezone=UTC"
        ));
        registry.add("spring.datasource.username", () -> System.getProperty("test.db.username", "root"));
        registry.add("spring.datasource.password", () -> System.getProperty("test.db.password", ""));
    }

    @BeforeAll
    void initSchema() {
        recreateDatabase();
        executeSqlFiles(dataSource);
        seedBaseUser(jdbc, passwordEncoder);
        afterSchemaInitialized(jdbc);
    }

    protected void afterSchemaInitialized(JdbcTemplate jdbc) {}

    protected long seedUserId() { return 1L; }
    protected String seedEmail() { return "test@example.com"; }
    protected String seedUsername() { return "test_user"; }
    protected String seedPassword() { return "test"; }

    private void recreateDatabase() {
        String adminUrl = System.getProperty("test.db.admin.url",
                "jdbc:mysql://127.0.0.1:3306/?useSSL=false&allowPublicKeyRetrieval=true&serverTimezone=UTC");
        String user = System.getProperty("test.db.username", "root");
        String pass = System.getProperty("test.db.password", "");
        try (Connection conn = java.sql.DriverManager.getConnection(adminUrl, user, pass);
             Statement st = conn.createStatement()) {
            st.execute("DROP DATABASE IF EXISTS iia_test");
            st.execute("CREATE DATABASE iia_test DEFAULT CHARACTER SET utf8mb4");
        } catch (java.sql.SQLException e) {
            throw new RuntimeException("Failed to recreate iia_test database", e);
        }
    }

    private void executeSqlFiles(DataSource dataSource) {
        Function<String, org.springframework.core.io.Resource> sanitize = (path) -> {
            try {
                String content = java.nio.file.Files.readString(java.nio.file.Path.of(path));
                String sanitized = Pattern.compile("(?im)^\\s*USE\\s+[^;]+;\\s*$")
                        .matcher(content)
                        .replaceAll("");
                byte[] sqlBytes = java.util.Objects.requireNonNull(
                        java.util.Objects.requireNonNull(sanitized, "SQL content must not be null")
                                .getBytes(StandardCharsets.UTF_8),
                        "SQL bytes must not be null");
                return new org.springframework.core.io.ByteArrayResource(sqlBytes, path);
            } catch (java.io.IOException ex) {
                throw new RuntimeException("Failed to read SQL file: " + path, ex);
            }
        };
        Path sqlDir = Paths.get(System.getProperty("user.dir")).getParent().resolve("sql");
        org.springframework.jdbc.datasource.init.ResourceDatabasePopulator pop =
                new org.springframework.jdbc.datasource.init.ResourceDatabasePopulator(
                        sanitize.apply(sqlDir.resolve("create_auth.sql").toString()),
                        sanitize.apply(sqlDir.resolve("create_task.sql").toString()));
        pop.execute(java.util.Objects.requireNonNull(dataSource, "DataSource must not be null"));
    }

    private void seedBaseUser(JdbcTemplate jdbc, PasswordEncoder passwordEncoder) {
        long userId = seedUserId();
        String email = seedEmail();
        String username = seedUsername();
        String hash = passwordEncoder.encode(seedPassword());

        jdbc.update("DELETE FROM iia_mail WHERE email = ?", email);
        jdbc.update("DELETE FROM iia_profile WHERE user_id = ?", userId);
        jdbc.update("DELETE FROM iia_auth WHERE user_id = ?", userId);

        jdbc.update("INSERT INTO iia_auth(user_id, password_hash) VALUES (?, ?)", userId, hash);
        jdbc.update("INSERT INTO iia_profile(user_id, username) VALUES (?, ?)", userId, username);
        jdbc.update("INSERT INTO iia_mail(user_id, email) VALUES (?, ?)", userId, email);
    }
    
    // ========== 基础测试函数 ==========
    
    /**
     * 创建项目
     */
    protected Long createProject(String projectName) throws Exception {
        return createProject(projectName, 200);
    }

    protected Long createProject(String projectName, int expectCode) throws Exception {
        ProjectCreateRequest request = new ProjectCreateRequest();
        request.setName(projectName);

        mockMvc.perform(post("/api/reminder/project/create")
                .contentType(java.util.Objects.requireNonNull(MediaType.APPLICATION_JSON))
                .content(java.util.Objects.requireNonNull(objectMapper.writeValueAsString(request))))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.code").value(expectCode));

        if (expectCode != 200) {
            return null;
        }

        List<Project> projects = projectMapper.findByUserIdAndArchived(1L, false);
        java.util.Optional<Project> opt = projects.stream()
                .filter(p -> projectName.equals(p.getName()))
                .findFirst();

        if (!opt.isPresent()) {
            throw new RuntimeException("项目创建失败: " + projectName);
        }

        return opt.get().getProjectId();
    }

    /**
     * 更新项目
     */
    protected void updateProject(ProjectUpdateRequest request) throws Exception {
        updateProject(request, 200);
    }

    protected void updateProject(ProjectUpdateRequest request, int expectCode) throws Exception {
        mockMvc.perform(post("/api/reminder/project/update")
                .contentType(java.util.Objects.requireNonNull(MediaType.APPLICATION_JSON))
                .content(java.util.Objects.requireNonNull(objectMapper.writeValueAsString(request))))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.code").value(expectCode));
    }

    protected void deleteProject(ProjectDeleteRequest request) throws Exception {
        deleteProject(request, 200);
    }

    protected void deleteProject(ProjectDeleteRequest request, int expectCode) throws Exception {
        mockMvc.perform(post("/api/reminder/project/delete")
                .contentType(java.util.Objects.requireNonNull(MediaType.APPLICATION_JSON))
                .content(java.util.Objects.requireNonNull(objectMapper.writeValueAsString(request))))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.code").value(expectCode));
    }
    
    /**
     * 创建根任务
     */
    protected Long createRootTask(Long projectId, String title) throws Exception {
        TaskCreateRequest request = new TaskCreateRequest();
        if (projectId != null) {
            request.setProjectId(projectId);
        }
        request.setTitle(title);

        mockMvc.perform(post("/api/reminder/task/create")
                .contentType(java.util.Objects.requireNonNull(MediaType.APPLICATION_JSON))
                .content(java.util.Objects.requireNonNull(objectMapper.writeValueAsString(request))))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.code").value(200));

        // 从数据库获取创建的任务（使用默认用户ID 1L）
        List<Task> tasks = (projectId == null)
                ? taskMapper.findByUserIdAndProjectIdIsNull(1L)
                : taskMapper.findByUserIdAndProjectId(1L, projectId);
        Optional<Task> task = tasks.stream()
                .filter(t -> title.equals(t.getTitle()))
                .filter(t -> t.getParentTaskId() == null)
                .findFirst();

        return task.map(Task::getTaskId)
                .orElseThrow(() -> new RuntimeException("任务创建失败: " + title));
    }
    
    /**
     * 创建子任务
     */
    protected Long createSubTask(Long parentTaskId, String title) throws Exception {
        Task parentTask = taskMapper.findById(parentTaskId);
        if (parentTask == null) {
            throw new RuntimeException("父任务不存在: " + parentTaskId);
        }
        
        TaskCreateRequest request = new TaskCreateRequest();
        request.setProjectId(parentTask.getProjectId());
        request.setTitle(title);
        request.setParentTaskId(parentTaskId);
        
        mockMvc.perform(post("/api/reminder/task/create")
                .contentType(java.util.Objects.requireNonNull(MediaType.APPLICATION_JSON))
                .content(java.util.Objects.requireNonNull(objectMapper.writeValueAsString(request))))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.code").value(200));
        
        // 从数据库获取创建的子任务（使用默认用户ID 1L）
        List<Task> tasks = taskMapper.findByUserIdAndParentTaskId(1L, parentTaskId);
        Optional<Task> task = tasks.stream()
                .filter(t -> t.getTitle().equals(title))
                .findFirst();
        
        return task.map(Task::getTaskId)
                .orElseThrow(() -> new RuntimeException("子任务创建失败: " + title));
    }
    
    /**
     * 更新任务完成状态
     */
    protected void updateTaskCompletedStatus(Long taskId, Boolean completed) throws Exception {
        TaskUpdateCompletedRequest request = new TaskUpdateCompletedRequest();
        request.setTaskId(taskId);
        request.setIsCompleted(completed);
        
        mockMvc.perform(post("/api/reminder/tasks/update/completed")
                .contentType(java.util.Objects.requireNonNull(MediaType.APPLICATION_JSON))
                .content(java.util.Objects.requireNonNull(objectMapper.writeValueAsString(request))))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.code").value(200));
    }
    
    /**
     * 更新任务废弃状态
     */
    protected void updateTaskAbandonedStatus(Long taskId, Boolean abandoned) throws Exception {
        TaskUpdateAbandonedRequest request = new TaskUpdateAbandonedRequest();
        request.setTaskId(taskId);
        request.setIsAbandoned(abandoned);
        
        mockMvc.perform(post("/api/reminder/tasks/update/abandoned")
                .contentType(java.util.Objects.requireNonNull(MediaType.APPLICATION_JSON))
                .content(java.util.Objects.requireNonNull(objectMapper.writeValueAsString(request))))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.code").value(200));
    }
    
    /**
     * 获取任务
     */
    protected Task getTask(Long taskId) {
        return taskMapper.findById(taskId);
    }
    
    /**
     * 断言任务状态
     */
    protected void assertTaskStatus(Long taskId, Boolean expectedCompleted, Boolean expectedAbandoned) {
        Task task = getTask(taskId);
        if (expectedCompleted != null) {
            org.junit.jupiter.api.Assertions.assertEquals(expectedCompleted, task.getIsCompleted(),
                    "任务完成状态不匹配, 任务ID: " + taskId);
        }
        if (expectedAbandoned != null) {
            org.junit.jupiter.api.Assertions.assertEquals(expectedAbandoned, task.getIsAbandoned(),
                    "任务废弃状态不匹配, 任务ID: " + taskId);
        }
    }
    
    /**
     * 创建父子任务场景
     */
    protected Long[] createParentChildScenario(String projectName, String parentTitle, String childTitle) throws Exception {
        Long projectId = createProject(projectName);
        Long parentTaskId = createRootTask(projectId, parentTitle);
        Long childTaskId = createSubTask(parentTaskId, childTitle);
        return new Long[]{projectId, parentTaskId, childTaskId};
    }
}
