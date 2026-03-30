package com.charles.server.config;

import io.swagger.v3.oas.annotations.OpenAPIDefinition;
import io.swagger.v3.oas.annotations.enums.SecuritySchemeIn;
import io.swagger.v3.oas.annotations.enums.SecuritySchemeType;
import io.swagger.v3.oas.annotations.info.Contact;
import io.swagger.v3.oas.annotations.info.Info;
import io.swagger.v3.oas.annotations.info.License;
import io.swagger.v3.oas.annotations.security.SecurityRequirement;
import io.swagger.v3.oas.annotations.security.SecurityScheme;
import io.swagger.v3.oas.models.OpenAPI;
import io.swagger.v3.oas.models.servers.Server;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
@OpenAPIDefinition(
    info = @Info(
        title = "IIA Server API",
        version = "1.0.0",
        description = "IIA (Intelligent Information Assistant) Server API Documentation",
        contact = @Contact(
            name = "Charles",
            email = "inforassistant@foxmail.com"
        ),
        license = @License(
            name = "Apache 2.0",
            url = "http://www.apache.org/licenses/LICENSE-2.0.html"
        )
    ),
    security = @SecurityRequirement(name = "bearer-jwt")
)
@SecurityScheme(
    name = "bearer-jwt",
    type = SecuritySchemeType.HTTP,
    scheme = "bearer",
    bearerFormat = "JWT",
    in = SecuritySchemeIn.HEADER,
    description = "JWT authentication token, format: Bearer {token}",
    extensions = {
        @io.swagger.v3.oas.annotations.extensions.Extension(
            name = "x-apifox",
            properties = {
                @io.swagger.v3.oas.annotations.extensions.ExtensionProperty(name = "variable", value = "access_token")
            }
        )
    }
)
public class OpenApiConfig {

    @Bean
    public OpenAPI customOpenAPI() {
        return new OpenAPI()
            .addServersItem(new Server().url("http://localhost:9424").description("Local Development Environment"))
            .addServersItem(new Server().url("http://10.15.0.21:9424").description("Test Environment"));
    }
}