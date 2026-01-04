#!/bin/bash
cd "$(dirname "$0")/.."

echo "========================================"
echo "清理向量数据库和模型缓存"
echo "========================================"
echo ""

echo "[1/3] 检查项目目录下的向量数据库..."
if [ -d "chroma_db" ]; then
    echo "找到 chroma_db 目录"
    echo ""
    echo "检测到的向量数据库："
    ls -1 chroma_db 2>/dev/null | grep -v "^\.$" | grep -v "^\.\.$" || echo "  (空目录)"
    echo ""
    read -p "是否删除所有向量数据库？(y/N): " confirm
    if [ "$confirm" = "y" ] || [ "$confirm" = "Y" ]; then
        echo "正在删除所有向量数据库..."
        rm -rf chroma_db
        if [ -d "chroma_db" ]; then
            echo "删除失败，请手动删除: chroma_db"
        else
            echo "✅ 所有向量数据库已删除"
        fi
    else
        echo "跳过删除向量数据库"
    fi
else
    echo "chroma_db 目录不存在"
fi
echo ""

echo "[2/3] 检查 HuggingFace 模型缓存..."
HF_CACHE="$HOME/.cache/huggingface"
if [ -d "$HF_CACHE" ]; then
    echo "HuggingFace 缓存位置: $HF_CACHE"
    size=$(du -sh "$HF_CACHE" 2>/dev/null | cut -f1)
    echo "缓存大小: $size"
    echo "警告：删除模型缓存后，下次使用需要重新下载模型（约400-500MB）"
    echo ""
    read -p "是否删除 HuggingFace 模型缓存？(y/N): " confirm
    if [ "$confirm" = "y" ] || [ "$confirm" = "Y" ]; then
        echo "正在删除 HuggingFace 缓存..."
        rm -rf "$HF_CACHE"
        if [ -d "$HF_CACHE" ]; then
            echo "删除失败，请手动删除: $HF_CACHE"
        else
            echo "✅ HuggingFace 缓存已删除"
        fi
    else
        echo "跳过删除 HuggingFace 缓存"
    fi
else
    echo "HuggingFace 缓存目录不存在"
fi
echo ""

echo "[3/3] 检查其他可能的缓存位置..."
TRANSFORMERS_CACHE="$HOME/.cache/transformers"
if [ -d "$TRANSFORMERS_CACHE" ]; then
    echo "找到 Transformers 缓存: $TRANSFORMERS_CACHE"
    read -p "是否删除 Transformers 缓存？(y/N): " confirm
    if [ "$confirm" = "y" ] || [ "$confirm" = "Y" ]; then
        rm -rf "$TRANSFORMERS_CACHE"
        echo "✅ Transformers 缓存已删除"
    fi
fi
echo ""

echo "========================================"
echo "清理完成！"
echo "========================================"
echo ""
echo "提示："
echo "- 向量数据库已删除，下次加载文档时会重新创建"
echo "- 如果删除了模型缓存，首次使用需要重新下载模型"
echo ""


