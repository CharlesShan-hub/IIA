package com.charles.server.reminder.controller;

import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.security.SecurityRequirement;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.servlet.http.HttpServletRequest;
import org.springframework.beans.factory.annotation.Autowired;
import lombok.extern.slf4j.Slf4j;

import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.charles.server.reminder.service.OperationService;
import com.charles.server.auth.service.TokenService;
import com.charles.server.utils.ResponseUtils;

@Slf4j
@RequestMapping("/api/reminder/operation")
@RestController
@Tag(name = "Operation", description = "Operation revert API")
public class OperationController {

    @Autowired
    private OperationService operationService;
    @Autowired
    private TokenService tokenService;

    @PostMapping("revert")
    @Operation(
        summary = "Revert Operation",
        description = "Revert a reminder operation"
    )
    @SecurityRequirement(name = "bearer-jwt")
    public ResponseUtils<Void> revert(HttpServletRequest request) {
        Long userId = tokenService.getUserIdFromRequest(request);
        operationService.revert(userId);
        log.info("User {} revert operation successfully", userId);
        return ResponseUtils.buildEmptySuccessResponse("Reminder Operation Reverted");
    }
}
