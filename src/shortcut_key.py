#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
快捷键功能模块
Shortcut Key Functionality Module
"""

import tkinter as tk


class ShortcutKeyMixin:
    """快捷键功能混合类"""

    def setup_shortcuts(self):
        """设置所有快捷键绑定"""
        # Ctrl+O - 打开图片
        self.root.bind('<Control-o>', self.shortcut_open_image)

        # Ctrl+C - 复制图片本体到剪切板
        self.root.bind('<Control-c>', self.shortcut_copy_image_body)

        # Alt+C - 复制图片路径到剪切板
        self.root.bind('<Alt-c>', self.shortcut_copy_image_path)

        # Alt+P - 播放开始/暂停
        self.root.bind('<Alt-p>', self.shortcut_toggle_playback)

        # 设置取色器事件绑定
        self.setup_sampling_events()

        # 输出快捷键提示
        print("快捷键已启用:")
        print("  Ctrl+O    - 打开图片")
        print("  Ctrl+C    - 复制图片本体")
        print("  Alt+C     - 复制图片路径")
        print("  Alt+P     - 播放/暂停")
        print("  Ctrl+Alt  - 取色器模式（按住激活）")

    def shortcut_open_image(self, event=None):
        """快捷键：打开图片"""
        try:
            self.open_image()
            print("快捷键: 打开图片对话框")
        except Exception as e:
            print(f"打开图片失败: {e}")
        return "break"

    def shortcut_copy_image_body(self, event=None):
        """快捷键：复制图片本体到剪切板"""
        try:
            self.copy_image_body_to_clipboard()
        except Exception as e:
            print(f"复制图片本体失败: {e}")
        return "break"

    def shortcut_copy_image_path(self, event=None):
        """快捷键：复制图片路径到剪切板"""
        try:
            self.copy_image_path_to_clipboard()
            print("快捷键: 已复制图片路径")
        except Exception as e:
            print(f"复制图片路径失败: {e}")
        return "break"

    def shortcut_toggle_playback(self, event=None):
        """快捷键：切换播放状态"""
        try:
            self.toggle_playback()
            status = "播放" if self.is_playing else "暂停"
            print(f"快捷键: {status}")
        except Exception as e:
            print(f"切换播放状态失败: {e}")
        return "break"