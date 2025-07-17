#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
图片信息显示功能模块
Image Information Display Module
"""

import os
import sys
import subprocess
import tkinter as tk
from PIL import Image


class ImageInfoMixin:
    """图片信息显示功能混合类"""

    def show_image_info(self):
        """显示当前图片的详细信息"""
        if not self.image_paths or self.current_index < 0 or self.current_index >= len(self.image_paths):
            return

        current_path = self.image_paths[self.current_index]

        try:
            with Image.open(current_path) as img:
                info = {
                    "路径": current_path,
                    "文件名": os.path.basename(current_path),
                    "格式": img.format,
                    "尺寸": f"{img.width} x {img.height}",
                    "模式": img.mode,
                    "文件大小": f"{os.path.getsize(current_path)} 字节"
                }
        except Exception as e:
            info = {"错误": str(e)}

        # 创建信息对话框
        info_dialog = tk.Toplevel(self.root)
        info_dialog.title("图片详细信息")
        info_dialog.geometry("400x350")
        info_dialog.transient(self.root)
        info_dialog.grab_set()

        # 信息框架
        info_frame = tk.Frame(info_dialog)
        info_frame.pack(fill='both', expand=True, padx=10, pady=10)

        # 表格显示信息
        for i, (key, value) in enumerate(info.items()):
            category_label = tk.Label(info_frame, text=f"{key}:", anchor='w')
            category_label.grid(row=i, column=0, sticky='w', padx=5, pady=2)
            value_label = tk.Label(info_frame, text=value, anchor='w', wraplength=300)
            value_label.grid(row=i, column=1, sticky='w', padx=5, pady=2)

        # 按钮框架
        button_frame = tk.Frame(info_dialog)
        button_frame.pack(fill='x', padx=10, pady=10)

        def temp_change_button_text(button, new_text, duration=2000):
            """临时改变按钮文本"""
            original_text = button['text']
            button.config(text=new_text)
            button.after(duration, lambda: button.config(text=original_text))

        def copy_path_to_clipboard():
            """复制路径到剪贴板"""
            self.root.clipboard_clear()
            self.root.clipboard_append(current_path)
            self.root.update()
            temp_change_button_text(path_button, "路径已复制")

        path_button = tk.Button(button_frame, text="复制图片路径", command=copy_path_to_clipboard)
        path_button.pack(fill='x', padx=5, pady=5)

        def open_directory_and_copy_filename():
            """定位文件并复制文件名"""
            if sys.platform == 'win32':
                subprocess.run(['explorer', '/select,', current_path])
            elif sys.platform == 'darwin':
                subprocess.run(['open', '-R', current_path])
            else:
                subprocess.run(['xdg-open', os.path.dirname(current_path)])

            filename = os.path.basename(current_path)
            self.root.clipboard_clear()
            self.root.clipboard_append(filename)
            self.root.update()
            temp_change_button_text(dir_button, f"文件名 '{filename}' 已复制")

        dir_button = tk.Button(button_frame, text="定位并复制文件名", command=open_directory_and_copy_filename)
        dir_button.pack(fill='x', padx=5, pady=5)