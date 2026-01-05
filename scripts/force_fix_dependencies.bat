@echo off
echo ========================================
echo 强制修复依赖冲突（降级 langchain-community）
echo ========================================
echo.

cd /d "%~dp0"

echo [步骤 1/4] 删除锁定文件...
if exist "poetry.lock" (
    del /f /q poetry.lock
    echo ✅ 已删除 poetry.lock
)
echo.

echo [步骤 2/4] 强制移除 langchain-community...
poetry remove langchain-community 2>nul
echo ✅ 已移除 langchain-community
echo.

echo [步骤 3/5] 安装 langsmith (兼容版本)...
poetry add "langsmith>=0.1.125,<0.4" --no-interaction
echo.

echo [步骤 4/5] 安装 NumPy 1.x（必须先安装）...
poetry add "numpy>=1.24.0,<2.0.0" --no-interaction
if %ERRORLEVEL% NEQ 0 (
    echo ⚠️ NumPy 安装失败，尝试强制安装...
    poetry add "numpy==1.26.4" --no-interaction
)
echo.

echo [步骤 5/5] 强制安装 langchain-community 0.3.22...
poetry add "langchain-community==0.3.22" --no-interaction
if %ERRORLEVEL% NEQ 0 (
    echo ⚠️ 0.3.22 安装失败，尝试 0.3.21...
    poetry add "langchain-community==0.3.21" --no-interaction
    if %ERRORLEVEL% NEQ 0 (
        echo ⚠️ 0.3.21 安装失败，尝试 0.3.20...
        poetry add "langchain-community==0.3.20" --no-interaction
    )
)
echo.

echo ========================================
echo 验证安装...
echo ========================================
poetry run python -c "import numpy; import langchain_community; print(f'NumPy: {numpy.__version__}'); print(f'LangChain Community: {langchain_community.__version__}')" 2>nul
if %ERRORLEVEL% EQU 0 (
    echo.
    echo ✅ 依赖修复成功！
    echo.
    echo 现在可以运行: poetry install
) else (
    echo.
    echo ⚠️ 验证失败，请检查错误信息
    echo.
    echo 如果仍然失败，可以尝试:
    echo   poetry add "langchain-community==0.3.22" --no-interaction
    echo   poetry add "numpy==1.26.4" --no-interaction
)
echo.
pause

