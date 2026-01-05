@echo off
echo ========================================
echo 修复依赖冲突问题
echo ========================================
echo.

cd /d "%~dp0"

echo [步骤 1/3] 删除旧的锁定文件...
if exist "poetry.lock" (
    del /f /q poetry.lock
    echo ✅ 已删除 poetry.lock
) else (
    echo ℹ️ poetry.lock 不存在，跳过
)
echo.

echo [步骤 2/3] 移除冲突的包...
poetry remove langchain-community numpy 2>nul
echo ✅ 已移除冲突的包
echo.

echo [步骤 3/3] 安装兼容版本的依赖...
echo.
echo 正在安装 NumPy (1.x 版本，必须先安装)...
poetry add "numpy>=1.24.0,<2.0.0"
echo.
echo 正在安装 langchain-community (必须使用 0.3.22 或更早版本)...
poetry add "langchain-community==0.3.22"
if %ERRORLEVEL% NEQ 0 (
    echo ⚠️ 安装 0.3.22 失败，尝试安装 0.3.21...
    poetry add "langchain-community==0.3.21"
)
echo.
echo 正在安装 ChromaDB...
poetry add "chromadb>=0.4.22,<0.5.0"
echo.

echo ========================================
echo 修复完成！
echo ========================================
echo.
echo 验证安装...
poetry run python -c "import numpy; import langchain_community; import chromadb; print(f'✅ NumPy: {numpy.__version__}'); print(f'✅ LangChain Community: {langchain_community.__version__}'); print(f'✅ ChromaDB: {chromadb.__version__}')" 2>nul
if %ERRORLEVEL% EQU 0 (
    echo.
    echo ✅ 所有依赖安装成功！
) else (
    echo.
    echo ⚠️ 验证失败，请检查错误信息
)
echo.
pause

