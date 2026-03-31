package com.charles.server.config;

import lombok.Data;
import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.stereotype.Component;

@Component
@ConfigurationProperties(prefix = "app")
@Data
public class AppConfig {
    private String env = "dev";
    private Verification verification = new Verification();
    private boolean debug = false;
    private boolean mockEmail = false;
    private Logging logging = new Logging();
    private Security security = new Security();
    
    @Data
    public static class Verification {
        private Code code = new Code();
        
        @Data
        public static class Code {
            private boolean returnToClient = false;
        }
    }
    
    @Data
    public static class Logging {
        private boolean sql = false;
        private boolean request = false;
    }
    
    @Data
    public static class Security {
        private Cors cors = new Cors();
        
        @Data
        public static class Cors {
            private String allowedOrigins = "";
            private String allowedMethods = "*";
            private String allowedHeaders = "*";
            private boolean allowCredentials = true;
        }
    }
    
    // 便捷方法
    public boolean isDevelopment() {
        return "dev".equals(env) || "local".equals(env);
    }
    
    public boolean isProduction() {
        return "prod".equals(env);
    }
    
    public boolean shouldReturnVerificationCode() {
        return verification.getCode().isReturnToClient();
    }
}