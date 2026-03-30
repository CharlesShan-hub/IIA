package com.charles.server.advice;

import com.charles.server.reminder.exception.ProjectException;
import com.charles.server.reminder.exception.TaskException;
import com.charles.server.reminder.exception.TagException;
import com.charles.server.auth.exception.TokenException;
import com.charles.server.auth.exception.AuthException;
import com.charles.server.utils.ResponseUtils;
import org.springframework.http.ResponseEntity;
import org.springframework.http.converter.HttpMessageNotReadableException;
import org.springframework.web.bind.MissingServletRequestParameterException;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;

@RestControllerAdvice
public class GlobalExceptionHandler {

    @ExceptionHandler(TokenException.class)
    public ResponseEntity<ResponseUtils<Object>> handleToken(TokenException ex) {
        return ResponseEntity.ok(ResponseUtils.buildErrorResponse(ex.getCode(), ex.getMessage()));
    }

    @ExceptionHandler(AuthException.class)
    public ResponseEntity<ResponseUtils<Object>> handleAuth(AuthException ex) {
        return ResponseEntity.ok(ResponseUtils.buildErrorResponse(ex.getCode(), ex.getMessage()));
    }

    @ExceptionHandler(ProjectException.class)
    public ResponseEntity<ResponseUtils<Object>> handleProject(ProjectException ex) {
        return ResponseEntity.ok(ResponseUtils.buildErrorResponse(ex.getCode(), ex.getMessage()));
    }

    @ExceptionHandler(TagException.class)
    public ResponseEntity<ResponseUtils<Object>> handleTag(TagException ex) {
        return ResponseEntity.ok(ResponseUtils.buildErrorResponse(ex.getCode(), ex.getMessage()));
    }

    @ExceptionHandler(TaskException.class)
    public ResponseEntity<ResponseUtils<Object>> handleTask(TaskException ex) {
        return ResponseEntity.ok(ResponseUtils.buildErrorResponse(ex.getCode(), ex.getMessage()));
    }

    @ExceptionHandler({HttpMessageNotReadableException.class, MissingServletRequestParameterException.class})
    public ResponseEntity<ResponseUtils<Object>> handleBadRequest(Exception ex) {
        return ResponseEntity.ok(ResponseUtils.buildErrorResponse(400, "Bad Request"));
    }

    // @ExceptionHandler(MethodArgumentNotValidException.class)
    // public ResponseEntity<Map<String,Object>> handleInvalid(MethodArgumentNotValidException ex) {
    //     String msg = ex.getBindingResult().getFieldErrors().stream()
    //             .map(e -> e.getField() + " " + e.getDefaultMessage())
    //             .collect(Collectors.joining("; "));
    //     return ResponseEntity.ok(ResponseUtils.buildErrorResponse(422, msg));
    // }

    // @ExceptionHandler(ConstraintViolationException.class)
    // public ResponseEntity<Map<String,Object>> handleConstraint(ConstraintViolationException ex) {
    //     String msg = ex.getConstraintViolations().stream()
    //             .map(v -> v.getPropertyPath() + " " + v.getMessage())
    //             .collect(Collectors.joining("; "));
    //     return ResponseEntity.ok(ResponseUtils.buildErrorResponse(422, msg));
    // }

    // @ExceptionHandler(AuthException.class)
    // public ResponseEntity<Map<String,Object>> handleAuth(AuthException ex) {
    //     int code;
    //     switch (ex.getErrorType()) {
    //         case EMAIL_ALREADY_REGISTERED: code = 409; break;
    //         case USER_NOT_FOUND: code = 404; break;
    //         case INVALID_CREDENTIALS:
    //         case VERIFICATION_CODE_INVALID:
    //         default: code = 401; break;
    //     }
    //     return ResponseEntity.ok(ResponseUtils.buildErrorResponse(code, ex.getMessage()));
    // }

    // @ExceptionHandler({TaskAccessException.class})
    // public ResponseEntity<Map<String,Object>> handleAccess(RuntimeException ex) {
    //     return ResponseEntity.ok(ResponseUtils.buildErrorResponse(403, ex.getMessage()));
    // }

    // @ExceptionHandler({DuplicateKeyException.class, DataIntegrityViolationException.class})
    // public ResponseEntity<Map<String,Object>> handleConflict(Exception ex) {
    //     return ResponseEntity.ok(ResponseUtils.buildErrorResponse(409, "Data conflict"));
    // }

    // @ExceptionHandler({java.util.NoSuchElementException.class})
    // public ResponseEntity<Map<String,Object>> handleNoSuchElement(java.util.NoSuchElementException ex) {
    //     return ResponseEntity.ok(ResponseUtils.buildErrorResponse(404, ex.getMessage()));
    // }

    // @ExceptionHandler(IllegalArgumentException.class)
    // public ResponseEntity<Map<String,Object>> handleIllegalArg(IllegalArgumentException ex) {
    //     String msg = ex.getMessage();
    //     int code = (msg != null && msg.toLowerCase().contains("already exists")) ? 409 : 400;
    //     return ResponseEntity.ok(ResponseUtils.buildErrorResponse(code, ex.getMessage()));
    // }

    // @ExceptionHandler(Throwable.class)
    // public ResponseEntity<Map<String,Object>> handleUnknown(Throwable ex) {
    //     return ResponseEntity.ok(ResponseUtils.buildErrorResponse(500, "Internal Server Error"));
    // }
}