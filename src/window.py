#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
窗口管理功能模块 - 性能优化版
Window Management Functionality Module - Performance Optimized
"""

import os
import threading
import time
import tkinter as tk
import glob
import re


class WindowMixin:
    """窗口管理功能混合类"""

    def on_resize(self, event):
        """窗口大小改变事件"""
        if self.resize_timer:
            self.root.after_cancel(self.resize_timer)
        self.fast_redraw()
        self.resize_timer = self.root.after(200, self.high_quality_redraw)

    def monitor_dialogs(self):
        """后台线程：检测并居中对话框"""
        while self.running:
            try:
                self.root.update_idletasks()
                root_x = self.root.winfo_x()
                root_y = self.root.winfo_y()
                root_width = self.root.winfo_width()
                root_height = self.root.winfo_height()

                for widget in self.root.winfo_children():
                    if not isinstance(widget, tk.Toplevel) or not widget.winfo_viewable():
                        continue

                    if widget in self.excluded_dialogs:
                        continue

                    widget.update_idletasks()
                    dialog_width = widget.winfo_width()
                    dialog_height = widget.winfo_height()

                    if dialog_width <= 1 or dialog_height <= 1:
                        continue

                    dialog_x = root_x + (root_width - dialog_width) // 2
                    dialog_y = root_y + (root_height - dialog_height) // 2
                    dialog_x = max(0, dialog_x)
                    dialog_y = max(0, dialog_y)

                    current_x = widget.winfo_x()
                    current_y = widget.winfo_y()

                    last_pos = self.dialog_positions.get(widget, (current_x, current_y))
                    if (current_x, current_y) != last_pos:
                        self.excluded_dialogs.add(widget)
                        self.dialog_positions[widget] = (current_x, current_y)
                        continue

                    if current_x != dialog_x or current_y != dialog_y:
                        widget.geometry(f"+{dialog_x}+{dialog_y}")
                        self.dialog_positions[widget] = (dialog_x, dialog_y)

                active_dialogs = {w for w in self.root.winfo_children() if isinstance(w, tk.Toplevel)}
                self.excluded_dialogs &= active_dialogs
                self.dialog_positions = {k: v for k, v in self.dialog_positions.items() if k in active_dialogs}

            except Exception as e:
                print(f"对话框监控线程错误: {e}")
            time.sleep(0.05)

    def adjust_window_size(self, img):
        """
        优化版窗口大小调整 - 根据图片大小和系统性能智能调整动画参数
        """
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        min_size = 300
        max_size_factor = 0.69
        max_width = int(screen_width * max_size_factor)
        max_height = int(screen_height * max_size_factor)

        img_width, img_height = img.size

        if img_width < min_size or img_height < min_size:
            return

        if img_width > max_width or img_height > max_height:
            img_aspect = img_width / img_height
            if max_width / max_height > img_aspect:
                target_height = max_height
                target_width = int(target_height * img_aspect)
            else:
                target_width = max_width
                target_height = int(target_width / img_aspect)
        else:
            target_width = img_width
            target_height = img_height

        self.root.update_idletasks()
        current_width = self.root.winfo_width()
        current_height = self.root.winfo_height()

        # 如果尺寸变化很小，直接设置而不使用动画
        size_diff = abs(target_width - current_width) + abs(target_height - current_height)
        if size_diff < 10:
            return

        # 智能动画参数计算
        animation_params = self._calculate_animation_parameters(
            img_width, img_height, current_width, current_height,
            target_width, target_height, size_diff
        )

        steps = animation_params['steps']
        interval = animation_params['interval']
        use_easing = animation_params['use_easing']

        def animate(step=0):
            if step > steps:
                # 确保最终尺寸精确
                final_geometry = f"{target_width}x{target_height}"
                self.root.geometry(final_geometry)
                return

            # 计算进度
            progress = step / steps

            if use_easing:
                # 使用缓动函数，但简化计算
                progress = self._simple_ease_in_out(progress)

            # 计算当前尺寸
            new_width = int(current_width + (target_width - current_width) * progress)
            new_height = int(current_height + (target_height - current_height) * progress)

            # 批量更新geometry，减少系统调用
            geometry = f"{new_width}x{new_height}"
            self.root.geometry(geometry)

            # 调度下一帧
            self.root.after(interval, animate, step + 1)

        # 延迟启动动画，让当前操作完成
        self.root.after(5, animate)

    def _calculate_animation_parameters(self, img_width, img_height, current_width,
                                        current_height, target_width, target_height, size_diff):
        """
        根据图片特征和变化幅度智能计算动画参数
        """
        # 图片像素总数
        img_pixels = img_width * img_height

        # 窗口尺寸变化程度
        width_change_ratio = abs(target_width - current_width) / max(current_width, 1)
        height_change_ratio = abs(target_height - current_height) / max(current_height, 1)
        max_change_ratio = max(width_change_ratio, height_change_ratio)

        # 基于图片大小的性能分类
        if img_pixels > 8000000:  # 8MP以上 - 超大图片
            base_steps = 8
            base_interval = 35
            use_easing = False
        elif img_pixels > 4000000:  # 4-8MP - 大图片
            base_steps = 12
            base_interval = 25
            use_easing = False
        elif img_pixels > 1000000:  # 1-4MP - 中等图片
            base_steps = 18
            base_interval = 20
            use_easing = True
        else:  # 小于1MP - 小图片
            base_steps = 25
            base_interval = 16
            use_easing = True

        # 根据尺寸变化调整参数
        if max_change_ratio > 0.5:  # 大幅变化
            steps = max(6, int(base_steps * 0.7))  # 减少步数
            interval = base_interval + 5  # 增加间隔
        elif max_change_ratio > 0.2:  # 中等变化
            steps = base_steps
            interval = base_interval
        else:  # 小幅变化
            steps = min(base_steps + 5, 30)  # 增加步数但有上限
            interval = max(12, base_interval - 3)  # 减少间隔但有下限

        # 如果变化非常小，进一步优化
        if size_diff < 50:
            steps = min(10, steps)
            interval = max(interval, 20)

        return {
            'steps': steps,
            'interval': interval,
            'use_easing': use_easing
        }

    def _simple_ease_in_out(self, t):
        """
        简化的缓动函数，减少计算开销
        """
        if t < 0.5:
            return 2 * t * t
        else:
            return 1 - 2 * (1 - t) * (1 - t)

    def _should_skip_animation(self, img_width, img_height, size_diff):
        """
        判断是否应该跳过动画（直接设置尺寸）
        """
        # 超大图片且尺寸变化很大时跳过动画
        if img_width * img_height > 16000000 and size_diff > 200:
            return True

        # 系统性能检测（简化版）
        try:
            import psutil
            cpu_percent = psutil.cpu_percent(interval=0.1)
            if cpu_percent > 80:  # CPU使用率过高
                return True
        except:
            pass

        return False

    def load_directory_images(self, directory):
        """加载目录中的图片"""
        self.last_directory = directory
        self.loading_active = False
        self.release_all_images()
        self.image_paths = []

        extensions = ['jpg', 'jpeg', 'png', 'bmp', 'gif', 'webp', 'tiff']
        pattern = os.path.join(directory, '*')

        for file_path in glob.glob(pattern, recursive=False):
            ext = os.path.splitext(file_path)[1][1:].lower()
            if ext in extensions:
                self.image_paths.append(os.path.normpath(file_path))

        self.image_paths.sort(key=self.natural_sort_key)

        size_threshold = 3 * 1024 * 1024
        large_image_found = False

        for file_path in self.image_paths:
            try:
                file_size = os.path.getsize(file_path)
                if file_size > size_threshold:
                    large_image_found = True
                    break
            except OSError:
                continue

        if len(self.image_paths) > 30 or large_image_found:
            self.show_loading_dialog()
            self.loading_active = True
            threading.Thread(target=self.async_load_images, daemon=True).start()
        else:
            self.sync_load_images()

    @staticmethod
    def natural_sort_key(s):
        """自然排序键"""
        return [int(text) if text.isdigit() else text.lower() for text in re.split(r'(\d+)', s)]

    def sync_load_images(self):
        """同步加载图片"""
        indices = {self.current_index, self.current_index - 1, self.current_index + 1}
        for idx in indices:
            if 0 <= idx < len(self.image_paths):
                self.load_image_to_cache(self.image_paths[idx])
        self.enable_navigation()

    def show_current_image(self):
        """显示当前图片 - 优化版本，在窗口调整前先检查是否需要动画"""
        if not self.image_paths or self.current_index >= len(self.image_paths):
            return

        current_path = self.image_paths[self.current_index]

        preload_indices = {self.current_index - 1, self.current_index + 1}
        for idx in preload_indices:
            if 0 <= idx < len(self.image_paths):
                threading.Thread(target=self.load_image_to_cache,
                                 args=(self.image_paths[idx],),
                                 daemon=True).start()

        if current_path not in self.image_cache:
            self.load_image_to_cache(current_path)

        self.root.title(f"图片查看器 - {os.path.basename(current_path)}")
        self.update_lru(current_path)

        img_data = self.image_cache.get(current_path)
        if not img_data:
            return
        img, _ = img_data

        window_width = self.canvas.winfo_width()
        window_height = self.canvas.winfo_height()

        # 重置缩放
        self.zoom_factor = 1.0

        # 计算铺满屏幕的缩放比例
        img_aspect = img.width / img.height
        window_aspect = window_width / window_height

        if window_aspect > img_aspect:
            # 按高度铺满
            scale = window_height / img.height
        else:
            # 按宽度铺满
            scale = window_width / img.width

        # 设置视口以铺满整个窗口
        self.viewport_width = window_width / scale
        self.viewport_height = window_height / scale

        # 居中视口
        self.viewport_x = max(0, (img.width - self.viewport_width) / 2)
        self.viewport_y = max(0, (img.height - self.viewport_height) / 2)

        # 确保视口不超出图片边界
        self.viewport_x = max(0, min(self.viewport_x, img.width - self.viewport_width))
        self.viewport_y = max(0, min(self.viewport_y, img.height - self.viewport_height))

        # 确保视口尺寸不超过图片尺寸
        self.viewport_width = min(self.viewport_width, img.width)
        self.viewport_height = min(self.viewport_height, img.height)

        # 检查是否需要跳过窗口调整动画
        current_width = self.root.winfo_width()
        current_height = self.root.winfo_height()
        size_diff = abs(img.width - current_width) + abs(img.height - current_height)

        if self._should_skip_animation(img.width, img.height, size_diff):
            # 直接设置窗口大小，不使用动画
            screen_width = self.root.winfo_screenwidth()
            screen_height = self.root.winfo_screenheight()
            max_width = int(screen_width * 0.69)
            max_height = int(screen_height * 0.69)

            target_width = min(img.width, max_width)
            target_height = min(img.height, max_height)

            self.root.geometry(f"{target_width}x{target_height}")
        else:
            # 使用优化的动画
            self.adjust_window_size(img)

        self.fast_redraw()
        self.analyze_edge_colors()

    def update_lru(self, path):
        """更新LRU缓存"""
        if path in self.lru_list:
            self.lru_list.move_to_end(path)