#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
配置管理模块
Configuration Management Module
"""

import os
import json
import threading


class ConfigManager:
    """配置管理器 - 负责读取和保存程序配置"""

    def __init__(self):
        """初始化配置管理器"""
        self.config_dir = os.path.join(os.path.dirname(__file__), 'config')
        self.config_file = os.path.join(self.config_dir, 'data.json')
        self.lock = threading.Lock()

        # 防重复保存
        self.save_pending = False
        self.last_save_time = 0
        self.save_delay = 500  # 500ms延迟合并保存

        # 默认配置
        self.default_config = {
            'cache_ratio': 0.4,
            'window_mode': 'dynamic',  # 'dynamic' 或 'fixed'
            'fixed_window_size': [800, 600],
            'last_window_size': [1024, 768]
        }

        self.config = self.default_config.copy()
        self._ensure_config_dir()
        self.load_config()

    def _ensure_config_dir(self):
        """确保配置目录存在"""
        try:
            if not os.path.exists(self.config_dir):
                os.makedirs(self.config_dir, exist_ok=True)
        except Exception as e:
            print(f"创建配置目录失败: {e}")

    def load_config(self):
        """从文件加载配置"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    loaded_config = json.load(f)

                # 合并配置（保留默认值）
                for key, value in loaded_config.items():
                    if key in self.default_config:
                        self.config[key] = value

                # 静默加载，不输出信息
            else:
                # 静默创建默认配置文件
                self.save_config(silent=True)
        except Exception as e:
            # 只在出错时输出
            print(f"加载配置失败: {e}")
            self.config = self.default_config.copy()

    def save_config(self, silent=True):
        """保存配置到文件"""
        try:
            with self.lock:
                self._ensure_config_dir()
                with open(self.config_file, 'w', encoding='utf-8') as f:
                    json.dump(self.config, f, indent=4, ensure_ascii=False)
                # 默认静默保存
                if not silent:
                    print(f"配置已保存: {self.config_file}")
        except Exception as e:
            print(f"保存配置失败: {e}")

    def get(self, key, default=None):
        """获取配置值"""
        return self.config.get(key, default)

    def set(self, key, value, auto_save=True):
        """设置配置值"""
        if self.config.get(key) != value:
            self.config[key] = value
            if auto_save:
                self.save_async_debounced()

    def save_async(self, silent=True):
        """异步保存配置"""
        threading.Thread(target=lambda: self.save_config(silent), daemon=True).start()

    def save_async_debounced(self):
        """防抖异步保存配置"""
        import time
        current_time = time.time() * 1000

        if not self.save_pending:
            self.save_pending = True
            self.last_save_time = current_time

            def delayed_save():
                time.sleep(self.save_delay / 1000)
                if self.save_pending and time.time() * 1000 - self.last_save_time >= self.save_delay:
                    self.save_pending = False
                    self.save_config(silent=True)  # 防抖保存永远静默

            threading.Thread(target=delayed_save, daemon=True).start()
        else:
            self.last_save_time = current_time

    # 便捷方法
    def get_cache_ratio(self):
        """获取缓存比例"""
        return self.get('cache_ratio', 0.4)

    def set_cache_ratio(self, ratio):
        """设置缓存比例"""
        self.set('cache_ratio', ratio, auto_save=False)
        self.save_async(silent=True)  # 彻底静默

    def get_window_mode(self):
        """获取窗口模式"""
        return self.get('window_mode', 'dynamic')

    def set_window_mode(self, mode):
        """设置窗口模式"""
        self.set('window_mode', mode, auto_save=False)
        self.save_async(silent=True)  # 彻底静默

    def get_fixed_window_size(self):
        """获取固定窗口尺寸"""
        size = self.get('fixed_window_size', [800, 600])
        return tuple(size) if isinstance(size, list) else size

    def set_fixed_window_size(self, width, height):
        """设置固定窗口尺寸"""
        self.set('fixed_window_size', [width, height])

    def get_last_window_size(self):
        """获取上次窗口尺寸"""
        size = self.get('last_window_size', [1024, 768])
        return tuple(size) if isinstance(size, list) else size

    def set_last_window_size(self, width, height):
        """设置上次窗口尺寸"""
        self.set('last_window_size', [width, height])

    def get_config_dict(self):
        """获取完整配置字典"""
        return self.config.copy()

    def reset_to_default(self):
        """重置为默认配置"""
        self.config = self.default_config.copy()
        self.save_config()
        print("配置已重置为默认值")


class ConfigMixin:
    """配置管理混合类"""

    def _init_config_manager(self):
        """初始化配置管理器"""
        self.config_manager = ConfigManager()

        # 应用保存的配置
        self._apply_saved_config()

    def _apply_saved_config(self):
        """应用保存的配置"""
        # 应用缓存比例
        self.cache_ratio = self.config_manager.get_cache_ratio()

        # 应用窗口模式
        window_mode = self.config_manager.get_window_mode()
        if window_mode == 'fixed':
            self.window_size_fixed = True
            self.fixed_window_size = self.config_manager.get_fixed_window_size()
        else:
            self.window_size_fixed = False

        print(f"已应用配置: 缓存比例={self.cache_ratio:.2f}, 窗口模式={window_mode}")

    def save_cache_ratio_config(self, ratio):
        """保存缓存比例配置"""
        self.config_manager.set_cache_ratio(ratio)

    def save_window_mode_config(self, mode):
        """保存窗口模式配置"""
        self.config_manager.set_window_mode(mode)

    def save_window_size_config(self, width, height):
        """保存窗口尺寸配置"""
        if self.window_size_fixed:
            self.config_manager.set_fixed_window_size(width, height)
        else:
            self.config_manager.set_last_window_size(width, height)

    def get_config_info(self):
        """获取配置信息"""
        return {
            'config_file': self.config_manager.config_file,
            'cache_ratio': self.config_manager.get_cache_ratio(),
            'window_mode': self.config_manager.get_window_mode(),
            'fixed_window_size': self.config_manager.get_fixed_window_size(),
            'last_window_size': self.config_manager.get_last_window_size()
        }