#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
悬浮信息框管理组件
Overlay Information Box Management Component
"""


class OverlayManager:
    """悬浮信息框管理器"""

    def __init__(self, parent):
        """
        初始化悬浮框管理器

        Args:
            parent: 父对象（ImageViewer实例）
        """
        self.parent = parent
        self.overlay_elements = {}
        self.overlay_width = 200
        self.overlay_height = 80
        self.animation_id = None

        # 当前位置和目标位置
        self.current_x = 0
        self.current_y = 0
        self.target_x = 0
        self.target_y = 0

    def create_overlay(self):
        """创建悬浮信息框"""
        if self.overlay_exists():
            return

        canvas_width = self.parent.canvas.winfo_width()
        canvas_height = self.parent.canvas.winfo_height()

        # 初始位置设在右下角
        self.target_x = canvas_width - self.overlay_width - 10
        self.target_y = canvas_height - self.overlay_height - 10
        self.current_x = self.target_x
        self.current_y = self.target_y

        # 获取当前主题颜色
        theme_colors = self.parent.color_detector.get_current_theme_colors()

        # 创建背景框
        self.overlay_elements['background'] = self.parent.canvas.create_rectangle(
            self.current_x, self.current_y,
            self.current_x + self.overlay_width, self.current_y + self.overlay_height,
            fill=theme_colors['background'],
            stipple='gray50',
            outline=theme_colors['outline'],
            width=1
        )

        # 创建文本元素
        self._create_text_elements(theme_colors['text'])

        # 启动淡入动画
        self._animate_fade_in()

    def _create_text_elements(self, text_color):
        """
        创建文本显示元素

        Args:
            text_color: 文本颜色
        """
        base_x = self.current_x + 10
        base_y = self.current_y

        self.overlay_elements['rgb_text'] = self.parent.canvas.create_text(
            base_x, base_y + 15,
            text="RGB: ---",
            fill=text_color,
            anchor='w',
            font=('Arial', 9)
        )

        self.overlay_elements['hex_text'] = self.parent.canvas.create_text(
            base_x, base_y + 35,
            text="HEX: ---",
            fill=text_color,
            anchor='w',
            font=('Arial', 9)
        )

        self.overlay_elements['coord_text'] = self.parent.canvas.create_text(
            base_x, base_y + 55,
            text="坐标: ---",
            fill=text_color,
            anchor='w',
            font=('Arial', 9)
        )

    def destroy_overlay(self):
        """销毁悬浮信息框（带淡出动画）"""
        if not self.overlay_exists():
            return

        # 取消进行中的动画
        self._cancel_animation()

        # 启动淡出动画
        self._animate_fade_out()

    def overlay_exists(self):
        """
        检查悬浮框是否存在

        Returns:
            bool: 是否存在
        """
        return bool(self.overlay_elements.get('background'))

    def update_display(self, rgb_text, hex_text, coord_text):
        """
        更新显示内容

        Args:
            rgb_text: RGB文本
            hex_text: HEX文本
            coord_text: 坐标文本
        """
        if not self.overlay_exists():
            return

        try:
            self.parent.canvas.itemconfig(self.overlay_elements['rgb_text'], text=rgb_text)
            self.parent.canvas.itemconfig(self.overlay_elements['hex_text'], text=hex_text)
            self.parent.canvas.itemconfig(self.overlay_elements['coord_text'], text=coord_text)
        except Exception as e:
            print(f"更新悬浮框显示失败: {e}")

    def update_position(self, new_x, new_y, animate=True):
        """
        更新悬浮框位置

        Args:
            new_x: 新的X坐标
            new_y: 新的Y坐标
            animate: 是否使用动画
        """
        if not self.overlay_exists():
            return

        self.target_x = new_x
        self.target_y = new_y

        if animate:
            self._animate_move()
        else:
            self.current_x = new_x
            self.current_y = new_y
            self._update_coords()

    def _animate_move(self):
        """移动动画"""
        if self.animation_id:
            self.parent.root.after_cancel(self.animation_id)

        start_x = self.current_x
        start_y = self.current_y

        # 如果位置变化很小，直接设置
        if (abs(self.target_x - start_x) < 5 and
                abs(self.target_y - start_y) < 5):
            self.current_x = self.target_x
            self.current_y = self.target_y
            self._update_coords()
            return

        steps = 15
        duration = 300

        def animate_step(step=0):
            if step > steps:
                # 动画完成
                self.current_x = self.target_x
                self.current_y = self.target_y
                self._update_coords()
                return

            # 使用缓动函数计算当前位置
            progress = self.parent.ease_in_out(step, steps, "cubic")
            self.current_x = start_x + (self.target_x - start_x) * progress
            self.current_y = start_y + (self.target_y - start_y) * progress

            self._update_coords()

            # 安排下一帧
            self.animation_id = self.parent.root.after(
                duration // steps,
                lambda: animate_step(step + 1)
            )

        animate_step(0)

    def _animate_fade_in(self):
        """淡入动画"""
        steps = 8
        duration = 240  # 总时长240ms

        def fade_step(step=0):
            if step > steps:
                return

            # 计算透明度
            progress = self.parent.ease_in_out(step, steps, "smooth")
            alpha = int(255 * progress)

            # 更新颜色
            self._update_element_alpha(alpha)

            # 安排下一帧
            self.parent.root.after(
                duration // steps,
                lambda: fade_step(step + 1)
            )

        fade_step(0)

    def _animate_fade_out(self):
        """淡出动画"""
        steps = 8
        duration = 160  # 总时长160ms

        def fade_step(step=0):
            if step > steps:
                # 动画完成，删除元素
                self._remove_elements()
                return

            # 计算透明度
            progress = self.parent.ease_in_out(step, steps, "smooth")
            alpha = int(255 * (1 - progress))

            # 更新颜色
            self._update_element_alpha(alpha)

            # 安排下一帧
            self.parent.root.after(
                duration // steps,
                lambda: fade_step(step + 1)
            )

        fade_step(0)

    def _update_element_alpha(self, alpha):
        """
        更新元素透明度

        Args:
            alpha: 透明度值 (0-255)
        """
        if not self.overlay_exists():
            return

        try:
            # 获取当前主题
            theme_colors = self.parent.color_detector.get_current_theme_colors()

            # 计算带透明度的颜色
            text_color = self._apply_alpha(theme_colors['text'], alpha)
            outline_color = self._apply_alpha(theme_colors['outline'], alpha)

            # 更新文本颜色
            for text_key in ['rgb_text', 'hex_text', 'coord_text']:
                if text_key in self.overlay_elements:
                    self.parent.canvas.itemconfig(
                        self.overlay_elements[text_key],
                        fill=text_color
                    )

            # 更新边框颜色
            if 'background' in self.overlay_elements:
                self.parent.canvas.itemconfig(
                    self.overlay_elements['background'],
                    outline=outline_color
                )

        except Exception as e:
            print(f"更新元素透明度失败: {e}")

    def _apply_alpha(self, color, alpha):
        """
        为颜色应用透明度

        Args:
            color: 原始颜色 (如 "#ffffff")
            alpha: 透明度 (0-255)

        Returns:
            str: 带透明度的颜色
        """
        if color.startswith('#'):
            # 解析hex颜色
            hex_color = color[1:]
            if len(hex_color) == 6:
                r = int(hex_color[0:2], 16)
                g = int(hex_color[2:4], 16)
                b = int(hex_color[4:6], 16)
            else:
                r = g = b = 255
        else:
            r = g = b = 255

        # 应用透明度
        r = int(r * alpha / 255)
        g = int(g * alpha / 255)
        b = int(b * alpha / 255)

        return f"#{r:02x}{g:02x}{b:02x}"

    def _update_coords(self):
        """更新所有元素坐标"""
        if not self.overlay_exists():
            return

        try:
            # 更新背景框
            self.parent.canvas.coords(
                self.overlay_elements['background'],
                self.current_x, self.current_y,
                self.current_x + self.overlay_width, self.current_y + self.overlay_height
            )

            # 更新文本位置
            base_x = self.current_x + 10
            base_y = self.current_y

            self.parent.canvas.coords(self.overlay_elements['rgb_text'], base_x, base_y + 15)
            self.parent.canvas.coords(self.overlay_elements['hex_text'], base_x, base_y + 35)
            self.parent.canvas.coords(self.overlay_elements['coord_text'], base_x, base_y + 55)

        except Exception as e:
            print(f"更新坐标失败: {e}")

    def _cancel_animation(self):
        """取消进行中的动画"""
        if self.animation_id:
            self.parent.root.after_cancel(self.animation_id)
            self.animation_id = None

    def _remove_elements(self):
        """移除所有画布元素"""
        try:
            for element_id in self.overlay_elements.values():
                if element_id:
                    self.parent.canvas.delete(element_id)
        except Exception as e:
            print(f"删除悬浮框元素失败: {e}")
        finally:
            self.overlay_elements.clear()

    def get_bounds(self):
        """
        获取悬浮框边界

        Returns:
            tuple: (x, y, width, height)
        """
        if not self.overlay_exists():
            return (0, 0, 0, 0)

        return (self.current_x, self.current_y, self.overlay_width, self.overlay_height)

    def update_theme_colors(self, theme_colors):
        """
        更新主题颜色（用于主题切换动画）

        Args:
            theme_colors: 新的主题颜色配置
        """
        if not self.overlay_exists():
            return

        try:
            # 更新文本颜色
            for text_key in ['rgb_text', 'hex_text', 'coord_text']:
                if text_key in self.overlay_elements:
                    self.parent.canvas.itemconfig(
                        self.overlay_elements[text_key],
                        fill=theme_colors['text']
                    )

            # 更新背景和边框
            if 'background' in self.overlay_elements:
                self.parent.canvas.itemconfig(
                    self.overlay_elements['background'],
                    fill=theme_colors['background'],
                    outline=theme_colors['outline']
                )

        except Exception as e:
            print(f"更新主题颜色失败: {e}")