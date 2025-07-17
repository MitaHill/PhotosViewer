#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
图片导航功能模块
Photo Navigation Functionality Module
"""

import time


class NavigationMixin:
    """图片导航功能混合类"""

    def navigate(self, direction):
        """导航到上一张或下一张图片"""
        max_index = len(self.image_paths) - 1
        if direction == "prev":
            self.current_index = max(0, self.current_index - 1)
        else:
            self.current_index = min(max_index, self.current_index + 1)

        self.zoom_factor = 1.0
        self.show_current_image()

        # 节流控制
        current_time = time.time()
        if hasattr(self, 'last_navigate_time') and current_time - self.last_navigate_time < 0.05:
            return False

        self.last_navigate_time = current_time
        return True

    def enable_navigation(self):
        """启用导航功能"""
        if not self.is_playing:
            self.root.bind('<Left>', self.on_left_press)
            self.root.bind('<KeyRelease-Left>', self.on_left_release)
            self.root.bind('<Right>', self.on_right_press)
            self.root.bind('<KeyRelease-Right>', self.on_right_release)

    def disable_navigation(self):
        """禁用导航功能"""
        self.root.unbind('<Left>')
        self.root.unbind('<Right>')

    def start_repeat(self, direction):
        """开始重复导航操作"""
        max_pending_events = 30

        def repeat(delay, step=0):
            if not self.auto_press:
                return

            if self.root.tk.call('after', 'info') and len(self.root.tk.call('after', 'info')) > max_pending_events:
                self.repeat_id = self.root.after(self.max_delay, lambda: repeat(self.max_delay, step))
                return

            self.navigate(direction)

            acceleration_factor = min(0.5, step / 30.0)
            new_delay = max(self.min_delay, int(self.max_delay * (1 - acceleration_factor * self.speed_boost)))

            self.repeat_id = self.root.after(new_delay, lambda: repeat(new_delay, step + 1))

        self.stop_repeat()
        self.auto_press = True
        initial_delay = self.max_delay
        self.repeat_id = self.root.after(initial_delay, lambda: repeat(initial_delay, 0))

    def stop_repeat(self):
        """停止重复导航操作"""
        self.auto_press = False
        if self.repeat_id:
            self.root.after_cancel(self.repeat_id)
            self.repeat_id = None

    def on_left_press(self, event):
        """左键按下事件"""
        if not self.auto_press and not self.is_playing:
            self.navigate("prev")
            self.start_repeat("prev")

    def on_left_release(self, event):
        """左键释放事件"""
        self.stop_repeat()

    def on_right_press(self, event):
        """右键按下事件"""
        if not self.auto_press and not self.is_playing:
            self.navigate("next")
            self.start_repeat("next")

    def on_right_release(self, event):
        """右键释放事件"""
        self.stop_repeat()