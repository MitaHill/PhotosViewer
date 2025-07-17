#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
复制图片本体功能模块
Copy Image Body Functionality Module
"""

import os
import sys
import io
from tkinter import messagebox
from PIL import Image


class CopyImageBodyMixin:
    """复制图片本体功能混合类"""

    def copy_image_body_to_clipboard(self, event=None):
        """将当前图片本体复制到系统剪切板"""
        if not self.image_paths or self.current_index < 0 or self.current_index >= len(self.image_paths):
            messagebox.showerror("错误", "没有图片可复制")
            return

        current_path = self.image_paths[self.current_index]

        try:
            if sys.platform == 'win32':
                # Windows平台
                self._copy_image_windows(current_path)
            elif sys.platform == 'darwin':
                # macOS平台
                self._copy_image_macos(current_path)
            elif sys.platform.startswith('linux'):
                # Linux平台
                self._copy_image_linux(current_path)
            else:
                messagebox.showinfo("提示", "当前平台不支持复制图片到剪切板")

        except Exception as e:
            messagebox.showerror("错误", f"复制图片失败: {str(e)}")

    def _copy_image_windows(self, image_path):
        """Windows平台复制图片实现"""
        try:
            import win32clipboard
            from PIL import Image

            # 打开并转换图片
            with Image.open(image_path) as img:
                # 转换为RGB格式（BMP需要）
                if img.mode != 'RGB':
                    img = img.convert('RGB')

                # 转换为BMP格式的字节数据
                output = io.BytesIO()
                img.save(output, format='BMP')
                data = output.getvalue()[14:]  # 跳过BMP文件头
                output.close()

                # 复制到剪切板
                win32clipboard.OpenClipboard()
                win32clipboard.EmptyClipboard()
                win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
                win32clipboard.CloseClipboard()

            print("图片已复制到剪切板 (Windows)")

        except ImportError:
            # 如果没有win32clipboard，尝试使用其他方法
            self._copy_image_fallback_windows(image_path)

    def _copy_image_fallback_windows(self, image_path):
        """Windows平台备用复制方法"""
        import subprocess
        import tempfile

        try:
            # 使用PowerShell脚本复制图片
            ps_script = f'''
            Add-Type -AssemblyName System.Windows.Forms
            $img = [System.Drawing.Image]::FromFile("{image_path}")
            [System.Windows.Forms.Clipboard]::SetImage($img)
            $img.Dispose()
            '''

            result = subprocess.run([
                'powershell', '-Command', ps_script
            ], capture_output=True, text=True, timeout=10)

            if result.returncode == 0:
                print("图片已复制到剪切板 (PowerShell)")
            else:
                raise Exception("PowerShell复制失败")

        except Exception as e:
            print(f"Windows备用方法失败: {e}")
            messagebox.showinfo("提示", "复制图片功能需要安装 pywin32 模块")

    def _copy_image_macos(self, image_path):
        """macOS平台复制图片实现"""
        import subprocess

        try:
            # 使用osascript和AppleScript复制图片
            script = f'''
            set theFile to POSIX file "{image_path}"
            tell application "Finder"
                set the clipboard to theFile
            end tell
            '''

            result = subprocess.run([
                'osascript', '-e', script
            ], capture_output=True, text=True, timeout=10)

            if result.returncode == 0:
                print("图片已复制到剪切板 (macOS)")
            else:
                # 尝试另一种方法
                self._copy_image_macos_alternative(image_path)

        except Exception as e:
            print(f"macOS复制失败: {e}")
            messagebox.showinfo("提示", "macOS暂不支持直接复制图片，已复制文件路径")
            self.copy_image_path_to_clipboard()

    def _copy_image_macos_alternative(self, image_path):
        """macOS备用复制方法"""
        import subprocess

        try:
            # 使用pbcopy命令复制图片数据
            with open(image_path, 'rb') as f:
                subprocess.run([
                    'pbcopy'
                ], input=f.read(), timeout=10)

            print("图片数据已复制到剪切板 (macOS)")

        except Exception as e:
            print(f"macOS备用方法失败: {e}")
            raise

    def _copy_image_linux(self, image_path):
        """Linux平台复制图片实现"""
        import subprocess

        try:
            # 检查是否有xclip
            result = subprocess.run(['which', 'xclip'], capture_output=True)
            if result.returncode == 0:
                self._copy_image_xclip(image_path)
                return

            # 检查是否有wl-clipboard (Wayland)
            result = subprocess.run(['which', 'wl-copy'], capture_output=True)
            if result.returncode == 0:
                self._copy_image_wayland(image_path)
                return

            # 如果都没有，提示安装
            messagebox.showinfo("提示",
                                "Linux平台需要安装 xclip 或 wl-clipboard 才能复制图片\n"
                                "Ubuntu/Debian: sudo apt install xclip\n"
                                "已改为复制图片路径")
            self.copy_image_path_to_clipboard()

        except Exception as e:
            print(f"Linux复制失败: {e}")
            messagebox.showinfo("提示", "Linux平台复制图片失败，已复制路径")
            self.copy_image_path_to_clipboard()

    def _copy_image_xclip(self, image_path):
        """使用xclip复制图片"""
        import subprocess
        import mimetypes

        # 获取MIME类型
        mime_type, _ = mimetypes.guess_type(image_path)
        if not mime_type or not mime_type.startswith('image/'):
            mime_type = 'image/png'

        with open(image_path, 'rb') as f:
            subprocess.run([
                'xclip', '-selection', 'clipboard', '-t', mime_type
            ], input=f.read(), timeout=10)

        print("图片已复制到剪切板 (xclip)")

    def _copy_image_wayland(self, image_path):
        """使用wl-copy复制图片 (Wayland)"""
        import subprocess
        import mimetypes

        # 获取MIME类型
        mime_type, _ = mimetypes.guess_type(image_path)
        if not mime_type or not mime_type.startswith('image/'):
            mime_type = 'image/png'

        with open(image_path, 'rb') as f:
            subprocess.run([
                'wl-copy', '--type', mime_type
            ], input=f.read(), timeout=10)

        print("图片已复制到剪切板 (wl-copy)")

    def get_clipboard_image_support_info(self):
        """获取当前平台的图片剪切板支持信息"""
        if sys.platform == 'win32':
            try:
                import win32clipboard
                return "Windows: 完全支持 (win32clipboard)"
            except ImportError:
                return "Windows: 部分支持 (需要安装 pywin32)"
        elif sys.platform == 'darwin':
            return "macOS: 支持 (AppleScript)"
        elif sys.platform.startswith('linux'):
            import subprocess
            try:
                subprocess.run(['which', 'xclip'], capture_output=True, check=True)
                return "Linux: 支持 (xclip)"
            except:
                try:
                    subprocess.run(['which', 'wl-copy'], capture_output=True, check=True)
                    return "Linux: 支持 (wl-clipboard)"
                except:
                    return "Linux: 不支持 (需要安装 xclip 或 wl-clipboard)"
        else:
            return "未知平台: 不支持"