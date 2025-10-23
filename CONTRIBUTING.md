# 贡献指南 / Contributing Guide

[English](#english) | [中文](#中文)

---

## 中文

感谢您对 PhotosViewer 项目感兴趣！我们欢迎任何形式的贡献。

### 🌟 如何贡献

#### 报告问题 Bug Reports

如果您发现了 bug，请：

1. 在 [Issues](https://github.com/MitaHill/PhotosViewer/issues) 页面搜索，确认问题尚未被报告
2. 创建新的 Issue，并提供：
   - 详细的问题描述
   - 复现步骤
   - 预期行为和实际行为
   - 系统环境信息（操作系统、Python 版本等）
   - 相关的错误信息或截图

#### 功能建议 Feature Requests

如果您有新功能的想法：

1. 在 Issues 中搜索类似的建议
2. 创建新的 Feature Request Issue
3. 详细描述功能的用途和预期行为
4. 如果可能，提供使用场景的例子

#### 提交代码 Pull Requests

我们欢迎您提交代码！请遵循以下步骤：

1. **Fork 项目**
   ```bash
   # 在 GitHub 上 Fork 项目
   # 然后克隆您的 fork
   git clone https://github.com/your-username/PhotosViewer.git
   cd PhotosViewer
   ```

2. **创建分支**
   ```bash
   git checkout -b feature/your-feature-name
   # 或
   git checkout -b fix/your-bug-fix
   ```

3. **设置开发环境**
   ```bash
   # 创建虚拟环境
   python -m venv venv

   # 激活虚拟环境
   # Windows:
   venv\Scripts\activate
   # Linux/Mac:
   source venv/bin/activate

   # 安装依赖
   pip install -r requirements.txt
   ```

4. **进行修改**
   - 编写清晰、可维护的代码
   - 遵循项目的代码风格
   - 添加必要的注释和文档字符串
   - 确保代码在不同平台上能正常运行

5. **测试您的修改**
   ```bash
   # 运行程序确保功能正常
   python app.py

   # 测试不同的使用场景
   # 检查是否有错误或警告
   ```

6. **提交更改**
   ```bash
   git add .
   git commit -m "类型: 简短描述

   详细描述您的更改内容和原因"
   ```

   提交信息格式：
   - `feat: 添加新功能`
   - `fix: 修复 bug`
   - `docs: 更新文档`
   - `style: 代码格式调整`
   - `refactor: 代码重构`
   - `perf: 性能优化`
   - `test: 添加测试`
   - `chore: 构建/工具变动`

7. **推送到 GitHub**
   ```bash
   git push origin feature/your-feature-name
   ```

8. **创建 Pull Request**
   - 在 GitHub 上创建 Pull Request
   - 详细描述您的更改
   - 引用相关的 Issue（如有）
   - 等待代码审查

### 📝 代码规范

#### Python 代码风格

- 遵循 [PEP 8](https://www.python.org/dev/peps/pep-0008/) 规范
- 使用 4 个空格缩进（不使用 Tab）
- 行长度限制在 120 字符以内
- 函数和类添加文档字符串（docstring）
- 使用有意义的变量和函数名

#### 示例代码

```python
def process_image(image_path):
    """
    处理图片并返回处理结果

    Args:
        image_path (str): 图片文件路径

    Returns:
        PIL.Image: 处理后的图片对象

    Raises:
        FileNotFoundError: 当图片文件不存在时
    """
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"图片文件不存在: {image_path}")

    # 处理逻辑...
    return processed_image
```

#### 模块化设计

- 新功能应该作为独立的 Mixin 类添加到 `src/` 目录
- 保持功能模块的单一职责
- 在 `src/__init__.py` 中集成新的 Mixin

### 🧪 测试

- 在提交 PR 前，在多个平台上测试您的代码（如果可能）
- 测试边界情况和错误处理
- 确保不会引入新的 bug 或破坏现有功能

### 📚 文档

如果您的更改影响用户使用：

- 更新 README.md
- 在 CHANGELOG.md 中记录更改
- 添加或更新代码注释
- 如果是新功能，考虑添加使用示例

### 💬 沟通

- 在开始重大更改前，最好先创建 Issue 讨论
- 保持友好和专业的沟通态度
- 及时回复代码审查的评论

### ❓ 需要帮助？

如果您有任何问题：

- 查看 [README.md](README.md) 了解项目详情
- 在 Issues 中搜索类似问题
- 创建新的 Issue 提问

---

## English

Thank you for your interest in contributing to PhotosViewer! We welcome all forms of contributions.

### 🌟 How to Contribute

#### Bug Reports

If you find a bug:

1. Search in [Issues](https://github.com/MitaHill/PhotosViewer/issues) to ensure it hasn't been reported
2. Create a new Issue with:
   - Detailed description of the problem
   - Steps to reproduce
   - Expected vs actual behavior
   - System environment (OS, Python version, etc.)
   - Relevant error messages or screenshots

#### Feature Requests

If you have an idea for a new feature:

1. Search Issues for similar suggestions
2. Create a new Feature Request Issue
3. Describe the feature's purpose and expected behavior
4. Provide use case examples if possible

#### Pull Requests

We welcome code contributions! Please follow these steps:

1. **Fork the project**
   ```bash
   # Fork on GitHub
   # Then clone your fork
   git clone https://github.com/your-username/PhotosViewer.git
   cd PhotosViewer
   ```

2. **Create a branch**
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/your-bug-fix
   ```

3. **Set up development environment**
   ```bash
   # Create virtual environment
   python -m venv venv

   # Activate virtual environment
   # Windows:
   venv\Scripts\activate
   # Linux/Mac:
   source venv/bin/activate

   # Install dependencies
   pip install -r requirements.txt
   ```

4. **Make changes**
   - Write clear, maintainable code
   - Follow project code style
   - Add necessary comments and docstrings
   - Ensure cross-platform compatibility

5. **Test your changes**
   ```bash
   # Run the application
   python app.py

   # Test different scenarios
   # Check for errors or warnings
   ```

6. **Commit changes**
   ```bash
   git add .
   git commit -m "type: brief description

   Detailed description of your changes and reasons"
   ```

   Commit message format:
   - `feat: add new feature`
   - `fix: bug fix`
   - `docs: documentation update`
   - `style: code formatting`
   - `refactor: code refactoring`
   - `perf: performance improvement`
   - `test: add tests`
   - `chore: build/tools changes`

7. **Push to GitHub**
   ```bash
   git push origin feature/your-feature-name
   ```

8. **Create Pull Request**
   - Create PR on GitHub
   - Describe your changes in detail
   - Reference related Issues (if any)
   - Wait for code review

### 📝 Code Standards

#### Python Code Style

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- Use 4 spaces for indentation (no tabs)
- Limit line length to 120 characters
- Add docstrings to functions and classes
- Use meaningful variable and function names

#### Example Code

```python
def process_image(image_path):
    """
    Process image and return result

    Args:
        image_path (str): Path to image file

    Returns:
        PIL.Image: Processed image object

    Raises:
        FileNotFoundError: When image file doesn't exist
    """
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image file not found: {image_path}")

    # Processing logic...
    return processed_image
```

#### Modular Design

- New features should be added as separate Mixin classes in `src/` directory
- Maintain single responsibility principle
- Integrate new Mixin in `src/__init__.py`

### 🧪 Testing

- Test your code on multiple platforms before submitting PR (if possible)
- Test edge cases and error handling
- Ensure no new bugs or breaking changes

### 📚 Documentation

If your changes affect user experience:

- Update README.md
- Record changes in CHANGELOG.md
- Add or update code comments
- Consider adding usage examples for new features

### 💬 Communication

- Discuss major changes in an Issue before starting
- Maintain friendly and professional communication
- Respond to code review comments promptly

### ❓ Need Help?

If you have questions:

- Check [README.md](README.md) for project details
- Search Issues for similar questions
- Create a new Issue to ask

---

## 行为准则 / Code of Conduct

### 我们的承诺 / Our Pledge

为了营造一个开放和友好的环境，我们承诺让参与项目和社区的每个人都不受骚扰，无论年龄、体型、残疾、族裔、性别特征、性别认同与表达、经验水平、教育程度、社会经济地位、国籍、个人外貌、种族、宗教或性取向如何。

In the interest of fostering an open and welcoming environment, we pledge to make participation in our project and community a harassment-free experience for everyone.

### 我们的标准 / Our Standards

积极行为包括 / Positive behaviors include:
- 使用友好和包容的语言 / Using welcoming and inclusive language
- 尊重不同的观点和经验 / Respecting differing viewpoints and experiences
- 优雅地接受建设性批评 / Gracefully accepting constructive criticism
- 关注对社区最有利的事情 / Focusing on what is best for the community
- 对其他社区成员表示同情 / Showing empathy towards other community members

不可接受的行为包括 / Unacceptable behaviors include:
- 使用性化的语言或图像 / Use of sexualized language or imagery
- 挑衅、侮辱或贬损性评论 / Trolling, insulting or derogatory comments
- 公开或私下骚扰 / Public or private harassment
- 未经许可发布他人的私人信息 / Publishing others' private information without permission

---

感谢您的贡献！/ Thank you for contributing!

**项目维护者 / Project Maintainer**: Clash / 善良米塔
