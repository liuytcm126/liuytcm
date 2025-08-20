# 构建说明

## 环境要求

- Python 3.8 或更高版本
- pip 包管理器
- 至少 2GB 可用磁盘空间

## 构建步骤

### 自动构建（推荐）

**Windows系统：**
```cmd
build.bat
```

**macOS/Linux系统：**
```bash
chmod +x build.sh
./build.sh
```

### 手动构建

1. 安装依赖：
```bash
pip install -r requirements.txt
pip install pyinstaller Pillow
```

2. 运行构建脚本：
```bash
python build_config.py
```

## 输出文件

构建完成后，将在以下位置生成文件：

- `dist/NeuroScales/` - 可执行文件目录
- `NeuroScales_v1.0.0_Portable.zip` - 便携版压缩包
- `installer.nsi` - Windows安装程序脚本
- `README.md` - 用户说明文档
- `LICENSE` - 软件许可证

## 故障排除

### 常见问题

1. **Python未找到**
   - 确保已安装Python 3.8+
   - 检查PATH环境变量

2. **依赖安装失败**
   - 升级pip：`pip install --upgrade pip`
   - 使用国内镜像：`pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt`

3. **构建失败**
   - 检查磁盘空间是否充足
   - 确保所有源文件完整
   - 查看错误日志定位问题

4. **图标生成失败**
   - 手动安装Pillow：`pip install Pillow`
   - 或手动添加icon.ico文件到assets目录

### 获取帮助

如遇到其他问题，请联系：
- 邮箱：support@neuroscales.com
- 项目主页：www.neuroscales.com