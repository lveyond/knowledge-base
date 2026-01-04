# 🛠️ 脚本目录

本目录包含项目的所有启动和安装脚本。

## 📜 脚本列表

### Windows 脚本

- **install_dependencies.bat** - 依赖安装脚本（Windows）
- **run.bat** - 应用启动脚本（Windows）

### Linux/Mac 脚本

- **install_dependencies.sh** - 依赖安装脚本（Linux/Mac）
- **run.sh** - 应用启动脚本（Linux/Mac）

## 🚀 使用方法

### 安装依赖

**Windows:**
```bash
scripts\install_dependencies.bat
```

**Linux/Mac:**
```bash
chmod +x scripts/install_dependencies.sh
./scripts/install_dependencies.sh
```

### 启动应用

**Windows:**
```bash
scripts\run.bat
```

**Linux/Mac:**
```bash
chmod +x scripts/run.sh
./scripts/run.sh
```

## ⚠️ 注意事项

- 所有脚本会自动切换到项目根目录执行
- 确保在项目根目录下运行脚本，或使用相对路径
- Linux/Mac 脚本需要执行权限（使用 `chmod +x`）


