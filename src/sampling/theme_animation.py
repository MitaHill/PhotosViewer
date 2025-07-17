#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
主题切换动画组件
Theme Change Animation Component
"""

import threading


class ThemeAnimation:
    """主题切换动画管理器"""

    def __init__(self, parent):
        """
        初始化主题动画器

        Args:
            parent: 父对象（ImageViewer实例）
        """
        self.parent = parent
        self.animation_active = False
        self.animation_id = None

        # 动画参数配置
        self.animation_steps = 12
        self.animation_duration = 350  # 总时长(ms)
        self.easing_type = "cubic"

        # 颜色插值缓存
        self._color_cache = {}

    def animate_theme_change(self, old_theme, new_theme, theme_colors):
        """
        执行主题切换动画

        Args:
            old_theme: 旧主题名称
            new_theme: 新主题名称
            theme_colors: 主题颜色配置字典
        """
        if self.animation_active:
            self._cancel_current_animation()

        if not hasattr(self.parent, 'overlay_manager') or not self.parent.overlay_manager.overlay_exists():
            return

        self.animation_active = True

        # 获取颜色配置
        old_colors = theme_colors[old_theme]
        new_colors = theme_colors[new_theme]

        # 启动动画
        self._start_color_transition(old_colors, new_colors)

        print(f"主题变色动画开始: {old_theme} -> {new_theme}")

    def _start_color_transition(self, old_colors, new_colors):
        """
        开始颜色过渡动画

        Args:
            old_colors: 旧主题颜色
            new_colors: 新主题颜色
        """
        step_duration = self.animation_duration // self.animation_steps

        def animate_step(step=0):
            if step > self.animation_steps or not self.animation_active:
                # 动画完成或被取消
                self._finish_animation(new_colors)
                return

            # 计算当前步骤的进度
            progress = self.parent.ease_in_out(step, self.animation_steps, self.easing_type)

            # 插值计算当前颜色
            current_colors = self._interpolate_colors(old_colors, new_colors, progress)

            # 更新悬浮框颜色
            self._apply_colors_to_overlay(current_colors)

            # 安排下一帧
            self.animation_id = self.parent.root.after(
                step_duration,
                lambda: animate_step(step + 1)
            )

        animate_step(0)

    def _interpolate_colors(self, color1_dict, color2_dict, progress):
        """
        在两组颜色之间进行插值

        Args:
            color1_dict: 起始颜色字典
            color2_dict: 结束颜色字典
            progress: 进度 (0.0 - 1.0)

        Returns:
            dict: 插值后的颜色字典
        """
        result = {}

        for key in color1_dict:
            if key in color2_dict:
                color1 = color1_dict[key]
                color2 = color2_dict[key]
                result[key] = self._interpolate_single_color(color1, color2, progress)
            else:
                result[key] = color1_dict[key]

        return result

    def _interpolate_single_color(self, color1, color2, progress):
        """
        在两个颜色之间进行插值

        Args:
            color1: 起始颜色 (如 "#ffffff")
            color2: 结束颜色 (如 "#000000")
            progress: 进度 (0.0 - 1.0)

        Returns:
            str: 插值后的颜色
        """
        # 检查缓存
        cache_key = (color1, color2, round(progress, 3))
        if cache_key in self._color_cache:
            return self._color_cache[cache_key]

        try:
            # 解析起始颜色
            r1, g1, b1 = self._parse_hex_color(color1)
            r2, g2, b2 = self._parse_hex_color(color2)

            # 线性插值
            r = int(r1 + (r2 - r1) * progress)
            g = int(g1 + (g2 - g1) * progress)
            b = int(b1 + (b2 - b1) * progress)

            # 确保值在有效范围内
            r = max(0, min(255, r))
            g = max(0, min(255, g))
            b = max(0, min(255, b))

            result = f"#{r:02x}{g:02x}{b:02x}"

            # 缓存结果
            self._color_cache[cache_key] = result

            return result

        except Exception as e:
            print(f"颜色插值失败: {e}")
            return color2  # 返回目标颜色作为备选

    def _parse_hex_color(self, hex_color):
        """
        解析十六进制颜色

        Args:
            hex_color: 十六进制颜色字符串

        Returns:
            tuple: (r, g, b) 值
        """
        if not hex_color.startswith('#'):
            raise ValueError(f"无效的颜色格式: {hex_color}")

        hex_color = hex_color[1:]  # 移除 #

        if len(hex_color) != 6:
            raise ValueError(f"颜色长度错误: {hex_color}")

        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)

        return r, g, b

    def _apply_colors_to_overlay(self, colors):
        """
        将颜色应用到悬浮框

        Args:
            colors: 颜色字典
        """
        try:
            if hasattr(self.parent, 'overlay_manager'):
                self.parent.overlay_manager.update_theme_colors(colors)
        except Exception as e:
            print(f"应用颜色到悬浮框失败: {e}")

    def _finish_animation(self, final_colors):
        """
        完成动画并清理

        Args:
            final_colors: 最终颜色
        """
        try:
            # 应用最终颜色
            self._apply_colors_to_overlay(final_colors)

            # 清理状态
            self.animation_active = False
            self.animation_id = None

            print("主题变色动画完成")

        except Exception as e:
            print(f"完成动画时出错: {e}")

    def _cancel_current_animation(self):
        """取消当前进行的动画"""
        if self.animation_id:
            self.parent.root.after_cancel(self.animation_id)
            self.animation_id = None

        self.animation_active = False
        print("主题动画已取消")

    def set_animation_parameters(self, steps=12, duration=350, easing="cubic"):
        """
        设置动画参数

        Args:
            steps: 动画步数
            duration: 总时长(ms)
            easing: 缓动类型
        """
        self.animation_steps = max(5, min(30, steps))  # 限制在合理范围内
        self.animation_duration = max(100, min(1000, duration))  # 限制在合理范围内
        self.easing_type = easing

        print(f"动画参数已更新: 步数={self.animation_steps}, 时长={self.animation_duration}ms, 缓动={self.easing_type}")

    def animate_color_pulse(self, color, intensity=0.3, cycles=2):
        """
        颜色脉冲动画（用于强调效果）

        Args:
            color: 基础颜色
            intensity: 脉冲强度 (0.0-1.0)
            cycles: 脉冲周期数
        """
        if self.animation_active:
            return

        if not hasattr(self.parent, 'overlay_manager') or not self.parent.overlay_manager.overlay_exists():
            return

        self.animation_active = True

        # 计算脉冲颜色
        pulse_color = self._adjust_color_brightness(color, intensity)

        total_steps = cycles * 2 * 10  # 每个周期20步（10步变亮+10步变暗）
        step_duration = 50  # 每步50ms

        def pulse_step(step=0):
            if step >= total_steps or not self.animation_active:
                # 恢复原色并结束
                self._apply_single_color_to_all(color)
                self.animation_active = False
                return

            # 计算当前周期内的进度
            cycle_progress = (step % 20) / 20.0
            if cycle_progress > 0.5:
                cycle_progress = 1.0 - cycle_progress
            cycle_progress *= 2  # 放大到 0-1 范围

            # 插值颜色
            current_color = self._interpolate_single_color(color, pulse_color, cycle_progress)

            # 应用颜色
            self._apply_single_color_to_all(current_color)

            # 安排下一帧
            self.animation_id = self.parent.root.after(
                step_duration,
                lambda: pulse_step(step + 1)
            )

        pulse_step(0)

    def _adjust_color_brightness(self, color, factor):
        """
        调整颜色亮度

        Args:
            color: 原始颜色
            factor: 亮度因子 (-1.0 到 1.0)

        Returns:
            str: 调整后的颜色
        """
        try:
            r, g, b = self._parse_hex_color(color)

            if factor > 0:
                # 变亮
                r = int(r + (255 - r) * factor)
                g = int(g + (255 - g) * factor)
                b = int(b + (255 - b) * factor)
            else:
                # 变暗
                factor = abs(factor)
                r = int(r * (1 - factor))
                g = int(g * (1 - factor))
                b = int(b * (1 - factor))

            return f"#{r:02x}{g:02x}{b:02x}"

        except Exception as e:
            print(f"调整颜色亮度失败: {e}")
            return color

    def _apply_single_color_to_all(self, color):
        """
        将单一颜色应用到所有文本元素

        Args:
            color: 颜色值
        """
        try:
            colors = {
                'text': color,
                'background': self.parent.color_detector.get_theme_color('background'),
                'outline': color
            }
            self._apply_colors_to_overlay(colors)
        except Exception as e:
            print(f"应用颜色失败: {e}")

    def clear_color_cache(self):
        """清空颜色插值缓存"""
        self._color_cache.clear()
        print("颜色缓存已清空")

    def is_animating(self):
        """
        检查是否正在执行动画

        Returns:
            bool: 是否在动画中
        """
        return self.animation_active

    def stop_animation(self):
        """强制停止当前动画"""
        if self.animation_active:
            self._cancel_current_animation()

            # 应用当前主题的最终颜色
            current_colors = self.parent.color_detector.get_current_theme_colors()
            self._apply_colors_to_overlay(current_colors)

    def preview_color_transition(self, color1, color2, steps=10):
        """
        预览颜色过渡效果（调试用）

        Args:
            color1: 起始颜色
            color2: 结束颜色
            steps: 过渡步数

        Returns:
            list: 过渡颜色列表
        """
        transition = []
        for i in range(steps + 1):
            progress = i / steps
            color = self._interpolate_single_color(color1, color2, progress)
            transition.append(color)

        return transition