#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
边框颜色变更功能模块
Border Color Change Functionality Module
"""

import threading
from collections import Counter


class BorderColorMixin:
    """边框颜色变更功能混合类"""

    def analyze_edge_colors(self):
        """分析图片边缘颜色占比并以动画形式调整背景颜色"""
        if not self.image_paths:
            return
        current_path = self.image_paths[self.current_index]
        img_data = self.image_cache.get(current_path)
        if not img_data:
            return
        img, _ = img_data

        def compute_dominant_color():
            # 提取边缘像素
            width, height = img.size
            edge_pixels = []
            for x in range(width):  # 上边缘
                edge_pixels.append(img.getpixel((x, 0)))
            for x in range(width):  # 下边缘
                edge_pixels.append(img.getpixel((x, height - 1)))
            for y in range(height):  # 左边缘
                edge_pixels.append(img.getpixel((0, y)))
            for y in range(height):  # 右边缘
                edge_pixels.append(img.getpixel((width - 1, y)))

            # 计算主导颜色
            color_counts = Counter(edge_pixels)
            dominant_color = color_counts.most_common(1)[0][0]
            target_hex = f"#{dominant_color[0]:02x}{dominant_color[1]:02x}{dominant_color[2]:02x}"

            # 获取当前背景颜色
            current_hex = self.canvas['bg']
            try:
                current_rgb = tuple(int(current_hex.lstrip('#')[i:i + 2], 16) for i in (0, 2, 4))
            except ValueError:
                current_rgb = (51, 51, 51)  # 默认 #333333

            # 动画参数
            steps = 20
            duration = 500
            step_time = duration // steps

            def interpolate_color(start_rgb, end_rgb, progress):
                """计算两颜色之间的插值"""
                r = int(start_rgb[0] + (end_rgb[0] - start_rgb[0]) * progress)
                g = int(start_rgb[1] + (end_rgb[1] - start_rgb[1]) * progress)
                b = int(start_rgb[2] + (end_rgb[2] - start_rgb[2]) * progress)
                return f"#{r:02x}{g:02x}{b:02x}"

            def animate_transition(step=0):
                if step > steps:
                    self.canvas.config(bg=target_hex)
                    return
                progress = step / steps
                eased_progress = self.ease_in_out(step, steps)
                new_color = interpolate_color(current_rgb, dominant_color, eased_progress)
                self.canvas.config(bg=new_color)
                self.root.after(step_time, animate_transition, step + 1)

            self.root.after(0, animate_transition)

        threading.Thread(target=compute_dominant_color, daemon=True).start()