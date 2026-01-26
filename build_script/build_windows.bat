@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul
echo ========================================
echo 智能知识库系统 - Windows打包脚本
echo ========================================
echo.

REM ========================================
REM 第一步：检测并选择Python 3.11
REM ========================================

set "PYTHON311_PATH="
set "PYTHON_CMD="
set "USE_VENV=0"

REM 检查常见的Python 3.11安装路径
if exist "C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python311\python.exe" (
    set "PYTHON311_PATH=C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python311\python.exe"
)
if exist "C:\Program Files\Python311\python.exe" (
    set "PYTHON311_PATH=C:\Program Files\Python311\python.exe"
)
if exist "C:\Python311\python.exe" (
    set "PYTHON311_PATH=C:\Python311\python.exe"
)

REM 如果找到了Python 3.11路径，使用它
if not "!PYTHON311_PATH!"=="" (
    echo [检测到Python 3.11] !PYTHON311_PATH!
    set "PYTHON_CMD=!PYTHON311_PATH!"
    goto :check_version
)

REM 尝试使用系统PATH中的python，检查版本
echo [检测Python版本]...
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [错误] 未检测到Python
    goto :no_python
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo 当前Python版本: !PYTHON_VERSION!

REM 检查版本号是否包含3.11
echo !PYTHON_VERSION! | findstr /C:"3.11" >nul
if %ERRORLEVEL% EQU 0 (
    echo [✓] 检测到Python 3.11版本
    set "PYTHON_CMD=python"
    goto :check_version
)

REM 未找到Python 3.11
:no_python
echo.
echo [警告] 未检测到Python 3.11
echo.
echo 请确保已安装Python 3.11，并执行以下操作之一：
echo.
echo 方案一：安装Python 3.11到默认位置
echo   - 下载地址: https://www.python.org/downloads/
echo   - 安装时勾选"Add Python to PATH"
echo.
echo 方案二：手动指定Python 3.11路径
echo   编辑此脚本，在开头设置 PYTHON311_PATH 变量
echo   例如: set "PYTHON311_PATH=C:\Python311\python.exe"
echo.
echo 方案三：使用虚拟环境（推荐）
echo   脚本将自动创建Python 3.11虚拟环境
echo.
set /p CREATE_VENV="是否创建Python 3.11虚拟环境？(Y/N): "
if /i "!CREATE_VENV!"=="Y" (
    goto :create_venv
) else (
    echo.
    echo [错误] 打包需要Python 3.11，请先安装或配置
    pause
    exit /b 1
)

:check_version
REM 验证Python版本
echo.
echo [1/5] 检查Python版本...
%PYTHON_CMD% --version
for /f "tokens=2" %%i in ('%PYTHON_CMD% --version 2^>^&1') do set CHECK_VERSION=%%i
echo !CHECK_VERSION! | findstr /C:"3.11" >nul
if %ERRORLEVEL% NEQ 0 (
    echo [警告] 当前Python版本不是3.11，可能导致打包失败
    echo 检测到的版本: !CHECK_VERSION!
    set /p CONTINUE="是否继续？(Y/N): "
    if /i not "!CONTINUE!"=="Y" (
        exit /b 1
    )
)
echo.

REM 切换到项目根目录
cd /d "%~dp0\.."

echo [2/5] 检查并安装打包工具...
%PYTHON_CMD% -m pip install --upgrade pip >nul 2>&1
%PYTHON_CMD% -m pip install pyinstaller >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [错误] PyInstaller安装失败
    pause
    exit /b 1
)
echo PyInstaller已安装
echo.

echo [3/5] 清理旧的构建文件...
if exist "build" rmdir /s /q "build"
if exist "dist" rmdir /s /q "dist"
if exist "智能知识库系统.spec" del /q "智能知识库系统.spec"
echo 清理完成
echo.

echo [4/5] 开始打包应用程序...
echo 这可能需要几分钟时间，请耐心等待...
echo.

REM 使用spec文件打包（spec文件中已定义打包模式）
%PYTHON_CMD% -m PyInstaller build_script\build_windows.spec --clean --noconfirm

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [错误] 打包失败，请检查错误信息
    pause
    exit /b 1
)

echo.
echo [5/5] 创建启动脚本和安装包...
echo.

REM 创建启动脚本
(
echo @echo off
echo chcp 65001 ^>nul
echo cd /d "%%~dp0"
echo echo ========================================
echo echo 正在启动智能知识库系统...
echo echo ========================================
echo echo.
echo echo 应用启动后会自动在浏览器中打开
echo echo 如果没有自动打开，请访问: http://localhost:8501
echo echo.
echo echo 按 Ctrl+C 可以停止应用
echo echo.
echo "智能知识库系统\智能知识库系统.exe"
echo pause
) > dist\启动应用.bat

REM 复制使用说明到dist目录
if exist "build_script\使用说明-打包版.txt" (
    copy /Y "build_script\使用说明-打包版.txt" "dist\使用说明.txt" >nul
)

REM 创建README文件
(
echo # 智能知识库系统 - Windows版本
echo.
echo ## 使用说明
echo.
echo 1. 双击"启动应用.bat"启动应用程序
echo 2. 或者直接运行"智能知识库系统.exe"
echo 3. 应用程序会自动在浏览器中打开
echo.
echo ## 注意事项
echo.
echo - 首次运行可能需要下载AI模型文件（约130MB），请确保网络连接正常
echo - 如果遇到问题，请查看"使用说明.txt"
echo.
) > dist\智能知识库系统\README.txt

echo.
echo ========================================
echo 打包完成！
echo ========================================
echo.
echo 打包文件位置: dist\
echo.
echo 打包内容：
echo - dist\智能知识库系统\  - 主程序文件夹（包含exe和所有依赖）
echo - dist\启动应用.bat     - 启动脚本
echo - dist\使用说明.txt     - 使用说明
echo.
echo 您可以：
echo 1. 将整个 dist\ 文件夹压缩后分发给用户
echo 2. 或者使用 Inno Setup 等工具创建安装程序
echo.
echo 注意：打包后的文件较大（约500MB-1GB），这是正常的
echo 因为包含了Python解释器和所有依赖库
echo.
echo 用户使用方法：
echo 1. 解压文件
echo 2. 双击"启动应用.bat"即可使用
echo.
if %USE_VENV% EQU 1 (
    echo 提示：虚拟环境已创建在 venv_build 目录
    echo 下次打包可以直接使用此虚拟环境
    echo.
)
pause
exit /b 0

REM ========================================
REM 创建虚拟环境流程
REM ========================================
:create_venv
echo.
echo [创建Python 3.11虚拟环境]...
echo.

REM 切换到项目根目录
cd /d "%~dp0\.."

REM 检查是否有Python 3.11可用
set "VENV_PYTHON="
if exist "C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python311\python.exe" (
    set "VENV_PYTHON=C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python311\python.exe"
) else if exist "C:\Program Files\Python311\python.exe" (
    set "VENV_PYTHON=C:\Program Files\Python311\python.exe"
) else if exist "C:\Python311\python.exe" (
    set "VENV_PYTHON=C:\Python311\python.exe"
)

if "!VENV_PYTHON!"=="" (
    echo [错误] 未找到Python 3.11安装
    echo 请先安装Python 3.11: https://www.python.org/downloads/
    echo.
    echo 安装后，请确保Python 3.11在以下位置之一：
    echo   - C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python311\
    echo   - C:\Program Files\Python311\
    echo   - C:\Python311\
    pause
    exit /b 1
)

REM 创建虚拟环境
set "VENV_DIR=venv_build"
if exist "!VENV_DIR!" (
    echo 虚拟环境已存在: !VENV_DIR!
    echo 是否重新创建？(Y/N)
    set /p RECREATE=""
    if /i "!RECREATE!"=="Y" (
        echo 删除旧虚拟环境...
        rmdir /s /q "!VENV_DIR!"
        echo 正在创建新的虚拟环境...
        "!VENV_PYTHON!" -m venv "!VENV_DIR!"
        if !ERRORLEVEL! NEQ 0 (
            echo [错误] 虚拟环境创建失败
            pause
            exit /b 1
        )
        echo 虚拟环境创建成功
    ) else (
        echo 使用现有虚拟环境
    )
) else (
    echo 正在创建虚拟环境...
    "!VENV_PYTHON!" -m venv "!VENV_DIR!"
    if !ERRORLEVEL! NEQ 0 (
        echo [错误] 虚拟环境创建失败
        pause
        exit /b 1
    )
    echo 虚拟环境创建成功
)

REM 使用虚拟环境
set "PYTHON_CMD=!VENV_DIR!\Scripts\python.exe"
set "USE_VENV=1"
echo.
echo [使用虚拟环境] !PYTHON_CMD!
!PYTHON_CMD! --version
echo.

REM 安装依赖
echo [安装打包依赖]...
!PYTHON_CMD! -m pip install --upgrade pip >nul 2>&1
!PYTHON_CMD! -m pip install pyinstaller >nul 2>&1
if !ERRORLEVEL! NEQ 0 (
    echo [错误] PyInstaller安装失败
    pause
    exit /b 1
)
echo PyInstaller已安装
echo.

REM 继续执行打包流程
goto :check_version
