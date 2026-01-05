@echo off
cd /d "%~dp0\.."
echo ========================================
echo Poetry 环境配置脚本
echo ========================================
echo.

echo [步骤 1/3] 检查 Poetry 是否已安装...
poetry --version
if errorlevel 1 (
    echo Poetry 未安装！
    echo 请先安装 Poetry: https://python-poetry.org/docs/#installation
    pause
    exit /b 1
)
echo.

echo [步骤 2/3] 检查 Python 3.11 是否可用...
py -3.11 --version
if errorlevel 1 (
    echo Python 3.11 未找到！
    echo 请确保已安装 Python 3.11
    pause
    exit /b 1
)
echo.

echo [步骤 3/3] 配置 Poetry 使用 Python 3.11...
poetry env use py -3.11
if errorlevel 1 (
    echo 配置失败！
    echo 尝试使用完整路径...
    echo 请手动运行: poetry env use "C:\Python311\python.exe"
    pause
    exit /b 1
)
echo.

echo [安装依赖] 正在安装项目依赖...
poetry install
if errorlevel 1 (
    echo 依赖安装失败！
    pause
    exit /b 1
)
echo.

echo ========================================
echo Poetry 环境配置完成！
echo ========================================
echo.
echo 使用说明：
echo 1. 激活环境: poetry shell
echo 2. 运行项目: streamlit run knowledge_base_deepseek.py
echo 3. 或直接运行: poetry run streamlit run knowledge_base_deepseek.py
echo.
echo 详细说明请查看: docs\POETRY_SETUP.md
echo.
pause

