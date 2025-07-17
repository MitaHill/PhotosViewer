#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
缓存重置功能模块
Cache Reset Functionality Module
"""


class ResetCacheMixin:
    """缓存重置功能混合类"""

    def reset_cache(self):
        """
        重置所有图片缓存，释放内存
        当发现内存占用过高或缓存可能存在问题时可调用此方法
        """
        # 检查是否有加载的图片
        if not self.image_paths:
            return

        # 清理所有缓存的图片资源
        self.release_all_images()
        print("缓存已重置")

        # 重新加载当前图片
        self.show_current_image()

    def release_all_images(self):
        """释放所有图片缓存"""
        for path in list(self.image_cache.keys()):
            img, size = self.image_cache.pop(path)
            img.close()
        self.lru_list.clear()
        self.current_cache_size = 0
        self.canvas.delete("all")
        self.canvas.image = None

    def remove_oldest_image(self):
        """移除最旧的图片缓存"""
        if self.lru_list:
            oldest_path = next(iter(self.lru_list))
            if oldest_path in self.image_cache:
                img, size = self.image_cache.pop(oldest_path)
                img.close()
                del self.lru_list[oldest_path]
                self.current_cache_size -= size

    @staticmethod
    def format_memory(size):
        """格式化内存大小显示"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024:
                return f"{size:.1f} {unit}"
            size /= 1024
        return f"{size:.1f} GB"