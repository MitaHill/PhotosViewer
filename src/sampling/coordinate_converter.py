#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
坐标转换组件
Coordinate Conversion Component
"""


class CoordinateConverter:
    """画布坐标与图像像素坐标转换器"""

    def __init__(self, parent):
        """
        初始化坐标转换器

        Args:
            parent: 父对象（ImageViewer实例）
        """
        self.parent = parent

        # 缓存计算结果以提高性能
        self._cached_canvas_size = (0, 0)
        self._cached_display_params = None
        self._cache_valid = False

    def canvas_to_image_pixel(self, canvas_x, canvas_y):
        """
        将画布坐标转换为图像像素坐标

        Args:
            canvas_x: 画布X坐标
            canvas_y: 画布Y坐标

        Returns:
            tuple: 图像像素坐标 (img_x, img_y) 或 (None, None)
        """
        if not self.parent.image_paths:
            return None, None

        current_path = self.parent.image_paths[self.parent.current_index]
        img_data = self.parent.image_cache.get(current_path)
        if not img_data:
            return None, None

        img, _ = img_data

        # 获取显示参数
        display_params = self._get_display_parameters()
        if not display_params:
            return None, None

        window_width, window_height, display_width, display_height, img_left, img_top = display_params

        # 检查鼠标是否在图像显示区域内
        if not self._is_point_in_image_area(canvas_x, canvas_y, img_left, img_top, display_width, display_height):
            return None, None

        # 转换为相对坐标 (0.0 - 1.0)
        rel_x = (canvas_x - img_left) / display_width
        rel_y = (canvas_y - img_top) / display_height

        # 转换为图像像素坐标
        img_x = self.parent.viewport_x + rel_x * self.parent.viewport_width
        img_y = self.parent.viewport_y + rel_y * self.parent.viewport_height

        # 确保坐标在图像范围内
        if not self._is_pixel_in_image_bounds(img_x, img_y, img.width, img.height):
            return None, None

        return img_x, img_y

    def image_pixel_to_canvas(self, img_x, img_y):
        """
        将图像像素坐标转换为画布坐标

        Args:
            img_x: 图像X坐标
            img_y: 图像Y坐标

        Returns:
            tuple: 画布坐标 (canvas_x, canvas_y) 或 (None, None)
        """
        if not self.parent.image_paths:
            return None, None

        current_path = self.parent.image_paths[self.parent.current_index]
        img_data = self.parent.image_cache.get(current_path)
        if not img_data:
            return None, None

        img, _ = img_data

        # 检查像素是否在图像范围内
        if not self._is_pixel_in_image_bounds(img_x, img_y, img.width, img.height):
            return None, None

        # 获取显示参数
        display_params = self._get_display_parameters()
        if not display_params:
            return None, None

        window_width, window_height, display_width, display_height, img_left, img_top = display_params

        # 转换为相对坐标
        rel_x = (img_x - self.parent.viewport_x) / self.parent.viewport_width
        rel_y = (img_y - self.parent.viewport_y) / self.parent.viewport_height

        # 转换为画布坐标
        canvas_x = img_left + rel_x * display_width
        canvas_y = img_top + rel_y * display_height

        return canvas_x, canvas_y

    def get_visible_image_bounds(self):
        """
        获取当前可见图像区域的边界

        Returns:
            dict: 包含边界信息的字典或None
        """
        display_params = self._get_display_parameters()
        if not display_params:
            return None

        window_width, window_height, display_width, display_height, img_left, img_top = display_params

        return {
            'canvas_left': img_left,
            'canvas_top': img_top,
            'canvas_right': img_left + display_width,
            'canvas_bottom': img_top + display_height,
            'display_width': display_width,
            'display_height': display_height,
            'viewport_x': self.parent.viewport_x,
            'viewport_y': self.parent.viewport_y,
            'viewport_width': self.parent.viewport_width,
            'viewport_height': self.parent.viewport_height
        }

    def _get_display_parameters(self):
        """
        获取当前图像显示参数

        Returns:
            tuple: (window_width, window_height, display_width, display_height, img_left, img_top) 或 None
        """
        # 获取画布尺寸
        window_width = self.parent.canvas.winfo_width()
        window_height = self.parent.canvas.winfo_height()

        # 检查画布尺寸有效性
        if window_width < 10 or window_height < 10:
            return None

        # 检查缓存是否有效
        current_canvas_size = (window_width, window_height)
        if (self._cache_valid and
                self._cached_canvas_size == current_canvas_size and
                self._cached_display_params):
            return self._cached_display_params

        # 重新计算显示参数
        try:
            # 计算图像显示区域
            img_aspect = self.parent.viewport_width / self.parent.viewport_height
            window_aspect = window_width / window_height

            if window_aspect > img_aspect:
                # 窗口比图像更宽，按高度适配
                display_height = window_height
                display_width = display_height * img_aspect
                img_left = (window_width - display_width) / 2
                img_top = 0
            else:
                # 窗口比图像更窄，按宽度适配
                display_width = window_width
                display_height = display_width / img_aspect
                img_left = 0
                img_top = (window_height - display_height) / 2

            # 缓存结果
            display_params = (window_width, window_height, display_width, display_height, img_left, img_top)
            self._cached_canvas_size = current_canvas_size
            self._cached_display_params = display_params
            self._cache_valid = True

            return display_params

        except (ZeroDivisionError, AttributeError):
            return None

    def _is_point_in_image_area(self, canvas_x, canvas_y, img_left, img_top, display_width, display_height):
        """
        检查点是否在图像显示区域内

        Args:
            canvas_x, canvas_y: 画布坐标
            img_left, img_top: 图像显示区域左上角
            display_width, display_height: 图像显示区域尺寸

        Returns:
            bool: 是否在区域内
        """
        return (img_left <= canvas_x <= img_left + display_width and
                img_top <= canvas_y <= img_top + display_height)

    def _is_pixel_in_image_bounds(self, img_x, img_y, img_width, img_height):
        """
        检查像素坐标是否在图像边界内

        Args:
            img_x, img_y: 图像像素坐标
            img_width, img_height: 图像尺寸

        Returns:
            bool: 是否在边界内
        """
        return (0 <= img_x < img_width and 0 <= img_y < img_height)

    def invalidate_cache(self):
        """使缓存失效（当图像或视口发生变化时调用）"""
        self._cache_valid = False
        self._cached_display_params = None

    def get_scale_factor(self):
        """
        获取当前的缩放比例

        Returns:
            float: 缩放比例（图像像素/画布像素）或None
        """
        display_params = self._get_display_parameters()
        if not display_params:
            return None

        window_width, window_height, display_width, display_height, img_left, img_top = display_params

        # 计算缩放比例
        scale_x = self.parent.viewport_width / display_width
        scale_y = self.parent.viewport_height / display_height

        # 返回平均缩放比例
        return (scale_x + scale_y) / 2

    def get_canvas_center(self):
        """
        获取画布中心点对应的图像像素坐标

        Returns:
            tuple: 图像像素坐标 (img_x, img_y) 或 (None, None)
        """
        window_width = self.parent.canvas.winfo_width()
        window_height = self.parent.canvas.winfo_height()

        center_x = window_width / 2
        center_y = window_height / 2

        return self.canvas_to_image_pixel(center_x, center_y)

    def get_distance_in_pixels(self, canvas_distance):
        """
        将画布距离转换为图像像素距离

        Args:
            canvas_distance: 画布上的距离

        Returns:
            float: 对应的图像像素距离或None
        """
        scale_factor = self.get_scale_factor()
        if scale_factor is None:
            return None

        return canvas_distance * scale_factor

    def get_viewport_info(self):
        """
        获取当前视口信息

        Returns:
            dict: 视口信息字典
        """
        if not self.parent.image_paths:
            return None

        current_path = self.parent.image_paths[self.parent.current_index]
        img_data = self.parent.image_cache.get(current_path)
        if not img_data:
            return None

        img, _ = img_data
        scale_factor = self.get_scale_factor()

        return {
            'image_width': img.width,
            'image_height': img.height,
            'viewport_x': self.parent.viewport_x,
            'viewport_y': self.parent.viewport_y,
            'viewport_width': self.parent.viewport_width,
            'viewport_height': self.parent.viewport_height,
            'zoom_factor': self.parent.zoom_factor,
            'scale_factor': scale_factor
        }