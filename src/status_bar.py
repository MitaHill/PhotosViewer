#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
状态栏输出处理模块
Status Bar Output Handler Module
"""

import tkinter as tk


class StatusBarOutput:
    """状态栏输出处理器，支持动画效果的消息显示"""

    def __init__(self, text_widget, lines_list, max_lines=1, animation_steps=8, animation_delay=10,
                 enable_console=True):
        """
        初始化状态栏输出处理器

        Args:
            text_widget: Tkinter文本控件
            lines_list: 存储状态行的列表
            max_lines: 最大显示行数
            animation_steps: 动画的步骤数量
            animation_delay: 每步动画的延迟(毫秒)
            enable_console: 是否同步输出到控制台
        """
        self.text_widget = text_widget
        self.lines_list = lines_list
        self.max_lines = max_lines
        self.animation_steps = animation_steps
        self.animation_delay = animation_delay
        self.animating = False
        self.message_queue = []
        self.animation_id = None
        self.enable_console = enable_console

        # 保存原始的标准输出
        import sys
        self.original_stdout = sys.__stdout__

        # 设置文本控件样式
        self.text_widget.config(
            wrap=tk.WORD,
            padx=5,
            pady=2,
            highlightthickness=0,
            font=('TkDefaultFont', 12)
        )

        # 预先创建动画标签
        self._create_animation_tags()

        # 窗口引用
        self._root = self.text_widget.winfo_toplevel()

        # 双缓冲设置
        try:
            self._root.call('::tk::unsupported::MacWindowStyle', 'style',
                            self._root._w, 'help', 'noActivates')
            self._root.update_idletasks()
        except:
            pass

    def _create_animation_tags(self):
        """预先创建所有需要的动画标签"""
        self.text_widget.tag_configure("slide_in", foreground="#333333")
        self.text_widget.tag_configure("slide_out", foreground="#999999")

        # 预创建渐变动画的所有颜色标签
        for step in range(self.animation_steps):
            intensity = int(255 - (255 * step / self.animation_steps))
            color = f"#{intensity:02x}{intensity:02x}{intensity:02x}"
            self.text_widget.tag_configure(f"fade_{step}", foreground=color)

    def write(self, message):
        """写入新消息到状态栏"""
        message = message.rstrip('\n')
        if not message:
            return

        # 同时输出到控制台
        if self.enable_console and self.original_stdout:
            try:
                self.original_stdout.write(message + '\n')
                self.original_stdout.flush()
            except:
                pass

        self.message_queue.append(message)

        if not self.animating:
            self._process_next_message()

    def _process_next_message(self):
        """处理队列中的下一条消息"""
        if not self.message_queue:
            self.animating = False
            return

        self.animating = True
        message = self.message_queue.pop(0)

        # 更新行列表
        self.lines_list.append(message)
        while len(self.lines_list) > self.max_lines:
            self.lines_list.pop(0)

        # 开始滑动动画
        self._animate_slide(message)

    def _cancel_animation(self):
        """取消当前正在进行的动画"""
        if self.animation_id:
            self._root.after_cancel(self.animation_id)
            self.animation_id = None

    def _animate_slide(self, new_message):
        """执行滑动动画"""
        self._cancel_animation()
        self.text_widget.config(state=tk.NORMAL)

        old_text = self.text_widget.get(1.0, tk.END).strip()
        height = self.text_widget.winfo_height()

        self._slide_step(old_text, new_message, height, 0)

    def _slide_step(self, old_text, new_message, height, step):
        """单个滑动动画步骤"""
        if step >= self.animation_steps * 2:
            # 动画完成
            self.text_widget.delete(1.0, tk.END)
            new_text = '\n'.join(self.lines_list)
            self.text_widget.insert(tk.END, new_text, "slide_in")
            self.text_widget.config(state=tk.DISABLED)

            self.animation_id = self._root.after(50, self._process_next_message)
            return

        # 清除文本区域
        self.text_widget.delete(1.0, tk.END)

        if step < self.animation_steps:
            # 滑出动画阶段
            if old_text:
                offset = int((step / self.animation_steps) * height)
                self.text_widget.insert(tk.END, old_text, "slide_out")
                self.text_widget.yview_scroll(offset, "pixels")
        else:
            # 滑入动画阶段
            new_text = '\n'.join(self.lines_list)
            self.text_widget.insert(tk.END, new_text, "slide_in")

            inner_step = step - self.animation_steps
            offset = int(((self.animation_steps - inner_step) / self.animation_steps) * height)
            self.text_widget.yview_scroll(offset, "pixels")

        # 安排下一个动画步骤
        self.animation_id = self._root.after(
            self.animation_delay,
            lambda: self._slide_step(old_text, new_message, height, step + 1)
        )

    def _fade_animation(self, new_message):
        """渐变动画"""
        self._cancel_animation()
        self.text_widget.config(state=tk.NORMAL)

        old_text = self.text_widget.get(1.0, tk.END).strip()
        self._fade_step(old_text, new_message, 0)

    def _fade_step(self, old_text, new_message, step):
        """单个渐变动画步骤"""
        total_steps = self.animation_steps * 2

        if step >= total_steps:
            # 动画完成
            self.text_widget.delete(1.0, tk.END)
            new_text = '\n'.join(self.lines_list)
            self.text_widget.insert(tk.END, new_text)
            self.text_widget.config(state=tk.DISABLED)

            self.animation_id = self._root.after(50, self._process_next_message)
            return

        self.text_widget.delete(1.0, tk.END)

        if step < self.animation_steps:
            # 渐出阶段
            if old_text:
                fade_index = self.animation_steps - step - 1
                self.text_widget.insert(tk.END, old_text, f"fade_{fade_index}")
        else:
            # 渐入阶段
            new_text = '\n'.join(self.lines_list)
            fade_index = step - self.animation_steps
            self.text_widget.insert(tk.END, new_text, f"fade_{fade_index}")

        # 安排下一个渐变步骤
        self.animation_id = self._root.after(
            self.animation_delay,
            lambda: self._fade_step(old_text, new_message, step + 1)
        )

    def flush(self):
        """兼容 sys.stdout 的接口"""
        pass

    def set_animation_params(self, steps=10, delay=15):
        """设置动画参数"""
        self.animation_steps = steps
        self.animation_delay = delay
        self._create_animation_tags()

    def cancel_all_animations(self):
        """取消所有动画并清空队列"""
        self._cancel_animation()
        self.message_queue.clear()
        self.animating = False

    def set_font_size(self, size=12):
        """设置状态栏字体大小"""
        self.text_widget.config(font=('TkDefaultFont', size))

    def set_console_output(self, enabled):
        """
        设置是否同步输出到控制台

        Args:
            enabled: 是否启用控制台输出
        """
        self.enable_console = enabled
        if enabled:
            print("状态栏消息将同步输出到控制台")
        else:
            print("状态栏消息不再输出到控制台")

    def __del__(self):
        """析构函数，确保清理资源"""
        self.cancel_all_animations()