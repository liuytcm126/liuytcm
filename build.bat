@echo off
chcp 65001 >nul
REM 神经内科量表评估系统构建脚本 (Windows)
REM 开发者：LIUYING

echo 神经内科量表评估系统 - 构建脚本
echo 开发者：LIUYING
echo ======================================

REM 检查Python环境
python --version >nul 2>&1
if errorlevel 1 (
    echo 错误：未找到Python，请先安装Python 3.8或更高版本
    pause
    exit /b 1
)

echo Python版本：
python --version

REM 检查pip
pip --version >nul 2>&1
if errorlevel 1 (
    echo 错误：未找到pip，请先安装pip
    pause
    exit /b 1
)

REM 升级pip
echo 升级pip...
python -m pip install --upgrade pip

REM 安装依赖
echo 安装项目依赖...
pip install -r requirements.txt

REM 安装PyInstaller（如果未安装）
echo 检查PyInstaller...
pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo 安装PyInstaller...
    pip install pyinstaller
)

REM 安装PIL（用于图标生成）
echo 检查Pillow...
pip show Pillow >nul 2>&1
if errorlevel 1 (
    echo 安装Pillow...
    pip install Pillow
)

REM 运行构建
echo 开始构建...
python build_config.py

echo 构建完成！
echo 请查看dist目录中的输出文件
pause