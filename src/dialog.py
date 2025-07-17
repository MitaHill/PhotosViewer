#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
对话框管理功能模块
Dialog Management Functionality Module
"""

import os
import threading
import tkinter as tk
from tkinter import ttk


class DialogMixin:
    """对话框管理功能混合类"""

    def show_loading_dialog(self):
        """显示加载进度对话框"""
        self.loading_dialog = tk.Toplevel(self.root)
        self.loading_dialog.title("正在加载...")
        self.loading_dialog.transient(self.root)
        self.loading_dialog.grab_set()

        self.progress = ttk.Progressbar(self.loading_dialog, length=300, mode='determinate')
        self.progress.pack(padx=20, pady=10)

        self.loading_label = tk.Label(self.loading_dialog, text="正在加载图片，请稍候...")
        self.loading_label.pack(pady=5)

        self.current_image_label = tk.Label(self.loading_dialog, text="当前加载: 无", wraplength=300)
        self.current_image_label.pack(pady=5)

    def update_progress(self, loaded, total):
        """更新加载进度"""
        if self.loading_dialog.winfo_exists():
            self.progress['value'] = (loaded / total) * 100
            self.loading_label.config(
                text=f"已加载 {loaded}/{total} 张图片 内存：({self.format_memory(self.current_cache_size)} / {self.format_memory(self.cache_size_limit)})"
            )

    def close_loading_dialog(self):
        """关闭加载对话框"""
        if self.loading_dialog.winfo_exists():
            self.loading_dialog.grab_release()
            self.loading_dialog.destroy()

    def update_current_image_label(self, filename, size):
        """更新当前加载图片标签"""
        if self.loading_dialog.winfo_exists():
            self.current_image_label.config(
                text=f"当前加载: {filename} ({self.format_memory(size)})"
            )

    def async_load_images(self):
        """异步加载图片"""
        total = len(self.image_paths)
        loaded = 0
        priority_indices = set(range(0, 3)) | set(range(len(self.image_paths) - 3, len(self.image_paths)))

        for idx in priority_indices:
            if 0 <= idx < len(self.image_paths) and self.loading_active:
                path = self.image_paths[idx]
                file_size = os.path.getsize(path)
                self.root.after(0, self.update_current_image_label, os.path.basename(path), file_size)
                if self.load_image_to_cache(path):
                    loaded += 1
                    self.root.after(0, self.update_progress, loaded, total)

        for idx, path in enumerate(self.image_paths):
            if idx not in priority_indices and self.loading_active:
                file_size = os.path.getsize(path)
                self.root.after(0, self.update_current_image_label, os.path.basename(path), file_size)
                if self.load_image_to_cache(path):
                    loaded += 1
                    self.root.after(0, self.update_progress, loaded, total)

        self.root.after(0, self.close_loading_dialog)
        self.root.after(0, self.enable_navigation)

    def load_image_to_cache(self, path):
        """加载图片到缓存"""
        if path in self.image_cache:
            return True
        try:
            from PIL import Image
            with Image.open(path) as img:
                img = img.convert('RGB')
                width, height = img.size
                channels = 3
                bytes_per_pixel = 1
                img_size = width * height * channels * bytes_per_pixel

                if img_size > self.cache_size_limit * 0.5:
                    return False

                while self.current_cache_size + img_size > self.cache_size_limit and self.lru_list:
                    self.remove_oldest_image()

                if self.current_cache_size + img_size > self.cache_size_limit:
                    return False

                self.image_cache[path] = (img.copy(), img_size)
                self.lru_list[path] = True
                self.lru_list.move_to_end(path)
                self.current_cache_size += img_size
                return True
        except Exception as e:
            print(f"无法加载图片 {path}: {e}")
            return False