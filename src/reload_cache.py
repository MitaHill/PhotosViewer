#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
缓存重载功能模块
Cache Reload Functionality Module
"""


class ReloadCacheMixin:
    """缓存重载功能混合类"""

    def reload_memory(self):
        """重载内存缓存"""
        if not self.image_paths or not self.last_directory:
            print("当前没有加载任何图片或目录")
            return

        # 清空当前缓存
        self.release_all_images()
        print("正在重载内存...")

        # 重新加载目录中的图片
        self.load_directory_images(self.last_directory)
        self.show_current_image()
        print(f"内存重载完成，当前缓存大小: {self.format_memory(self.current_cache_size)}")