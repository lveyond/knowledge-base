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

echo [步骤 4/5] 尝试安装 ChromaDB（可能需要编译）...
echo 如果这一步失败，请参考 docs\INSTALL.md 中的解决方案
pip install chromadb
if errorlevel 1 (
    echo.
    echo ========================================
    echo ChromaDB 安装失败！
    echo ========================================
    echo.
    echo 可能的原因：
    echo 1. 缺少 Microsoft Visual C++ 14.0 或更高版本
    echo 2. Python 版本太新（建议使用 Python 3.11 或 3.12）
    echo.
    echo 解决方案：
    echo 1. 安装 Microsoft C++ Build Tools:
    echo    https://visualstudio.microsoft.com/visual-cpp-build-tools/
    echo.
    echo 2. 或者尝试使用预编译包:
    echo    pip install zstandard --only-binary :all:
    echo    pip install chromadb
    echo.
    echo 3. 查看 docs\INSTALL.md 获取更多解决方案
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

