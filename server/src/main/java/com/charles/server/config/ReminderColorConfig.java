package com.charles.server.config;

import com.charles.server.utils.ColorUtils;
import jakarta.annotation.PostConstruct;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;

@Component
public class ReminderColorConfig {

    @Value("${reminder.color.default:#409EFF}")
    private String defaultColor;

    @PostConstruct
    void init() {
        ColorUtils.setDefaultColor(defaultColor);
    }
}