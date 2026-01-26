@echo off
chcp 65001 >nul
echo ========================================
echo 智能知识库系统 - 简化打包脚本
echo ========================================
echo.
echo 此脚本将创建一个包含所有文件的安装包
echo 用户只需解压并运行 install.bat 即可使用
echo.

REM 切换到项目根目录
cd /d "%~dp0\.."

REM 检查Python是否安装
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [错误] 未检测到Python，请先安装Python 3.11或更高版本
    pause
    exit /b 1
)

set "PACKAGE_DIR=dist\智能知识库系统-安装包"

echo [1/3] 创建打包目录...
if exist "%PACKAGE_DIR%" rmdir /s /q "%PACKAGE_DIR%"
mkdir "%PACKAGE_DIR%"
echo.

echo [2/3] 复制文件...
echo 正在复制必需文件...

REM 复制主程序
copy /Y "knowledge_base_deepseek.py" "%PACKAGE_DIR%\" >nul
copy /Y "requirements.txt" "%PACKAGE_DIR%\" >nul
copy /Y "README.md" "%PACKAGE_DIR%\" >nul
copy /Y "build_script\使用说明-打包版.txt" "%PACKAGE_DIR%\" >nul

REM 复制安装脚本
copy /Y "build_script\install.bat" "%PACKAGE_DIR%\" >nul

REM 复制脚本目录
if exist "scripts" (
    xcopy /E /I /Y "scripts" "%PACKAGE_DIR%\scripts\" >nul
)

REM 复制文档目录
if exist "docs" (
    xcopy /E /I /Y "docs" "%PACKAGE_DIR%\docs\" >nul
)

REM 复制prompt_templates目录（如果存在）
if exist "prompt_templates" (
    xcopy /E /I /Y "prompt_templates" "%PACKAGE_DIR%\prompt_templates\" >nul
)

REM 复制其他工具脚本
if exist "download_model.py" copy /Y "download_model.py" "%PACKAGE_DIR%\" >nul
if exist "flowchart_to_drawio.py" copy /Y "flowchart_to_drawio.py" "%PACKAGE_DIR%\" >nul
if exist "gantt_to_drawio.py" copy /Y "gantt_to_drawio.py" "%PACKAGE_DIR%\" >nul

echo 文件复制完成
echo.

echo [3/3] 创建使用说明...
(
echo 智能知识库系统 - 安装包
echo ========================================
echo.
echo 安装步骤：
echo 1. 确保已安装Python 3.11或更高版本
echo 2. 双击运行 install.bat
echo 3. 等待安装完成
echo 4. 使用桌面快捷方式启动应用
echo.
echo 详细说明请查看：使用说明-打包版.txt
echo.
) > "%PACKAGE_DIR%\安装说明.txt"

echo.
echo ========================================
echo 打包完成！
echo ========================================
echo.
echo 打包文件位置: %PACKAGE_DIR%
echo.
echo 您可以：
echo 1. 将 %PACKAGE_DIR% 文件夹压缩成ZIP文件
echo 2. 分发给用户，用户解压后运行 install.bat 即可
echo.
pause
