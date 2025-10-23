# PhotosViewer / 图片查看器

[English](#english) | [中文](#中文)

---

## 中文

一个功能强大、易于使用的 Python 图片查看器应用程序，具有丰富的图片处理和管理功能。

### 📖 项目简介

PhotosViewer 是一个专业级的桌面图片查看器，采用 Python 和 Tkinter 构建，为图片浏览、编辑和管理提供完整的解决方案。该应用程序结合了直观的用户界面、强大的性能优化和丰富的功能特性。

**版本**: 2.9
**作者**: Clash/善良米塔
**许可证**: MIT

### ✨ 核心功能

#### 🖼️ 图片浏览
- **多格式支持** - 支持 JPEG、PNG、BMP、GIF、TIFF、WebP 等主流图片格式
- **文件夹浏览** - 自动加载当前文件夹所有图片，支持快速切换
- **智能缓存** - 基于 LRU 算法的内存缓存，提升浏览性能
- **拖放支持** - 支持拖放文件和文件夹到窗口打开
- **幻灯片播放** - 自动播放功能，可调节播放间隔

#### 🔧 图片编辑
- **旋转功能** - 支持顺时针/逆时针 90° 旋转
- **翻转功能** - 支持水平和垂直翻转
- **缩放控制** - 灵活的缩放功能，支持鼠标滚轮缩放
- **取色器** - 专业的颜色拾取工具，支持多种颜色格式（RGB、HEX、HSV 等）
- **拖动查看** - 缩放后可拖动图片查看不同区域

#### 🎨 界面特性
- **自适应窗口** - 智能调整窗口大小以适应图片
- **窗口模式切换** - 固定/动态窗口大小模式（Alt+X）
- **边框颜色** - 可自定义画布边框颜色
- **状态栏** - 实时显示图片信息、内存使用等状态
- **全屏模式** - 支持全屏浏览

#### 📁 文件管理
- **重命名** - 快速重命名当前图片（F2）
- **删除** - 删除当前图片到回收站
- **复制路径** - 复制图片路径到剪贴板
- **复制图片** - 复制图片到剪贴板（Windows 支持）
- **图片列表** - 显示当前文件夹所有图片列表
- **图片信息** - 查看详细的 EXIF 信息和图片属性

#### ⚡ 性能优化
- **并发加载** - 多线程预加载图片
- **内存管理** - 智能内存缓存控制，防止内存溢出
- **快速导航** - 键盘重复按键加速导航
- **动画优化** - 流畅的界面过渡动画

### 🛠️ 技术栈

- **编程语言**: Python 3.6+
- **GUI 框架**: Tkinter / TkinterDnD2
- **图片处理**: Pillow (PIL)
- **系统监控**: psutil
- **Windows 支持**: pywin32 (可选，用于剪贴板功能)
- **平台支持**: Windows、macOS、Linux

### 📋 系统要求

#### 基础要求
- Python 3.6 或更高版本
- 至少 512MB 可用内存
- 支持图形界面的操作系统

#### 依赖库
- `Pillow` - 图片处理
- `psutil` - 系统资源监控
- `tkinterdnd2` - 拖放功能支持（可选）
- `pywin32` - Windows 剪贴板支持（可选，仅 Windows）

### 🚀 安装与使用

#### 方法一：从源码运行（开发者）

1. **克隆项目**
```bash
git clone https://github.com/MitaHill/PhotosViewer.git
cd PhotosViewer
```

2. **安装依赖**
```bash
pip install -r requirements.txt
```

3. **运行程序**
```bash
python app.py
```

或者打开图片时运行：
```bash
python app.py /path/to/image.jpg
```

#### 方法二：Windows 打包版本

1. 运行打包脚本（Windows）：
```bash
Packge.bat
```

2. 在 `dist` 目录中找到生成的可执行文件

### 🎮 使用说明

#### 基本操作
- **打开图片**:
  - 文件菜单 → 打开 (Ctrl+O)
  - 拖放图片或文件夹到窗口
  - 命令行参数：`python app.py image.jpg`
- **浏览图片**:
  - 左右箭头键切换上一张/下一张
  - 鼠标滚轮缩放
  - 鼠标左键拖动移动图片
- **图片编辑**:
  - 编辑菜单 → 旋转/翻转
  - 工具菜单 → 取色器
- **查看信息**: 视图菜单 → 图片信息

#### 完整快捷键列表

| 功能分类 | 快捷键 | 说明 |
|---------|--------|------|
| **文件操作** |
| 打开文件 | `Ctrl+O` | 打开图片文件对话框 |
| 重命名 | `F2` | 重命名当前图片 |
| 删除 | `Delete` | 删除当前图片（移至回收站） |
| 退出 | `Ctrl+Q` | 退出程序 |
| **导航** |
| 上一张 | `←` / `A` | 显示上一张图片 |
| 下一张 | `→` / `D` | 显示下一张图片 |
| 播放/暂停 | `Space` | 切换幻灯片播放 |
| **缩放** |
| 放大 | `+` / `=` | 放大图片 |
| 缩小 | `-` | 缩小图片 |
| 适应窗口 | `F` | 图片适应窗口大小 |
| 实际大小 | `Ctrl+1` | 显示图片实际大小 (100%) |
| **编辑** |
| 顺时针旋转 | `Ctrl+R` | 旋转 90° |
| 逆时针旋转 | `Ctrl+Shift+R` | 逆时针旋转 90° |
| 水平翻转 | `Ctrl+H` | 水平镜像翻转 |
| 垂直翻转 | `Ctrl+Shift+H` | 垂直镜像翻转 |
| **工具** |
| 取色器 | `C` | 启动/关闭取色器工具 |
| 复制路径 | `Ctrl+Shift+C` | 复制图片路径到剪贴板 |
| 复制图片 | `Ctrl+C` | 复制图片到剪贴板 |
| **视图** |
| 图片列表 | `Ctrl+L` | 显示当前文件夹图片列表 |
| 图片信息 | `Ctrl+I` | 显示图片详细信息 |
| 窗口模式切换 | `Alt+X` | 切换固定/动态窗口模式 |
| 帮助 | `F1` | 显示帮助信息 |

### 📁 项目结构

```
PhotosViewer/
├── app.py                      # 主程序入口
├── Packge.bat                  # Windows 打包脚本
├── requirements.txt            # 依赖包列表
├── LICENSE                     # MIT 许可证
├── README.md                   # 项目说明文档（中英双语）
├── CHANGELOG.md                # 版本更新日志
├── CONTRIBUTING.md             # 贡献指南
└── src/                        # 源代码目录
    ├── __init__.py            # ImageViewer 主类
    ├── animation.py           # 动画效果
    ├── button.py              # 按钮组件
    ├── change_border_color.py # 边框颜色设置
    ├── change_cache.py        # 缓存管理
    ├── config_manager.py      # 配置管理
    ├── copy_images_body.py    # 图片复制功能
    ├── copy_path.py           # 路径复制
    ├── delete_photo.py        # 图片删除
    ├── dialog.py              # 对话框管理
    ├── drag.py                # 拖动功能
    ├── help.py                # 帮助信息
    ├── images_flip.py         # 图片翻转
    ├── images_info.py         # 图片信息显示
    ├── images_rotation.py     # 图片旋转
    ├── photos_list.py         # 图片列表
    ├── play.py                # 播放控制
    ├── position_photo.py      # 图片定位
    ├── reload_cache.py        # 缓存重载
    ├── rename_photo.py        # 图片重命名
    ├── reset_cache.py         # 缓存重置
    ├── sampling_mixin.py      # 取色器主功能
    ├── shortcut_key.py        # 快捷键管理
    ├── status_bar.py          # 状态栏
    ├── switch_previous_or_next.py  # 图片导航
    ├── window.py              # 窗口管理
    ├── window_size_toggle.py  # 窗口大小切换
    ├── zoom.py                # 缩放功能
    ├── config/                # 配置文件
    │   └── data.json         # 应用配置
    ├── img/                   # 图片资源
    │   └── logo.ico          # 应用图标
    └── sampling/              # 取色器模块
        ├── __init__.py       # 取色器管理器
        ├── color_detector.py # 颜色检测
        ├── coordinate_converter.py  # 坐标转换
        ├── overlay_manager.py       # 覆盖层管理
        ├── pixel_sampler.py         # 像素采样
        ├── position_calculator.py   # 位置计算
        └── theme_animation.py       # 主题动画
```

### 🔧 技术架构

本项目采用模块化设计，使用 Mixin 模式组织代码：

- **核心类**: `ImageViewer` - 整合所有功能模块
- **功能模块**: 每个 Mixin 类负责特定功能
- **配置管理**: JSON 配置文件持久化设置
- **性能优化**: LRU 缓存 + 多线程预加载
- **跨平台**: 支持 Windows/macOS/Linux

### 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！详细信息请查看 [CONTRIBUTING.md](CONTRIBUTING.md)

### 📝 版本历史

查看 [CHANGELOG.md](CHANGELOG.md) 了解详细的版本更新记录。

**当前版本**: v2.9

### 🎯 开发计划

#### v3.0 计划
- [ ] 批量图片处理
- [ ] 图片裁剪功能
- [ ] 更多图片格式支持 (HEIC, RAW)
- [ ] 主题系统（深色/浅色模式）
- [ ] 图片对比功能
- [ ] 插件系统

#### 未来功能
- [ ] AI 图片增强
- [ ] 图片标签和分类
- [ ] 云存储集成
- [ ] 图片编辑历史记录

### 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

### 👨‍💻 作者

**Clash / 善良米塔**
- GitHub: [@MitaHill](https://github.com/MitaHill)
- 项目原地址: https://github.com/clash16/photo

### 🙏 致谢

- 感谢 Python Tkinter 社区提供的优秀文档和示例
- 感谢所有为开源项目做出贡献的开发者
- 感谢所有使用和反馈的用户

### 🌟 Star History

如果这个项目对您有帮助，请给它一个 ⭐ Star！

---

## English

A powerful and user-friendly Python image viewer application with rich image processing and management features.

### 📖 Introduction

PhotosViewer is a professional desktop image viewer built with Python and Tkinter, providing a complete solution for image browsing, editing, and management. The application combines an intuitive user interface, powerful performance optimization, and rich feature set.

**Version**: 2.9
**Author**: Clash/善良米塔
**License**: MIT

### ✨ Key Features

#### 🖼️ Image Viewing
- **Multi-format Support** - JPEG, PNG, BMP, GIF, TIFF, WebP and more
- **Folder Navigation** - Auto-load all images in current folder
- **Smart Caching** - LRU-based memory cache for better performance
- **Drag & Drop** - Support drag-and-drop files and folders
- **Slideshow** - Auto-play with adjustable intervals

#### 🔧 Image Editing
- **Rotation** - Clockwise/counter-clockwise 90° rotation
- **Flip** - Horizontal and vertical flip
- **Zoom Control** - Flexible zooming with mouse wheel support
- **Color Picker** - Professional color sampling tool (RGB, HEX, HSV, etc.)
- **Pan & Drag** - Drag to view different areas when zoomed

#### 🎨 Interface Features
- **Adaptive Window** - Smart window sizing to fit images
- **Window Mode Toggle** - Fixed/dynamic window size mode (Alt+X)
- **Border Color** - Customizable canvas border color
- **Status Bar** - Real-time display of image info, memory usage
- **Fullscreen Mode** - Fullscreen viewing support

#### 📁 File Management
- **Rename** - Quick rename current image (F2)
- **Delete** - Move image to recycle bin
- **Copy Path** - Copy image path to clipboard
- **Copy Image** - Copy image to clipboard (Windows support)
- **Image List** - Display all images in current folder
- **Image Info** - View detailed EXIF data and properties

#### ⚡ Performance
- **Concurrent Loading** - Multi-threaded image preloading
- **Memory Management** - Smart cache control to prevent overflow
- **Fast Navigation** - Keyboard repeat acceleration
- **Animation** - Smooth UI transitions

### 🛠️ Tech Stack

- **Language**: Python 3.6+
- **GUI Framework**: Tkinter / TkinterDnD2
- **Image Processing**: Pillow (PIL)
- **System Monitoring**: psutil
- **Windows Support**: pywin32 (optional, for clipboard)
- **Platform**: Windows, macOS, Linux

### 📋 Requirements

#### Basic
- Python 3.6 or higher
- At least 512MB available memory
- OS with GUI support

#### Dependencies
- `Pillow` - Image processing
- `psutil` - System resource monitoring
- `tkinterdnd2` - Drag-and-drop support (optional)
- `pywin32` - Windows clipboard support (optional, Windows only)

### 🚀 Installation

#### Method 1: Run from Source

1. **Clone the repository**
```bash
git clone https://github.com/MitaHill/PhotosViewer.git
cd PhotosViewer
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Run the application**
```bash
python app.py
```

Or open with an image:
```bash
python app.py /path/to/image.jpg
```

#### Method 2: Windows Package

1. Run the package script (Windows):
```bash
Packge.bat
```

2. Find the executable in the `dist` directory

### 🎮 Usage

#### Basic Operations
- **Open Image**:
  - File menu → Open (Ctrl+O)
  - Drag and drop image/folder to window
  - Command line: `python app.py image.jpg`
- **Browse Images**:
  - Arrow keys to switch between images
  - Mouse wheel to zoom
  - Left mouse button to drag
- **Edit Images**:
  - Edit menu → Rotate/Flip
  - Tools menu → Color Picker
- **View Info**: View menu → Image Info

#### Keyboard Shortcuts

| Category | Shortcut | Description |
|----------|----------|-------------|
| **File** |
| Open File | `Ctrl+O` | Open image file dialog |
| Rename | `F2` | Rename current image |
| Delete | `Delete` | Move to recycle bin |
| Exit | `Ctrl+Q` | Exit application |
| **Navigation** |
| Previous | `←` / `A` | Previous image |
| Next | `→` / `D` | Next image |
| Play/Pause | `Space` | Toggle slideshow |
| **Zoom** |
| Zoom In | `+` / `=` | Zoom in |
| Zoom Out | `-` | Zoom out |
| Fit Window | `F` | Fit to window |
| Actual Size | `Ctrl+1` | 100% size |
| **Edit** |
| Rotate CW | `Ctrl+R` | Rotate 90° clockwise |
| Rotate CCW | `Ctrl+Shift+R` | Rotate 90° counter-clockwise |
| Flip H | `Ctrl+H` | Horizontal flip |
| Flip V | `Ctrl+Shift+H` | Vertical flip |
| **Tools** |
| Color Picker | `C` | Toggle color picker |
| Copy Path | `Ctrl+Shift+C` | Copy image path |
| Copy Image | `Ctrl+C` | Copy image to clipboard |
| **View** |
| Image List | `Ctrl+L` | Show image list |
| Image Info | `Ctrl+I` | Show image information |
| Window Toggle | `Alt+X` | Toggle fixed/dynamic mode |
| Help | `F1` | Show help |

### 📄 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) for details.

### 👨‍💻 Author

**Clash / 善良米塔**
- GitHub: [@MitaHill](https://github.com/MitaHill)
- Original Project: https://github.com/clash16/photo

### 🙏 Acknowledgments

- Thanks to the Python Tkinter community for excellent documentation
- Thanks to all contributors to open source projects
- Thanks to all users for their feedback and support

### 🌟 Give it a Star!

If you find this project helpful, please give it a ⭐ Star!

---

© 2025 Mita Hill. All rights reserved.
