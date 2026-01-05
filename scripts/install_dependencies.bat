@echo off
cd /d "%~dp0\.."
echo ========================================
echo 智能知识库系统 - 依赖安装脚本
echo ========================================
echo.

echo [步骤 1/5] 更新 pip、setuptools 和 wheel...
python -m pip install --upgrade pip setuptools wheel
if errorlevel 1 (
    echo 更新失败，请检查 Python 环境
    pause
    exit /b 1
)
echo.

echo [步骤 2/5] 安装基础依赖包...
pip install streamlit python-docx pypdf pandas openpyxl requests
if errorlevel 1 (
    echo 基础包安装失败
    pause
    exit /b 1
)
echo.

echo [步骤 3/5] 安装 LangChain 相关包...
pip install langchain langchain-community langchain-core
if errorlevel 1 (
    echo LangChain 安装失败
    pause
    exit /b 1
)
echo.

echo [步骤 4/5] 安装 zstandard 和 ChromaDB...
echo.
echo 正在尝试安装 zstandard（优先使用预编译包）...
pip install zstandard --only-binary :all: --prefer-binary
if errorlevel 1 (
    echo.
    echo 预编译包安装失败，尝试从源码安装...
    echo 注意：这可能需要 Microsoft Visual C++ 14.0 或更高版本
    pip install zstandard
    if errorlevel 1 (
        echo.
        echo ========================================
        echo zstandard 安装失败！
        echo ========================================
        echo.
        echo 可能的原因：
        echo 1. 缺少 Microsoft Visual C++ 14.0 或更高版本
        echo 2. Python 版本太新（当前版本可能没有预编译包）
        echo.
        echo 解决方案：
        echo 1. 安装 Microsoft C++ Build Tools:
        echo    https://visualstudio.microsoft.com/visual-cpp-build-tools/
        echo    下载后安装 "C++ build tools" 工作负载
        echo.
        echo 2. 或者尝试使用 conda 安装:
        echo    conda install -c conda-forge zstandard chromadb
        echo.
        echo 3. 或者使用最小化版本（无向量数据库功能）:
        echo    pip install -r requirements-minimal.txt
        echo.
        echo 4. 查看 docs\INSTALL.md 获取更多解决方案
        echo.
        pause
        exit /b 1
    )
)
echo.
echo 正在安装 ChromaDB...
pip install chromadb
if errorlevel 1 (
    echo.
    echo ========================================
    echo ChromaDB 安装失败！
    echo ========================================
    echo.
    echo 可能的原因：
    echo 1. zstandard 未正确安装
    echo 2. 缺少其他编译依赖
    echo.
    echo 解决方案：
    echo 1. 确保 zstandard 已正确安装
    echo 2. 安装 Microsoft C++ Build Tools:
    echo    https://visualstudio.microsoft.com/visual-cpp-build-tools/
    echo.
    echo 3. 或者使用最小化版本（无向量数据库功能）:
    echo    pip install -r requirements-minimal.txt
    echo.
    pause
    exit /b 1
)
echo.

echo [步骤 5/5] 安装 AI 相关包...
pip install sentence-transformers torch transformers
if errorlevel 1 (
    echo AI 包安装失败
    pause
    exit /b 1
)
echo.

echo ========================================
echo 所有依赖安装完成！
echo ========================================
echo.
echo 验证安装...
python -c "import streamlit; import chromadb; import langchain; print('✓ 所有包安装成功！')"
if errorlevel 1 (
    echo 验证失败，某些包可能未正确安装
) else (
    echo.
    echo 可以开始运行项目了！
    echo 运行命令: streamlit run knowledge_base_deepseek.py
)
echo.
pause

