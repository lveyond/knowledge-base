# 📥 手动下载模型指南

当网络连接不稳定或无法访问 HuggingFace 时，可以手动下载模型文件。

## 🎯 模型信息

- **模型名称**: `BAAI/bge-small-zh-v1.5`
- **模型大小**: 约 130 MB
- **用途**: 中文文本嵌入（向量化）

## 📋 方法一：使用 huggingface-cli（推荐）

### 1. 安装 huggingface-hub

```bash
pip install huggingface-hub
```

### 2. 下载模型

```bash
huggingface-cli download BAAI/bge-small-zh-v1.5 --local-dir ./models/BAAI--bge-small-zh-v1.5
```

或者下载到 HuggingFace 默认缓存目录：

```bash
huggingface-cli download BAAI/bge-small-zh-v1.5
```

默认缓存位置：
- **Windows**: `C:\Users\<用户名>\.cache\huggingface\hub\models--BAAI--bge-small-zh-v1.5\`
- **Linux/Mac**: `~/.cache/huggingface/hub/models--BAAI--bge-small-zh-v1.5/`

## 📋 方法二：使用 Python 脚本下载

创建并运行以下脚本：

```python
from huggingface_hub import snapshot_download

# 下载到项目目录
snapshot_download(
    repo_id="BAAI/bge-small-zh-v1.5",
    local_dir="./models/BAAI--bge-small-zh-v1.5",
    local_dir_use_symlinks=False
)

print("✅ 模型下载完成！")
```

或者下载到默认缓存目录：

```python
from huggingface_hub import snapshot_download

snapshot_download(
    repo_id="BAAI/bge-small-zh-v1.5",
    local_dir_use_symlinks=False
)

print("✅ 模型下载完成！")
```

## 📋 方法三：使用 Git LFS（适合有 Git 环境）

```bash
git lfs install
git clone https://huggingface.co/BAAI/bge-small-zh-v1.5 ./models/BAAI--bge-small-zh-v1.5
```

## 📋 方法四：从镜像站点下载

如果无法访问 HuggingFace，可以使用镜像站点：

### 使用 HF-Mirror（国内镜像）

```bash
# 设置环境变量
export HF_ENDPOINT=https://hf-mirror.com

# 然后使用 huggingface-cli 下载
huggingface-cli download BAAI/bge-small-zh-v1.5 --local-dir ./models/BAAI--bge-small-zh-v1.5
```

或者在 Python 中：

```python
import os
os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com'

from huggingface_hub import snapshot_download
snapshot_download(
    repo_id="BAAI/bge-small-zh-v1.5",
    local_dir="./models/BAAI--bge-small-zh-v1.5",
    local_dir_use_symlinks=False
)
```

## 📋 方法五：手动下载文件（最后手段）

如果以上方法都不可用，可以手动下载：

1. **访问模型页面**: https://huggingface.co/BAAI/bge-small-zh-v1.5
2. **下载所有文件**（需要登录 HuggingFace 账号）:
   - `config.json`
   - `modules.json`
   - `pytorch_model.bin` 或 `model.safetensors`
   - `tokenizer_config.json`
   - `vocab.txt`
   - `special_tokens_map.json`
   - 其他相关文件

3. **创建目录结构**:
   ```
   models/
   └── BAAI--bge-small-zh-v1.5/
       ├── config.json
       ├── modules.json
       ├── pytorch_model.bin
       ├── tokenizer_config.json
       ├── vocab.txt
       └── ...
   ```

## ✅ 验证下载

下载完成后，程序会自动检测并使用本地模型。支持的路径包括：

1. **项目目录**: `./models/BAAI--bge-small-zh-v1.5/`
2. **HuggingFace 缓存**: `~/.cache/huggingface/hub/models--BAAI--bge-small-zh-v1.5/snapshots/<版本号>/`
3. **自定义路径**: 如果模型在其他位置，可以修改代码中的 `get_model_path` 函数

## 🔧 故障排除

### 问题：下载中断

**解决方案**: 使用 `resume_download=True` 参数：

```python
from huggingface_hub import snapshot_download

snapshot_download(
    repo_id="BAAI/bge-small-zh-v1.5",
    local_dir="./models/BAAI--bge-small-zh-v1.5",
    resume_download=True
)
```

### 问题：网络连接超时

**解决方案**: 
1. 使用镜像站点（方法四）
2. 使用代理
3. 分多次下载，使用 `resume_download=True` 续传

### 问题：磁盘空间不足

**解决方案**: 
- 模型大小约 130 MB，确保有至少 200 MB 可用空间
- 可以下载到其他磁盘，然后创建符号链接

## 📝 注意事项

1. **模型路径格式**: 
   - HuggingFace 模型名称中的 `/` 在本地路径中需要替换为 `--`
   - 例如：`BAAI/bge-small-zh-v1.5` → `BAAI--bge-small-zh-v1.5`

2. **版本一致性**: 
   - 确保创建向量数据库和加载向量数据库时使用相同的模型版本
   - 如果更换模型，需要重新创建向量数据库

3. **文件完整性**: 
   - 确保所有必需的文件都已下载
   - 如果文件不完整，程序可能会报错

## 🚀 快速开始

最简单的下载方式（使用镜像）：

```bash
# 1. 安装依赖
pip install huggingface-hub

# 2. 设置镜像（可选，国内用户推荐）
set HF_ENDPOINT=https://hf-mirror.com  # Windows
# export HF_ENDPOINT=https://hf-mirror.com  # Linux/Mac

# 3. 下载模型
huggingface-cli download BAAI/bge-small-zh-v1.5
```

下载完成后，重新运行程序即可自动使用本地模型！

