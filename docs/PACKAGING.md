# 📦 项目打包和分享指南

## 📋 打包给朋友使用

### 必需文件（必须包含）

以下文件是项目运行所必需的，**必须**包含在打包中：

#### 1. 核心代码文件
- `knowledge_base_deepseek.py` - 主程序文件

#### 2. 依赖配置文件
- `requirements.txt` - 完整依赖列表（推荐）
- `requirements-minimal.txt` - 最小化依赖列表（可选，如果朋友不需要向量数据库功能）

#### 3. 文档文件
- `README.md` - 项目说明文档
- `docs/` 目录下的所有文档：
  - `docs/INSTALL.md` - 安装指南
  - `docs/API_KEY_STORAGE.md` - API密钥保存说明
  - `docs/API_TIMEOUT_FIX.md` - API超时问题解决
  - `docs/SAVE_FEATURES.md` - 保存功能说明
  - `docs/VECTOR_DB_CLEANUP.md` - 向量数据库清理说明
  - `docs/README.md` - 文档说明

#### 4. 脚本文件（可选但推荐）
- `scripts/` 目录下的所有脚本：
  - `scripts/install_dependencies.bat` - Windows安装脚本
  - `scripts/install_dependencies.sh` - Linux/Mac安装脚本
  - `scripts/run.bat` - Windows启动脚本
  - `scripts/run.sh` - Linux/Mac启动脚本
  - `scripts/cleanup_vector_db.bat` - Windows清理脚本
  - `scripts/cleanup_vector_db.sh` - Linux/Mac清理脚本
  - `scripts/README.md` - 脚本说明

### 不需要打包的文件（不要包含）

以下文件是运行时生成的或包含敏感信息，**不要**包含在打包中：

#### 1. 敏感信息文件
- `.deepseek_config.json` - API密钥配置文件（包含个人密钥）

#### 2. 运行时生成的数据
- `chroma_db/` - 向量数据库目录（用户首次运行时会自动生成）
- `saved_reports/` - 保存的报告目录（用户使用时生成）
- `saved_qa/` - 保存的问答记录目录（用户使用时生成）

#### 3. Python缓存和虚拟环境
- `__pycache__/` - Python缓存目录
- `venv/`、`env/`、`.venv/` - 虚拟环境目录
- `*.pyc`、`*.pyo` - Python编译文件

#### 4. IDE配置文件
- `.vscode/` - VS Code配置
- `.idea/` - PyCharm配置

#### 5. 操作系统文件
- `.DS_Store` - macOS系统文件
- `Thumbs.db` - Windows缩略图缓存

### 📦 打包方式

#### 方式一：手动打包（推荐）

1. 创建一个新文件夹，例如 `knowledge-base-v1.0`
2. 复制以下内容：
   ```
   knowledge-base-v1.0/
   ├── knowledge_base_deepseek.py
   ├── requirements.txt
   ├── requirements-minimal.txt
   ├── README.md
   ├── .gitignore
   ├── docs/
   │   ├── INSTALL.md
   │   ├── API_KEY_STORAGE.md
   │   ├── API_TIMEOUT_FIX.md
   │   ├── SAVE_FEATURES.md
   │   ├── VECTOR_DB_CLEANUP.md
   │   └── README.md
   └── scripts/
       ├── install_dependencies.bat
       ├── install_dependencies.sh
       ├── run.bat
       ├── run.sh
       ├── cleanup_vector_db.bat
       ├── cleanup_vector_db.sh
       └── README.md
   ```
3. 压缩为 ZIP 或 7Z 文件

#### 方式二：使用 Git 导出

```bash
# 克隆项目（如果使用Git）
git clone <repository-url>
cd knowledge-base

# 创建打包文件（排除.git目录）
tar -czf knowledge-base.tar.gz --exclude='.git' --exclude='chroma_db' --exclude='saved_reports' --exclude='saved_qa' --exclude='.deepseek_config.json' --exclude='__pycache__' --exclude='venv' --exclude='.vscode' .
```

#### 方式三：使用 PowerShell（Windows）

```powershell
# 创建临时目录
$tempDir = "knowledge-base-packaged"
New-Item -ItemType Directory -Path $tempDir -Force

# 复制必需文件
Copy-Item "knowledge_base_deepseek.py" $tempDir
Copy-Item "requirements*.txt" $tempDir
Copy-Item "README.md" $tempDir
Copy-Item ".gitignore" $tempDir
Copy-Item "docs" $tempDir -Recurse
Copy-Item "scripts" $tempDir -Recurse

# 压缩
Compress-Archive -Path $tempDir -DestinationPath "knowledge-base.zip" -Force

# 清理临时目录
Remove-Item $tempDir -Recurse -Force
```

## 🚀 上传到 GitHub

### .gitignore 检查清单

当前的 `.gitignore` 文件已经正确配置，会忽略以下内容：

✅ **已正确忽略：**
- Python缓存文件（`__pycache__/`、`*.pyc`等）
- 虚拟环境目录（`venv/`、`env/`等）
- 向量数据库（`chroma_db/`）
- API密钥配置（`.deepseek_config.json`）
- 保存的报告和问答（`saved_reports/`、`saved_qa/`）
- IDE配置文件（`.vscode/`、`.idea/`）
- 操作系统文件（`.DS_Store`、`Thumbs.db`）
- 日志文件（`*.log`）
- 环境变量文件（`.env`、`.env.local`）
- 数据库文件（`*.db`、`*.sqlite`、`*.sqlite3`）

### 上传前检查

在上传前，请确认：

1. ✅ **没有包含敏感信息**
   - 检查 `.deepseek_config.json` 是否被忽略
   - 确认没有硬编码的API密钥

2. ✅ **没有包含用户数据**
   - 确认 `chroma_db/` 目录被忽略
   - 确认 `saved_reports/` 和 `saved_qa/` 目录被忽略

3. ✅ **没有包含临时文件**
   - 确认 `__pycache__/` 被忽略
   - 确认虚拟环境目录被忽略

### 上传步骤

```bash
# 1. 初始化Git仓库（如果还没有）
git init

# 2. 添加所有文件（.gitignore会自动排除不需要的文件）
git add .

# 3. 检查将要提交的文件（确保没有敏感信息）
git status

# 4. 提交
git commit -m "Initial commit: 智能知识库系统"

# 5. 在GitHub上创建新仓库，然后推送
git remote add origin https://github.com/yourusername/knowledge-base.git
git branch -M main
git push -u origin main
```

### 验证 .gitignore 是否生效

```bash
# 检查哪些文件会被Git跟踪
git status

# 或者查看所有被跟踪的文件
git ls-files

# 确认以下文件/目录不在列表中：
# - .deepseek_config.json
# - chroma_db/
# - saved_reports/
# - saved_qa/
# - __pycache__/
# - venv/
```

## 📝 注意事项

1. **API密钥安全**：确保 `.deepseek_config.json` 文件不会被上传，因为它包含个人API密钥
2. **向量数据库**：`chroma_db/` 目录可能很大，且是用户特定的，不应上传
3. **用户数据**：`saved_reports/` 和 `saved_qa/` 包含用户生成的内容，不应上传
4. **依赖安装**：朋友使用时需要先安装依赖：`pip install -r requirements.txt`

## 🎯 快速检查清单

打包前检查：
- [ ] 包含 `knowledge_base_deepseek.py`
- [ ] 包含 `requirements.txt`
- [ ] 包含 `README.md`
- [ ] 包含 `docs/` 目录
- [ ] 包含 `scripts/` 目录（可选）
- [ ] **不包含** `.deepseek_config.json`
- [ ] **不包含** `chroma_db/` 目录
- [ ] **不包含** `saved_reports/` 目录
- [ ] **不包含** `saved_qa/` 目录
- [ ] **不包含** `__pycache__/` 目录
- [ ] **不包含** 虚拟环境目录

上传GitHub前检查：
- [ ] 运行 `git status` 确认没有敏感文件
- [ ] 确认 `.gitignore` 文件存在且正确
- [ ] 确认没有硬编码的API密钥
- [ ] 确认没有用户数据文件


