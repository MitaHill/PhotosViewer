#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
像素颜色采样组件
Pixel Color Sampling Component
"""

import colorsys
from collections import namedtuple

# 颜色信息数据结构
ColorInfo = namedtuple('ColorInfo', ['rgb', 'hex', 'hsv', 'hsl', 'cmyk', 'name'])


class PixelSampler:
    """像素颜色采样器"""

    def __init__(self, parent):
        """
        初始化像素采样器

        Args:
            parent: 父对象（ImageViewer实例）
        """
        self.parent = parent

        # 颜色名称映射（基础颜色）
        self.color_names = {
            (0, 0, 0): "黑色",
            (255, 255, 255): "白色",
            (255, 0, 0): "红色",
            (0, 255, 0): "绿色",
            (0, 0, 255): "蓝色",
            (255, 255, 0): "黄色",
            (255, 0, 255): "洋红",
            (0, 255, 255): "青色",
            (128, 128, 128): "灰色",
            (192, 192, 192): "浅灰",
            (128, 0, 0): "深红",
            (0, 128, 0): "深绿",
            (0, 0, 128): "深蓝",
            (128, 128, 0): "橄榄色",
            (128, 0, 128): "紫色",
            (0, 128, 128): "青绿色",
            (255, 165, 0): "橙色",
            (255, 192, 203): "粉色",
            (165, 42, 42): "棕色",
            (255, 215, 0): "金色"
        }

        # 采样历史记录
        self.sample_history = []
        self.max_history = 50

        # 性能优化设置
        self.enable_extended_info = True
        self.enable_color_name_detection = True

    def get_pixel_color(self, img_x, img_y):
        """
        获取指定像素的RGB颜色

        Args:
            img_x: 图像X坐标
            img_y: 图像Y坐标

        Returns:
            tuple: RGB颜色元组 (r, g, b) 或 None
        """
        if not self.parent.image_paths:
            return None

        current_path = self.parent.image_paths[self.parent.current_index]
        img_data = self.parent.image_cache.get(current_path)
        if not img_data:
            return None

        img, _ = img_data

        try:
            # 确保坐标为整数且在范围内
            x = int(max(0, min(img_x, img.width - 1)))
            y = int(max(0, min(img_y, img.height - 1)))

            # 获取像素颜色
            pixel = img.getpixel((x, y))

            # 处理不同的图像模式
            rgb = self._normalize_pixel_to_rgb(pixel, img.mode)

            # 添加到历史记录
            if rgb:
                self._add_to_history(rgb, x, y)

            return rgb

        except Exception as e:
            print(f"获取像素颜色失败: {e}")
            return None

    def get_extended_color_info(self, img_x, img_y):
        """
        获取扩展的颜色信息

        Args:
            img_x: 图像X坐标
            img_y: 图像Y坐标

        Returns:
            ColorInfo: 详细颜色信息或None
        """
        if not self.enable_extended_info:
            rgb = self.get_pixel_color(img_x, img_y)
            return ColorInfo(rgb, None, None, None, None, None) if rgb else None

        rgb = self.get_pixel_color(img_x, img_y)
        if not rgb:
            return None

        r, g, b = rgb

        # 计算HEX值
        hex_color = f"#{r:02x}{g:02x}{b:02x}"

        # 计算HSV值
        hsv = self._rgb_to_hsv(r, g, b)

        # 计算HSL值
        hsl = self._rgb_to_hsl(r, g, b)

        # 计算CMYK值
        cmyk = self._rgb_to_cmyk(r, g, b)

        # 获取颜色名称
        color_name = self._get_color_name(r, g, b) if self.enable_color_name_detection else None

        return ColorInfo(rgb, hex_color, hsv, hsl, cmyk, color_name)

    def get_area_average_color(self, center_x, center_y, radius=3):
        """
        获取指定区域的平均颜色

        Args:
            center_x: 中心X坐标
            center_y: 中心Y坐标
            radius: 采样半径

        Returns:
            tuple: 平均RGB颜色 (r, g, b) 或 None
        """
        if not self.parent.image_paths:
            return None

        current_path = self.parent.image_paths[self.parent.current_index]
        img_data = self.parent.image_cache.get(current_path)
        if not img_data:
            return None

        img, _ = img_data

        try:
            total_r = total_g = total_b = 0
            sample_count = 0

            # 采样区域内的像素
            for dx in range(-radius, radius + 1):
                for dy in range(-radius, radius + 1):
                    x = int(center_x + dx)
                    y = int(center_y + dy)

                    # 检查坐标是否在图像范围内
                    if 0 <= x < img.width and 0 <= y < img.height:
                        pixel = img.getpixel((x, y))
                        rgb = self._normalize_pixel_to_rgb(pixel, img.mode)

                        if rgb:
                            total_r += rgb[0]
                            total_g += rgb[1]
                            total_b += rgb[2]
                            sample_count += 1

            if sample_count > 0:
                avg_r = int(total_r / sample_count)
                avg_g = int(total_g / sample_count)
                avg_b = int(total_b / sample_count)
                return (avg_r, avg_g, avg_b)

        except Exception as e:
            print(f"获取区域平均颜色失败: {e}")

        return None

    def _normalize_pixel_to_rgb(self, pixel, mode):
        """
        将像素值标准化为RGB元组

        Args:
            pixel: 像素值
            mode: 图像模式

        Returns:
            tuple: RGB颜色元组
        """
        try:
            if mode in ('RGB', 'RGBA'):
                if isinstance(pixel, (list, tuple)) and len(pixel) >= 3:
                    return (int(pixel[0]), int(pixel[1]), int(pixel[2]))
            elif mode in ('L', 'LA'):
                # 灰度图像
                if isinstance(pixel, (int, float)):
                    val = int(pixel)
                    return (val, val, val)
                elif isinstance(pixel, (list, tuple)) and len(pixel) >= 1:
                    val = int(pixel[0])
                    return (val, val, val)
            elif mode == 'CMYK':
                if isinstance(pixel, (list, tuple)) and len(pixel) >= 4:
                    # CMYK转RGB（简化版本）
                    c, m, y, k = pixel
                    r = int(255 * (1 - c / 100) * (1 - k / 100))
                    g = int(255 * (1 - m / 100) * (1 - k / 100))
                    b = int(255 * (1 - y / 100) * (1 - k / 100))
                    return (r, g, b)
            elif mode == 'HSV':
                if isinstance(pixel, (list, tuple)) and len(pixel) >= 3:
                    h, s, v = pixel
                    r, g, b = colorsys.hsv_to_rgb(h / 360, s / 100, v / 100)
                    return (int(r * 255), int(g * 255), int(b * 255))
            elif mode == 'P':
                # 调色板模式，需要获取调色板
                if isinstance(pixel, int):
                    # 简化处理，返回灰度值
                    return (pixel, pixel, pixel)

            # 默认处理
            if isinstance(pixel, (int, float)):
                val = int(pixel)
                return (val, val, val)
            elif isinstance(pixel, (list, tuple)) and len(pixel) >= 3:
                return (int(pixel[0]), int(pixel[1]), int(pixel[2]))

        except Exception as e:
            print(f"像素标准化失败: {e}")

        return None

    def _rgb_to_hsv(self, r, g, b):
        """RGB转HSV"""
        h, s, v = colorsys.rgb_to_hsv(r / 255.0, g / 255.0, b / 255.0)
        return (int(h * 360), int(s * 100), int(v * 100))

    def _rgb_to_hsl(self, r, g, b):
        """RGB转HSL"""
        h, l, s = colorsys.rgb_to_hls(r / 255.0, g / 255.0, b / 255.0)
        return (int(h * 360), int(s * 100), int(l * 100))

    def _rgb_to_cmyk(self, r, g, b):
        """RGB转CMYK"""
        if r == 0 and g == 0 and b == 0:
            return (0, 0, 0, 100)

        c = 1 - r / 255.0
        m = 1 - g / 255.0
        y = 1 - b / 255.0
        k = min(c, m, y)

        if k < 1:
            c = int((c - k) / (1 - k) * 100)
            m = int((m - k) / (1 - k) * 100)
            y = int((y - k) / (1 - k) * 100)
        else:
            c = m = y = 0

        k = int(k * 100)
        return (c, m, y, k)

    def _get_color_name(self, r, g, b):
        """
        获取颜色名称（近似匹配）

        Args:
            r, g, b: RGB值

        Returns:
            str: 颜色名称或None
        """
        min_distance = float('inf')
        closest_name = None

        for (cr, cg, cb), name in self.color_names.items():
            # 计算欧几里得距离
            distance = ((r - cr) ** 2 + (g - cg) ** 2 + (b - cb) ** 2) ** 0.5
            if distance < min_distance:
                min_distance = distance
                closest_name = name

        # 只有距离足够小才返回名称
        if min_distance < 50:  # 阈值可调整
            return closest_name

        return None

    def _add_to_history(self, rgb, x, y):
        """
        添加颜色到历史记录

        Args:
            rgb: RGB颜色
            x, y: 坐标
        """
        timestamp = self.parent.root.tk.call('clock', 'milliseconds')

        history_item = {
            'rgb': rgb,
            'position': (x, y),
            'timestamp': timestamp
        }

        self.sample_history.append(history_item)

        # 维护历史记录大小
        if len(self.sample_history) > self.max_history:
            self.sample_history.pop(0)

    def get_sample_history(self, count=10):
        """
        获取采样历史记录

        Args:
            count: 返回的记录数量

        Returns:
            list: 历史记录列表
        """
        return self.sample_history[-count:] if self.sample_history else []

    def clear_history(self):
        """清空采样历史"""
        self.sample_history.clear()

    def set_performance_mode(self, extended_info=True, color_names=True):
        """
        设置性能模式

        Args:
            extended_info: 是否启用扩展颜色信息
            color_names: 是否启用颜色名称检测
        """
        self.enable_extended_info = extended_info
        self.enable_color_name_detection = color_names

    def get_dominant_colors(self, sample_count=100):
        """
        获取当前图像的主导颜色

        Args:
            sample_count: 采样点数量

        Returns:
            list: 主导颜色列表 [(rgb, percentage), ...]
        """
        if not self.parent.image_paths:
            return []

        current_path = self.parent.image_paths[self.parent.current_index]
        img_data = self.parent.image_cache.get(current_path)
        if not img_data:
            return []

        img, _ = img_data

        try:
            # 随机采样
            import random
            colors = []

            for _ in range(sample_count):
                x = random.randint(0, img.width - 1)
                y = random.randint(0, img.height - 1)
                rgb = self.get_pixel_color(x, y)
                if rgb:
                    colors.append(rgb)

            # 统计颜色出现频率
            from collections import Counter
            color_counts = Counter(colors)
            total_samples = len(colors)

            # 返回前5个主导颜色
            dominant = []
            for color, count in color_counts.most_common(5):
                percentage = (count / total_samples) * 100
                dominant.append((color, percentage))

            return dominant

        except Exception as e:
            print(f"获取主导颜色失败: {e}")
            return []