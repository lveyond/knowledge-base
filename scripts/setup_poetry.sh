#!/bin/bash

cd "$(dirname "$0")/.."

echo "========================================"
echo "Poetry 环境配置脚本"
echo "========================================"
echo ""

echo "[步骤 1/3] 检查 Poetry 是否已安装..."
if ! command -v poetry &> /dev/null; then
    echo "Poetry 未安装！"
    echo "请先安装 Poetry: https://python-poetry.org/docs/#installation"
    exit 1
fi
poetry --version
echo ""

echo "[步骤 2/3] 检查 Python 3.11 是否可用..."
if ! command -v python3.11 &> /dev/null; then
    echo "Python 3.11 未找到！"
    echo "请确保已安装 Python 3.11"
    exit 1
fi
python3.11 --version
echo ""

echo "[步骤 3/3] 配置 Poetry 使用 Python 3.11..."
poetry env use python3.11
if [ $? -ne 0 ]; then
    echo "配置失败！"
    exit 1
fi
echo ""

echo "[安装依赖] 正在安装项目依赖..."
poetry install
if [ $? -ne 0 ]; then
    echo "依赖安装失败！"
    exit 1
fi
echo ""

echo "========================================"
echo "Poetry 环境配置完成！"
echo "========================================"
echo ""
echo "使用说明："
echo "1. 激活环境: poetry shell"
echo "2. 运行项目: streamlit run knowledge_base_deepseek.py"
echo "3. 或直接运行: poetry run streamlit run knowledge_base_deepseek.py"
echo ""
echo "详细说明请查看: docs/POETRY_SETUP.md"
echo ""

