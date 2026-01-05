@echo off
echo ========================================
echo ChromaDB HNSW 索引错误修复工具
echo ========================================
echo.

cd /d "%~dp0"

echo [步骤 1/2] 强制删除损坏的向量数据库...
if exist "chroma_db" (
    echo 找到 chroma_db 目录，正在强制删除...
    rmdir /s /q chroma_db 2>nul
    timeout /t 1 /nobreak >nul
    if exist "chroma_db" (
        echo ⚠️ 删除失败，目录可能被锁定
        echo 请关闭所有相关程序后手动删除: chroma_db
        echo.
        echo 或者使用以下 PowerShell 命令强制删除:
        echo Remove-Item -Path "chroma_db" -Recurse -Force
    ) else (
        echo ✅ 向量数据库目录已删除
    )
) else (
    echo ✅ chroma_db 目录不存在，无需清理
)
echo.

echo [步骤 2/2] 检查 ChromaDB 版本...
poetry show chromadb 2>nul
if %ERRORLEVEL% EQU 0 (
    echo.
    echo 💡 建议: 如果问题持续，可以尝试重新安装 ChromaDB:
    echo    poetry remove chromadb
    echo    poetry add chromadb==0.4.22
) else (
    echo 未检测到 Poetry 环境，跳过版本检查
)
echo.

echo ========================================
echo 修复完成！
echo ========================================
echo.
echo 现在可以重新运行程序，向量数据库将自动重新创建。
echo.
pause

