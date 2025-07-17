#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
图片重命名功能模块
Photo Renaming Functionality Module
"""

import os
import tkinter as tk
from tkinter import messagebox


class RenamePhotoMixin:
    """图片重命名功能混合类"""

    def rename_current_image(self, event=None):
        """重命名当前图片文件"""
        if not self.image_paths or self.current_index < 0 or self.current_index >= len(self.image_paths):
            return

        current_path = self.image_paths[self.current_index]
        old_name = os.path.basename(current_path)

        # 创建重命名对话框
        dialog = tk.Toplevel(self.root)
        dialog.title("重命名图片")
        dialog.transient(self.root)
        dialog.grab_set()

        tk.Label(dialog, text="请输入新文件名:").pack(pady=5)
        name_entry = tk.Entry(dialog, width=40)
        name_entry.insert(0, old_name)
        name_entry.pack(pady=5)
        name_entry.focus_set()

        def on_submit():
            """处理用户提交的新文件名"""
            new_name = name_entry.get().strip()

            if not new_name:
                messagebox.showerror("错误", "文件名不能为空")
                return

            if new_name == old_name:
                dialog.destroy()
                return

            new_path = os.path.join(os.path.dirname(current_path), new_name)

            try:
                if os.path.exists(new_path):
                    messagebox.showerror("错误", "目标文件名已存在")
                    return

                # 重命名文件
                os.rename(current_path, new_path)

                # 更新缓存中的引用
                if current_path in self.image_cache:
                    img_data = self.image_cache.pop(current_path)
                    self.image_cache[new_path] = img_data

                    del self.lru_list[current_path]
                    self.lru_list[new_path] = True
                    self.lru_list.move_to_end(new_path)

                # 更新图片路径列表和窗口标题
                self.image_paths[self.current_index] = new_path
                print(f"已重命名: {current_path} -> {new_path}")
                self.root.title(f"图片查看器 - {os.path.basename(new_path)}")

                dialog.destroy()

            except Exception as e:
                messagebox.showerror("错误", f"重命名失败: {str(e)}")

        tk.Button(dialog, text="确认", command=on_submit).pack(pady=5)
        dialog.bind('<Return>', lambda e: on_submit())