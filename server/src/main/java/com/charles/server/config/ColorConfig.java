package com.charles.server.config;

import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.stereotype.Component;
import org.springframework.beans.factory.annotation.Value;
import com.charles.server.utils.ColorUtils;

@Component
@ConfigurationProperties(prefix = "color")
public class ColorConfig {

    @Value("${color.project}")
    private String projectColor;

    @Value("${color.tag}")
    private String tagColor;

    public String getProjectColor(String color) {
        return ColorUtils.getColorWithDefault(color, projectColor);
    }
    public String getTagColor(String color) {
        return ColorUtils.getColorWithDefault(color, tagColor);
    }
}