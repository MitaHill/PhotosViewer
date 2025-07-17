#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
播放控制功能模块
Playback Control Functionality Module
"""

import tkinter as tk


class PlaybackMixin:
    """播放控制功能混合类"""

    def toggle_playback(self, event=None):
        """切换播放/暂停状态"""
        if not self.image_paths:
            return

        self.is_playing = not self.is_playing
        if self.is_playing:
            self.start_playback()
        else:
            self.pause_playback()

    def start_playback(self):
        """开始播放"""
        self.root.title("图片查看器 - 播放中...")

        # 禁用导航和交互
        self.disable_navigation()
        self.canvas.unbind('<MouseWheel>')
        self.canvas.unbind('<ButtonPress-1>')
        self.canvas.unbind('<B1-Motion>')
        self.canvas.unbind('<ButtonRelease-1>')

        # 禁用菜单项
        self.menubar.entryconfig("上一张", state="disabled")
        self.menubar.entryconfig("下一张", state="disabled")

        self.auto_advance()

    def pause_playback(self):
        """暂停播放"""
        self.is_playing = False

        if self.playback_id:
            self.root.after_cancel(self.playback_id)
            self.playback_id = None

        # 恢复窗口标题
        if self.image_paths:
            current_name = self.image_paths[self.current_index].split('/')[-1]
            self.root.title(f"图片查看器 - {current_name}")

        # 恢复导航和交互
        self.enable_navigation()
        self.canvas.bind('<MouseWheel>', self.on_mousewheel)
        self.canvas.bind('<ButtonPress-1>', self.on_drag_start)
        self.canvas.bind('<B1-Motion>', self.on_drag)
        self.canvas.bind('<ButtonRelease-1>', self.on_drag_end)

        # 恢复菜单项
        self.menubar.entryconfig("上一张", state="normal")
        self.menubar.entryconfig("下一张", state="normal")

    def stop_playback(self):
        """停止播放"""
        self.pause_playback()
        self.current_index = 0
        self.show_current_image()

    def auto_advance(self):
        """自动播放下一张"""
        if self.is_playing and self.current_index < len(self.image_paths) - 1:
            self.navigate("next")
            interval = getattr(self, 'playback_interval', 1)
            self.playback_id = self.root.after(interval, self.auto_advance)
        else:
            self.stop_playback()

    def custom_playback_interval(self):
        """自定义播放间隔"""
        if not self.image_paths:
            return

        dialog = tk.Toplevel(self.root)
        dialog.title("调节播放间隔")
        dialog.transient(self.root)
        dialog.grab_set()

        tk.Label(dialog, text="请输入播放间隔（毫秒）:").pack(pady=5)
        interval_entry = tk.Entry(dialog)
        interval_entry.insert(0, str(getattr(self, 'playback_interval', 1)))
        interval_entry.pack(pady=5)
        interval_entry.focus_set()

        def on_submit():
            try:
                interval = int(interval_entry.get())
                if interval <= 0:
                    raise ValueError("间隔必须大于0")

                self.playback_interval = interval
                print(f"播放间隔设置为: {self.playback_interval}ms")
                dialog.destroy()

                # 重新启动播放以应用新间隔
                if self.is_playing:
                    self.pause_playback()
                    self.start_playback()

            except ValueError:
                print("错误，请输入有效的正整数")

        tk.Button(dialog, text="确认", command=on_submit).pack(pady=5)
        dialog.bind('<Return>', lambda e: on_submit())