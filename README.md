# 📚 智能知识库系统 (DeepSeek版)

一个基于 Streamlit 和 DeepSeek API 的智能知识库系统，支持多种文档格式的读取、向量化存储和智能问答。

## ✨ 功能特性

- 📄 **多格式文档支持**：支持 TXT、DOCX、PDF、Excel (XLSX/XLS) 文件
- 🔍 **本地向量数据库**：使用 ChromaDB 和 HuggingFace 嵌入模型，无需外部 API 密钥
- 🤖 **智能问答**：基于 DeepSeek API 的文档问答功能
- 📊 **文档总结**：自动生成知识库总结报告
- 🎯 **语义搜索**：基于向量相似度的文档检索
- 💬 **对话历史**：保存问答历史记录

## 🚀 快速开始

### 1. 安装依赖

**推荐方式（使用安装脚本）：**

```bash
# Windows
scripts\install_dependencies.bat

# Linux/Mac
chmod +x scripts/install_dependencies.sh
./scripts/install_dependencies.sh
```

**手动安装：**

```bash
# 首先更新 pip 和构建工具
python -m pip install --upgrade pip setuptools wheel

# 然后安装依赖
pip install -r requirements.txt
```

**⚠️ 如果遇到编译错误（zstandard/chromadb）：**

如果安装 `chromadb` 时出现需要 Microsoft Visual C++ 14.0 的错误，请：

1. **方案一（推荐）**：使用安装脚本 `scripts/install_dependencies.bat`，它会分步安装并提供错误提示
2. **方案二**：安装 [Microsoft C++ Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/)
3. **方案三**：使用最小化版本（无向量数据库功能）：
   ```bash
   pip install -r requirements-minimal.txt
   ```
4. **详细解决方案**：请查看 [docs/INSTALL.md](docs/INSTALL.md)

### 2. 获取 DeepSeek API 密钥

1. 访问 [DeepSeek Platform](https://platform.deepseek.com/)
2. 注册账号并获取 API 密钥

### 3. 运行应用

```bash
# 方式一：直接运行
streamlit run knowledge_base_deepseek.py

# 方式二：使用启动脚本
# Windows
scripts\run.bat

# Linux/Mac
chmod +x scripts/run.sh
./scripts/run.sh
```

应用将在浏览器中自动打开，默认地址：`http://localhost:8501`

## 📖 使用说明

### 加载文档

**方式一：加载文件夹**
1. 在侧边栏的"文件夹路径"输入框中输入文档文件夹路径
2. 点击"📂 加载文件夹"按钮
3. 系统会自动读取文件夹中的所有支持格式文件

**方式二：上传文件**
1. 在侧边栏点击"选择文件"
2. 选择要上传的文件（支持多选）
3. 点击"上传文件"按钮

### 智能问答

1. 在侧边栏输入 DeepSeek API 密钥
2. 在主界面的"输入您的问题"文本框中输入问题
3. 点击"🔍 搜索答案"按钮
4. 系统会基于文档内容生成答案

### 生成总结报告

1. 加载文档后，点击"生成知识库总结报告"按钮
2. 系统会分析所有文档并生成详细报告
3. 可以下载报告为文本文件

## 🛠️ 技术栈

- **前端框架**：Streamlit
- **向量数据库**：ChromaDB
- **嵌入模型**：BAAI/bge-small-zh-v1.5 (HuggingFace)
- **LLM API**：DeepSeek
- **文档处理**：
  - python-docx (Word文档)
  - pypdf (PDF文档)
  - pandas/openpyxl (Excel文档)

## 📁 项目结构

```
knowledge-base/
├── knowledge_base_deepseek.py  # 主程序文件
├── requirements.txt            # 依赖包列表
├── requirements-minimal.txt    # 最小化依赖列表
├── README.md                   # 项目说明
├── docs/                       # 文档目录
│   ├── INSTALL.md             # 安装指南
│   ├── API_KEY_STORAGE.md     # API密钥保存说明
│   ├── API_TIMEOUT_FIX.md     # API超时问题解决
│   └── SAVE_FEATURES.md       # 保存功能说明
├── scripts/                    # 脚本目录
│   ├── install_dependencies.bat  # Windows安装脚本
│   ├── install_dependencies.sh   # Linux/Mac安装脚本
│   ├── run.bat                  # Windows启动脚本
│   └── run.sh                   # Linux/Mac启动脚本
└── chroma_db/                  # 向量数据库存储目录（自动生成）
```

## ⚙️ 配置说明

### DeepSeek API 模型选择

- **deepseek-chat**：通用对话模型，适合大多数问答场景
- **deepseek-coder**：代码专用模型，适合技术文档和代码相关问题

### 向量数据库配置

- 使用本地嵌入模型，无需额外 API 密钥
- 向量数据库存储在 `./chroma_db` 目录
- 首次加载文档时会自动创建向量数据库

## 🔧 常见问题

### Q: 安装依赖时出现 zstandard/chromadb 编译错误？

A: 这是因为 `chromadb` 依赖 `zstandard`，需要编译工具。解决方案：
- Windows: 安装 [Microsoft C++ Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/)
- 或使用 `scripts/install_dependencies.bat` 脚本分步安装
- 或使用 `requirements-minimal.txt`（无向量数据库功能）
- 详细说明请查看 [docs/INSTALL.md](docs/INSTALL.md)

### Q: 向量数据库创建失败怎么办？

A: 
- 确保已安装所有依赖包，特别是 `sentence-transformers` 和 `chromadb`
- 首次运行时会自动下载嵌入模型（约几百MB），需要一定时间和网络连接
- 如果 `chromadb` 未安装，程序仍可运行，但会使用所有文档内容进行问答（可能较慢）

### Q: PDF 文件读取失败？

A: 确保已安装 `pypdf` 包。某些加密或特殊格式的 PDF 可能无法读取。

### Q: Excel 文件读取失败？

A: 确保已安装 `pandas` 和 `openpyxl` 包。

### Q: 如何提高问答质量？

A: 
- 确保文档内容清晰完整
- 使用更具体的问题
- 尝试使用不同的模型（deepseek-chat 或 deepseek-coder）

## 📝 注意事项

- DeepSeek API 需要有效的 API 密钥才能使用问答功能
- 向量数据库功能不需要 API 密钥，可以独立使用
- 首次运行时会下载嵌入模型（约几百MB），请确保网络连接正常
- 大量文档处理可能需要较长时间，请耐心等待

## 📄 许可证

本项目仅供学习和研究使用。

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

