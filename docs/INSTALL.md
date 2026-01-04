# 安装指南

## 问题说明

如果在安装依赖时遇到 `zstandard` 编译错误（需要 Microsoft Visual C++ 14.0），请按照以下步骤解决。

## 解决方案

### 方案一：更新 pip 和构建工具（推荐）

```bash
# 1. 更新 pip、setuptools 和 wheel
python -m pip install --upgrade pip setuptools wheel

# 2. 安装依赖
pip install -r requirements.txt
```

### 方案二：安装 Visual C++ Build Tools

如果方案一不行，需要安装编译工具：

1. 下载并安装 [Microsoft C++ Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/)
2. 安装时选择 "C++ 生成工具" 工作负载
3. 重新运行 `pip install -r requirements.txt`

### 方案三：使用预编译包（如果可用）

```bash
# 先尝试安装预编译的 zstandard
pip install zstandard --only-binary :all:

# 如果成功，再安装其他依赖
pip install -r requirements.txt
```

### 方案四：分步安装（最稳妥）

```bash
# 1. 更新工具
python -m pip install --upgrade pip setuptools wheel

# 2. 先安装基础包
pip install streamlit python-docx pypdf pandas openpyxl requests

# 3. 安装 langchain 相关（通常不需要编译）
pip install langchain langchain-community langchain-core

# 4. 尝试安装 chromadb（可能需要编译）
pip install chromadb

# 5. 安装 AI 相关包
pip install sentence-transformers torch transformers
```

### 方案五：使用 conda（如果有 conda 环境）

```bash
conda install -c conda-forge chromadb
pip install -r requirements.txt
```

## 如果仍然失败

如果以上方案都不行，可以考虑：

1. **使用 Python 3.11 或 3.12**（Python 3.14 可能太新，某些包可能还没有预编译版本）
2. **使用 WSL2**（Windows Subsystem for Linux）在 Linux 环境中安装
3. **使用 Docker** 容器运行项目

## 验证安装

安装完成后，运行以下命令验证：

```bash
python -c "import streamlit; import chromadb; import langchain; print('所有包安装成功！')"
```

