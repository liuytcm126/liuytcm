#!/bin/bash
# 神经内科量表评估系统构建脚本
# 开发人员：LIUYING
# 版本：1.0.0               

echo "神经内科量表评估系统构建脚本"
echo "开发人员：LIUYING"
echo "版本：1.0.0"
echo "=============================="

# 检查Python环境
echo "检查Python环境..."
python3 --version
if [ $? -ne 0 ]; then
    echo "错误：未找到Python3"
    exit 1
fi

# 检查依赖包
echo "检查依赖包..."
pip3 install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "错误：依赖包安装失败"
    exit 1
fi

# 安装PyInstaller
echo "安装PyInstaller..."
pip3 install pyinstaller
if [ $? -ne 0 ]; then
    echo "错误：PyInstaller安装失败"
    exit 1
fi

# 执行构建
echo "开始构建..."
python3 build_config.py
if [ $? -eq 0 ]; then
    echo "构建成功！"
else
    echo "构建失败！"
    exit 1
fi

echo "构建完成！"
echo "请查看dist目录中的输出文件"