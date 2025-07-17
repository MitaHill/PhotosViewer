#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
取色器模块初始化文件
Sampling Module Initialization
"""

from .color_detector import ColorDetector
from .overlay_manager import OverlayManager
from .coordinate_converter import CoordinateConverter
from .pixel_sampler import PixelSampler, ColorInfo
from .theme_animation import ThemeAnimation
from .position_calculator import PositionCalculator

# 版本信息
__version__ = "1.0.0"
__author__ = "Clash/善良米塔"

# 模块导出
__all__ = [
    'ColorDetector',
    'OverlayManager',
    'CoordinateConverter',
    'PixelSampler',
    'ColorInfo',
    'ThemeAnimation',
    'PositionCalculator',
    'SamplingManager'
]


class SamplingManager:
    """
    取色器管理器 - 统一管理所有取色器组件
    提供高级接口和组件协调功能
    """

    def __init__(self, parent):
        """
        初始化取色器管理器

        Args:
            parent: 父对象（ImageViewer实例）
        """
        self.parent = parent
        self.initialized = False

        # 组件实例
        self.color_detector = None
        self.overlay_manager = None
        self.coordinate_converter = None
        self.pixel_sampler = None
        self.theme_animation = None
        self.position_calculator = None

        # 管理器状态
        self.active = False
        self.performance_mode = "normal"  # normal, performance, quality

        # 统计信息
        self.stats = {
            'total_samples': 0,
            'theme_changes': 0,
            'position_updates': 0,
            'animation_count': 0
        }

    def initialize(self):
        """初始化所有组件"""
        if self.initialized:
            return

        try:
            # 初始化核心组件
            self.color_detector = ColorDetector(self.parent)
            self.overlay_manager = OverlayManager(self.parent)
            self.coordinate_converter = CoordinateConverter(self.parent)
            self.pixel_sampler = PixelSampler(self.parent)
            self.theme_animation = ThemeAnimation(self.parent)
            self.position_calculator = PositionCalculator(self.parent)

            # 将组件暴露给父对象，以便其他地方可以访问
            self.parent.color_detector = self.color_detector
            self.parent.overlay_manager = self.overlay_manager
            self.parent.coordinate_converter = self.coordinate_converter
            self.parent.pixel_sampler = self.pixel_sampler
            self.parent.theme_animation = self.theme_animation
            self.parent.position_calculator = self.position_calculator

            # 设置组件间的协作关系
            self._setup_component_coordination()

            self.initialized = True
            print("取色器管理器初始化完成")

        except Exception as e:
            print(f"取色器管理器初始化失败: {e}")
            raise

    def _setup_component_coordination(self):
        """设置组件间的协作关系"""
        # 主题检测器与动画器的协作
        original_set_theme = self.color_detector._set_theme

        def enhanced_set_theme(new_theme):
            old_theme = self.color_detector.current_theme
            original_set_theme(new_theme)

            # 更新统计
            if old_theme != new_theme:
                self.stats['theme_changes'] += 1

            # 触发主题切换动画
            if (hasattr(self.parent, 'overlay_manager') and
                    self.overlay_manager.overlay_exists()):
                self.theme_animation.animate_theme_change(
                    old_theme,
                    new_theme,
                    self.color_detector.theme_colors
                )

        self.color_detector._set_theme = enhanced_set_theme

        # 位置计算器与覆盖管理器的协作
        original_update_position = self.position_calculator.update_position_if_needed

        def enhanced_update_position(mouse_x, mouse_y):
            result = original_update_position(mouse_x, mouse_y)
            self.stats['position_updates'] += 1
            return result

        self.position_calculator.update_position_if_needed = enhanced_update_position

    def activate(self):
        """激活取色器"""
        if not self.initialized:
            self.initialize()

        if not self.parent.image_paths:
            return False

        try:
            self.active = True

            # 检测并设置主题
            self.color_detector.detect_and_set_theme()

            # 创建悬浮框
            self.overlay_manager.create_overlay()

            # 立即更新初始信息
            self._update_initial_display()

            print(f"取色器已激活 - 性能模式: {self.performance_mode}")
            return True

        except Exception as e:
            print(f"激活取色器失败: {e}")
            self.active = False
            return False

    def deactivate(self):
        """停用取色器"""
        if not self.active:
            return

        try:
            # 停止所有动画
            if self.theme_animation and self.theme_animation.is_animating():
                self.theme_animation.stop_animation()

            # 销毁悬浮框
            if self.overlay_manager:
                self.overlay_manager.destroy_overlay()

            # 清理历史记录
            if self.position_calculator:
                self.position_calculator.clear_history()

            if self.pixel_sampler:
                self.pixel_sampler.clear_history()

            self.active = False
            print("取色器已停用")

        except Exception as e:
            print(f"停用取色器时出错: {e}")

    def update_from_mouse_motion(self, canvas_x, canvas_y):
        """
        处理鼠标移动事件

        Args:
            canvas_x, canvas_y: 画布坐标
        """
        if not self.active:
            return

        try:
            # 更新位置（智能避让）
            self.position_calculator.update_position_if_needed(canvas_x, canvas_y)

            # 获取并更新颜色信息
            self._update_color_display(canvas_x, canvas_y)

        except Exception as e:
            print(f"处理鼠标移动事件失败: {e}")

    def _update_initial_display(self):
        """更新初始显示信息"""
        try:
            # 获取当前鼠标位置
            mouse_x = self.parent.root.winfo_pointerx() - self.parent.canvas.winfo_rootx()
            mouse_y = self.parent.root.winfo_pointery() - self.parent.canvas.winfo_rooty()

            # 更新显示
            self._update_color_display(mouse_x, mouse_y)

        except Exception:
            # 如果获取失败，显示默认信息
            if self.overlay_manager:
                self.overlay_manager.update_display("RGB: ---", "HEX: ---", "坐标: ---")

    def _update_color_display(self, canvas_x, canvas_y):
        """
        更新颜色显示信息

        Args:
            canvas_x, canvas_y: 画布坐标
        """
        # 转换坐标
        img_x, img_y = self.coordinate_converter.canvas_to_image_pixel(canvas_x, canvas_y)

        if img_x is None or img_y is None:
            if self.overlay_manager:
                self.overlay_manager.update_display("RGB: ---", "HEX: ---", "坐标: ---")
            return

        # 根据性能模式获取颜色信息
        if self.performance_mode == "performance":
            # 性能模式：只获取基本RGB
            rgb = self.pixel_sampler.get_pixel_color(img_x, img_y)
            if rgb:
                r, g, b = rgb
                hex_color = f"#{r:02x}{g:02x}{b:02x}"
                coord_text = f"坐标: ({int(img_x)}, {int(img_y)})"

                if self.overlay_manager:
                    self.overlay_manager.update_display(
                        f"RGB: ({r}, {g}, {b})",
                        f"HEX: {hex_color}",
                        coord_text
                    )

                self.stats['total_samples'] += 1

        elif self.performance_mode == "quality":
            # 质量模式：获取区域平均颜色
            rgb = self.pixel_sampler.get_area_average_color(img_x, img_y, radius=2)
            if rgb:
                r, g, b = rgb
                hex_color = f"#{r:02x}{g:02x}{b:02x}"
                coord_text = f"坐标: ({int(img_x)}, {int(img_y)}) [平均]"

                if self.overlay_manager:
                    self.overlay_manager.update_display(
                        f"RGB: ({r}, {g}, {b})",
                        f"HEX: {hex_color}",
                        coord_text
                    )

                self.stats['total_samples'] += 1

        else:
            # 普通模式：标准取色
            rgb = self.pixel_sampler.get_pixel_color(img_x, img_y)
            if rgb:
                r, g, b = rgb
                hex_color = f"#{r:02x}{g:02x}{b:02x}"
                coord_text = f"坐标: ({int(img_x)}, {int(img_y)})"

                if self.overlay_manager:
                    self.overlay_manager.update_display(
                        f"RGB: ({r}, {g}, {b})",
                        f"HEX: {hex_color}",
                        coord_text
                    )

                self.stats['total_samples'] += 1

        # 如果没有获取到颜色，显示默认信息
        if not rgb and self.overlay_manager:
            self.overlay_manager.update_display("RGB: ---", "HEX: ---", "坐标: ---")

    def set_performance_mode(self, mode):
        """
        设置性能模式

        Args:
            mode: 性能模式 ("performance", "normal", "quality")
        """
        valid_modes = ["performance", "normal", "quality"]
        if mode not in valid_modes:
            print(f"无效的性能模式: {mode}，有效模式: {valid_modes}")
            return

        self.performance_mode = mode

        # 根据模式调整组件设置
        if mode == "performance":
            # 性能优先：禁用扩展功能
            if self.pixel_sampler:
                self.pixel_sampler.set_performance_mode(extended_info=False, color_names=False)
            if self.position_calculator:
                self.position_calculator.set_update_threshold(100)  # 降低更新频率
            if self.theme_animation:
                self.theme_animation.set_animation_parameters(steps=8, duration=200)  # 简化动画

        elif mode == "quality":
            # 质量优先：启用所有功能
            if self.pixel_sampler:
                self.pixel_sampler.set_performance_mode(extended_info=True, color_names=True)
            if self.position_calculator:
                self.position_calculator.set_update_threshold(30)  # 提高更新频率
            if self.theme_animation:
                self.theme_animation.set_animation_parameters(steps=15, duration=500)  # 精细动画

        else:
            # 普通模式：平衡设置
            if self.pixel_sampler:
                self.pixel_sampler.set_performance_mode(extended_info=True, color_names=False)
            if self.position_calculator:
                self.position_calculator.set_update_threshold(50)
            if self.theme_animation:
                self.theme_animation.set_animation_parameters(steps=12, duration=350)

        print(f"性能模式已设置为: {mode}")

    def get_extended_color_info(self, canvas_x, canvas_y):
        """
        获取扩展颜色信息（用于调试或高级功能）

        Args:
            canvas_x, canvas_y: 画布坐标

        Returns:
            ColorInfo: 详细颜色信息或None
        """
        if not self.active or not self.pixel_sampler:
            return None

        img_x, img_y = self.coordinate_converter.canvas_to_image_pixel(canvas_x, canvas_y)
        if img_x is None or img_y is None:
            return None

        return self.pixel_sampler.get_extended_color_info(img_x, img_y)

    def get_statistics(self):
        """
        获取取色器统计信息

        Returns:
            dict: 统计信息
        """
        stats = self.stats.copy()

        # 添加组件级统计
        if self.position_calculator:
            stats.update(self.position_calculator.get_statistics())

        if self.pixel_sampler:
            stats['sample_history_count'] = len(self.pixel_sampler.get_sample_history())

        stats['active'] = self.active
        stats['performance_mode'] = self.performance_mode
        stats['initialized'] = self.initialized

        return stats

    def reset_statistics(self):
        """重置统计信息"""
        self.stats = {
            'total_samples': 0,
            'theme_changes': 0,
            'position_updates': 0,
            'animation_count': 0
        }
        print("统计信息已重置")

    def cleanup(self):
        """清理资源"""
        try:
            if self.active:
                self.deactivate()

            # 清理各组件
            if self.theme_animation:
                self.theme_animation.clear_color_cache()

            if self.coordinate_converter:
                self.coordinate_converter.invalidate_cache()

            print("取色器资源清理完成")

        except Exception as e:
            print(f"清理取色器资源时出错: {e}")

    def __del__(self):
        """析构函数"""
        self.cleanup()