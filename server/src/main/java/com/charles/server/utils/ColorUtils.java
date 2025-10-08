package com.charles.server.utils;

import java.util.regex.Matcher;
import java.util.regex.Pattern;

/**
 * 颜色处理工具类，用于颜色格式转换
 */
public class ColorUtils {

    // RGB格式的正则表达式
    private static final Pattern RGB_PATTERN = Pattern.compile("rgb\\((\\d{1,3}),\\s*(\\d{1,3}),\\s*(\\d{1,3})\\)");

    /**
     * 转换颜色字符串为十六进制格式
     * 如果是#开头的十六进制格式，则直接返回
     * 如果是rgb格式，则转换为十六进制格式
     * @param color 颜色字符串
     * @return 十六进制格式的颜色字符串
     */
    public static String normalizeColor(String color) {
        if (color == null || color.trim().isEmpty()) {
            return null;
        }

        // 去除前后空格
        color = color.trim();

        // 如果已经是以#开头的十六进制格式，则直接返回
        if (color.startsWith("#") && (color.length() == 7 || color.length() == 9)) {
            return color;
        }

        // 如果是RGB格式，则转换为十六进制
        Matcher matcher = RGB_PATTERN.matcher(color);
        if (matcher.matches()) {
            try {
                int r = Integer.parseInt(matcher.group(1));
                int g = Integer.parseInt(matcher.group(2));
                int b = Integer.parseInt(matcher.group(3));

                // 验证RGB值的范围是否有效 (0-255)
                if (r >= 0 && r <= 255 && g >= 0 && g <= 255 && b >= 0 && b <= 255) {
                    return String.format("#%02X%02X%02X", r, g, b);
                }
            } catch (NumberFormatException e) {
                // 数字格式错误，返回null
            }
        }

        // 无法识别的颜色格式，返回null
        return null;
    }

    /**
     * 安全地获取颜色值，提供默认值
     * @param color 原始颜色值
     * @param defaultValue 默认颜色值
     * @return 标准化后的颜色值或默认值
     */
    public static String getColorOrDefault(String color, String defaultValue) {
        String normalizedColor = normalizeColor(color);
        return normalizedColor != null ? normalizedColor : defaultValue;
    }
}