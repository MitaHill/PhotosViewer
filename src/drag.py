#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
拖拽功能模块
Drag and Drop Functionality Module
"""

import os
from tkinter import messagebox


class DragMixin:
    """拖拽功能混合类"""

    def on_drag_start(self, event):
        """开始拖拽"""
        if not self.image_paths or self.is_playing:
            return
        self.dragging = True
        self.drag_start_x = event.x
        self.drag_start_y = event.y

    def on_drag(self, event):
        """拖拽过程"""
        if not self.dragging:
            return

        dx = event.x - self.drag_start_x
        dy = event.y - self.drag_start_y
        img_dx, img_dy = self.canvas_delta_to_image(dx, dy)

        current_path = self.image_paths[self.current_index]
        img_data = self.image_cache.get(current_path)
        if img_data:
            img, _ = img_data
            self.viewport_x = max(0, min(self.viewport_x - img_dx, img.width - self.viewport_width))
            self.viewport_y = max(0, min(self.viewport_y - img_dy, img.height - self.viewport_height))

        self.fast_redraw()
        self.drag_start_x = event.x
        self.drag_start_y = event.y

    def on_drag_end(self, event):
        """结束拖拽"""
        self.dragging = False

    def canvas_delta_to_image(self, dx, dy):
        """画布坐标变化转换为图像坐标变化"""
        window_width = self.canvas.winfo_width()
        window_height = self.canvas.winfo_height()
        if window_width < 10 or window_height < 10:
            return 0, 0
        scale = min(window_width / self.viewport_width, window_height / self.viewport_height)
        return dx / scale, dy / scale

    def handle_drop(self, event):
        """处理文件拖放事件"""
        dropped_data = event.data
        if not dropped_data:
            return

        dropped_items = self._parse_dropped_data(dropped_data)
        supported_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.gif', '.webp', '.tiff'}

        image_files = []
        directories = []

        for item in dropped_items:
            if os.path.isdir(item):
                directories.append(item)
            elif os.path.isfile(item) and os.path.splitext(item)[1].lower() in supported_extensions:
                image_files.append(item)

        if image_files and not directories:
            self._handle_image_files(image_files)
        elif len(directories) == 1 and not image_files:
            has_images = self._directory_contains_images(directories[0], supported_extensions)
            if has_images:
                self._handle_single_directory(directories[0])
            else:
                messagebox.showerror("错误", "所选目录不包含支持的图片文件。")
        elif len(directories) > 1:
            messagebox.showerror("错误", "无法处理多个目录。请一次只拖放一个目录。")
        else:
            print("未检测到有效的图片文件或目录")

    def _parse_dropped_data(self, dropped_data):
        """解析拖放数据"""
        if dropped_data.startswith('{') and dropped_data.endswith('}'):
            items = dropped_data[1:-1].split('} {')
        else:
            items = dropped_data.split()
        return [os.path.normpath(item) for item in items]

    def _handle_image_files(self, image_files):
        """处理拖放的图片文件"""
        if len(image_files) == 1:
            image_path = image_files[0]
            directory = os.path.dirname(image_path)
            self._load_images_from_directory(directory)
            self._display_selected_image(image_path)
            print(f"已加载单个图片：{os.path.basename(image_path)}")
        else:
            directories = {os.path.dirname(img) for img in image_files}
            if len(directories) > 1:
                messagebox.showerror("错误", "无法处理来自多个目录的图片。请确保所有图片来自同一目录。")
                return

            directory = directories.pop()
            self._load_images_from_directory(directory)
            self._display_selected_image(image_files[0])
            print(f"已加载多个图片（{len(image_files)}），跳转到：{os.path.basename(image_files[0])}")

    def _handle_single_directory(self, directory):
        """处理拖放的单个目录"""
        self._load_images_from_directory(directory)
        if not self.image_paths:
            messagebox.showerror("错误", "所选目录不包含支持的图片文件。")
            return

        self.current_index = 0
        self.show_current_image()
        self.is_playing = True
        self.start_playback()
        print(f"已加载目录：{directory}，从第一张图片开始播放")

    def _load_images_from_directory(self, directory):
        """从目录加载图片"""
        if directory != self.last_directory or not self.image_paths:
            self.last_directory = directory
            self.load_directory_images(directory)

    def _display_selected_image(self, image_path):
        """显示选择的图片"""
        if not self.image_paths:
            return

        try:
            self.current_index = self.image_paths.index(image_path)
        except ValueError:
            self.current_index = 0
        self.show_current_image()

    def _directory_contains_images(self, directory, supported_extensions):
        """检查目录是否包含图片文件"""
        for root, _, files in os.walk(directory):
            for file in files:
                if os.path.splitext(file)[1].lower() in supported_extensions:
                    return True
        return False