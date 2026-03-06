package com.charles.server.utils;

import java.util.regex.Matcher;
import java.util.regex.Pattern;

/**
 * 颜色处理工具类，用于颜色格式转换
 */
public class ColorUtils {

    private static final Pattern HEX_SHORT_PATTERN = Pattern.compile("^#([0-9A-Fa-f]{3}|[0-9A-Fa-f]{4})$");
    private static final Pattern HEX_LONG_PATTERN = Pattern.compile("^#([0-9A-Fa-f]{6}|[0-9A-Fa-f]{8})$");
    private static final Pattern RGB_A_PATTERN = Pattern.compile("rgba?\\((\\d{1,3})\\s*,\\s*(\\d{1,3})\\s*,\\s*(\\d{1,3})(?:\\s*,\\s*([\\d.]+))?\\)", Pattern.CASE_INSENSITIVE);

    /**
     * 转换颜色字符串为十六进制格式
     * 如果是#开头的十六进制格式，则直接返回
     * 如果是rgb格式，则转换为十六进制格式
     * @param color 颜色字符串
     * @return 十六进制格式的颜色字符串
     */
    public static String normalizeColor(String color) {
        if (color == null) {
            return null;
        }
        color = color.trim();
        if (color.isEmpty()) {
            return null;
        }

        // 长十六进制示例（大小写均可）：
        //   #RRGGBB   如 #1a2b3c -> #1A2B3C
        //   #RRGGBBAA 如 #1a2b3c80 -> #1A2B3C80
        // 输出：保持长度不变，统一为大写
        if (HEX_LONG_PATTERN.matcher(color).matches()) {
            String hex = color.substring(1);
            return "#" + hex.toUpperCase();
        }

        Matcher shortHex = HEX_SHORT_PATTERN.matcher(color);
        // 短十六进制示例：
        //   #RGB  如 #f0a  -> #FF00AA
        //   #RGBA 如 #f0a8 -> #FF00AA88（每位重复一次并大写）
        if (shortHex.matches()) {
            String s = shortHex.group(1);
            StringBuilder sb = new StringBuilder("#");
            for (int i = 0; i < s.length(); i++) {
                char c = s.charAt(i);
                sb.append(Character.toUpperCase(c)).append(Character.toUpperCase(c));
            }
            return sb.toString();
        }

        // rgb/rgba 示例（大小写不敏感，逗号与空格可变）：
        //   rgb(255, 0, 128)      -> #FF0080
        //   rgba(255,0,0,0.5)     -> #FF000080（alpha 为 0–1 小数）
        //   rgba(34,12,64,128)    -> #220C4080（alpha 为 0–255 整数）
        Matcher m = RGB_A_PATTERN.matcher(color);
        if (m.matches()) {
            try {
                int r = Integer.parseInt(m.group(1));
                int g = Integer.parseInt(m.group(2));
                int b = Integer.parseInt(m.group(3));
                if (r < 0 || r > 255 || g < 0 || g > 255 || b < 0 || b > 255) {
                    return null;
                }
                String aStr = m.group(4);
                if (aStr == null) {
                    return String.format("#%02X%02X%02X", r, g, b);
                } else {
                    int alpha;
                    if (aStr.contains(".")) {
                        double ad = Double.parseDouble(aStr);
                        if (ad < 0.0 || ad > 1.0) {
                            return null;
                        }
                        alpha = (int) Math.round(ad * 255);
                    } else {
                        int ai = Integer.parseInt(aStr);
                        if (ai < 0 || ai > 255) {
                            return null;
                        }
                        alpha = ai;
                    }
                    return String.format("#%02X%02X%02X%02X", r, g, b, alpha);
                }
            } catch (NumberFormatException e) {
                return null;
            }
        }

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