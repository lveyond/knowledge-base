# 📦 Windows打包脚本目录

本目录包含所有用于将智能知识库系统打包成Windows应用程序的脚本和配置文件。

## 📁 文件说明

### 打包脚本

- **`build_windows.bat`** - PyInstaller打包脚本（推荐）
  - 将应用打包成独立的Windows可执行程序
  - 用户无需安装Python环境
  - 打包文件较大（约500MB-1GB），但使用简单

- **`build_simple.bat`** - 简化打包脚本（安装包方案）
  - 创建包含所有文件的安装包
  - 用户需要先安装Python环境
  - 打包文件小，安装快速

### 配置文件

- **`build_windows.spec`** - PyInstaller配置文件
  - 定义打包参数和依赖项
  - 可以自定义修改打包配置

- **`launcher.py`** - 启动器脚本
  - 用于打包后的应用启动
  - 自动启动Streamlit并打开浏览器

### 安装脚本

- **`install.bat`** - 一键安装脚本
  - 自动检查Python环境
  - 安装所有依赖包
  - 创建桌面快捷方式

### 文档文件

- **`打包说明.txt`** - 打包说明文档
  - 详细的打包步骤和注意事项
  - 两种打包方案的对比

- **`使用说明-打包版.txt`** - 打包版本使用说明
  - 面向最终用户的使用指南
  - 常见问题解答

## 🚀 快速开始

### 方案一：PyInstaller打包（推荐）

```bash
# 进入build_script目录
cd build_script

# 运行打包脚本
build_windows.bat

# 打包完成后，文件位于项目根目录的 dist\ 目录
```

### 方案二：安装包方案

```bash
# 进入build_script目录
cd build_script

# 运行简化打包脚本
build_simple.bat

# 打包完成后，文件位于 dist\智能知识库系统-安装包\
```

## 📖 详细文档

更多详细信息请查看：

- [打包说明.txt](打包说明.txt) - 快速参考
- [使用说明-打包版.txt](使用说明-打包版.txt) - 用户使用指南
- [../docs/WINDOWS_PACKAGING.md](../docs/WINDOWS_PACKAGING.md) - 完整打包指南

## ⚠️ 注意事项

1. **打包前准备**：
   - 确保Python 3.11+已安装
   - 安装所有依赖：`pip install -r requirements.txt`
   - 测试应用可以正常运行

2. **打包时间**：
   - 首次打包可能需要10-30分钟
   - 请耐心等待，不要中断

3. **打包文件大小**：
   - PyInstaller打包版本较大（约500MB-1GB）是正常的
   - 因为包含了Python解释器和所有依赖库

4. **测试**：
   - 打包完成后建议在干净的Windows系统上测试
   - 确保所有功能正常工作

## 🔧 自定义配置

如果需要修改打包配置：

1. **修改应用名称**：编辑 `build_windows.spec` 中的 `name='智能知识库系统'`
2. **添加图标**：在 `build_windows.spec` 中指定 `icon='路径/图标.ico'`
3. **隐藏控制台**：将 `console=True` 改为 `console=False`

## 📞 技术支持

如果遇到打包问题，请：

1. 查看 [打包说明.txt](打包说明.txt)
2. 查看 [../docs/WINDOWS_PACKAGING.md](../docs/WINDOWS_PACKAGING.md)
3. 检查错误日志
4. 在GitHub上提交Issue

---

**提示**：建议使用PyInstaller打包方案，虽然文件较大，但用户使用最简单，无需任何额外配置。
