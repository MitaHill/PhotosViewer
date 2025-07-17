#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
动画工具功能模块
Animation Utility Functions Module
"""

import math


class AnimationMixin:
    """动画工具功能混合类"""

    def ease_in_out(self, step, total_steps, easing_type="cubic", amplitude=1.0, overshoot=1.70158):
        """
        非线性缓动函数，支持多种缓动类型

        Args:
            step: 当前步数（从0开始）
            total_steps: 总步数
            easing_type: 缓动类型
            amplitude: 弹性缓动振幅
            overshoot: 回弹缓动超调量

        Returns:
            float: 缓动进度值，范围[0, 1]
        """
        if total_steps <= 0:
            raise ValueError("total_steps 必须大于 0")

        if step < 0 or step > total_steps:
            step = max(0, min(step, total_steps))

        t = step / total_steps

        if easing_type == "linear":
            return t
        elif easing_type == "quadratic":
            return t * t if t < 0.5 else 1 - (1 - t) * (1 - t)
        elif easing_type == "cubic":
            if t < 0.5:
                return 4 * t * t * t
            else:
                p = 2 * t - 2
                return 0.5 * p * p * p + 1
        elif easing_type == "quartic":
            return t ** 4 if t < 0.5 else 1 - (1 - t) ** 4
        elif easing_type == "elastic":
            if t == 0:
                return 0
            if t == 1:
                return 1
            p = 0.3
            s = p / 4
            return amplitude * (2 ** (-10 * t)) * math.sin((t - s) * (2 * math.pi) / p) + 1
        elif easing_type == "back":
            return t * t * ((overshoot + 1) * t - overshoot) if t < 0.5 else \
                1 + (1 - t) * (1 - t) * ((overshoot + 1) * (1 - t) + overshoot)
        elif easing_type == "smooth":
            return 0.5 - 0.5 * math.cos(t * math.pi)
        else:
            return t

    def improved_cubic_easing(self, t, easing_type="cubic", amplitude=1.0, overshoot=1.70158):
        """
        改进的缓动函数，基于百分比时间值

        Args:
            t: 标准化时间值，范围[0, 1]
            easing_type: 缓动类型
            amplitude: 弹性缓动振幅
            overshoot: 回弹缓动超调量

        Returns:
            float: 缓动进度值，范围[0, 1]
        """
        step = int(t * 100)
        total_steps = 100
        return self.ease_in_out(step, total_steps, easing_type, amplitude, overshoot)