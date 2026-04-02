package com.charles.server.debug.controller;

import com.charles.server.debug.service.DebugService;
import com.charles.server.utils.ResponseUtils;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import io.swagger.v3.oas.annotations.security.SecurityRequirement;
import jakarta.servlet.http.HttpServletRequest;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.context.annotation.Profile;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import io.swagger.v3.oas.annotations.media.Schema;

@Slf4j
@RestController
@RequestMapping("/api/debug")
@RequiredArgsConstructor
@Profile({"dev", "test"})
@Tag(name = "Debug Utilities", description = "Development & Debugging tools. Only available in dev/test profiles.")
public class DebugController {

    private final DebugService debugService;

    @PostMapping("clear-unauth-data")
    @Operation(summary = "Clear Unauthenticated Business Data", description = "DANGEROUS: Removes all tasks, projects, and tags for the current user.")
    @SecurityRequirement(name = "bearer-jwt")
    @Schema(description = "Clears all business data for the current user.")
    public ResponseUtils<Void> clearUnauthData(HttpServletRequest request) {
        debugService.dropUnauthTables();
        log.warn("Debug API: User cleared unauthenticated business data");
        return ResponseUtils.buildEmptySuccessResponse("All unauthenticated business data has been cleared.");
    }

    @PostMapping("clear-all-data")
    @Operation(summary = "Clear All System Data", description = "EXTREMELY DANGEROUS: Wipes entire database tables.")
    @SecurityRequirement(name = "bearer-jwt")
    @Schema(description = "Clears all system data, including user accounts.")
    public ResponseUtils<Void> resetSystem() {
        debugService.dropAllTables();
        log.warn("Debug API: System-wide data reset performed!");
        return ResponseUtils.buildEmptySuccessResponse("System data reset successful.");
    }
}