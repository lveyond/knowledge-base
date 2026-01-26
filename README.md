# 📚 智能知识库系统 (DeepSeek版)

一个基于 Streamlit 和 DeepSeek API 的智能知识库系统，支持多种文档格式的读取、向量化存储和智能问答。

## ✨ 功能特性

- 📄 **多格式文档支持**：支持 TXT、DOCX、PDF、Excel (XLSX/XLS) 文件
- 🔍 **本地向量数据库**：使用 ChromaDB 和 HuggingFace 嵌入模型，无需外部 API 密钥
- 🤖 **智能问答**：基于 DeepSeek API 的文档问答功能
- 📊 **文档总结**：自动生成知识库总结报告
- 🎯 **语义搜索**：基于向量相似度的文档检索
- 💬 **对话历史**：保存问答历史记录
- 📐 **流程图生成**：将符号化流程图文本转换为 draw.io 格式文件
- 📊 **甘特图生成**：将项目进度甘特图表数据转换为 draw.io 格式文件

## 🚀 快速开始

### 📦 Windows用户 - 一键安装版本（推荐）

如果您是Windows用户且不想手动安装Python环境，可以使用打包版本：

1. **下载打包版本**（如果有提供）
2. **解压文件**
3. **双击"启动应用.bat"**即可使用

详细说明请查看：[Windows打包版本使用说明](使用说明-打包版.txt)

### 1. 安装依赖

**⭐ 推荐方式（使用 Poetry - Python 3.11 环境）：**

```bash
# 1. 配置 Poetry 使用 Python 3.11
poetry env use py -3.11

# 2. 安装所有依赖
poetry install

# 3. 激活环境并运行
poetry shell
streamlit run knowledge_base_deepseek.py

# 或者直接运行（无需激活）
poetry run streamlit run knowledge_base_deepseek.py
```

📖 **详细 Poetry 使用说明**：请查看 [docs/POETRY_SETUP.md](docs/POETRY_SETUP.md)

**方式二（使用安装脚本）：**

```bash
# Windows
scripts\install_dependencies.bat

# Linux/Mac
chmod +x scripts/install_dependencies.sh
./scripts/install_dependencies.sh
```

**方式三（手动安装）：**

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

### 制作流程图文件

1. 在"高级功能"区域点击"📐 制作流程图文件"按钮
2. 从批量总结报告中复制流程图部分的文本
3. 将文本粘贴到对话框中
4. 点击"生成流程图"按钮
5. 系统会自动生成并下载 draw.io 格式的流程图文件
6. 使用 [draw.io](https://app.diagrams.net/) 打开文件进行编辑

**流程图格式示例：**
```
[阶段一]
↓
[阶段二]
→ 子任务1 → 子任务2
↓
[阶段三]
```

### 制作甘特图文件

1. 准备项目进度甘特图表数据（表格格式）
2. 使用命令行工具转换：
   ```bash
   python gantt_to_drawio.py -i gantt_data.txt -o output.drawio
   ```
3. 使用 [draw.io](https://app.diagrams.net/) 打开文件进行编辑

**甘特图数据格式示例：**
```
任务ID	任务名称	开始时间	结束时间	工期(月)	前置任务	责任方/备注
1	项目启动	M0	M1	2		
1.1	项目立项	M0	M0+0.5	0.5		甲方、乙方
1.2	需求调研	M0+0.5	M1	0.5	1.1	乙方
```

📖 **详细使用说明**：请查看 [docs/GANTT_CONVERTER.md](docs/GANTT_CONVERTER.md)

📝 **Prompt模板**：使用AI生成甘特图数据时，可使用 [docs/GANTT_PROMPT_TEMPLATE.md](docs/GANTT_PROMPT_TEMPLATE.md) 中的模板

💡 **快速开始**：
- 使用示例数据测试：`python gantt_to_drawio.py -i example_gantt_data.txt -o test.drawio`
- 使用简化模板：复制 `gantt_prompt_template.txt` 的内容，填写项目信息后发送给AI

## 🛠️ 技术栈

- **前端框架**：Streamlit
- **向量数据库**：ChromaDB
- **嵌入模型**：BAAI/bge-small-zh-v1.5 (HuggingFace)
- **LLM API**：DeepSeek
- **文档处理**：
  - python-docx (Word文档)
  - pypdf (PDF文档)
  - pandas/openpyxl (Excel文档)

## 📦 Windows应用程序打包

如果您想将本项目打包成Windows可执行程序，请参考：

- **打包指南**：[docs/WINDOWS_PACKAGING.md](docs/WINDOWS_PACKAGING.md)
- **打包脚本目录**：`build_script/`（包含所有打包相关文件）
  - `build_windows.bat` - PyInstaller打包脚本（推荐）
  - `build_simple.bat` - 简化打包脚本（安装包方案）
  - `build_windows.spec` - PyInstaller配置文件
  - `install.bat` - 一键安装脚本
  - `launcher.py` - 启动器脚本
  - `打包说明.txt` - 打包说明文档
  - `使用说明-打包版.txt` - 打包版本使用说明

### 快速打包

```bash
# 进入打包脚本目录
cd build_script

# 运行打包脚本（PyInstaller方案）
build_windows.bat

# 或运行简化打包脚本（安装包方案）
build_simple.bat

# 打包完成后，文件位于 dist\智能知识库系统\
```

## 📁 项目结构

```
knowledge-base/
├── knowledge_base_deepseek.py  # 主程序文件
├── download_model.py            # 模型下载脚本
├── flowchart_to_drawio.py       # 流程图转draw.io工具
├── gantt_to_drawio.py          # 甘特图转draw.io工具
├── pyproject.toml               # Poetry 项目配置文件
├── poetry.lock                  # Poetry 锁定文件
├── requirements.txt            # 依赖包列表（pip 方式）
├── requirements-minimal.txt    # 最小化依赖列表
├── README.md                   # 项目说明
├── .streamlit/                 # Streamlit 配置目录
│   └── config.toml             # Streamlit 配置文件
├── build_script/               # Windows打包脚本目录
│   ├── build_windows.bat       # PyInstaller打包脚本（推荐）
│   ├── build_simple.bat        # 简化打包脚本（安装包方案）
│   ├── build_windows.spec      # PyInstaller配置文件
│   ├── install.bat             # 一键安装脚本
│   ├── launcher.py             # 启动器脚本（用于打包）
│   ├── 打包说明.txt            # 打包说明文档
│   └── 使用说明-打包版.txt     # 打包版本使用说明
├── docs/                       # 文档目录
│   ├── INSTALL.md             # 安装指南
│   ├── MODEL_DOWNLOAD_GUIDE.md # 模型下载指南
│   ├── API_KEY_STORAGE.md     # API密钥保存说明
│   ├── API_TIMEOUT_FIX.md     # API超时问题解决
│   ├── POETRY_SETUP.md        # Poetry 使用说明
│   ├── PACKAGING.md           # 打包说明
│   ├── WINDOWS_PACKAGING.md   # Windows打包详细指南
│   ├── SAVE_FEATURES.md       # 保存功能说明
│   ├── VECTOR_DB_CLEANUP.md   # 向量数据库清理说明
│   ├── FLOWCHART_CONVERTER.md # 流程图转换工具说明
│   └── GANTT_CONVERTER.md     # 甘特图转换工具说明
├── scripts/                    # 脚本目录
│   ├── install_dependencies.bat  # Windows安装脚本
│   ├── install_dependencies.sh   # Linux/Mac安装脚本
│   ├── run.bat                  # Windows启动脚本
│   ├── run.sh                   # Linux/Mac启动脚本
│   ├── setup_poetry.bat         # Windows Poetry设置脚本
│   ├── setup_poetry.sh          # Linux/Mac Poetry设置脚本
│   ├── cleanup_vector_db.bat    # Windows向量数据库清理脚本
│   ├── cleanup_vector_db.sh     # Linux/Mac向量数据库清理脚本
│   ├── fix_dependencies.bat     # Windows依赖修复脚本
│   ├── fix_dependencies.sh     # Linux/Mac依赖修复脚本
│   ├── fix_chromadb.bat         # ChromaDB修复脚本
│   ├── fix_zstandard_install.bat # zstandard安装修复脚本
│   ├── force_fix_dependencies.bat # 强制修复依赖脚本
│   └── README.md                # 脚本使用说明
├── prompt_templates/           # Prompt模版目录
│   ├── summary_templates.json  # 总结模版配置
│   └── analysis_templates.json # 分析模版配置
├── models/                     # 本地模型存储目录（可选）
│   └── BAAI--bge-small-zh-v1.5/  # 手动下载的模型文件
├── chroma_db/                  # 向量数据库存储目录（自动生成）
└── saved_reports/              # 保存的报告目录（自动生成）
```

## ⚙️ 配置说明

### DeepSeek API 模型选择

- **deepseek-chat**：通用对话模型，适合大多数问答场景
- **deepseek-coder**：代码专用模型，适合技术文档和代码相关问题

### 向量数据库配置

- 使用本地嵌入模型，无需额外 API 密钥
- 向量数据库存储在 `./chroma_db` 目录
- 首次加载文档时会自动创建向量数据库

### 📥 手动下载 HuggingFace 模型（网络不稳定时）

当网络连接不稳定或无法访问 HuggingFace 时，可以手动下载模型文件。

**模型信息：**
- 模型名称：`BAAI/bge-small-zh-v1.5`
- 模型大小：约 130 MB
- 用途：中文文本嵌入（向量化）

**方法一：使用下载脚本（推荐）**

```bash
python download_model.py
```

脚本会引导你选择下载方式和位置，支持：
- 使用国内镜像（HF-Mirror）
- 断点续传
- 选择下载位置（项目目录或 HuggingFace 缓存目录）

**方法二：使用命令行工具**

```bash
# 1. 安装依赖
pip install huggingface-hub

# 2. 设置镜像（可选，国内用户推荐）
set HF_ENDPOINT=https://hf-mirror.com  # Windows
# export HF_ENDPOINT=https://hf-mirror.com  # Linux/Mac

# 3. 下载模型到项目目录
huggingface-cli download BAAI/bge-small-zh-v1.5 --local-dir ./models/BAAI--bge-small-zh-v1.5

# 或下载到 HuggingFace 默认缓存目录
huggingface-cli download BAAI/bge-small-zh-v1.5
```

**方法三：使用 Python 代码**

```python
from huggingface_hub import snapshot_download
import os

# 使用镜像（可选，国内用户推荐）
os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com'

# 下载到项目目录
snapshot_download(
    repo_id="BAAI/bge-small-zh-v1.5",
    local_dir="./models/BAAI--bge-small-zh-v1.5",
    local_dir_use_symlinks=False,
    resume_download=True  # 支持断点续传
)
```

**支持的模型路径：**

程序会自动检测以下位置的模型：
1. **项目目录**：`./models/BAAI--bge-small-zh-v1.5/`
2. **HuggingFace 缓存**：`~/.cache/huggingface/hub/models--BAAI--bge-small-zh-v1.5/`
3. 如果都不存在，会自动从 HuggingFace 下载

**详细说明：** 请查看 [docs/MODEL_DOWNLOAD_GUIDE.md](docs/MODEL_DOWNLOAD_GUIDE.md)

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
- 首次运行时会自动下载嵌入模型（约 130MB），需要一定时间和网络连接
- 如果 `chromadb` 未安装，程序仍可运行，但会使用所有文档内容进行问答（可能较慢）

### Q: 下载模型时网络连接失败或超时？

A: 如果遇到网络问题，可以手动下载模型：

1. **使用下载脚本**（最简单）：
   ```bash
   python download_model.py
   ```

2. **使用国内镜像**：
   ```bash
   set HF_ENDPOINT=https://hf-mirror.com  # Windows
   huggingface-cli download BAAI/bge-small-zh-v1.5
   ```

3. **手动下载后放置到项目目录**：
   - 下载模型到 `./models/BAAI--bge-small-zh-v1.5/` 目录
   - 程序会自动检测并使用本地模型

详细说明请查看 [docs/MODEL_DOWNLOAD_GUIDE.md](docs/MODEL_DOWNLOAD_GUIDE.md)

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
- 首次运行时会自动下载嵌入模型（约 130MB），请确保网络连接正常
- 如果网络不稳定，可以使用 `download_model.py` 脚本手动下载模型
- 程序会自动检测本地模型，优先使用本地文件，避免重复下载
- 大量文档处理可能需要较长时间，请耐心等待

## 📄 许可证

本项目采用双重许可证，**仅限个人和非商业使用**：

- **MIT License (Non-Commercial)** - 查看 [LICENSE-MIT-NC](LICENSE-MIT-NC) 文件
- **Apache License 2.0 (Non-Commercial)** - 查看 [LICENSE-APACHE-NC](LICENSE-APACHE-NC) 文件

**使用限制：**
- ✅ **允许**：个人学习、研究、教育用途
- ✅ **允许**：非营利组织使用
- ❌ **禁止**：任何商业用途（包括但不限于：商业产品、服务、销售、营利性企业内部使用等）

如需商业使用，请联系版权所有者获取商业许可证。

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

---

## ©️ 版权说明

**Copyright © 2026 吕滢**

- **GitHub**: [@lveyond](https://github.com/lveyond)
- **QQ/WeChat**: 329613507

本项目采用 MIT 和 Apache 2.0 双重许可证（仅限个人和非商业使用）。
