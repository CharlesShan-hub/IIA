package com.charles.server.reminder.controller;

// import com.charles.server.auth.service.TokenService;
// import com.charles.server.reminder.entity.Recurrence;
// import com.charles.server.reminder.service.RecurrenceService;

// import com.charles.server.utils.ResponseUtils;
// import jakarta.servlet.http.HttpServletRequest;
// import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.web.bind.annotation.*;

// import java.util.Map;

@RestController
@RequestMapping("/api/reminder/recurrences")
@RequiredArgsConstructor
@Slf4j
public class RecurrenceController {
    
    // private final RecurrenceService recurrenceService;
    // private final TokenService tokenService;
    
    /**
     * 根据任务ID查询循环配置
     */
    // @GetMapping("/task/{taskId}")
    // public Map<String, Object> getByTaskId(@PathVariable("taskId") Long taskId, HttpServletRequest request) {
    //     try {
    //         Long userId = tokenService.getUserIdFromRequest(request);
    //         log.info("用户查询循环任务配置: userId={}, taskId={}", userId, taskId);
            
    //         Recurrence recurrence = recurrenceService.getByTaskId(taskId);
    //         if (recurrence != null) {
    //             return ResponseUtils.buildSuccessResponse(recurrence, "查询循环任务配置成功");
    //         } else {
    //             return ResponseUtils.buildErrorResponse("未找到循环任务配置");
    //         }
    //     } catch (Exception e) {
    //         log.error("查询循环任务配置失败: taskId={}, error: {}", taskId, e.getMessage(), e);
    //         return ResponseUtils.buildErrorResponse("查询循环任务配置失败: " + e.getMessage());
    //     }
    // }
    
    /**
     * 更新循环任务配置
     */
    // @PutMapping
    // public Map<String, Object> update(@RequestBody Recurrence recurrence, HttpServletRequest request) {
    //     try {
    //         Long userId = tokenService.getUserIdFromRequest(request);
    //         log.info("用户更新循环任务配置: userId={}, recurrence={}", userId, recurrence);
            
    //         int result = recurrenceService.update(recurrence);
    //         if (result > 0) {
    //             return ResponseUtils.buildSuccessResponse(null, "更新循环任务配置成功");
    //         } else {
    //             return ResponseUtils.buildErrorResponse("更新循环任务配置失败");
    //         }
    //     } catch (Exception e) {
    //         log.error("更新循环任务配置失败: {}, error: {}", recurrence, e.getMessage(), e);
    //         return ResponseUtils.buildErrorResponse("更新循环任务配置失败: " + e.getMessage());
    //     }
    // }
    
    /**
     * 更新下一次发生时间
     */
    // @PutMapping("/next-time/{taskId}")
    // public Map<String, Object> updateNextTime(@PathVariable("taskId") Long taskId, 
    //                                          @RequestParam("nextTime") LocalDateTime nextTime, 
    //                                          HttpServletRequest request) {
    //     try {
    //         Long userId = tokenService.getUserIdFromRequest(request);
    //         log.info("用户更新循环任务下一次发生时间: userId={}, taskId={}, nextTime={}", userId, taskId, nextTime);
            
    //         int result = recurrenceService.updateNextTime(taskId, nextTime);
    //         if (result > 0) {
    //             return ResponseUtils.buildSuccessResponse(null, "更新下一次发生时间成功");
    //         } else {
    //             return ResponseUtils.buildErrorResponse("更新下一次发生时间失败");
    //         }
    //     } catch (Exception e) {
    //         log.error("更新循环任务下一次发生时间失败: taskId={}, nextTime={}, error: {}", taskId, nextTime, e.getMessage(), e);
    //         return ResponseUtils.buildErrorResponse("更新下一次发生时间失败: " + e.getMessage());
    //     }
    // }
    
    /**
     * 更新重复次数
     */
    // @PutMapping("/count/{taskId}")
    // public Map<String, Object> updateCount(@PathVariable("taskId") Long taskId, 
    //                                       @RequestParam("count") Integer count, 
    //                                       HttpServletRequest request) {
    //     try {
    //         Long userId = tokenService.getUserIdFromRequest(request);
    //         log.info("用户更新循环任务重复次数: userId={}, taskId={}, count={}", userId, taskId, count);
            
    //         int result = recurrenceService.updateCount(taskId, count);
    //         if (result > 0) {
    //             return ResponseUtils.buildSuccessResponse(null, "更新重复次数成功");
    //         } else {
    //             return ResponseUtils.buildErrorResponse("更新重复次数失败");
    //         }
    //     } catch (Exception e) {
    //         log.error("更新循环任务重复次数失败: taskId={}, count={}, error: {}", taskId, count, e.getMessage(), e);
    //         return ResponseUtils.buildErrorResponse("更新重复次数失败: " + e.getMessage());
    //     }
    // }
    
    /**
     * 删除循环任务配置
     */
    // @DeleteMapping("/task/{taskId}")
    // public Map<String, Object> deleteByTaskId(@PathVariable("taskId") Long taskId, HttpServletRequest request) {
    //     try {
    //         Long userId = tokenService.getUserIdFromRequest(request);
    //         log.info("用户删除循环任务配置: userId={}, taskId={}", userId, taskId);
            
    //         int result = recurrenceService.deleteByTaskId(taskId);
    //         if (result > 0) {
    //             return ResponseUtils.buildSuccessResponse(null, "删除循环任务配置成功");
    //         } else {
    //             return ResponseUtils.buildErrorResponse("删除循环任务配置失败");
    //         }
    //     } catch (Exception e) {
    //         log.error("删除循环任务配置失败: taskId={}, error: {}", taskId, e.getMessage(), e);
    //         return ResponseUtils.buildErrorResponse("删除循环任务配置失败: " + e.getMessage());
    //     }
    // }
    
    /**
     * 查询用户即将发生的循环任务
     */
    // @GetMapping("/upcoming")
    // public Map<String, Object> getUpcomingByUserId(@RequestParam("deadline") LocalDateTime deadline, 
    //                                              HttpServletRequest request) {
    //     try {
    //         Long userId = tokenService.getUserIdFromRequest(request);
    //         log.info("用户查询即将发生的循环任务: userId={}, deadline={}", userId, deadline);
            
    //         List<Recurrence> recurrences = recurrenceService.getUpcomingByUserId(userId, deadline);
    //         return ResponseUtils.buildSuccessResponse(recurrences, "查询即将发生的循环任务成功");
    //     } catch (Exception e) {
    //         log.error("查询即将发生的循环任务失败: userId={}, deadline={}, error: {}", tokenService.getUserIdFromRequest(request), deadline, e.getMessage(), e);
    //         return ResponseUtils.buildErrorResponse("查询即将发生的循环任务失败: " + e.getMessage());
    //     }
    // }
}