#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
图片查看器模块初始化文件
Image Viewer Module Initialization
Version: 2.9
"""

import os
import sys
import glob
import concurrent.futures
import math
import signal
import queue
import re
import subprocess
import threading
import time
import io
from PIL import Image, ImageTk
from collections import OrderedDict, Counter
import tkinter as tk
from tkinter import END, filedialog, ttk, messagebox
import psutil
from tkinterdnd2 import *

# 尝试导入Windows特定模块
try:
    import win32clipboard
except ImportError:
    win32clipboard = None

# 导入各个功能模块
from .status_bar import StatusBarOutput
from .reset_cache import ResetCacheMixin
from .delete_photo import DeletePhotoMixin
from .copy_path import CopyPathMixin
from .position_photo import PositionPhotoMixin
from .rename_photo import RenamePhotoMixin
from .reload_cache import ReloadCacheMixin
from .change_cache import ChangeCacheMixin
from .photos_list import PhotosListMixin
from .switch_previous_or_next import NavigationMixin
from .play import PlaybackMixin
from .images_info import ImageInfoMixin
from .images_rotation import RotationMixin
from .images_flip import FlipMixin
from .help import HelpMixin
from .drag import DragMixin
from .zoom import ZoomMixin
from .animation import AnimationMixin
from .change_border_color import BorderColorMixin
from .window import WindowMixin
from .button import ButtonMixin
from .dialog import DialogMixin
# 新增的功能模块
from .shortcut_key import ShortcutKeyMixin
from .copy_images_body import CopyImageBodyMixin
from .sampling_mixin import SamplingMixin


class ImageViewer(
    ResetCacheMixin,
    DeletePhotoMixin,
    CopyPathMixin,
    PositionPhotoMixin,
    RenamePhotoMixin,
    ReloadCacheMixin,
    ChangeCacheMixin,
    PhotosListMixin,
    NavigationMixin,
    PlaybackMixin,
    ImageInfoMixin,
    RotationMixin,
    FlipMixin,
    HelpMixin,
    DragMixin,
    ZoomMixin,
    AnimationMixin,
    BorderColorMixin,
    WindowMixin,
    ButtonMixin,
    DialogMixin,
    # 新增的功能混合类
    ShortcutKeyMixin,
    CopyImageBodyMixin,
    SamplingMixin
):
    """
    图片查看器主类
    继承所有功能模块的混合类
    """

    def __init__(self, root, initial_image=None):
        """
        图片查看器初始化方法

        Args:
            root: Tkinter根窗口
            initial_image: 可选，初始加载的图片路径
        """
        self.root = root
        self.root.title("图片查看器")

        # 初始化所有变量
        self._init_variables()

        # 创建UI组件
        self._create_ui()

        # 绑定事件处理
        self._bind_events()

        # 设置快捷键
        self.setup_shortcuts()

        # 更新内存限制并完成初始化
        self.update_memory_limit()
        self.beready()

        # 启动对话框监控
        self._setup_dialog_monitoring()

        # 加载初始图片（如果提供）
        if initial_image:
            self.load_initial_image(initial_image)

    def _init_variables(self):
        """初始化所有实例变量"""
        # 图片和显示相关
        self.image_paths = []
        self.current_index = 0
        self.zoom_factor = 1.0
        self.last_directory = None

        # 视口设置
        self.viewport_x = 0
        self.viewport_y = 0
        self.viewport_width = 0
        self.viewport_height = 0

        # 拖动相关
        self.dragging = False
        self.drag_start_x = 0
        self.drag_start_y = 0

        # 播放控制
        self.is_playing = False
        self.playback_id = None
        self.playback_interval = 1
        self.auto_press = False

        # 内存管理
        self.cache_ratio = 0.4
        self.cache_size_limit = 0
        self.current_cache_size = 0
        self.image_cache = {}
        self.lru_list = OrderedDict()

        # 导航控制
        self.navigate_delay = 50
        self.speed_boost = 0.5
        self.min_delay = 100
        self.max_delay = 500
        self.repeat_id = None

        # 加载状态
        self.loading_active = False
        self.resize_timer = None

        # 对话框监控
        self.dialog_positions = {}
        self.excluded_dialogs = set()
        self.running = True
        self.closing = False

        # 状态栏相关
        self.status_lines = []

        # 完全禁用PIL图片大小限制
        Image.MAX_IMAGE_PIXELS = None

        # 用于存储预计算的帧
        self.frame_queue = queue.Queue()

        # 键盘线程
        self.key_queue = queue.Queue()
        self.key_thread_running = True
        self.key_state = {"Left": False, "Right": False}

        # Windows剪切板支持
        self.win32clipboard = win32clipboard

        # 取色器相关变量
        self.sampling_active = False
        self.sampling_manager = None
        self.ctrl_pressed = False
        self.alt_pressed = False

    def _create_ui(self):
        """创建所有UI组件"""
        # 创建菜单栏
        self.create_menu()

        # 创建主画布
        self.canvas = tk.Canvas(
            self.root,
            bg='#333333',
            highlightthickness=0
        )
        self.canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # 创建状态栏
        self.status_bar = tk.Text(
            self.root,
            height=1,
            wrap=tk.WORD,
            bg="#f0f0f0",
            relief=tk.SUNKEN
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X, padx=5, pady=5)
        self.status_bar.config(state=tk.DISABLED)

        # 重定向标准输出到状态栏
        sys.stdout = StatusBarOutput(self.status_bar, self.status_lines, enable_console=True)

        # 添加拖放支持
        self.root.drop_target_register(DND_FILES)

    def _bind_events(self):
        """绑定所有事件处理函数"""
        # 画布事件
        self.canvas.bind('<ButtonPress-1>', self.on_drag_start)
        self.canvas.bind('<B1-Motion>', self.on_drag)
        self.canvas.bind('<ButtonRelease-1>', self.on_drag_end)
        self.canvas.bind('<MouseWheel>', self.on_mousewheel)

        # 窗口事件
        self.root.bind('<Configure>', self.on_resize)
        self.root.bind('<Left>', lambda e: "break")
        self.root.bind('<Right>', lambda e: "break")
        self.root.bind('<space>', self.toggle_playback)

        # 保留原有的快捷键绑定（将被新的快捷键系统覆盖）
        self.root.bind('<F2>', self.rename_current_image)

        # 拖放事件
        self.root.dnd_bind('<<Drop>>', self.handle_drop)

        # 关闭事件
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        signal.signal(signal.SIGINT, self.signal_handler)

    def _setup_dialog_monitoring(self):
        """设置对话框监控线程"""
        self.dialog_monitor_thread = threading.Thread(
            target=self.monitor_dialogs,
            daemon=True
        )
        self.dialog_monitor_thread.start()

    def beready(self):
        """初始化完成标志"""
        print("准备就绪")
        # 显示剪切板支持信息
        clipboard_info = self.get_clipboard_image_support_info()
        print(f"剪切板支持: {clipboard_info}")

    def update_memory_limit(self):
        """更新内存限制"""
        virtual_memory = psutil.virtual_memory()
        self.cache_size_limit = int(virtual_memory.available * self.cache_ratio)

    def load_initial_image(self, initial_image):
        """加载初始图片"""
        directory = os.path.dirname(initial_image)
        self.load_directory_images(directory)
        try:
            self.current_index = self.image_paths.index(initial_image)
        except ValueError:
            self.current_index = 0
        self.show_current_image()

    def on_closing(self):
        """处理关闭按钮事件"""
        if not self.closing:
            self.root.title("图片查看器 - 关闭中")
            self.closing = True
            threading.Thread(target=self.shutdown, daemon=True).start()

    def signal_handler(self, signum, frame):
        """处理键盘中断"""
        if not self.closing:
            self.root.title("图片查看器 - 关闭中")
            self.closing = True
            threading.Thread(target=self.shutdown, daemon=True).start()

    def shutdown(self):
        """线程中执行关闭操作"""
        print("正在释放内存并关闭程序...")
        self.running = False
        self.key_thread_running = False

        # 停用取色器
        if self.sampling_active:
            self._deactivate_sampling()

        # 等待对话框监控线程结束
        if self.dialog_monitor_thread.is_alive():
            self.dialog_monitor_thread.join(timeout=1.0)

        # 释放图片缓存
        self.release_all_images()

        # 关闭所有对话框
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Toplevel) and widget.winfo_exists():
                try:
                    widget.destroy()
                except Exception as e:
                    print(f"关闭对话框时出错: {e}")

        # 销毁主窗口并退出
        try:
            self.root.quit()
            self.root.destroy()
        except Exception as e:
            print(f"销毁主窗口时出错: {e}")
        finally:
            sys.exit(0)


# 导出主类
__all__ = ['ImageViewer', 'StatusBarOutput']