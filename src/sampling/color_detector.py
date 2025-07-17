#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
背景颜色检测组件
Background Color Detection Component
"""

import threading
from collections import Counter


class ColorDetector:
    """背景颜色检测和主题切换器"""

    def __init__(self, parent):
        """
        初始化颜色检测器

        Args:
            parent: 父对象（ImageViewer实例）
        """
        self.parent = parent
        self.current_theme = "dark"  # 默认深色主题
        self.theme_colors = {
            "dark": {
                "text": "#ffffff",
                "background": "#000000",
                "outline": "#ffffff"
            },
            "light": {
                "text": "#000000",
                "background": "#ffffff",
                "outline": "#000000"
            }
        }

    def detect_and_set_theme(self):
        """
        检测当前图片背景颜色并设置合适的主题
        使用异步检测避免阻塞UI
        """
        if not self.parent.image_paths:
            return

        # 异步检测背景颜色
        threading.Thread(
            target=self._async_detect_background_color,
            daemon=True
        ).start()

    def _async_detect_background_color(self):
        """异步检测背景颜色"""
        try:
            current_path = self.parent.image_paths[self.parent.current_index]
            img_data = self.parent.image_cache.get(current_path)

            if not img_data:
                return

            img, _ = img_data

            # 采样图片边缘颜色
            edge_colors = self._sample_edge_colors(img)

            # 分析主导颜色
            dominant_color = self._analyze_dominant_color(edge_colors)

            # 判断明暗并设置主题
            new_theme = self._determine_theme_from_color(dominant_color)

            # 在主线程中更新主题
            self.parent.root.after(0, lambda: self._set_theme(new_theme))

        except Exception as e:
            print(f"背景颜色检测失败: {e}")

    def _sample_edge_colors(self, img, sample_density=5):
        """
        采样图片边缘颜色

        Args:
            img: PIL图像对象
            sample_density: 采样密度，数值越小采样点越多

        Returns:
            list: 边缘颜色列表
        """
        width, height = img.size
        edge_colors = []

        try:
            # 采样上边缘
            for x in range(0, width, sample_density):
                pixel = img.getpixel((x, 0))
                edge_colors.append(self._normalize_pixel(pixel))

            # 采样下边缘
            for x in range(0, width, sample_density):
                pixel = img.getpixel((x, height - 1))
                edge_colors.append(self._normalize_pixel(pixel))

            # 采样左边缘
            for y in range(0, height, sample_density):
                pixel = img.getpixel((0, y))
                edge_colors.append(self._normalize_pixel(pixel))

            # 采样右边缘
            for y in range(0, height, sample_density):
                pixel = img.getpixel((width - 1, y))
                edge_colors.append(self._normalize_pixel(pixel))

        except Exception as e:
            print(f"边缘采样失败: {e}")
            # 返回默认颜色（深色）
            return [(0, 0, 0)]

        return edge_colors

    def _normalize_pixel(self, pixel):
        """
        标准化像素颜色为RGB元组

        Args:
            pixel: 像素值（可能是单值、元组等）

        Returns:
            tuple: RGB颜色元组
        """
        if isinstance(pixel, (int, float)):
            # 灰度图像
            val = int(pixel)
            return (val, val, val)
        elif isinstance(pixel, (list, tuple)):
            if len(pixel) >= 3:
                # RGB或RGBA图像
                return (int(pixel[0]), int(pixel[1]), int(pixel[2]))
            elif len(pixel) == 1:
                # 单通道
                val = int(pixel[0])
                return (val, val, val)

        # 默认返回黑色
        return (0, 0, 0)

    def _analyze_dominant_color(self, edge_colors):
        """
        分析主导颜色

        Args:
            edge_colors: 边缘颜色列表

        Returns:
            tuple: 主导RGB颜色
        """
        if not edge_colors:
            return (0, 0, 0)

        # 将相似颜色归类（降低颜色分辨率以减少噪音）
        simplified_colors = []
        for r, g, b in edge_colors:
            # 将颜色量化到32级别（256/8=32）
            simplified_r = (r // 8) * 8
            simplified_g = (g // 8) * 8
            simplified_b = (b // 8) * 8
            simplified_colors.append((simplified_r, simplified_g, simplified_b))

        # 统计最常见的颜色
        color_counts = Counter(simplified_colors)
        dominant_color = color_counts.most_common(1)[0][0]

        return dominant_color

    def _determine_theme_from_color(self, rgb_color):
        """
        根据RGB颜色判断应使用的主题

        Args:
            rgb_color: RGB颜色元组

        Returns:
            str: 主题名称 ("light" 或 "dark")
        """
        r, g, b = rgb_color

        # 计算亮度（使用标准亮度公式）
        luminance = 0.299 * r + 0.587 * g + 0.114 * b

        # 亮度阈值（0-255范围内）
        threshold = 128

        if luminance > threshold:
            return "light"  # 背景较亮，使用深色文字
        else:
            return "dark"  # 背景较暗，使用浅色文字

    def _set_theme(self, new_theme):
        """
        设置新主题

        Args:
            new_theme: 新主题名称
        """
        if new_theme == self.current_theme:
            return  # 主题未变化

        old_theme = self.current_theme
        self.current_theme = new_theme

        print(f"主题切换: {old_theme} -> {new_theme}")

        # 如果悬浮窗存在，启动主题切换动画
        if hasattr(self.parent, 'overlay_manager') and self.parent.overlay_manager.overlay_exists():
            self.parent.theme_animation.animate_theme_change(
                old_theme,
                new_theme,
                self.theme_colors
            )

    def get_current_theme_colors(self):
        """
        获取当前主题的颜色配置

        Returns:
            dict: 当前主题颜色配置
        """
        return self.theme_colors[self.current_theme]

    def get_theme_color(self, element):
        """
        获取当前主题下特定元素的颜色

        Args:
            element: 元素名称 ("text", "background", "outline")

        Returns:
            str: 颜色值
        """
        return self.theme_colors[self.current_theme].get(element, "#ffffff")

    def force_theme(self, theme_name):
        """
        强制设置主题（用于测试或特殊需求）

        Args:
            theme_name: 主题名称
        """
        if theme_name in self.theme_colors:
            old_theme = self.current_theme
            self.current_theme = theme_name

            if hasattr(self.parent, 'overlay_manager') and self.parent.overlay_manager.overlay_exists():
                self.parent.theme_animation.animate_theme_change(
                    old_theme,
                    theme_name,
                    self.theme_colors
                )