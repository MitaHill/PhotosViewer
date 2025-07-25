#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
取色器二层调度组件
Color Sampling Dispatcher Component
"""

import sys
import os

# 修复导入路径问题
try:
    # 开发环境导入
    from sampling import SamplingManager
except ImportError:
    try:
        # PyInstaller 打包环境导入
        from .sampling import SamplingManager
    except ImportError:
        try:
            # 备用导入方式
            current_dir = os.path.dirname(os.path.abspath(__file__))
            sampling_dir = os.path.join(current_dir, 'sampling')
            if sampling_dir not in sys.path:
                sys.path.insert(0, sampling_dir)
            from sampling import SamplingManager
        except ImportError as e:
            print(f"无法导入 SamplingManager: {e}")
            # 创建一个空的占位类
            class SamplingManager:
                def __init__(self, parent):
                    self.parent = parent
                def initialize(self):
                    pass
                def activate(self):
                    return False
                def deactivate(self):
                    pass
                def update_from_mouse_motion(self, x, y):
                    pass


class SamplingMixin:
    """取色器功能混合类 - 二层调度器"""

    def setup_sampling_events(self):
        """设置取色器事件绑定"""
        # 初始化取色器管理器
        try:
            self.sampling_manager = SamplingManager(self)
            self.sampling_manager.initialize()
        except Exception as e:
            print(f"取色器初始化失败: {e}")
            return

        # 绑定键盘事件
        self._bind_sampling_keys()

        # 绑定鼠标事件
        self.canvas.bind('<Motion>', self._on_mouse_motion)

        # 确保窗口能接收键盘事件
        self.root.focus_set()

    def _bind_sampling_keys(self):
        """绑定取色器相关按键"""
        # 监听按键按下和释放
        self.root.bind('<KeyPress-Control_L>', self._on_ctrl_press)
        self.root.bind('<KeyPress-Control_R>', self._on_ctrl_press)
        self.root.bind('<KeyRelease-Control_L>', self._on_ctrl_release)
        self.root.bind('<KeyRelease-Control_R>', self._on_ctrl_release)

        self.root.bind('<KeyPress-Alt_L>', self._on_alt_press)
        self.root.bind('<KeyPress-Alt_R>', self._on_alt_press)
        self.root.bind('<KeyRelease-Alt_L>', self._on_alt_release)
        self.root.bind('<KeyRelease-Alt_R>', self._on_alt_release)

    def _on_ctrl_press(self, event):
        """Ctrl键按下"""
        self.ctrl_pressed = True
        self._check_sampling_activation()

    def _on_ctrl_release(self, event):
        """Ctrl键释放"""
        self.ctrl_pressed = False
        self._check_sampling_deactivation()

    def _on_alt_press(self, event):
        """Alt键按下"""
        self.alt_pressed = True
        self._check_sampling_activation()

    def _on_alt_release(self, event):
        """Alt键释放"""
        self.alt_pressed = False
        self._check_sampling_deactivation()

    def _check_sampling_activation(self):
        """检查是否激活取色器"""
        if self.ctrl_pressed and self.alt_pressed and not self.sampling_active:
            self._activate_sampling()

    def _check_sampling_deactivation(self):
        """检查是否停用取色器"""
        if not (self.ctrl_pressed and self.alt_pressed) and self.sampling_active:
            self._deactivate_sampling()

    def _activate_sampling(self):
        """激活取色器"""
        if not self.image_paths:
            return

        if hasattr(self, 'sampling_manager'):
            success = self.sampling_manager.activate()
            if success:
                self.sampling_active = True
                print("取色器已激活 (Ctrl+Alt)")

    def _deactivate_sampling(self):
        """停用取色器"""
        self.sampling_active = False
        if hasattr(self, 'sampling_manager'):
            self.sampling_manager.deactivate()
        print("取色器已停用")

    def _on_mouse_motion(self, event):
        """鼠标移动事件"""
        if not self.sampling_active or not hasattr(self, 'sampling_manager'):
            return

        # 委托给取色器管理器处理
        self.sampling_manager.update_from_mouse_motion(event.x, event.y)