@echo off
echo ========================================
echo 清理向量数据库和模型缓存
echo ========================================
echo.

cd /d "%~dp0\.."

echo [1/3] 检查项目目录下的向量数据库...
if exist "chroma_db" (
    echo 找到 chroma_db 目录
    echo.
    echo 检测到的向量数据库：
    dir /b /ad chroma_db 2>nul
    echo.
    set /p confirm="是否删除所有向量数据库？(Y/N): "
    if /i "%confirm%"=="Y" (
        echo 正在删除所有向量数据库...
        rmdir /s /q chroma_db
        if exist "chroma_db" (
            echo 删除失败，请手动删除: chroma_db
        ) else (
            echo ✅ 所有向量数据库已删除
        )
    ) else (
        echo 跳过删除向量数据库
    )
) else (
    echo chroma_db 目录不存在
)
echo.

echo [2/3] 检查 HuggingFace 模型缓存...
set HF_CACHE=%USERPROFILE%\.cache\huggingface
if exist "%HF_CACHE%" (
    echo HuggingFace 缓存位置: %HF_CACHE%
    echo 警告：删除模型缓存后，下次使用需要重新下载模型（约400-500MB）
    echo.
    set /p confirm="是否删除 HuggingFace 模型缓存？(Y/N): "
    if /i "%confirm%"=="Y" (
        echo 正在删除 HuggingFace 缓存...
        rmdir /s /q "%HF_CACHE%"
        if exist "%HF_CACHE%" (
            echo 删除失败，请手动删除: %HF_CACHE%
        ) else (
            echo ✅ HuggingFace 缓存已删除
        )
    ) else (
        echo 跳过删除 HuggingFace 缓存
    )
) else (
    echo HuggingFace 缓存目录不存在
)
echo.

echo [3/3] 检查其他可能的缓存位置...
set TRANSFORMERS_CACHE=%USERPROFILE%\.cache\transformers
if exist "%TRANSFORMERS_CACHE%" (
    echo 找到 Transformers 缓存: %TRANSFORMERS_CACHE%
    set /p confirm="是否删除 Transformers 缓存？(Y/N): "
    if /i "%confirm%"=="Y" (
        rmdir /s /q "%TRANSFORMERS_CACHE%"
        echo ✅ Transformers 缓存已删除
    )
)
echo.

echo ========================================
echo 清理完成！
echo ========================================
echo.
echo 提示：
echo - 向量数据库已删除，下次加载文档时会重新创建
echo - 如果删除了模型缓存，首次使用需要重新下载模型
echo.
pause


