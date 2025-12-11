Write-Output "##active_line7##"
#!/usr/bin/env python3
Write-Output "##active_line8##"
# -*- coding: utf-8 -*-
Write-Output "##active_line9##"
"""
Write-Output "##active_line10##"
PhotosViewer 自动构建脚本
Write-Output "##active_line11##"
支持构建多个平台的可执行文件
Write-Output "##active_line12##"
"""
Write-Output "##active_line13##"
Write-Output "##active_line14##"
import os
Write-Output "##active_line15##"
import sys
Write-Output "##active_line16##"
import subprocess
Write-Output "##active_line17##"
import platform
Write-Output "##active_line18##"
import shutil
Write-Output "##active_line19##"
from pathlib import Path
Write-Output "##active_line20##"
Write-Output "##active_line21##"
def run_command(cmd, cwd=None):
Write-Output "##active_line22##"
    """运行命令并返回输出"""
Write-Output "##active_line23##"
    print(f"运行命令: {cmd}")
Write-Output "##active_line24##"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=cwd)
Write-Output "##active_line25##"
    if result.returncode != 0:
Write-Output "##active_line26##"
        print(f"错误: {result.stderr}")
Write-Output "##active_line27##"
        return False
Write-Output "##active_line28##"
    print(f"输出: {result.stdout}")
Write-Output "##active_line29##"
    return True
Write-Output "##active_line30##"
Write-Output "##active_line31##"
def install_dependencies():
Write-Output "##active_line32##"
    """安装依赖"""
Write-Output "##active_line33##"
    print("安装依赖...")
Write-Output "##active_line34##"
Write-Output "##active_line35##"
    # 安装 Python 依赖
Write-Output "##active_line36##"
    if not run_command("pip install -r requirements.txt"):
Write-Output "##active_line37##"
        return False
Write-Output "##active_line38##"
Write-Output "##active_line39##"
    # 安装 PyInstaller
Write-Output "##active_line40##"
    if not run_command("pip install pyinstaller>=5.0.0"):
Write-Output "##active_line41##"
        return False
Write-Output "##active_line42##"
Write-Output "##active_line43##"
    return True
Write-Output "##active_line44##"
Write-Output "##active_line45##"
def build_windows():
Write-Output "##active_line46##"
    """构建 Windows 版本"""
Write-Output "##active_line47##"
    print("构建 Windows 版本...")
Write-Output "##active_line48##"
Write-Output "##active_line49##"
    # Windows 特定依赖
Write-Output "##active_line50##"
    if not run_command("pip install pywin32>=300"):
Write-Output "##active_line51##"
        return False
Write-Output "##active_line52##"
Write-Output "##active_line53##"
    # 构建可执行文件
Write-Output "##active_line54##"
    build_cmd = (
Write-Output "##active_line55##"
        'pyinstaller --onefile --windowed '
Write-Output "##active_line56##"
        '--name "PhotosViewer" '
Write-Output "##active_line57##"
        '--icon "assets/icon.ico" '
Write-Output "##active_line58##"
        '--add-data "assets;assets" '
Write-Output "##active_line59##"
        '--add-data "src;src" '
Write-Output "##active_line60##"
        '--hidden-import PIL '
Write-Output "##active_line61##"
        '--hidden-import PIL._tkinter_finder '
Write-Output "##active_line62##"
        'app.py'
Write-Output "##active_line63##"
    )
Write-Output "##active_line64##"
Write-Output "##active_line65##"
    if not run_command(build_cmd):
Write-Output "##active_line66##"
        return False
Write-Output "##active_line67##"
Write-Output "##active_line68##"
    # 移动构建结果
Write-Output "##active_line69##"
    dist_dir = Path("dist")
Write-Output "##active_line70##"
    if dist_dir.exists():
Write-Output "##active_line71##"
        windows_dir = Path("builds/windows")
Write-Output "##active_line72##"
        windows_dir.mkdir(parents=True, exist_ok=True)
Write-Output "##active_line73##"
Write-Output "##active_line74##"
        for file in dist_dir.glob("*.exe"):
Write-Output "##active_line75##"
            shutil.copy2(file, windows_dir / file.name)
Write-Output "##active_line76##"
            print(f"已复制: {file.name}")
Write-Output "##active_line77##"
Write-Output "##active_line78##"
    return True
Write-Output "##active_line79##"
Write-Output "##active_line80##"
def build_linux():
Write-Output "##active_line81##"
    """构建 Linux 版本"""
Write-Output "##active_line82##"
    print("构建 Linux 版本...")
Write-Output "##active_line83##"
Write-Output "##active_line84##"
    # 构建可执行文件
Write-Output "##active_line85##"
    build_cmd = (
Write-Output "##active_line86##"
        'pyinstaller --onefile '
Write-Output "##active_line87##"
        '--name "PhotosViewer" '
Write-Output "##active_line88##"
        '--add-data "assets:assets" '
Write-Output "##active_line89##"
        '--add-data "src:src" '
Write-Output "##active_line90##"
        '--hidden-import PIL '
Write-Output "##active_line91##"
        '--hidden-import PIL._tkinter_finder '
Write-Output "##active_line92##"
        'app.py'
Write-Output "##active_line93##"
    )
Write-Output "##active_line94##"
Write-Output "##active_line95##"
    if not run_command(build_cmd):
Write-Output "##active_line96##"
        return False
Write-Output "##active_line97##"
Write-Output "##active_line98##"
    # 移动构建结果
Write-Output "##active_line99##"
    dist_dir = Path("dist")
Write-Output "##active_line100##"
    if dist_dir.exists():
Write-Output "##active_line101##"
        linux_dir = Path("builds/linux")
Write-Output "##active_line102##"
        linux_dir.mkdir(parents=True, exist_ok=True)
Write-Output "##active_line103##"
Write-Output "##active_line104##"
        for file in dist_dir.glob("PhotosViewer"):
Write-Output "##active_line105##"
            shutil.copy2(file, linux_dir / file.name)
Write-Output "##active_line106##"
            print(f"已复制: {file.name}")
Write-Output "##active_line107##"
Write-Output "##active_line108##"
    return True
Write-Output "##active_line109##"
Write-Output "##active_line110##"
def build_macos():
Write-Output "##active_line111##"
    """构建 macOS 版本"""
Write-Output "##active_line112##"
    print("构建 macOS 版本...")
Write-Output "##active_line113##"
Write-Output "##active_line114##"
    # 构建可执行文件
Write-Output "##active_line115##"
    build_cmd = (
Write-Output "##active_line116##"
        'pyinstaller --onefile --windowed '
Write-Output "##active_line117##"
        '--name "PhotosViewer" '
Write-Output "##active_line118##"
        '--icon "assets/icon.icns" '
Write-Output "##active_line119##"
        '--add-data "assets:assets" '
Write-Output "##active_line120##"
        '--add-data "src:src" '
Write-Output "##active_line121##"
        '--hidden-import PIL '
Write-Output "##active_line122##"
        '--hidden-import PIL._tkinter_finder '
Write-Output "##active_line123##"
        'app.py'
Write-Output "##active_line124##"
    )
Write-Output "##active_line125##"
Write-Output "##active_line126##"
    if not run_command(build_cmd):
Write-Output "##active_line127##"
        return False
Write-Output "##active_line128##"
Write-Output "##active_line129##"
    # 移动构建结果
Write-Output "##active_line130##"
    dist_dir = Path("dist")
Write-Output "##active_line131##"
    if dist_dir.exists():
Write-Output "##active_line132##"
        macos_dir = Path("builds/macos")
Write-Output "##active_line133##"
        macos_dir.mkdir(parents=True, exist_ok=True)
Write-Output "##active_line134##"
Write-Output "##active_line135##"
        for file in dist_dir.glob("PhotosViewer"):
Write-Output "##active_line136##"
            shutil.copy2(file, macos_dir / file.name)
Write-Output "##active_line137##"
            print(f"已复制: {file.name}")
Write-Output "##active_line138##"
Write-Output "##active_line139##"
    return True
Write-Output "##active_line140##"
Write-Output "##active_line141##"
def create_archive():
Write-Output "##active_line142##"
    """创建压缩包"""
Write-Output "##active_line143##"
    print("创建压缩包...")
Write-Output "##active_line144##"
Write-Output "##active_line145##"
    builds_dir = Path("builds")
Write-Output "##active_line146##"
    if not builds_dir.exists():
Write-Output "##active_line147##"
        print("构建目录不存在")
Write-Output "##active_line148##"
        return False
Write-Output "##active_line149##"
Write-Output "##active_line150##"
    import zipfile
Write-Output "##active_line151##"
    import tarfile
Write-Output "##active_line152##"
Write-Output "##active_line153##"
    # 为每个平台创建压缩包
Write-Output "##active_line154##"
    for platform_dir in builds_dir.iterdir():
Write-Output "##active_line155##"
        if platform_dir.is_dir():
Write-Output "##active_line156##"
            platform_name = platform_dir.name
Write-Output "##active_line157##"
Write-Output "##active_line158##"
            if platform_name == "windows":
Write-Output "##active_line159##"
                # Windows 使用 zip
Write-Output "##active_line160##"
                zip_path = builds_dir / f"PhotosViewer_{platform_name}.zip"
Write-Output "##active_line161##"
                with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
Write-Output "##active_line162##"
                    for file in platform_dir.rglob("*"):
Write-Output "##active_line163##"
                        if file.is_file():
Write-Output "##active_line164##"
                            arcname = file.relative_to(platform_dir)
Write-Output "##active_line165##"
                            zipf.write(file, arcname)
Write-Output "##active_line166##"
                print(f"已创建: {zip_path.name}")
Write-Output "##active_line167##"
Write-Output "##active_line168##"
            else:
Write-Output "##active_line169##"
                # Linux/macOS 使用 tar.gz
Write-Output "##active_line170##"
                tar_path = builds_dir / f"PhotosViewer_{platform_name}.tar.gz"
Write-Output "##active_line171##"
                with tarfile.open(tar_path, 'w:gz') as tar:
Write-Output "##active_line172##"
                    for file in platform_dir.rglob("*"):
Write-Output "##active_line173##"
                        if file.is_file():
Write-Output "##active_line174##"
                            arcname = file.relative_to(platform_dir)
Write-Output "##active_line175##"
                            tar.add(file, arcname=arcname)
Write-Output "##active_line176##"
                print(f"已创建: {tar_path.name}")
Write-Output "##active_line177##"
Write-Output "##active_line178##"
    return True
Write-Output "##active_line179##"
Write-Output "##active_line180##"
def main():
Write-Output "##active_line181##"
    """主函数"""
Write-Output "##active_line182##"
    print("开始构建 PhotosViewer...")
Write-Output "##active_line183##"
Write-Output "##active_line184##"
    # 清理之前的构建
Write-Output "##active_line185##"
    for dir_name in ["dist", "build", "__pycache__"]:
Write-Output "##active_line186##"
        if Path(dir_name).exists():
Write-Output "##active_line187##"
            shutil.rmtree(dir_name)
Write-Output "##active_line188##"
Write-Output "##active_line189##"
    # 创建构建目录
Write-Output "##active_line190##"
    Path("builds").mkdir(exist_ok=True)
Write-Output "##active_line191##"
Write-Output "##active_line192##"
    # 安装依赖
Write-Output "##active_line193##"
    if not install_dependencies():
Write-Output "##active_line194##"
        print("依赖安装失败")
Write-Output "##active_line195##"
        return 1
Write-Output "##active_line196##"
Write-Output "##active_line197##"
    # 根据当前平台构建
Write-Output "##active_line198##"
    current_platform = platform.system().lower()
Write-Output "##active_line199##"
    success = False
Write-Output "##active_line200##"
Write-Output "##active_line201##"
    if current_platform == "windows":
Write-Output "##active_line202##"
        success = build_windows()
Write-Output "##active_line203##"
    elif current_platform == "linux":
Write-Output "##active_line204##"
        success = build_linux()
Write-Output "##active_line205##"
    elif current_platform == "darwin":
Write-Output "##active_line206##"
        success = build_macos()
Write-Output "##active_line207##"
    else:
Write-Output "##active_line208##"
        print(f"不支持的平台: {current_platform}")
Write-Output "##active_line209##"
        return 1
Write-Output "##active_line210##"
Write-Output "##active_line211##"
    if not success:
Write-Output "##active_line212##"
        print("构建失败")
Write-Output "##active_line213##"
        return 1
Write-Output "##active_line214##"
Write-Output "##active_line215##"
    # 创建压缩包
Write-Output "##active_line216##"
    if not create_archive():
Write-Output "##active_line217##"
        print("创建压缩包失败")
Write-Output "##active_line218##"
        return 1
Write-Output "##active_line219##"
Write-Output "##active_line220##"
    print("构建完成!")
Write-Output "##active_line221##"
    return 0
Write-Output "##active_line222##"
Write-Output "##active_line223##"
if __name__ == "__main__":
Write-Output "##active_line224##"
    sys.exit(main())
Write-Output "##active_line225##"
