#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
缓存配置功能模块 - 集成配置保存
Cache Configuration Functionality Module - With Config Persistence
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
        dialog.geometry("400x250")
        dialog.transient(self.root)
        dialog.grab_set()
        dialog.resizable(False, False)

        # 当前状态显示
        current_ratio = getattr(self, 'cache_ratio', 0.4)
        virtual_memory = psutil.virtual_memory()
        current_limit = int(virtual_memory.available * current_ratio)

        info_frame = tk.Frame(dialog)
        info_frame.pack(pady=10, padx=20, fill=tk.X)

        tk.Label(info_frame, text="当前设置:", font=('Arial', 10, 'bold')).pack(anchor=tk.W)
        tk.Label(info_frame, text=f"缓存比例: {current_ratio:.2f}").pack(anchor=tk.W)
        tk.Label(info_frame, text=f"缓存限制: {self.format_memory(current_limit)}").pack(anchor=tk.W)
        tk.Label(info_frame, text=f"可用内存: {self.format_memory(virtual_memory.available)}").pack(anchor=tk.W)

        # 输入框架
        input_frame = tk.Frame(dialog)
        input_frame.pack(pady=15, padx=20)

        tk.Label(input_frame, text="请输入缓存占空闲内存的比例（0.1-1.0）:").pack(anchor=tk.W)
        ratio_entry = tk.Entry(input_frame, width=15)
        ratio_entry.insert(0, str(current_ratio))
        ratio_entry.pack(pady=5, anchor=tk.W)
        ratio_entry.focus_set()

        # 预览框架
        preview_frame = tk.Frame(dialog)
        preview_frame.pack(pady=10, padx=20, fill=tk.X)

        preview_label = tk.Label(preview_frame, text="", fg="blue")
        preview_label.pack(anchor=tk.W)

        def update_preview():
            """更新预览信息"""
            try:
                ratio = float(ratio_entry.get())
                if 0.1 <= ratio <= 1.0:
                    new_limit = int(virtual_memory.available * ratio)
                    preview_label.config(
                        text=f"预览: 缓存限制将设为 {self.format_memory(new_limit)}",
                        fg="green"
                    )
                else:
                    preview_label.config(text="比例必须在0.1到1.0之间", fg="red")
            except ValueError:
                preview_label.config(text="请输入有效数字", fg="red")

        ratio_entry.bind('<KeyRelease>', lambda e: update_preview())
        update_preview()  # 初始预览

        def on_submit():
            try:
                ratio = float(ratio_entry.get())
                if not 0.1 <= ratio <= 1.0:
                    raise ValueError("比例必须在0.1到1.0之间")

                # 更新缓存配置
                self.cache_ratio = ratio
                virtual_memory = psutil.virtual_memory()
                self.cache_size_limit = int(virtual_memory.available * self.cache_ratio)

                # 保存到配置文件
                if hasattr(self, 'config_manager'):
                    self.config_manager.set_cache_ratio(ratio)
                    print(f"缓存配置已保存到: {self.config_manager.config_file}")

                print(f"缓存比例设置为: {self.cache_ratio:.2f}, 缓存限制: {self.format_memory(self.cache_size_limit)}")

                # 清空并重新加载缓存以应用新限制
                self.release_all_images()
                if self.image_paths and self.last_directory:
                    self.load_directory_images(self.last_directory)
                    self.show_current_image()

                dialog.destroy()

            except ValueError as e:
                tk.messagebox.showerror("错误", str(e))

        # 按钮框架
        button_frame = tk.Frame(dialog)
        button_frame.pack(pady=15)

        tk.Button(button_frame, text="确认", command=on_submit).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="取消", command=dialog.destroy).pack(side=tk.LEFT, padx=5)

        # 重置按钮
        def reset_to_default():
            ratio_entry.delete(0, tk.END)
            ratio_entry.insert(0, "0.4")
            update_preview()

        tk.Button(button_frame, text="重置默认(0.4)", command=reset_to_default).pack(side=tk.LEFT, padx=5)

        dialog.bind('<Return>', lambda e: on_submit())