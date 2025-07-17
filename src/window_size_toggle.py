#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
窗口大小固定切换功能模块 - 增强版
Window Size Toggle Functionality Module - Enhanced
"""

import tkinter as tk
from tkinter import messagebox
import time


class WindowSizeToggleMixin:
    """窗口大小固定切换功能混合类"""

    def _init_window_size_toggle_variables(self):
        """初始化窗口大小切换功能变量"""
        # 窗口大小固定状态
        self.window_size_fixed = False
        self.fixed_window_size = (800, 600)  # 默认固定尺寸
        self.last_dynamic_size = None  # 保存切换前的动态尺寸

        # 窗口尺寸监控
        self.last_window_check_time = 0
        self.window_size_check_interval = 200  # 200ms间隔
        self.monitoring_window_size = False
        self.size_monitor_id = None

    def setup_window_size_toggle(self):
        """设置窗口大小切换功能"""
        # 绑定快捷键 Alt+X
        self.root.bind('<Alt-x>', self.toggle_window_size_mode)
        self.root.bind('<Alt-X>', self.toggle_window_size_mode)

        # 开始监控窗口尺寸变化
        self.start_window_size_monitoring()

        print("窗口大小切换功能已启用 (Alt+X)")

    def start_window_size_monitoring(self):
        """开始监控窗口尺寸变化"""
        self.monitoring_window_size = True
        self._monitor_window_size()

    def _monitor_window_size(self):
        """监控窗口尺寸变化"""
        if not self.monitoring_window_size:
            return

        current_time = time.time() * 1000  # 转为毫秒

        if current_time - self.last_window_check_time >= self.window_size_check_interval:
            try:
                current_width = self.root.winfo_width()
                current_height = self.root.winfo_height()

                # 更新配置中的窗口尺寸
                if hasattr(self, 'config_manager'):
                    if self.window_size_fixed:
                        # 固定模式下更新固定尺寸
                        old_size = self.config_manager.get_fixed_window_size()
                        if old_size != (current_width, current_height):
                            self.fixed_window_size = (current_width, current_height)
                            self.config_manager.set_fixed_window_size(current_width, current_height)
                    else:
                        # 动态模式下记录当前尺寸
                        self.config_manager.set_last_window_size(current_width, current_height)

                self.last_window_check_time = current_time
            except Exception as e:
                pass  # 忽略窗口未准备好的错误

        # 调度下次检查
        self.size_monitor_id = self.root.after(50, self._monitor_window_size)

    def stop_window_size_monitoring(self):
        """停止监控窗口尺寸变化"""
        self.monitoring_window_size = False
        if self.size_monitor_id:
            self.root.after_cancel(self.size_monitor_id)
            self.size_monitor_id = None

    def toggle_window_size_mode(self, event=None):
        """切换窗口大小模式：固定 <-> 动态（Alt+X直接切换）"""
        if self.window_size_fixed:
            self._enable_dynamic_window()
        else:
            self._enable_fixed_window()

        return "break"

    def show_quick_toggle_dialog(self):
        """显示快速切换对话框（菜单按钮使用）"""
        dialog = tk.Toplevel(self.root)
        dialog.title("窗口模式切换")
        dialog.geometry("280x160")
        dialog.transient(self.root)
        dialog.grab_set()
        dialog.resizable(False, False)

        # 当前状态显示
        current_mode = "固定窗口" if self.window_size_fixed else "动态变化"
        current_size = f"{self.root.winfo_width()}x{self.root.winfo_height()}"

        status_frame = tk.Frame(dialog)
        status_frame.pack(pady=15)

        tk.Label(status_frame, text="当前状态:", font=('Arial', 10, 'bold')).pack()
        tk.Label(status_frame, text=f"{current_mode} ({current_size})",
                 fg="blue", font=('Arial', 10)).pack(pady=5)

        # 选择按钮
        button_frame = tk.Frame(dialog)
        button_frame.pack(pady=10)

        def set_fixed():
            if not self.window_size_fixed:
                self._enable_fixed_window()
            dialog.destroy()

        def set_dynamic():
            if self.window_size_fixed:
                self._enable_dynamic_window()
            dialog.destroy()

        # 固定窗口按钮
        fixed_btn = tk.Button(button_frame, text="固定窗口",
                              command=set_fixed, width=10)
        fixed_btn.pack(side=tk.LEFT, padx=5)

        # 动态变化按钮
        dynamic_btn = tk.Button(button_frame, text="动态变化",
                                command=set_dynamic, width=10)
        dynamic_btn.pack(side=tk.LEFT, padx=5)

        # 根据当前模式设置按钮状态
        if self.window_size_fixed:
            fixed_btn.config(relief=tk.SUNKEN, bg="#e0e0e0")
            dynamic_btn.config(relief=tk.RAISED)
        else:
            dynamic_btn.config(relief=tk.SUNKEN, bg="#e0e0e0")
            fixed_btn.config(relief=tk.RAISED)

        # 提示信息
        tip_frame = tk.Frame(dialog)
        tip_frame.pack(pady=5)
        tk.Label(tip_frame, text="提示: Alt+X 可直接快速切换",
                 fg="gray", font=('Arial', 8)).pack()

    def show_window_mode_dialog(self):
        """显示窗口模式切换对话框"""
        dialog = tk.Toplevel(self.root)
        dialog.title("窗口模式设置")
        dialog.geometry("380x320")
        dialog.transient(self.root)
        dialog.grab_set()
        dialog.resizable(False, False)
        dialog.configure(bg='#f5f5f5')

        # 标题
        tk.Label(dialog, text="窗口模式设置", font=('Arial', 14, 'bold'),
                 bg='#f5f5f5').pack(pady=15)

        # 当前状态
        status_frame = tk.LabelFrame(dialog, text="当前状态", font=('Arial', 10, 'bold'),
                                     bg='#f5f5f5', fg='#333333')
        status_frame.pack(fill=tk.X, padx=20, pady=10)

        current_mode = "固定模式" if self.window_size_fixed else "动态模式"
        current_size = f"{self.root.winfo_width()} × {self.root.winfo_height()}"
        fixed_size = f"{self.fixed_window_size[0]} × {self.fixed_window_size[1]}"

        tk.Label(status_frame, text=f"模式: {current_mode}", font=('Arial', 10),
                 bg='#f5f5f5', fg='#0066cc').pack(anchor=tk.W, padx=10, pady=2)
        tk.Label(status_frame, text=f"当前尺寸: {current_size}", font=('Arial', 9),
                 bg='#f5f5f5').pack(anchor=tk.W, padx=10, pady=1)
        tk.Label(status_frame, text=f"固定尺寸: {fixed_size}", font=('Arial', 9),
                 bg='#f5f5f5').pack(anchor=tk.W, padx=10, pady=(1, 8))

        # 按钮区域
        button_frame = tk.Frame(dialog, bg='#f5f5f5')
        button_frame.pack(pady=15)

        def enable_dynamic():
            self._enable_dynamic_window()
            dialog.destroy()

        def enable_fixed():
            self._enable_fixed_window()
            dialog.destroy()

        def configure_fixed():
            dialog.withdraw()
            self.configure_fixed_window_dialog()
            dialog.destroy()

        # 按钮样式
        btn_config = {'font': ('Arial', 10), 'width': 12, 'height': 2}

        # 动态按钮
        dynamic_btn = tk.Button(button_frame, text="开启动态窗口",
                                command=enable_dynamic, **btn_config)
        if not self.window_size_fixed:
            dynamic_btn.config(bg='#4CAF50', fg='white', relief=tk.SUNKEN)
        else:
            dynamic_btn.config(bg='#e8e8e8', fg='#333333')
        dynamic_btn.pack(side=tk.LEFT, padx=5)

        # 固定按钮
        fixed_btn = tk.Button(button_frame, text="关闭动态窗口",
                              command=enable_fixed, **btn_config)
        if self.window_size_fixed:
            fixed_btn.config(bg='#FF9800', fg='white', relief=tk.SUNKEN)
        else:
            fixed_btn.config(bg='#e8e8e8', fg='#333333')
        fixed_btn.pack(side=tk.LEFT, padx=5)

        # 配置按钮
        config_btn = tk.Button(button_frame, text="配置固定尺寸",
                               command=configure_fixed, **btn_config)
        config_btn.config(bg='#2196F3', fg='white')
        config_btn.pack(side=tk.LEFT, padx=5)

        # 底部提示
        tk.Label(dialog, text="💡 提示: 按 Alt+X 可快速切换模式",
                 font=('Arial', 9), bg='#f5f5f5', fg='#666666').pack(pady=10)

        tk.Button(dialog, text="关闭", command=dialog.destroy,
                  font=('Arial', 9), width=8, bg='#f0f0f0').pack(pady=5)

    def _enable_fixed_window(self):
        """启用固定窗口模式"""
        # 记录当前尺寸作为固定尺寸
        current_width = self.root.winfo_width()
        current_height = self.root.winfo_height()

        # 保存当前动态尺寸
        self.last_dynamic_size = (current_width, current_height)

        # 设置为固定模式
        self.window_size_fixed = True
        self.fixed_window_size = (current_width, current_height)

        # 禁用窗口大小调整
        self.root.resizable(False, False)

        # 保存配置
        if hasattr(self, 'config_manager'):
            self.config_manager.set_window_mode('fixed')
            self.config_manager.set_fixed_window_size(current_width, current_height)

        print(f"窗口已固定为当前尺寸: {current_width}x{current_height}")

    def _enable_dynamic_window(self):
        """启用动态窗口模式"""
        # 设置为动态模式
        self.window_size_fixed = False

        # 启用窗口大小调整
        self.root.resizable(True, True)

        # 保存配置
        if hasattr(self, 'config_manager'):
            self.config_manager.set_window_mode('dynamic')

        # 如果当前有图片，重新调整窗口大小
        if self.image_paths and hasattr(self, 'image_cache'):
            current_path = self.image_paths[self.current_index]
            img_data = self.image_cache.get(current_path)
            if img_data:
                img, _ = img_data
                self.adjust_window_size_override(img)

        print("窗口已切换为动态模式")

    def set_fixed_window_size(self, width, height):
        """设置固定窗口的尺寸"""
        self.fixed_window_size = (width, height)

        # 保存到配置
        if hasattr(self, 'config_manager'):
            self.config_manager.set_fixed_window_size(width, height)

        # 如果当前是固定模式，立即应用新尺寸
        if self.window_size_fixed:
            self.root.geometry(f"{width}x{height}")
            print(f"固定窗口尺寸已更新为: {width}x{height}")

    def get_window_size_status(self):
        """获取当前窗口大小模式状态"""
        return {
            'fixed': self.window_size_fixed,
            'fixed_size': self.fixed_window_size,
            'current_size': (self.root.winfo_width(), self.root.winfo_height()),
            'last_dynamic_size': self.last_dynamic_size
        }

    def adjust_window_size_override(self, img):
        """重写原有的调整窗口大小方法，在固定模式下跳过调整"""
        # 如果窗口大小被固定，跳过调整
        if self.window_size_fixed:
            return

        # 调用WindowMixin的窗口大小调整方法
        from .window import WindowMixin
        WindowMixin.adjust_window_size(self, img)

    def configure_fixed_window_dialog(self):
        """打开配置固定窗口尺寸的对话框"""
        dialog = tk.Toplevel(self.root)
        dialog.title("配置固定窗口尺寸")
        dialog.geometry("350x250")
        dialog.transient(self.root)
        dialog.grab_set()
        dialog.resizable(False, False)

        # 当前固定尺寸显示
        current_width, current_height = self.fixed_window_size
        current_actual_width = self.root.winfo_width()
        current_actual_height = self.root.winfo_height()

        # 信息显示
        info_frame = tk.Frame(dialog)
        info_frame.pack(pady=10, padx=20, fill=tk.X)

        tk.Label(info_frame, text="当前窗口尺寸:", font=('Arial', 10, 'bold')).pack(anchor=tk.W)
        tk.Label(info_frame, text=f"{current_actual_width} x {current_actual_height}").pack(anchor=tk.W)

        tk.Label(info_frame, text="固定模式尺寸:", font=('Arial', 10, 'bold')).pack(anchor=tk.W, pady=(10, 0))
        tk.Label(info_frame, text=f"{current_width} x {current_height}").pack(anchor=tk.W)

        # 输入框架
        input_frame = tk.Frame(dialog)
        input_frame.pack(pady=15, padx=20)

        # 宽度输入
        tk.Label(input_frame, text="新的固定尺寸:").pack(anchor=tk.W)
        size_frame = tk.Frame(input_frame)
        size_frame.pack(fill=tk.X, pady=5)

        tk.Label(size_frame, text="宽度:").pack(side=tk.LEFT)
        width_entry = tk.Entry(size_frame, width=8)
        width_entry.insert(0, str(current_width))
        width_entry.pack(side=tk.LEFT, padx=(5, 10))

        tk.Label(size_frame, text="高度:").pack(side=tk.LEFT)
        height_entry = tk.Entry(size_frame, width=8)
        height_entry.insert(0, str(current_height))
        height_entry.pack(side=tk.LEFT, padx=5)

        # 快捷按钮
        quick_frame = tk.Frame(input_frame)
        quick_frame.pack(fill=tk.X, pady=10)

        def use_current_size():
            width_entry.delete(0, tk.END)
            height_entry.delete(0, tk.END)
            width_entry.insert(0, str(current_actual_width))
            height_entry.insert(0, str(current_actual_height))

        tk.Button(quick_frame, text="使用当前窗口尺寸",
                  command=use_current_size, height=2,
                  font=('Arial', 10)).pack()

        # 状态显示
        status_text = "当前模式: " + ("固定" if self.window_size_fixed else "动态")
        status_label = tk.Label(dialog, text=status_text, fg="blue")
        status_label.pack(pady=5)

        def apply_settings():
            try:
                width = int(width_entry.get())
                height = int(height_entry.get())

                if width < 300 or height < 200:
                    messagebox.showerror("错误", "窗口尺寸不能小于 300x200")
                    return

                if width > 2000 or height > 1500:
                    messagebox.showerror("错误", "窗口尺寸不能大于 2000x1500")
                    return

                self.set_fixed_window_size(width, height)
                dialog.destroy()

            except ValueError:
                messagebox.showerror("错误", "请输入有效的数字")

        # 按钮框架
        button_frame = tk.Frame(dialog)
        button_frame.pack(pady=15)

        tk.Button(button_frame, text="应用", command=apply_settings).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="取消", command=dialog.destroy).pack(side=tk.LEFT, padx=5)

        # 绑定回车键
        dialog.bind('<Return>', lambda e: apply_settings())
        width_entry.focus_set()

    def cleanup_window_monitoring(self):
        """清理窗口监控"""
        self.stop_window_size_monitoring()