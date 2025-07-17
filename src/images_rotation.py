#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
图片旋转功能模块
Image Rotation Functionality Module
"""

import os
import threading
import concurrent.futures
import tkinter as tk
from PIL import Image


class RotationMixin:
    """图片旋转功能混合类"""

    def rotate_ccw_90(self):
        """逆时针旋转90°"""
        if not self.image_paths or self.is_playing:
            return
        self.animate_rotate(90)

    def rotate_ccw_180(self):
        """逆时针旋转180°"""
        if not self.image_paths or self.is_playing:
            return
        self.animate_rotate(180)

    def rotate_cw_90(self):
        """顺时针旋转90°"""
        if not self.image_paths or self.is_playing:
            return
        self.animate_rotate(-90)

    def rotate_cw_180(self):
        """顺时针旋转180°"""
        if not self.image_paths or self.is_playing:
            return
        self.animate_rotate(-180)

    def custom_rotate(self):
        """自定义旋转角度"""
        if not self.image_paths or self.is_playing:
            return

        dialog = tk.Toplevel(self.root)
        dialog.title("自定义旋转")
        dialog.transient(self.root)
        dialog.grab_set()

        tk.Label(dialog, text="请输入旋转角度 (°):").pack(pady=5)
        angle_entry = tk.Entry(dialog)
        angle_entry.pack(pady=5)
        angle_entry.focus_set()

        def on_submit():
            try:
                angle = float(angle_entry.get())
                self.animate_rotate(angle)
                dialog.destroy()
            except ValueError:
                print("请输入有效的角度（例如 180 或 -36）")

        tk.Button(dialog, text="确认", command=on_submit).pack(pady=5)
        dialog.bind('<Return>', lambda e: on_submit())

    def animate_rotate(self, target_angle):
        """带动画的旋转"""
        if not self.image_paths or self.is_playing:
            return

        current_path = self.image_paths[self.current_index]
        img_data = self.image_cache.get(current_path)
        if not img_data:
            return

        img, size = img_data
        steps = 10
        duration = 500
        step_time = duration // steps

        self.root.title(f"正在处理[{target_angle}°]中")

        def compute_frame(step):
            progress = self.ease_in_out(step, steps)
            current_angle = target_angle * progress
            return img.rotate(current_angle, expand=True, resample=Image.BICUBIC)

        def precompute_frames(img, target_angle, steps, callback):
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
                    self.image_cache[current_path] = (frame_cache[-1], size)
                    self.viewport_x = 0
                    self.viewport_y = 0
                    self.viewport_width = frame_cache[-1].width
                    self.viewport_height = frame_cache[-1].height
                    self.fast_redraw()
                    self.root.title(f"图片查看器 - {os.path.basename(current_path)}")
                    return

                rotated_img = frame_cache[step]
                self.image_cache[current_path] = (rotated_img, size)
                self.viewport_x = 0
                self.viewport_y = 0
                self.viewport_width = rotated_img.width
                self.viewport_height = rotated_img.height
                self.fast_redraw()
                self.root.after(step_time, update_frame, step + 1)

            update_frame(0)

        threading.Thread(target=precompute_frames, args=(img, target_angle, steps, on_frames_ready),
                         daemon=True).start()

    def rotate_image(self, angle):
        """直接旋转图片（无动画）"""
        current_path = self.image_paths[self.current_index]
        img_data = self.image_cache.get(current_path)
        if not img_data:
            return

        img, size = img_data
        rotated_img = img.rotate(angle, expand=True, resample=Image.BICUBIC)
        self.image_cache[current_path] = (rotated_img, size)
        self.viewport_x = 0
        self.viewport_y = 0
        self.viewport_width = rotated_img.width
        self.viewport_height = rotated_img.height
        self.fast_redraw()