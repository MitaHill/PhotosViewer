#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
缩放功能模块
Zoom Functionality Module
"""

from PIL import Image


class ZoomMixin:
    """缩放功能混合类"""

    def on_mousewheel(self, event):
        """鼠标滚轮缩放"""
        if not self.image_paths or self.is_playing or hasattr(self, '_zoom_cooldown'):
            return
        self._zoom_cooldown = True

        mouse_x = event.x
        mouse_y = event.y
        img_x, img_y = self.canvas_to_image_coords(mouse_x, mouse_y)
        scale = 1.2 if event.delta > 0 else 1 / 1.2
        self.zoom_at_point(img_x, img_y, scale)

        if hasattr(self, '_high_quality_timer'):
            self.root.after_cancel(self._high_quality_timer)
        self._high_quality_timer = self.root.after(200, self.high_quality_redraw)

        self.root.after(50, lambda: delattr(self, '_zoom_cooldown'))

    def canvas_to_image_coords(self, canvas_x, canvas_y):
        """画布坐标转换为图像坐标"""
        window_width = self.canvas.winfo_width()
        window_height = self.canvas.winfo_height()
        if window_width < 10 or window_height < 10:
            return 0, 0

        current_path = self.image_paths[self.current_index]
        img_data = self.image_cache.get(current_path)
        if not img_data:
            return 0, 0
        img, _ = img_data

        img_aspect = self.viewport_width / self.viewport_height
        window_aspect = window_width / window_height

        if window_aspect > img_aspect:
            display_height = window_height
            display_width = display_height * img_aspect
            img_left = (window_width - display_width) / 2
            img_top = 0
        else:
            display_width = window_width
            display_height = display_width / img_aspect
            img_left = 0
            img_top = (window_height - display_height) / 2

        if (canvas_x < img_left or canvas_x > img_left + display_width or
                canvas_y < img_top or canvas_y > img_top + display_height):
            return self.viewport_x + self.viewport_width / 2, self.viewport_y + self.viewport_height / 2

        rel_x = (canvas_x - img_left) / display_width
        rel_y = (canvas_y - img_top) / display_height
        img_x = self.viewport_x + rel_x * self.viewport_width
        img_y = self.viewport_y + rel_y * self.viewport_height

        return img_x, img_y

    def zoom_at_point(self, img_x, img_y, scale):
        """在指定点缩放"""
        if not self.image_paths or self.is_playing:
            return
        current_path = self.image_paths[self.current_index]
        img_data = self.image_cache.get(current_path)
        if not img_data:
            return
        img, _ = img_data

        rel_x = (img_x - self.viewport_x) / self.viewport_width
        rel_y = (img_y - self.viewport_y) / self.viewport_height
        new_zoom_factor = self.zoom_factor * scale

        window_width = self.canvas.winfo_width()
        window_height = self.canvas.winfo_height()
        orig_width = img.width
        orig_height = img.height
        img_aspect = orig_width / orig_height
        window_aspect = window_width / window_height

        # 计算铺满屏幕的缩放因子
        if window_aspect > img_aspect:
            fill_screen_zoom = window_height / orig_height
        else:
            fill_screen_zoom = window_width / orig_width

        min_zoom = fill_screen_zoom
        max_zoom = 5.0
        self.zoom_factor = max(min_zoom, min(max_zoom, new_zoom_factor))

        # 确保小图片也能正确铺满屏幕
        if orig_width < window_width and orig_height < window_height:
            # 小图片：使用更大的缩放因子铺满屏幕
            self.viewport_width = window_width / self.zoom_factor
            self.viewport_height = window_height / self.zoom_factor
        else:
            # 大图片：正常处理
            if self.zoom_factor == min_zoom:
                if window_aspect > img_aspect:
                    self.viewport_width = orig_width
                    self.viewport_height = window_height / fill_screen_zoom
                else:
                    self.viewport_width = window_width / fill_screen_zoom
                    self.viewport_height = orig_height
            else:
                self.viewport_width = window_width / self.zoom_factor
                self.viewport_height = window_height / self.zoom_factor

        self.viewport_x = img_x - rel_x * self.viewport_width
        self.viewport_y = img_y - rel_y * self.viewport_height
        self.viewport_x = max(0, min(self.viewport_x, orig_width - self.viewport_width))
        self.viewport_y = max(0, min(self.viewport_y, orig_height - self.viewport_height))

        self.fast_redraw()

    def fast_redraw(self):
        """快速重绘"""
        if not self.image_paths:
            return
        current_path = self.image_paths[self.current_index]
        img_data = self.image_cache.get(current_path)
        if img_data:
            self.redraw_image(img_data[0], Image.Resampling.NEAREST)

    def high_quality_redraw(self):
        """高质量重绘"""
        if not self.image_paths:
            return
        current_path = self.image_paths[self.current_index]
        img_data = self.image_cache.get(current_path)
        if img_data:
            self.redraw_image(img_data[0], Image.Resampling.LANCZOS)

    def redraw_image(self, img, resample_method):
        """重绘图像"""
        window_width = self.canvas.winfo_width()
        window_height = self.canvas.winfo_height()
        if window_width < 10 or window_height < 10:
            return

        # 确保视口不超出图片边界
        max_x = max(0, img.width - self.viewport_width)
        max_y = max(0, img.height - self.viewport_height)
        self.viewport_x = max(0, min(self.viewport_x, max_x))
        self.viewport_y = max(0, min(self.viewport_y, max_y))

        # 确保视口尺寸不超过图片尺寸
        viewport_w = min(self.viewport_width, img.width)
        viewport_h = min(self.viewport_height, img.height)

        box = (
            int(max(0, self.viewport_x)),
            int(max(0, self.viewport_y)),
            int(min(img.width, self.viewport_x + viewport_w)),
            int(min(img.height, self.viewport_y + viewport_h))
        )

        # 防止无效的裁剪区域
        if box[2] <= box[0] or box[3] <= box[1]:
            box = (0, 0, img.width, img.height)

        cropped_img = img.crop(box)

        # 计算实际显示尺寸，保持纵横比
        crop_aspect = cropped_img.width / cropped_img.height
        window_aspect = window_width / window_height

        if window_aspect > crop_aspect:
            new_height = window_height
            new_width = int(new_height * crop_aspect)
        else:
            new_width = window_width
            new_height = int(new_width / crop_aspect)

        # 防止尺寸为0
        new_width = max(1, new_width)
        new_height = max(1, new_height)

        resized_img = cropped_img.resize((new_width, new_height), resample_method)
        from PIL import ImageTk
        tk_img = ImageTk.PhotoImage(resized_img)

        self.canvas.delete("all")
        self.canvas.create_image(window_width // 2, window_height // 2, anchor="center", image=tk_img)
        self.canvas.image = tk_img