#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
神经内科量表评估系统 - 打包配置
开发人员：LIUYING
版本：1.0.0
描述：PyInstaller打包配置和构建脚本
"""

import os
import sys
import shutil
from pathlib import Path
import subprocess
import json
from datetime import datetime

class BuildConfig:
    """构建配置管理器"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.project_name = "神经内科量表评估系统"
        self.app_name = "NeuroScales"
        self.version = "1.0.0"
        self.author = "LIUYING"
        self.description = "专业的神经内科临床量表评估工具"
        
        # 路径配置
        self.main_script = self.project_root / "main.py"
        self.build_dir = self.project_root / "build"
        self.dist_dir = self.project_root / "dist"
        self.icon_file = self.project_root / "assets" / "icon.ico"
        self.assets_dir = self.project_root / "assets"
        
        # 确保目录存在
        self.assets_dir.mkdir(exist_ok=True)
        
    def clean_build_dirs(self):
        """清理构建目录"""
        print("清理构建目录...")
        for dir_path in [self.build_dir, self.dist_dir]:
            if dir_path.exists():
                shutil.rmtree(dir_path)
                print(f"已删除: {dir_path}")
                
    def create_pyinstaller_spec(self):
        """创建PyInstaller规格文件"""
        spec_content = f'''
# -*- mode: python ; coding: utf-8 -*-
from pathlib import Path

block_cipher = None

a = Analysis(
    ['{self.main_script.as_posix()}'],
    pathex=['{self.project_root.as_posix()}'],
    binaries=[],
    datas=[
        ('scales', 'scales'),
        ('assets', 'assets'),
    ],
    hiddenimports=[
        'tkinter',
        'tkinter.ttk',
        'tkinter.messagebox',
        'tkinter.filedialog',
        'tkinter.scrolledtext',
        'matplotlib',
        'matplotlib.backends.backend_tkagg',
        'matplotlib.pyplot',
        'matplotlib.dates',
        'matplotlib.font_manager',
        'pandas',
        'numpy',
        'json',
        'datetime',
        'pathlib',
        'webbrowser',
        'openpyxl',
        'xlsxwriter',
        'PIL',
        'PIL.Image',
        'PIL.ImageTk'
    ],
    hookspath=[],
    hooksconfig={{}},
    runtime_hooks=[],
    excludes=[
        'PyQt6',
        'PyQt6.QtCore',
        'PyQt6.QtGui', 
        'PyQt6.QtWidgets',
        'PyQt6.QtOpenGL',
        'PyQt6.QtPrintSupport',
        'PyQt6.QtSvg',
        'PyQt6.QtTest',
        'PyQt6.QtXml'
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='{self.app_name}',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='{self.icon_file.as_posix()}' if Path('{self.icon_file.as_posix()}').exists() else None,
    version='version_info.txt' if Path('version_info.txt').exists() else None,
)
'''
        
        spec_file = self.project_root / f"{self.app_name}.spec"
        with open(spec_file, 'w', encoding='utf-8') as f:
            f.write(spec_content)
        print(f"已创建规格文件: {spec_file}")
        return spec_file
        
    def create_version_info(self):
        """创建版本信息文件（Windows）"""
        version_info = f'''
# UTF-8
#
# For more details about fixed file info 'ffi' see:
# http://msdn.microsoft.com/en-us/library/ms646997.aspx
VSVersionInfo(
  ffi=FixedFileInfo(
    # filevers and prodvers should be always a tuple with four items: (1, 2, 3, 4)
    # Set not needed items to zero 0.
    filevers=(1, 0, 0, 0),
    prodvers=(1, 0, 0, 0),
    # Contains a bitmask that specifies the valid bits 'flags'r
    mask=0x3f,
    # Contains a bitmask that specifies the Boolean attributes of the file.
    flags=0x0,
    # The operating system for which this file was designed.
    # 0x4 - NT and there is no need to change it.
    OS=0x4,
    # The general type of file.
    # 0x1 - the file is an application.
    fileType=0x1,
    # The function of the file.
    # 0x0 - the function is not defined for this fileType
    subtype=0x0,
    # Creation date and time stamp.
    date=(0, 0)
    ),
  kids=[
    StringFileInfo(
      [
      StringTable(
        u'040904B0',
        [StringStruct(u'CompanyName', u'{self.author}'),
        StringStruct(u'FileDescription', u'{self.description}'),
        StringStruct(u'FileVersion', u'{self.version}'),
        StringStruct(u'InternalName', u'{self.app_name}'),
        StringStruct(u'LegalCopyright', u'© 2024 {self.author}. All rights reserved.'),
        StringStruct(u'OriginalFilename', u'{self.app_name}.exe'),
        StringStruct(u'ProductName', u'{self.project_name}'),
        StringStruct(u'ProductVersion', u'{self.version}')])
      ]), 
    VarFileInfo([VarStruct(u'Translation', [1033, 1200])])
  ]
)
'''
        
        version_file = self.project_root / "version_info.txt"
        with open(version_file, 'w', encoding='utf-8') as f:
            f.write(version_info)
        print(f"已创建版本信息文件: {version_file}")
        return version_file
        
    def check_icon(self):
        """检查并创建图标文件"""
        if not self.icon_file.exists():
            print(f"图标文件不存在: {self.icon_file}")
            print("将创建默认图标...")
            self.create_default_icon()
        else:
            print(f"图标文件已存在: {self.icon_file}")
            
    def create_default_icon(self):
        """创建默认图标"""
        try:
            from PIL import Image, ImageDraw, ImageFont
            
            # 创建图标图像
            size = 256
            img = Image.new('RGBA', (size, size), (46, 134, 171, 255))  # 医疗蓝背景
            draw = ImageDraw.Draw(img)
            
            # 绘制简单的医疗十字图标
            cross_color = (255, 255, 255, 255)  # 白色
            cross_width = size // 8
            cross_length = size // 2
            
            # 水平线
            x1 = (size - cross_length) // 2
            y1 = (size - cross_width) // 2
            x2 = x1 + cross_length
            y2 = y1 + cross_width
            draw.rectangle([x1, y1, x2, y2], fill=cross_color)
            
            # 垂直线
            x1 = (size - cross_width) // 2
            y1 = (size - cross_length) // 2
            x2 = x1 + cross_width
            y2 = y1 + cross_length
            draw.rectangle([x1, y1, x2, y2], fill=cross_color)
            
            # 保存为ICO格式
            img.save(self.icon_file, format='ICO', sizes=[(256, 256), (128, 128), (64, 64), (32, 32), (16, 16)])
            print(f"已创建默认图标: {self.icon_file}")
            
        except ImportError:
            print("PIL库未安装，无法创建图标。请手动添加icon.ico文件到assets目录")
        except Exception as e:
            print(f"创建图标失败: {e}")
            
    def create_installer_script(self):
        """创建安装程序脚本"""
        # Windows NSIS脚本
        nsis_script = f'''
; 神经内科量表评估系统安装脚本
; 开发者：{self.author}

!define APP_NAME "{self.project_name}"
!define APP_VERSION "{self.version}"
!define APP_PUBLISHER "{self.author}"
!define APP_EXE "{self.app_name}.exe"

Name "${{APP_NAME}}"
OutFile "${{APP_NAME}}_v${{APP_VERSION}}_Setup.exe"
InstallDir "$PROGRAMFILES\\${{APP_NAME}}"
RequestExecutionLevel admin

Page directory
Page instfiles

Section "MainSection" SEC01
  SetOutPath "$INSTDIR"
  File /r "dist\\{self.app_name}\\*"
  
  ; 创建桌面快捷方式
  CreateShortCut "$DESKTOP\\${{APP_NAME}}.lnk" "$INSTDIR\\${{APP_EXE}}"
  
  ; 创建开始菜单快捷方式
  CreateDirectory "$SMPROGRAMS\\${{APP_NAME}}"
  CreateShortCut "$SMPROGRAMS\\${{APP_NAME}}\\${{APP_NAME}}.lnk" "$INSTDIR\\${{APP_EXE}}"
  CreateShortCut "$SMPROGRAMS\\${{APP_NAME}}\\卸载.lnk" "$INSTDIR\\Uninstall.exe"
  
  ; 写入卸载信息
  WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${{APP_NAME}}" "DisplayName" "${{APP_NAME}}"
  WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${{APP_NAME}}" "UninstallString" "$INSTDIR\\Uninstall.exe"
  WriteUninstaller "$INSTDIR\\Uninstall.exe"
SectionEnd

Section "Uninstall"
  Delete "$INSTDIR\\*.*"
  RMDir /r "$INSTDIR"
  Delete "$DESKTOP\\${{APP_NAME}}.lnk"
  RMDir /r "$SMPROGRAMS\\${{APP_NAME}}"
  DeleteRegKey HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${{APP_NAME}}"
SectionEnd
'''
        
        nsis_file = self.project_root / "installer.nsi"
        with open(nsis_file, 'w', encoding='utf-8') as f:
            f.write(nsis_script)
        print(f"已创建NSIS安装脚本: {nsis_file}")
        
    def create_readme(self):
        """创建README文件"""
        readme_content = f'''
# {self.project_name}

## 简介

{self.description}

## 版本信息

- 版本：{self.version}
- 开发者：{self.author}
- 发布日期：{datetime.now().strftime('%Y年%m月%d日')}

## 系统要求

- 操作系统：Windows 10/11, macOS 10.14+, Linux (Ubuntu 18.04+)
- 内存：至少 4GB RAM
- 存储空间：至少 500MB 可用空间
- 显示器：1024x768 分辨率或更高

## 功能特性

### 量表评估
- **认知功能评估**：MMSE、MoCA、CDR等标准量表
- **情绪障碍评估**：HAMD-17、HAMA、SDS等专业量表
- **运动功能评估**：UPDRS-III、Berg平衡量表、Tinetti评估

### 数据管理
- 智能评分计算和结果分析
- 完整的数据存储和检索功能
- 多格式数据导出（Excel、CSV、JSON、PDF）
- 统计分析和可视化图表

### 用户体验
- 直观友好的图形界面
- 详细的使用说明和帮助文档
- 多平台支持和便携版本

## 安装说明

### Windows系统
1. 下载安装包 `{self.project_name}_v{self.version}_Setup.exe`
2. 右键选择"以管理员身份运行"
3. 按照安装向导完成安装
4. 从桌面或开始菜单启动程序

### macOS系统
1. 下载 `{self.app_name}_v{self.version}_macOS.dmg`
2. 双击打开DMG文件
3. 将应用拖拽到Applications文件夹
4. 从Launchpad或Applications文件夹启动

### Linux系统
1. 下载 `{self.app_name}_v{self.version}_Linux.tar.gz`
2. 解压到目标目录
3. 运行 `chmod +x {self.app_name}` 添加执行权限
4. 执行 `./{self.app_name}` 启动程序

### 便携版
1. 下载便携版压缩包
2. 解压到任意目录
3. 直接运行主程序文件

## 使用指南

### 快速开始
1. 启动程序后，选择要进行的量表评估类型
2. 填写患者基本信息
3. 按照量表要求逐项评分
4. 查看自动生成的评估结果和建议
5. 保存或导出评估报告

### 数据管理
- 在"数据管理"菜单中查看历史评估记录
- 使用筛选功能快速定位特定数据
- 生成统计分析报告和可视化图表
- 导出数据用于进一步分析

## 技术支持

如遇到问题或需要技术支持，请联系：
- 邮箱：support@neuroscales.com
- 官网：www.neuroscales.com
- 用户手册：www.neuroscales.com/docs

## 版权信息

© 2024 {self.author}. 保留所有权利.

本软件仅供医疗专业人员使用，用于临床评估和科研目的。
使用本软件进行临床决策时，请结合专业医学判断。
'''
        
        readme_file = self.project_root / "README.md"
        with open(readme_file, 'w', encoding='utf-8') as f:
            f.write(readme_content)
        print(f"已创建README文件: {readme_file}")
        
    def create_license(self):
        """创建许可证文件"""
        license_content = f'''
MIT License

Copyright (c) 2024 {self.author}

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''
        
        license_file = self.project_root / "LICENSE"
        with open(license_file, 'w', encoding='utf-8') as f:
            f.write(license_content)
        print(f"已创建许可证文件: {license_file}")
        
    def build_executable(self):
        """构建可执行文件"""
        print("开始构建可执行文件...")
        
        # 创建规格文件
        spec_file = self.create_pyinstaller_spec()
        
        # 运行PyInstaller
        cmd = [sys.executable, '-m', 'PyInstaller', '--clean', str(spec_file)]
        
        try:
            result = subprocess.run(cmd, cwd=self.project_root, capture_output=True, text=True)
            if result.returncode == 0:
                print("构建成功！")
                print(f"可执行文件位置: {self.dist_dir / self.app_name}")
                return True
            else:
                print(f"构建失败: {result.stderr}")
                return False
        except Exception as e:
            print(f"构建过程出错: {e}")
            return False
            
    def create_portable_package(self):
        """创建便携版打包"""
        print("创建便携版打包...")
        
        portable_dir = self.project_root / f"{self.app_name}_v{self.version}_Portable"
        if portable_dir.exists():
            shutil.rmtree(portable_dir)
        
        # 检查可执行文件是否存在
        exe_file = self.dist_dir / self.app_name
        if exe_file.exists():
            portable_dir.mkdir(exist_ok=True)
            if exe_file.is_file():
                shutil.copy2(exe_file, portable_dir)
            else:
                shutil.copytree(exe_file, portable_dir / self.app_name)
        
            # 添加便携版说明
            portable_readme = portable_dir / "便携版说明.txt"
            with open(portable_readme, 'w', encoding='utf-8') as f:
                f.write(f'''
{self.project_name} 便携版 v{self.version}

这是便携版本，无需安装即可使用。

使用方法：
1. 解压到任意目录
2. 双击 {self.app_name}.exe 启动程序
3. 首次运行会自动创建数据目录

注意事项：
- 请确保有足够的磁盘空间存储评估数据
- 建议定期备份data和results目录
- 如需卸载，直接删除整个文件夹即可

技术支持：support@neuroscales.com
''')
        
            # 创建压缩包
            archive_name = f"{self.app_name}_v{self.version}_Portable"
            shutil.make_archive(archive_name, 'zip', portable_dir)
            print(f"便携版已创建: {archive_name}.zip")
        else:
            print("未找到可执行文件，请先构建")
            
    def run_full_build(self):
        """执行完整构建流程"""
        print(f"开始构建 {self.project_name} v{self.version}")
        print("=" * 50)
        
        # 1. 清理构建目录
        self.clean_build_dirs()
        
        # 2. 检查和创建图标
        self.check_icon()
        
        # 3. 创建版本信息
        self.create_version_info()
        
        # 4. 创建文档
        self.create_readme()
        self.create_license()
        
        # 5. 创建安装脚本
        self.create_installer_script()
        
        # 6. 构建可执行文件
        if self.build_executable():
            # 7. 创建便携版
            self.create_portable_package()
            
            print("\n构建完成！")
            print(f"输出目录: {self.dist_dir}")
            print("\n生成的文件：")
            print(f"- 可执行文件: {self.dist_dir / self.app_name}")
            print(f"- 便携版: {self.app_name}_v{self.version}_Portable.zip")
            print(f"- 安装脚本: installer.nsi")
            print(f"- 说明文档: README.md")
        else:
            print("构建失败，请检查错误信息")

if __name__ == "__main__":
    builder = BuildConfig()
    builder.run_full_build()