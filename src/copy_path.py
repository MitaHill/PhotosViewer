#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
路径复制功能模块
Path Copy Functionality Module
"""

import os
import sys
import io
from tkinter import messagebox


class CopyPathMixin:
    """路径复制功能混合类"""

    def copy_image_path_to_clipboard(self, event=None):
        """将当前图片的完整路径复制到系统剪贴板"""
        if not self.image_paths or self.current_index < 0 or self.current_index >= len(self.image_paths):
            return

        current_path = self.image_paths[self.current_index]

        self.root.clipboard_clear()
        self.root.clipboard_append(current_path)
        self.root.update()

        print("图片路径已复制到剪切板")

    def copy_image_to_clipboard(self, event=None):
        """将当前图片文件本体复制到系统剪切板（仅Windows支持）"""
        if not self.image_paths or self.current_index < 0 or self.current_index >= len(self.image_paths):
            messagebox.showerror("错误", "没有图片可复制")
            return

        current_path = self.image_paths[self.current_index]

        try:
            if sys.platform == 'win32' and hasattr(self, 'win32clipboard') and self.win32clipboard:
                # Windows: 使用 win32clipboard 复制图片
                from PIL import Image
                with Image.open(current_path) as img:
                    output = io.BytesIO()
                    img.convert('RGB').save(output, format='BMP')
                    data = output.getvalue()[14:]  # 跳过 BMP 文件头
                    output.close()

                    self.win32clipboard.OpenClipboard()
                    self.win32clipboard.EmptyClipboard()
                    self.win32clipboard.SetClipboardData(self.win32clipboard.CF_DIB, data)
                    self.win32clipboard.CloseClipboard()
                    print("图片已复制到剪切板")
            else:
                # macOS 和 Linux 暂不支持直接复制图片本体
                messagebox.showinfo("提示", "当前平台不支持直接复制图片到剪切板，请使用 Ctrl+Shift+C 复制路径")
        except Exception as e:
            messagebox.showerror("错误", f"复制图片失败: {str(e)}")