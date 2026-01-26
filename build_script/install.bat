@echo off
chcp 65001 >nul
echo ========================================
echo 智能知识库系统 - 一键安装程序
echo ========================================
echo.

REM 检查管理员权限（可选）
net session >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo [提示] 检测到管理员权限
) else (
    echo [提示] 未使用管理员权限，将安装到当前用户目录
)
echo.

REM 设置安装目录
set "INSTALL_DIR=%USERPROFILE%\KnowledgeBase"
set "DESKTOP_SHORTCUT=%USERPROFILE%\Desktop\智能知识库系统.lnk"

echo [1/4] 检查Python环境...
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [错误] 未检测到Python环境
    echo.
    echo 请先安装Python 3.11或更高版本：
    echo 1. 访问 https://www.python.org/downloads/
    echo 2. 下载并安装Python（请勾选"Add Python to PATH"）
    echo 3. 重新运行此安装程序
    echo.
    pause
    exit /b 1
)

python --version
echo Python环境检查通过
echo.

echo [2/4] 创建安装目录...
if not exist "%INSTALL_DIR%" mkdir "%INSTALL_DIR%"
echo 安装目录: %INSTALL_DIR%
echo.

echo [3/4] 复制文件到安装目录...
echo 正在复制文件，请稍候...

REM 复制主程序文件
copy /Y "knowledge_base_deepseek.py" "%INSTALL_DIR%\" >nul 2>&1
copy /Y "requirements.txt" "%INSTALL_DIR%\" >nul 2>&1
copy /Y "README.md" "%INSTALL_DIR%\" >nul 2>&1

REM 复制脚本目录
if exist "scripts" (
    xcopy /E /I /Y "scripts" "%INSTALL_DIR%\scripts\" >nul 2>&1
)

REM 复制文档目录
if exist "docs" (
    xcopy /E /I /Y "docs" "%INSTALL_DIR%\docs\" >nul 2>&1
)

REM 复制prompt_templates目录（如果存在）
if exist "prompt_templates" (
    xcopy /E /I /Y "prompt_templates" "%INSTALL_DIR%\prompt_templates\" >nul 2>&1
)

echo 文件复制完成
echo.

echo [4/4] 安装Python依赖包...
echo 这可能需要几分钟时间，请耐心等待...
echo.

cd /d "%INSTALL_DIR%"
python -m pip install --upgrade pip >nul 2>&1
python -m pip install -r requirements.txt

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [警告] 部分依赖包安装失败
    echo 您可以稍后手动运行: pip install -r requirements.txt
    echo.
) else (
    echo.
    echo 依赖包安装完成
    echo.
)

REM 创建启动脚本
(
echo @echo off
echo chcp 65001 ^>nul
echo cd /d "%%~dp0"
echo echo ========================================
echo echo 正在启动智能知识库系统...
echo echo ========================================
echo echo.
echo streamlit run knowledge_base_deepseek.py
echo pause
) > "%INSTALL_DIR%\启动应用.bat"

REM 创建桌面快捷方式（需要PowerShell）
echo 创建桌面快捷方式...
powershell -Command "$WshShell = New-Object -ComObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%DESKTOP_SHORTCUT%'); $Shortcut.TargetPath = '%INSTALL_DIR%\启动应用.bat'; $Shortcut.WorkingDirectory = '%INSTALL_DIR%'; $Shortcut.Description = '智能知识库系统'; $Shortcut.Save()" >nul 2>&1

if %ERRORLEVEL% EQU 0 (
    echo 桌面快捷方式创建成功
) else (
    echo [提示] 无法创建桌面快捷方式，您可以手动创建
)

echo.
echo ========================================
echo 安装完成！
echo ========================================
echo.
echo 安装位置: %INSTALL_DIR%
echo.
echo 您可以通过以下方式启动应用：
echo 1. 双击桌面上的"智能知识库系统"快捷方式
echo 2. 运行: %INSTALL_DIR%\启动应用.bat
echo.
echo 应用启动后会自动在浏览器中打开
echo 默认地址: http://localhost:8501
echo.
pause
