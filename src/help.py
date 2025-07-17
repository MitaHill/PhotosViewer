#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
帮助和关于功能模块
Help and About Functionality Module
"""

import tkinter as tk


class HelpMixin:
    """帮助和关于功能混合类"""

    def show_about(self):
        """显示关于本项目信息"""
        about_dialog = tk.Toplevel(self.root)
        about_dialog.title("关于本项目——特点")
        about_dialog.geometry("500x300")
        about_dialog.transient(self.root)
        about_dialog.grab_set()

        text_widget = tk.Text(about_dialog, wrap=tk.WORD, height=15, width=50)
        text_widget.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        about_text = (
            "图片查看器\n"
            "====v2.9====\n"
            "\n"
            "这是一个功能强大的图片查看器\n"
            "1.高效的图像加载与缓存管理\n\n"
            "   密集图片可调整的缓存机制、多线程处理旋转动画\n\n"
            "2.自适应的边框\n"
            "   无论图片多大，都会试图将其控制在合理大小内\n\n"
            "3.幻灯片机制\n"
            "   可调节幻灯片播放间隔，搭配缓存机制可确保连续的图片切换\n\n"
            "4.更多的细节\n"
            "   程序背景的颜色根据图片边框颜色的配比进行变更\n"
            "   自定义旋转角度\n"
            "   旋转过程中采用多线程帧缓冲测率保证动画的流畅运行\n"
            "   水平翻转动画\n"
            "   文件菜单包含了使用者经常使用的操作选项\n"
            "   加载图片到内存中状态栏会显示当前正在缓存的图片\n"
            "   界面下方的状态栏可用于调试程序\n"
            "\n\n"
            "本项目使用了以下开源库和技术：\n"
            ">Python\n"
            "- Tkinter\n"
            "- Pillow\n"
            "- psutil\n"
            "- concurrent.futures\n\n"
            "- PyInstaller\n"
            "帮助\n"
            "Grok.com\n"
            "Chat.Deepseek.com\n"
            "Chatgpt.com\n"
            "Claude.ai\n"
            "制作由[Clash/善良米塔]"
        )

        text_widget.insert(tk.END, about_text)
        text_widget.config(state=tk.DISABLED)

    def show_attribution(self):
        """显示归属信息"""
        attrib_dialog = tk.Toplevel(self.root)
        attrib_dialog.title("归属")
        attrib_dialog.geometry("400x300")
        attrib_dialog.transient(self.root)
        attrib_dialog.grab_set()

        text_widget = tk.Text(attrib_dialog, wrap=tk.WORD, height=15, width=50)
        text_widget.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        attrib_text = (
            "归属信息\n"
            "====v2.9====\n"
            "\n"
            "制作来自于 Clash/善良米塔\n"
            "https://clash.ink\n"
            "\n"
            ">>作为537工具箱的一部分<<\n"
            "https://www.537studio.com\n"
            "\n"
            "更多内容请访问https://b.clash.ink/\n"
            "和https://github.com/clash16\n"
            "\n"
            "537工作室的更多内容请访问https://www.537studio.com\n"
            "和https://github.com/537Studio\n"
        )

        text_widget.insert(tk.END, attrib_text)
        text_widget.config(state=tk.DISABLED)

    def show_other_project(self):
        """显示其他项目信息"""
        print("帮助——其它项目")

        attrib_dialog = tk.Toplevel(self.root)
        attrib_dialog.title("其他项目")
        attrib_dialog.geometry("400x300")
        attrib_dialog.transient(self.root)
        attrib_dialog.grab_set()

        text_widget = tk.Text(attrib_dialog, wrap=tk.WORD, height=15, width=50)
        text_widget.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        attrib_text = (
            "图片查看器\n"
            "====v2.9====\n"
            "本项目的地址\n"
            "\n"
            "https://github.com/clash16/photo\n"
            "其它项目\n"
            "\n"
            "连接到:https://b.clash.ink/?id=11\n"
            "\n"
            "AI媒体:http://f.clash.ink:7868/\n"
            "\n"
            "\n"
            "更多内容在\n"
            "https://clash.ink/pages/#%E6%88%90%E6%9E%9C\n"
            "\n"
            "\n"
            "如何获取到更新\n"
            "请关注\n"
            "https://clash.ink\n"
            "https://b.clash.ink\n"
            "https://github.com/clash16/photo\n"
        )

        text_widget.insert(tk.END, attrib_text)
        text_widget.config(state=tk.DISABLED)