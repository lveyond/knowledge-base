# 📦 Windows应用程序打包指南

本指南介绍如何将智能知识库系统打包成Windows可执行程序，方便用户一键安装和使用。

## 🎯 打包方案

我们提供了两种打包方案：

### 方案一：使用PyInstaller打包成独立exe（推荐）

**优点：**
- 用户无需安装Python环境
- 一键运行，使用简单
- 所有依赖都打包在一起

**缺点：**
- 打包文件较大（约500MB-1GB）
- 首次打包时间较长

### 方案二：使用安装脚本（简单方案）

**优点：**
- 打包文件小
- 安装快速

**缺点：**
- 用户需要先安装Python环境

## 📋 方案一：PyInstaller打包（推荐）

### 前置要求

1. **Python 3.11或更高版本**
2. **安装打包工具**：
   ```bash
   pip install pyinstaller
   ```

### 打包步骤

1. **进入打包脚本目录**：
   ```bash
   cd build_script
   ```

2. **运行打包脚本**：
   ```bash
   build_windows.bat
   ```

3. **等待打包完成**（可能需要10-30分钟）

4. **打包结果**：
   - 打包文件位于项目根目录的 `dist\智能知识库系统\` 目录
   - 包含 `智能知识库系统.exe` 和所有依赖文件

5. **测试打包结果**：
   - 进入 `dist\` 目录
   - 双击 `启动应用.bat` 或直接运行 `智能知识库系统\智能知识库系统.exe`

6. **分发**：
   - 将整个 `dist\` 文件夹压缩成ZIP文件
   - 或者使用Inno Setup等工具创建安装程序

### 自定义打包配置

如果需要修改打包配置，可以编辑 `build_script\build_windows.spec` 文件：

- **修改应用名称**：修改 `name='KnowledgeBase'`
- **添加图标**：在 `icon=None` 处指定图标文件路径
- **隐藏控制台**：将 `console=True` 改为 `console=False`

### 常见问题

**Q: 打包后的exe文件很大？**

A: 这是正常的，因为包含了Python解释器和所有依赖库。可以考虑：
- 使用 `--exclude-module` 排除不需要的模块
- 使用UPX压缩（已在spec文件中启用）

**Q: 打包后无法运行？**

A: 检查以下几点：
1. 确保所有依赖都已正确安装
2. 检查是否有缺失的隐藏导入（hiddenimports）
3. 查看控制台错误信息

**Q: Streamlit应用无法启动？**

A: 确保：
1. Streamlit相关的所有模块都已包含
2. 数据文件（如prompt_templates）已正确复制

## 📋 方案二：安装脚本方案

### 使用步骤

1. **运行简化打包脚本**：
   ```bash
   cd build_script
   build_simple.bat
   ```

2. **打包结果**：
   - 打包文件位于 `dist\智能知识库系统-安装包\` 目录
   - 包含所有必需文件和 `install.bat` 安装脚本

3. **用户安装**：
   - 用户解压文件
   - 双击运行 `install.bat`
   - 脚本会自动安装Python依赖并创建快捷方式

4. **用户使用**：
   - 双击桌面快捷方式启动应用
   - 或运行安装目录下的 `启动应用.bat`

### 安装脚本功能

`build_script\install.bat` 脚本会自动：
1. 检查Python环境
2. 创建安装目录（默认：`%USERPROFILE%\KnowledgeBase`）
3. 复制所有必需文件
4. 安装Python依赖包
5. 创建桌面快捷方式
6. 创建启动脚本

## 🚀 创建安装程序（可选）

如果需要创建专业的Windows安装程序，可以使用以下工具：

### Inno Setup（推荐）

1. **下载Inno Setup**：https://jrsoftware.org/isinfo.php

2. **创建安装脚本**（示例）：
   ```iss
   [Setup]
   AppName=智能知识库系统
   AppVersion=1.0
   DefaultDirName={pf}\KnowledgeBase
   DefaultGroupName=智能知识库系统
   OutputDir=installer
   OutputBaseFilename=KnowledgeBase-Setup
   Compression=lzma2
   SolidCompression=yes

   [Files]
   Source: "dist\智能知识库系统\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs

   [Icons]
   Name: "{group}\智能知识库系统"; Filename: "{app}\启动应用.bat"
   Name: "{commondesktop}\智能知识库系统"; Filename: "{app}\启动应用.bat"

   [Run]
   Filename: "{app}\启动应用.bat"; Description: "启动智能知识库系统"; Flags: nowait postinstall skipifsilent
   ```

3. **编译安装程序**：
   - 在Inno Setup中打开脚本
   - 点击"构建"按钮
   - 生成 `KnowledgeBase-Setup.exe` 安装程序

### NSIS

也可以使用NSIS（Nullsoft Scriptable Install System）创建安装程序。

## 📝 打包检查清单

打包前检查：
- [ ] 所有必需文件都已包含
- [ ] 测试主程序可以正常运行
- [ ] 检查依赖是否完整
- [ ] 确认没有包含敏感信息（如API密钥）

打包后测试：
- [ ] 在干净的Windows系统上测试
- [ ] 测试所有功能是否正常
- [ ] 检查文件大小是否合理
- [ ] 确认启动速度可接受

## 🎁 分发建议

### 文件结构

推荐的分发结构：
```
智能知识库系统-v1.0/
├── 智能知识库系统/          # 主程序文件夹（PyInstaller方案）
│   ├── 智能知识库系统.exe   # 主程序
│   └── [其他依赖文件]
├── 启动应用.bat              # 启动脚本
├── 使用说明.txt              # 使用说明
└── README.txt                # 详细说明（可选）
```

### 用户说明

创建 `使用说明.txt` 文件，包含：
1. 系统要求
2. 安装步骤
3. 使用方法
4. 常见问题
5. 联系方式

## 🔧 高级配置

### 减小打包体积

1. **排除不需要的模块**：
   ```python
   excludes=['matplotlib', 'scipy', ...]
   ```

2. **使用虚拟环境**：
   - 创建干净的虚拟环境
   - 只安装必需的包
   - 在虚拟环境中打包

3. **UPX压缩**：
   - 已在spec文件中启用
   - 可以进一步压缩二进制文件

### 添加版本信息

在spec文件中添加版本信息：
```python
version='version_info.txt'
```

创建 `version_info.txt` 文件（需要特定格式）。

## 📞 技术支持

如果遇到打包问题，请：
1. 查看PyInstaller官方文档
2. 检查错误日志
3. 在GitHub上提交Issue

---

**注意**：首次打包可能需要较长时间，请耐心等待。打包完成后建议在干净的Windows系统上测试。
