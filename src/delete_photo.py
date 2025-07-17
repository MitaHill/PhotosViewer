#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
图片删除功能模块
Photo Deletion Functionality Module
"""

import os
from tkinter import messagebox


class DeletePhotoMixin:
    """图片删除功能混合类"""

    def delete_current_image(self):
        """
        删除当前显示的图片文件
        包含双重确认机制，防止误操作
        同时会更新缓存和图片列表
        """
        # 验证当前有有效的图片
        if not self.image_paths or self.current_index < 0 or self.current_index >= len(self.image_paths):
            return

        current_path = self.image_paths[self.current_index]
        file_name = os.path.basename(current_path)

        # 第一次确认对话框
        if not messagebox.askyesno("删除确认", f"确定要删除 '{file_name}' 吗？"):
            return

        # 第二次确认对话框，强调操作不可撤销
        if not messagebox.askyesno("再次确认", "此操作不可撤销，确认删除吗？"):
            return

        try:
            # 从内存缓存中移除图片
            if current_path in self.image_cache:
                img, size = self.image_cache.pop(current_path)
                img.close()  # 释放图片资源
                del self.lru_list[current_path]  # 从LRU列表中移除
                self.current_cache_size -= size  # 更新当前缓存大小

            # 从文件系统中删除文件
            os.remove(current_path)
            print(f"已删除: {current_path}")

            # 更新图片路径列表
            del self.image_paths[self.current_index]

            # 如果删除后没有图片了，清空画布并更新标题
            if not self.image_paths:
                self.canvas.delete("all")
                self.root.title("图片查看器 - 无图片")
                return

            # 调整当前索引（处理删除的是最后一张图片的情况）
            if self.current_index >= len(self.image_paths):
                self.current_index = len(self.image_paths) - 1

            # 显示调整后的当前图片
            self.show_current_image()

        except Exception as e:
            # 捕获并显示删除过程中的任何错误
            messagebox.showerror("错误", f"删除失败: {str(e)}")