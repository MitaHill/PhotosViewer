#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
图片定位功能模块
Photo Positioning Functionality Module
"""

import os
import sys
import subprocess
from tkinter import messagebox


class PositionPhotoMixin:
    """图片定位功能混合类"""

    def locate_image_in_directory(self, event=None):
        """在文件资源管理器中定位并选中当前图片"""
        if not self.image_paths or self.current_index < 0 or self.current_index >= len(self.image_paths):
            return

        current_path = self.image_paths[self.current_index]

        try:
            if sys.platform == 'win32':
                # Windows: 打开资源管理器并选中文件
                subprocess.run(['explorer', '/select,', current_path])
            elif sys.platform == 'darwin':
                # macOS: 在Finder中显示并选中文件
                subprocess.run(['open', '-R', current_path])
            else:
                # Linux: 打开包含文件的目录
                subprocess.run(['xdg-open', os.path.dirname(current_path)])

            print(f"已在目录中定位: {current_path}")

        except Exception as e:
            messagebox.showerror("错误", f"定位失败: {str(e)}")