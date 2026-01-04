#!/bin/bash
cd "$(dirname "$0")/.."

echo "========================================"
echo "智能知识库系统 - 依赖安装脚本"
echo "========================================"
echo ""

echo "[步骤 1/5] 更新 pip、setuptools 和 wheel..."
python3 -m pip install --upgrade pip setuptools wheel
if [ $? -ne 0 ]; then
    echo "更新失败，请检查 Python 环境"
    exit 1
fi
echo ""

echo "[步骤 2/5] 安装基础依赖包..."
pip install streamlit python-docx pypdf pandas openpyxl requests
if [ $? -ne 0 ]; then
    echo "基础包安装失败"
    exit 1
fi
echo ""

echo "[步骤 3/5] 安装 LangChain 相关包..."
pip install langchain langchain-community langchain-core
if [ $? -ne 0 ]; then
    echo "LangChain 安装失败"
    exit 1
fi
echo ""

echo "[步骤 4/5] 安装 ChromaDB..."
pip install chromadb
if [ $? -ne 0 ]; then
    echo ""
    echo "========================================"
    echo "ChromaDB 安装失败！"
    echo "========================================"
    echo ""
    echo "可能的原因："
    echo "1. 缺少编译工具（build-essential）"
    echo "2. Python 版本问题"
    echo ""
    echo "解决方案："
    echo "1. Ubuntu/Debian: sudo apt-get install build-essential"
    echo "2. CentOS/RHEL: sudo yum groupinstall 'Development Tools'"
    echo "3. 查看 docs/INSTALL.md 获取更多解决方案"
    echo ""
    exit 1
fi
echo ""

echo "[步骤 5/5] 安装 AI 相关包..."
pip install sentence-transformers torch transformers
if [ $? -ne 0 ]; then
    echo "AI 包安装失败"
    exit 1
fi
echo ""

echo "========================================"
echo "所有依赖安装完成！"
echo "========================================"
echo ""
echo "验证安装..."
python3 -c "import streamlit; import chromadb; import langchain; print('✓ 所有包安装成功！')"
if [ $? -ne 0 ]; then
    echo "验证失败，某些包可能未正确安装"
else
    echo ""
    echo "可以开始运行项目了！"
    echo "运行命令: streamlit run knowledge_base_deepseek.py"
fi
echo ""

