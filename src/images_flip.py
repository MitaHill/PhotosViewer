#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
图片翻转功能模块
Image Flip Functionality Module
"""

import os
import threading
import concurrent.futures
from PIL import Image


class FlipMixin:
    """图片翻转功能混合类"""

    def flip_horizontal(self):
        """水平翻转"""
        if not self.image_paths or self.is_playing:
            return

        current_path = self.image_paths[self.current_index]
        img_data = self.image_cache.get(current_path)
        if not img_data:
            return

        img, size = img_data

        if size > self.cache_size_limit * 0.5:
            print(f"图片大小 {size} 超过缓存限制 {self.cache_size_limit * 0.5}，无法翻转")
            return

        steps = 10
        duration = 500
        step_time = duration // steps

        self.root.title(f"正在水平翻转 - {os.path.basename(current_path)}")

        def compute_frame(step):
            progress = self.ease_in_out(step, steps, easing_type="quartic")
            scale_x = 1 - 2 * progress
            if scale_x == 0:
                scale_x = 0.01
            frame = img.transform(
                img.size,
                Image.AFFINE,
                (scale_x, 0, img.width * (1 - scale_x) / 2, 0, 1, 0),
                resample=Image.BICUBIC
            )
            return frame

        def precompute_frames(img, callback):
            frame_cache = [None] * (steps + 1)
            with concurrent.futures.ThreadPoolExecutor(max_workers=min(steps + 1, os.cpu_count() or 4)) as executor:
                futures = {executor.submit(compute_frame, step): step for step in range(steps + 1)}
                for future in concurrent.futures.as_completed(futures):
                    step = futures[future]
                    frame_cache[step] = future.result()
            callback(frame_cache)

        def on_frames_ready(frame_cache):
            def update_frame(step=0):
                if step > steps:
                    flipped_img = frame_cache[-1]
                    self.image_cache[current_path] = (flipped_img, size)
                    self.viewport_x = 0
                    self.viewport_y = 0
                    self.viewport_width = flipped_img.width
                    self.viewport_height = flipped_img.height
                    self.fast_redraw()
                    self.root.title(f"图片查看器 - {os.path.basename(current_path)}")
                    return

                current_frame = frame_cache[step]
                self.image_cache[current_path] = (current_frame, size)
                self.viewport_x = 0
                self.viewport_y = 0
                self.viewport_width = current_frame.width
                self.viewport_height = current_frame.height
                self.fast_redraw()
                self.root.after(step_time, update_frame, step + 1)

            update_frame(0)

        threading.Thread(target=precompute_frames, args=(img, on_frames_ready), daemon=True).start()

    def flip_vertical(self):
        """垂直翻转"""
        if not self.image_paths or self.is_playing:
            return

        current_path = self.image_paths[self.current_index]
        img_data = self.image_cache.get(current_path)
        if not img_data:
            return

        img, size = img_data

        if size > self.cache_size_limit * 0.5:
            print(f"图片大小 {size} 超过缓存限制 {self.cache_size_limit * 0.5}，无法翻转")
            return

        steps = 10
        duration = 500
        step_time = duration // steps

        self.root.title(f"正在垂直翻转 - {os.path.basename(current_path)}")

        def compute_frame(step):
            progress = self.ease_in_out(step, steps, easing_type="quartic")
            scale_y = 1 - 2 * progress
            if scale_y == 0:
                scale_y = 0.01
            frame = img.transform(
                img.size,
                Image.AFFINE,
                (1, 0, 0, 0, scale_y, img.height * (1 - scale_y) / 2),
                resample=Image.BICUBIC
            )
            return frame

        def precompute_frames(img, callback):
            frame_cache = [None] * (steps + 1)
            with concurrent.futures.ThreadPoolExecutor(max_workers=min(steps + 1, os.cpu_count() or 4)) as executor:
                futures = {executor.submit(compute_frame, step): step for step in range(steps + 1)}
                for future in concurrent.futures.as_completed(futures):
                    step = futures[future]
                    frame_cache[step] = future.result()
            callback(frame_cache)

        def on_frames_ready(frame_cache):
            def update_frame(step=0):
                if step > steps:
                    flipped_img = frame_cache[-1]
                    self.image_cache[current_path] = (flipped_img, size)
                    self.viewport_x = 0
                    self.viewport_y = 0
                    self.viewport_width = flipped_img.width
                    self.viewport_height = flipped_img.height
                    self.fast_redraw()
                    self.root.title(f"图片查看器 - {os.path.basename(current_path)}")
                    return

                current_frame = frame_cache[step]
                self.image_cache[current_path] = (current_frame, size)
                self.viewport_x = 0
                self.viewport_y = 0
                self.viewport_width = current_frame.width
                self.viewport_height = current_frame.height
                self.fast_redraw()
                self.root.after(step_time, update_frame, step + 1)

            update_frame(0)

        threading.Thread(target=precompute_frames, args=(img, on_frames_ready), daemon=True).start()