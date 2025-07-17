#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
按钮和菜单管理功能模块
Button and Menu Management Module
"""

import tkinter as tk


class ButtonMixin:
    """按钮和菜单管理功能混合类"""

    def create_menu(self):
        """创建菜单栏"""
        self.menubar = tk.Menu(self.root)

        # 文件菜单
        file_menu = tk.Menu(self.menubar, tearoff=0)
        file_menu.add_command(label="打开", command=self.open_image)
        file_menu.add_command(label="重置缓存", command=self.reset_cache)
        file_menu.add_command(label="删除当前图片", command=self.delete_current_image)
        file_menu.add_command(label="复制图片路径到剪切板", command=self.copy_image_path_to_clipboard)
        file_menu.add_command(label="在目录中定位图片", command=self.locate_image_in_directory)
        file_menu.add_command(label="重命名当前图片", command=self.rename_current_image)
        file_menu.add_command(label="重载内存", command=self.reload_memory)
        file_menu.add_command(label="调整缓存占空闲内存配比", command=self.adjust_cache_ratio)
        file_menu.add_command(label="图片列表", command=self.show_image_list)

        # 播放控制菜单
        play_menu = tk.Menu(self.menubar, tearoff=0)
        play_menu.add_command(label="播放/暂停", command=self.toggle_playback)
        play_menu.add_command(label="停止", command=self.stop_playback)
        play_menu.add_command(label="自定义调节播放间隔", command=self.custom_playback_interval)

        # 图片菜单
        image_menu = tk.Menu(self.menubar, tearoff=0)
        image_menu.add_command(label="图片详细信息", command=self.show_image_info)

        # 旋转子菜单
        rotate_menu = tk.Menu(image_menu, tearoff=0)
        rotate_menu.add_command(label="逆时针旋转90°", command=self.rotate_ccw_90)
        rotate_menu.add_command(label="逆时针旋转180°", command=self.rotate_ccw_180)
        rotate_menu.add_command(label="顺时针旋转90°", command=self.rotate_cw_90)
        rotate_menu.add_command(label="顺时针旋转180°", command=self.rotate_cw_180)
        rotate_menu.add_command(label="自定义旋转", command=self.custom_rotate)
        image_menu.add_cascade(label="旋转", menu=rotate_menu)

        # 翻转子菜单
        flip_menu = tk.Menu(image_menu, tearoff=0)
        flip_menu.add_command(label="水平翻转", command=self.flip_horizontal)
        flip_menu.add_command(label="垂直翻转", command=self.flip_vertical)
        image_menu.add_cascade(label="翻转", menu=flip_menu)

        # 帮助菜单
        help_menu = tk.Menu(self.menubar, tearoff=0)
        help_menu.add_command(label="关于本项目", command=self.show_about)
        help_menu.add_command(label="归属", command=self.show_attribution)
        help_menu.add_command(label="其它项目", command=self.show_other_project)

        # 添加到菜单栏
        self.menubar.add_cascade(label="文件", menu=file_menu)
        self.menubar.add_command(label="上一张", command=lambda: self.navigate("prev"))
        self.menubar.add_command(label="下一张", command=lambda: self.navigate("next"))
        self.menubar.add_cascade(label="播放控制", menu=play_menu)
        self.menubar.add_cascade(label="图片", menu=image_menu)
        self.menubar.add_cascade(label="帮助", menu=help_menu)

        self.root.config(menu=self.menubar)

    def open_image(self):
        """打开图片文件"""
        from tkinter import filedialog

        file_types = [
            ("图片文件", "*.jpg;*.jpeg;*.png;*.bmp;*.gif;*.webp;*.tiff"),
            ("所有文件", "*.*")
        ]
        file_path = filedialog.askopenfilename(filetypes=file_types)
        if not file_path:
            return

        import os
        file_path = os.path.normpath(file_path)
        directory = os.path.dirname(file_path)

        if directory == self.last_directory and self.image_paths:
            try:
                self.current_index = self.image_paths.index(file_path)
            except ValueError:
                self.current_index = 0
            self.show_current_image()
        else:
            self.last_directory = directory
            self.load_directory_images(directory)
            try:
                self.current_index = self.image_paths.index(file_path)
            except ValueError:
                self.current_index = 0
            self.show_current_image()