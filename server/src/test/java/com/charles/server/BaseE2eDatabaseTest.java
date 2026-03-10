package com.charles.server;

import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.TestInstance;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.test.context.DynamicPropertyRegistry;
import org.springframework.test.context.DynamicPropertySource;

import javax.sql.DataSource;
import java.nio.charset.StandardCharsets;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.sql.Connection;
import java.sql.Statement;
import java.util.function.Function;
import java.util.regex.Pattern;

@TestInstance(TestInstance.Lifecycle.PER_CLASS)
public abstract class BaseE2eDatabaseTest {

    @Autowired
    private javax.sql.DataSource dataSource;
    @Autowired
    private JdbcTemplate jdbc;
    @Autowired
    private PasswordEncoder passwordEncoder;

    @DynamicPropertySource
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
}
