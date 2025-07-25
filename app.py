#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
图片查看器主程序入口
Image Viewer Application Entry Point
Version: 2.9
Author: Clash/善良米塔
"""

import os
import sys
import signal
import tkinter as tk

# 检测是否为 PyInstaller 打包环境
if getattr(sys, 'frozen', False):
    # PyInstaller 打包环境
    application_path = sys._MEIPASS
else:
    # 开发环境
    application_path = os.path.dirname(os.path.abspath(__file__))

# 添加src目录到Python路径
src_dir = os.path.join(application_path, 'src')
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

# 尝试导入 tkinterdnd2，如果失败则使用标准 tkinter
try:
    from tkinterdnd2 import TkinterDnD

    DND_SUPPORT = True
except ImportError:
    DND_SUPPORT = False
    print("警告: tkinterdnd2 未安装，拖放功能将不可用")

from src import ImageViewer


def setup_signal_handlers():
    """设置信号处理器"""

    def signal_handler(signum, frame):
        print("接收到终止信号，正在关闭程序...")
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)
    if hasattr(signal, 'SIGTERM'):
        signal.signal(signal.SIGTERM, signal_handler)


def parse_arguments():
    """解析命令行参数"""
    initial_image = None
    if len(sys.argv) > 1:
        potential_image = sys.argv[1]
        if os.path.isfile(potential_image):
            initial_image = os.path.abspath(potential_image)
            print(f"命令行参数指定的初始图片: {initial_image}")
        else:
            print(f"警告: 指定的文件不存在: {potential_image}")

    return initial_image


def create_root_window():
    """创建并配置主窗口"""
    if DND_SUPPORT:
        try:
            root = TkinterDnD.Tk()
            print("已启用拖放功能")
        except Exception as e:
            print(f"TkinterDnD初始化失败: {e}")
            root = tk.Tk()
    else:
        root = tk.Tk()

    # 基本窗口配置
    root.title("图片查看器")
    root.geometry("1024x768")
    root.minsize(400, 300)

    # 设置程序图标
    try:
        if getattr(sys, 'frozen', False):
            # PyInstaller 环境
            icon_path = os.path.join(sys._MEIPASS, 'src', 'img', 'logo.ico')
        else:
            # 开发环境
            icon_path = os.path.join(src_dir, 'img', 'logo.ico')

        if os.path.exists(icon_path):
            root.iconbitmap(icon_path)
        else:
            print(f"图标文件未找到: {icon_path}")
    except Exception as e:
        print(f"设置图标失败: {e}")

    return root


def main():
    """主函数"""
    print("图片查看器 v2.9 启动中...")
    print("制作: Clash/善良米塔")
    print("项目地址: https://github.com/clash16/photo")

    # 设置信号处理
    setup_signal_handlers()

    # 解析命令行参数
    initial_image = parse_arguments()

    # 创建主窗口
    root = create_root_window()

    try:
        # 创建图片查看器实例
        print("正在初始化图片查看器...")
        viewer = ImageViewer(root, initial_image)

        print("图片查看器初始化完成")

        # 启动主事件循环
        root.mainloop()

    except KeyboardInterrupt:
        print("用户中断程序")
        sys.exit(0)
    except Exception as e:
        print(f"程序运行时发生错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    finally:
        print("程序已退出")


if __name__ == "__main__":
    main()