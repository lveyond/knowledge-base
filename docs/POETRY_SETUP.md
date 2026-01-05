# Poetry 环境配置指南

本指南介绍如何使用 Poetry 为项目创建独立的 Python 3.11 环境。

## 前置要求

1. 已安装 Poetry（版本 2.2.1 或更高）
2. 已安装 Python 3.11（推荐 3.11.9 或更高）

## 快速开始

### 1. 初始化 Poetry 环境（使用 Python 3.11）

```bash
# 方式一：使用 py 命令指定 Python 3.11
poetry env use py -3.11

# 方式二：如果知道 Python 3.11 的完整路径
poetry env use "C:\Python311\python.exe"

# 方式三：让 Poetry 自动检测（如果 Python 3.11 在 PATH 中）
poetry env use python3.11
```

### 2. 安装所有依赖

```bash
poetry install
```

这将：
- 创建独立的虚拟环境（使用 Python 3.11）
- 安装所有项目依赖
- 生成 `poetry.lock` 文件（锁定依赖版本）

### 3. 激活虚拟环境

**Windows (PowerShell):**
```powershell
poetry shell
```

**Windows (CMD):**
```cmd
poetry shell
```

**Linux/Mac:**
```bash
poetry shell
```

### 4. 运行项目

在激活的 Poetry 环境中：

```bash
# 方式一：在激活的 shell 中直接运行
streamlit run knowledge_base_deepseek.py

# 方式二：使用 poetry run（无需激活 shell）
poetry run streamlit run knowledge_base_deepseek.py
```

## 常用命令

### 环境管理

```bash
# 查看当前环境信息
poetry env info

# 查看所有环境
poetry env list

# 删除当前环境（重新创建）
poetry env remove python3.11
```

### 依赖管理

```bash
# 添加新依赖
poetry add package-name

# 添加开发依赖
poetry add --group dev package-name

# 更新所有依赖
poetry update

# 更新特定依赖
poetry update package-name

# 查看依赖树
poetry show --tree

# 导出为 requirements.txt（如果需要）
poetry export -f requirements.txt --output requirements.txt --without-hashes
```

### 运行命令

```bash
# 运行 Python 脚本
poetry run python script.py

# 运行 Streamlit 应用
poetry run streamlit run knowledge_base_deepseek.py

# 运行其他命令
poetry run command-name
```

## 切换 Python 版本

如果需要切换到不同的 Python 版本：

```bash
# 删除当前环境
poetry env remove python3.11

# 使用新的 Python 版本
poetry env use python3.12  # 或其他版本

# 重新安装依赖
poetry install
```

## 常见问题

### Q: Poetry 找不到 Python 3.11？

**解决方案：**
1. 确认 Python 3.11 已安装：
   ```bash
   py -3.11 --version
   ```

2. 使用完整路径：
   ```bash
   poetry env use "C:\Python311\python.exe"
   ```

3. 或者将 Python 3.11 添加到系统 PATH

### Q: 安装依赖时出现编译错误？

**解决方案：**
1. 确保使用 Python 3.11（而不是 3.14）
2. 如果仍有问题，可能需要安装 Microsoft C++ Build Tools：
   https://visualstudio.microsoft.com/visual-cpp-build-tools/

### Q: 如何退出 Poetry shell？

**解决方案：**
```bash
exit
# 或按 Ctrl+D (Linux/Mac)
```

### Q: 如何在 IDE 中使用 Poetry 环境？

**VS Code:**
1. 打开命令面板（Ctrl+Shift+P）
2. 输入 "Python: Select Interpreter"
3. 选择 Poetry 环境（通常在 `.venv` 或 Poetry 的缓存目录中）

**PyCharm:**
1. File -> Settings -> Project -> Python Interpreter
2. 点击齿轮图标 -> Add
3. 选择 "Poetry Environment"
4. 选择项目目录

## 优势

使用 Poetry 管理项目依赖的优势：

1. **独立环境**：每个项目有独立的虚拟环境，避免依赖冲突
2. **版本锁定**：`poetry.lock` 文件确保所有环境使用相同的依赖版本
3. **依赖解析**：自动解决依赖冲突
4. **易于管理**：简单的命令管理依赖和环境
5. **跨平台**：Windows、Linux、Mac 统一使用方式

## 与 requirements.txt 的关系

- `pyproject.toml`：定义项目依赖和配置（Poetry 使用）
- `requirements.txt`：传统 pip 方式（仍然保留，用于兼容）
- `poetry.lock`：锁定精确版本（Poetry 自动生成）

建议优先使用 Poetry，但 `requirements.txt` 仍然保留以便其他方式使用。

