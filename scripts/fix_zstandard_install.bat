@echo off
cd /d "%~dp0\.."
echo ========================================
echo zstandard 安装修复脚本
echo ========================================
echo.
echo 此脚本将尝试多种方法安装 zstandard
echo.

echo [方法 1] 尝试安装预编译的 zstandard 包...
pip install zstandard --only-binary :all: --prefer-binary
if not errorlevel 1 (
    echo ✓ zstandard 安装成功！
    echo.
    echo 现在可以继续安装其他依赖：
    echo pip install -r requirements.txt
    pause
    exit /b 0
)

echo.
echo [方法 2] 尝试安装特定版本的预编译包...
pip install zstandard==0.23.0 --only-binary :all: --prefer-binary
if not errorlevel 1 (
    echo ✓ zstandard 0.23.0 安装成功！
    echo.
    echo 现在可以继续安装其他依赖：
    echo pip install -r requirements.txt
    pause
    exit /b 0
)

echo.
echo [方法 3] 尝试从 PyPI 安装最新版本（可能需要编译）...
pip install --upgrade pip setuptools wheel
pip install zstandard
if not errorlevel 1 (
    echo ✓ zstandard 安装成功！
    echo.
    echo 现在可以继续安装其他依赖：
    echo pip install -r requirements.txt
    pause
    exit /b 0
)

echo.
echo ========================================
echo 所有方法都失败了！
echo ========================================
echo.
echo 问题分析：
echo - 您的 Python 版本可能太新（当前：Python 3.14）
echo - 缺少 Microsoft Visual C++ 14.0 或更高版本编译器
echo.
echo 推荐解决方案：
echo.
echo [方案 1] 安装 Microsoft C++ Build Tools（推荐）
echo 1. 访问: https://visualstudio.microsoft.com/visual-cpp-build-tools/
echo 2. 下载并安装 "Microsoft C++ Build Tools"
echo 3. 安装时选择 "C++ build tools" 工作负载
echo 4. 安装完成后重新运行此脚本
echo.
echo [方案 2] 使用 conda 环境（如果有 conda）
echo conda create -n knowledge-base python=3.11
echo conda activate knowledge-base
echo conda install -c conda-forge zstandard chromadb
echo pip install -r requirements.txt
echo.
echo [方案 3] 使用 Python 3.11 或 3.12（推荐版本）
echo 这些版本有更好的预编译包支持
echo.
echo [方案 4] 使用最小化版本（无向量数据库功能）
echo pip install -r requirements-minimal.txt
echo.
pause

