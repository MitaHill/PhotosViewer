# PhotosViewer

一个使用 Python Tkinter 库开发的简洁易用的图片查看器应用程序。

## 📖 项目简介

PhotosViewer 是一个轻量级的桌面图片查看器，专为快速浏览和管理图片而设计。该项目采用 Python 的 Tkinter 库构建，提供了直观的用户界面和流畅的图片浏览体验。

## ✨ 主要功能

- 🖼️ **多格式支持** - 支持常见图片格式（JPEG、PNG、BMP、GIF 等）
- 🔍 **缩放控制** - 支持图片放大、缩小和适应窗口大小
- ⌨️ **快捷键操作** - 便捷的键盘快捷键支持
- 📁 **文件夹浏览** - 快速切换同文件夹内的其他图片
- 🎨 **简洁界面** - 清爽的用户界面设计
- 💾 **轻量级** - 占用系统资源少，启动速度快

## 🛠️ 技术栈

- **编程语言**: Python
- **GUI 框架**: Tkinter
- **图片处理**: PIL (Pillow)
- **平台支持**: Windows、macOS、Linux

## 📋 系统要求

- Python 3.6+
- Tkinter (通常随 Python 安装)
- Pillow 库

## 🚀 安装与使用

### 环境准备

1. 确保已安装 Python 3.6 或更高版本
2. 安装必要的依赖库：

```bash
pip install Pillow
```

### 运行应用

1. 克隆项目到本地：
```bash
git clone https://github.com/MitaHill/PhotosViewer.git
cd PhotosViewer
```

2. 运行程序：
```bash
python main.py
```

## 🎮 使用说明

### 基本操作
- **打开图片**: 点击"打开"按钮或使用 Ctrl+O
- **上一张/下一张**: 使用方向键或点击导航按钮
- **缩放**: 使用鼠标滚轮或缩放按钮
- **适应窗口**: 按 F 键或点击适应按钮
- **全屏模式**: 按 F11 进入/退出全屏

### 快捷键
| 快捷键 | 功能 |
|--------|------|
| Ctrl+O | 打开文件 |
| ← → | 上一张/下一张 |
| + - | 放大/缩小 |
| F | 适应窗口 |
| F11 | 全屏切换 |
| ESC | 退出全屏 |

## 📁 项目结构

```
PhotosViewer/
├── main.py              # 主程序入口
├── viewer.py            # 图片查看器核心逻辑
├── ui.py               # 用户界面组件
├── utils.py            # 工具函数
├── requirements.txt    # 依赖包列表
├── LICENSE            # MIT 许可证
└── README.md          # 项目说明文档
```

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request 来帮助改进这个项目！

1. Fork 本项目
2. 创建您的特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交您的更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 提交 Pull Request

## 📝 开发计划

- [ ] 添加图片编辑功能（旋转、裁剪）
- [ ] 支持更多图片格式
- [ ] 添加图片信息显示（EXIF 数据）
- [ ] 实现幻灯片播放模式
- [ ] 添加主题切换功能

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 👨‍💻 作者

**Mita Hill** - [GitHub](https://github.com/MitaHill)

## 🙏 致谢

- 感谢 Python Tkinter 社区提供的优秀文档和示例
- 感谢所有为开源图片查看器项目做出贡献的开发者

---

如果您觉得这个项目有用，请给它一个 ⭐ Star！
