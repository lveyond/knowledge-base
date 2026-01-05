#!/bin/bash
cd "$(dirname "$0")/.."
echo "========================================"
echo "正在启动智能知识库系统..."
echo "========================================"
echo ""

# 检查是否使用 Poetry
if command -v poetry &> /dev/null; then
    echo "[使用 Poetry 环境]"
    echo ""
    # 检查是否已安装依赖
    if ! poetry check &> /dev/null; then
        echo "正在安装依赖..."
        poetry install
        echo ""
    fi
    echo "启动应用..."
    poetry run streamlit run knowledge_base_deepseek.py
else
    echo "[使用系统 Python 环境]"
    echo ""
    echo "提示: 检测到未安装 Poetry，使用系统 Python 环境"
    echo "建议: 安装 Poetry 以获得更好的依赖管理"
    echo "      安装方法: pip install poetry"
    echo ""
    echo "请确保已安装所有依赖: pip install -r requirements.txt"
    echo ""
    streamlit run knowledge_base_deepseek.py
fi

