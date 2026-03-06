package com.charles.server.utils;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class ColorUtilsTest {

    @Test
    void normalizeColor_acceptsLongHexRgb_uppercases() {
        assertEquals("#1A2B3C", ColorUtils.normalizeColor("#1a2b3c"));
        assertEquals("#1A2B3C80", ColorUtils.normalizeColor("#1a2b3c80"));
        assertEquals("#ABCDEF", ColorUtils.normalizeColor("#ABCDEF"));
        assertEquals("#ABCDEF01", ColorUtils.normalizeColor("#ABCDEF01"));
    }

    @Test
    void normalizeColor_expandsShortHex_andUppercases() {
        assertEquals("#FF00AA", ColorUtils.normalizeColor("#f0a"));
        assertEquals("#FF00AA88", ColorUtils.normalizeColor("#f0a8"));
        assertEquals("#AABBCC", ColorUtils.normalizeColor("#abc"));
        assertEquals("#AABBCCDD", ColorUtils.normalizeColor("#abcd"));
    }

    @Test
    void normalizeColor_parsesRgb_caseInsensitive_andSpacesFlexible() {
        assertEquals("#FF0080", ColorUtils.normalizeColor("rgb(255, 0, 128)"));
        assertEquals("#000000", ColorUtils.normalizeColor("rgb(0,0,0)"));
        assertEquals("#0C2238", ColorUtils.normalizeColor("RGB(12,34,56)"));
        assertEquals("#FFFFFF", ColorUtils.normalizeColor("rGb(255 ,255 ,255)"));
    }

    @Test
    void normalizeColor_parsesRgba_withDecimalAlpha_0to1() {
        assertEquals("#FF000080", ColorUtils.normalizeColor("rgba(255,0,0,0.5)"));
        assertEquals("#00000000", ColorUtils.normalizeColor("rgba(0,0,0,0.0)"));
        assertEquals("#000000FF", ColorUtils.normalizeColor("rgba(0,0,0,1.0)"));
        // rounding check: 0.3 * 255 ≈ 76.5 -> 77 -> 0x4D
        assertEquals("#1234564D", ColorUtils.normalizeColor("rgba(18,52,86,0.3)"));
    }

    @Test
    void normalizeColor_parsesRgba_withIntegerAlpha_0to255() {
        assertEquals("#220C4080", ColorUtils.normalizeColor("rgba(34,12,64,128)"));
        assertEquals("#220C4000", ColorUtils.normalizeColor("rgba(34,12,64,0)"));
        assertEquals("#220C40FF", ColorUtils.normalizeColor("rgba(34,12,64,255)"));
    }

    @Test
    void normalizeColor_trimsAndHandlesNullOrEmpty() {
        assertEquals("#FF00AA", ColorUtils.normalizeColor("  #f0a "));
        assertNull(ColorUtils.normalizeColor(null));
        assertNull(ColorUtils.normalizeColor(""));
        assertNull(ColorUtils.normalizeColor("   "));
    }

    @Test
    void normalizeColor_rejectsInvalidValues() {
        assertNull(ColorUtils.normalizeColor("rgb(300,0,0)"));
        assertNull(ColorUtils.normalizeColor("rgba(0,0,0,1.5)"));
        assertNull(ColorUtils.normalizeColor("#GGGGGG"));
        assertNull(ColorUtils.normalizeColor("#12"));
        assertNull(ColorUtils.normalizeColor("red"));
        assertNull(ColorUtils.normalizeColor("hsl(0,100%,50%)"));
    }

    @Test
    void getColorOrDefault_returnsDefaultWhenInvalid() {
        assertEquals("#112233", ColorUtils.getColorOrDefault("invalid", "#112233"));
        assertEquals("#AABBCC", ColorUtils.getColorOrDefault("#aabbcc", "#000000"));
        assertEquals("#FF000080", ColorUtils.getColorOrDefault("rgba(255,0,0,0.5)", "#000000"));
    }
}