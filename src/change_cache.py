#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
缓存配置功能模块
Cache Configuration Functionality Module
"""

import tkinter as tk
import psutil


class ChangeCacheMixin:
    """缓存配置功能混合类"""

    def adjust_cache_ratio(self):
        """调整缓存占空闲内存配比"""
        print("此工具使用内存作为缓存空间，以增加连续切换图片时的运行效率。")

        dialog = tk.Toplevel(self.root)
        dialog.title("调整缓存占空闲内存配比")
        dialog.transient(self.root)
        dialog.grab_set()

        tk.Label(dialog, text="请输入缓存占空闲内存的比例（0.1-1.0）:").pack(pady=5)
        ratio_entry = tk.Entry(dialog)
        ratio_entry.insert(0, str(getattr(self, 'cache_ratio', 0.4)))
        ratio_entry.pack(pady=5)
        ratio_entry.focus_set()

        def on_submit():
            try:
                ratio = float(ratio_entry.get())
                if not 0.1 <= ratio <= 1.0:
                    raise ValueError("比例必须在0.1到1.0之间")

                self.cache_ratio = ratio

                # 更新缓存限制
                virtual_memory = psutil.virtual_memory()
                self.cache_size_limit = int(virtual_memory.available * self.cache_ratio)

                print(
                    f"缓存比例设置为: {self.cache_ratio:.2f}x，缓存限制更新为: {self.format_memory(self.cache_size_limit)}")

                # 清空并重新加载缓存以应用新限制
                self.release_all_images()
                if self.image_paths and self.last_directory:
                    self.load_directory_images(self.last_directory)
                    self.show_current_image()

                dialog.destroy()

            except ValueError as e:
                print("比例必须在0.1到1.0之间")

        tk.Button(dialog, text="确认", command=on_submit).pack(pady=5)
        dialog.bind('<Return>', lambda e: on_submit())