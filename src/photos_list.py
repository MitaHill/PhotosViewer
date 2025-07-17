#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
图片列表功能模块
Photo List Display Functionality Module
"""

import os
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk


class PhotosListMixin:
    """图片列表功能混合类"""

    def show_image_list(self):
        """显示当前目录下的图片列表，允许跳转到指定图片"""
        if not self.image_paths or not self.last_directory:
            print("当前没有加载任何图片或目录")
            return

        # 创建图片列表对话框
        list_dialog = tk.Toplevel(self.root)
        list_dialog.title("图片列表")
        list_dialog.geometry("650x450")
        list_dialog.minsize(500, 350)
        list_dialog.transient(self.root)
        list_dialog.grab_set()

        # 配置样式
        style = ttk.Style()
        style.configure("Treeview", rowheight=30, font=('Arial', 10))
        style.configure("Treeview.Heading", font=('Arial', 11, 'bold'))
        style.map('Treeview', background=[('selected', '#4a6984')])

        # 主框架
        main_frame = tk.Frame(list_dialog)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

        # 标题标签
        header_frame = tk.Frame(main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 10))
        tk.Label(
            header_frame,
            text=f"目录: {os.path.basename(self.last_directory)}",
            font=('Arial', 12, 'bold'),
            anchor="w"
        ).pack(side=tk.LEFT, fill=tk.X)
        tk.Label(
            header_frame,
            text=f"共 {len(self.image_paths)} 张图片",
            font=('Arial', 11),
            fg="#555555"
        ).pack(side=tk.RIGHT)

        # 创建表格框架
        table_frame = tk.Frame(main_frame)
        table_frame.pack(fill=tk.BOTH, expand=True)

        # 创建 Treeview 表格
        tree = ttk.Treeview(table_frame, columns=("Index", "Filename", "Size"), show="headings", selectmode="browse")
        tree.heading("Index", text="序号")
        tree.heading("Filename", text="文件名")
        tree.heading("Size", text="大小")
        tree.column("Index", width=60, anchor="center")
        tree.column("Filename", width=450, anchor="w")
        tree.column("Size", width=100, anchor="e")

        # 填充表格数据
        for idx, image_path in enumerate(self.image_paths):
            filename = os.path.basename(image_path)
            try:
                file_size = os.path.getsize(image_path)
                if file_size < 1024:
                    size_str = f"{file_size} B"
                elif file_size < 1024 * 1024:
                    size_str = f"{file_size / 1024:.1f} KB"
                else:
                    size_str = f"{file_size / (1024 * 1024):.1f} MB"
            except:
                size_str = "未知"

            tree.insert("", tk.END, values=(idx + 1, filename, size_str))

        # 添加滚动条
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # 点击表格行跳转到对应图片
        def on_row_select(event):
            selected_item = tree.selection()
            if selected_item:
                # 添加动画效果
                for i in range(5):
                    tree.item(selected_item, tags=("flashing",))
                    style.map('Treeview', background=[('selected', '#6a99c7')])
                    list_dialog.update()
                    list_dialog.after(50)
                    style.map('Treeview', background=[('selected', '#4a6984')])
                    list_dialog.update()
                    list_dialog.after(50)

                index = int(tree.item(selected_item, "values")[0]) - 1
                self.current_index = index
                self.show_current_image()

                status_var.set(f"已跳转到: {os.path.basename(self.image_paths[index])}")
                status_label.config(fg="#228B22")
                list_dialog.after(3000, lambda: status_var.set(""))

        tree.bind("<Double-1>", on_row_select)

        # 单击选择行预览图片
        def on_single_click(event):
            selected_item = tree.selection()
            if selected_item:
                index = int(tree.item(selected_item, "values")[0]) - 1
                filename = os.path.basename(self.image_paths[index])
                preview_var.set(f"预览: {filename}")

                try:
                    img = Image.open(self.image_paths[index])
                    img.thumbnail((150, 150))
                    photo = ImageTk.PhotoImage(img)
                    preview_image.config(image=photo)
                    preview_image.image = photo
                except Exception as e:
                    preview_image.config(image="")
                    preview_var.set(f"预览: {filename} (无法加载)")

        tree.bind("<ButtonRelease-1>", on_single_click)

        # 预览框架
        preview_frame = tk.Frame(main_frame)
        preview_frame.pack(fill=tk.X, pady=(10, 5))

        preview_var = tk.StringVar()
        preview_label = tk.Label(preview_frame, textvariable=preview_var, font=('Arial', 10))
        preview_label.pack(side=tk.TOP, anchor="w")

        preview_image = tk.Label(preview_frame)
        preview_image.pack(side=tk.TOP, anchor="w", pady=(5, 0))

        # 输入框和跳转按钮
        input_frame = tk.Frame(main_frame)
        input_frame.pack(fill=tk.X, pady=(10, 5))

        tk.Label(input_frame, text="跳转到第几张图片:", font=('Arial', 10)).pack(side=tk.LEFT, padx=5)
        index_entry = tk.Entry(input_frame, width=10, font=('Arial', 10))
        index_entry.pack(side=tk.LEFT, padx=5)

        status_var = tk.StringVar()
        status_label = tk.Label(input_frame, textvariable=status_var, font=('Arial', 10), fg="#555555")
        status_label.pack(side=tk.RIGHT, padx=10)

        def jump_to_index():
            try:
                index = int(index_entry.get()) - 1
                if 0 <= index < len(self.image_paths):
                    self.current_index = index
                    self.show_current_image()
                    tree.selection_set(tree.get_children()[index])
                    tree.see(tree.get_children()[index])

                    # 输入框动画
                    original_bg = index_entry.cget("background")
                    for _ in range(3):
                        index_entry.config(background="#aaffaa")
                        list_dialog.update()
                        list_dialog.after(50)
                        index_entry.config(background=original_bg)
                        list_dialog.update()
                        list_dialog.after(50)

                    list_dialog.after(3000, lambda: status_var.set(""))
                else:
                    # 错误动画
                    original_bg = index_entry.cget("background")
                    for _ in range(3):
                        index_entry.config(background="#ffaaaa")
                        list_dialog.update()
                        list_dialog.after(50)
                        index_entry.config(background=original_bg)
                        list_dialog.update()
                        list_dialog.after(50)
            except ValueError:
                # 错误动画
                original_bg = index_entry.cget("background")
                for _ in range(3):
                    index_entry.config(background="#ffaaaa")
                    list_dialog.update()
                    list_dialog.after(50)
                    index_entry.config(background=original_bg)
                    list_dialog.update()
                    list_dialog.after(50)

        jump_button = tk.Button(
            input_frame,
            text="跳转",
            command=jump_to_index,
            bg="#4a6984",
            fg="white",
            font=('Arial', 10),
            relief=tk.RAISED,
            padx=10
        )
        jump_button.pack(side=tk.LEFT, padx=5)

        # 按钮悬停效果
        def on_enter(e):
            jump_button['background'] = '#6a99c7'

        def on_leave(e):
            jump_button['background'] = '#4a6984'

        jump_button.bind("<Enter>", on_enter)
        jump_button.bind("<Leave>", on_leave)

        index_entry.bind("<Return>", lambda e: jump_to_index())

        # 高亮当前图片
        if 0 <= self.current_index < len(self.image_paths):
            children = tree.get_children()
            if children:
                current_item = children[self.current_index]
                tree.see(current_item)
                tree.selection_set(current_item)
                on_single_click(None)

        # 渐入动画
        list_dialog.attributes('-alpha', 0.0)

        def fade_in():
            alpha = list_dialog.attributes('-alpha')
            if alpha < 1.0:
                alpha += 0.1
                list_dialog.attributes('-alpha', alpha)
                list_dialog.after(13, fade_in)

        list_dialog.after(0, fade_in)