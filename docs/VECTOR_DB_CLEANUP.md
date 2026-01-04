# 🗑️ 向量数据库清理指南

## 📊 空间占用说明

### 向量数据库空间占用

向量数据库的空间占用主要取决于：

1. **文档数量和大小**
   - 每个文档会被分割成多个文本块（chunk）
   - 每个文本块会生成一个向量（embedding）
   - 向量大小：约 384 维（BAAI/bge-small-zh-v1.5 模型）

2. **估算公式**
   ```
   向量数据库大小 ≈ 文档总大小 × 1.5 ~ 2.5 倍
   ```
   - 例如：100MB 文档 → 约 150-250MB 向量数据库
   - 包含：向量数据 + 元数据 + 索引文件

3. **实际占用**
   - 小型文档库（< 50MB）：通常 < 100MB
   - 中型文档库（50-500MB）：约 100MB - 1GB
   - 大型文档库（> 500MB）：可能 > 1GB

### HuggingFace 模型缓存

**位置**：`C:\Users\<用户名>\.cache\huggingface\`

**大小**：约 **400-500 MB**

**说明**：
- 首次使用时会自动下载嵌入模型
- 模型文件会被缓存，后续使用无需重新下载
- 如果删除，下次使用需要重新下载

## 🗑️ 清理方法

### 方法一：使用清理脚本（推荐）

**Windows:**
```bash
scripts\cleanup_vector_db.bat
```

**Linux/Mac:**
```bash
chmod +x scripts/cleanup_vector_db.sh
./scripts/cleanup_vector_db.sh
```

脚本会：
1. 删除项目目录下的 `chroma_db` 文件夹
2. 询问是否删除 HuggingFace 模型缓存
3. 显示清理结果

### 方法二：在应用界面中删除

1. 打开应用
2. 在侧边栏找到"向量数据库管理"
3. 点击"🗑️ 删除向量数据库"按钮
4. 向量数据库会被立即删除

### 方法三：手动删除

**删除向量数据库：**
```bash
# Windows
rmdir /s /q chroma_db

# Linux/Mac
rm -rf chroma_db
```

**删除 HuggingFace 模型缓存：**
```bash
# Windows
rmdir /s /q C:\Users\<用户名>\.cache\huggingface

# Linux/Mac
rm -rf ~/.cache/huggingface
```

## 📍 文件位置

### 向量数据库
- **位置**：项目根目录下的 `chroma_db/` 文件夹
- **路径示例**：`E:\Cursor原型\knowledge-base\chroma_db\`

### HuggingFace 模型缓存
- **Windows**：`C:\Users\<用户名>\.cache\huggingface\`
- **Linux/Mac**：`~/.cache/huggingface/`

## ⚠️ 注意事项

1. **删除向量数据库后**
   - 下次加载文档时会自动重新创建
   - 需要重新处理所有文档（可能需要几分钟）

2. **删除模型缓存后**
   - 首次使用需要重新下载模型（约400-500MB）
   - 需要网络连接
   - 下载可能需要几分钟

3. **建议**
   - 如果只是临时清理空间，可以只删除向量数据库
   - 如果确定不再使用，可以删除模型缓存
   - 模型缓存可以跨项目共享，删除后会影响所有使用该模型的项目

## 💡 节省空间的建议

1. **定期清理**
   - 如果不再需要某些文档的向量数据库，可以删除
   - 下次需要时重新创建即可

2. **选择性创建**
   - 如果文档很多，可以考虑只对重要文档创建向量数据库
   - 其他文档使用普通搜索功能

3. **使用外部存储**
   - 可以将向量数据库移动到其他盘（需要修改代码中的路径）
   - 或者使用云存储

4. **清理旧数据**
   - 定期清理不再使用的文档
   - 删除对应的向量数据库

## 🔍 检查空间占用

### 检查向量数据库大小

**Windows PowerShell:**
```powershell
cd "E:\Cursor原型\knowledge-base"
if (Test-Path "chroma_db") {
    $size = (Get-ChildItem -Path "chroma_db" -Recurse | Measure-Object -Property Length -Sum).Sum
    Write-Host "向量数据库大小: $([math]::Round($size / 1MB, 2)) MB"
}
```

**Linux/Mac:**
```bash
du -sh chroma_db
```

### 检查 HuggingFace 缓存大小

**Windows PowerShell:**
```powershell
$hfCache = "$env:USERPROFILE\.cache\huggingface"
if (Test-Path $hfCache) {
    $size = (Get-ChildItem -Path $hfCache -Recurse | Measure-Object -Property Length -Sum).Sum
    Write-Host "HuggingFace 缓存大小: $([math]::Round($size / 1GB, 2)) GB"
}
```

**Linux/Mac:**
```bash
du -sh ~/.cache/huggingface
```

## ❓ 常见问题

### Q: 删除向量数据库会影响应用使用吗？

A: 不会。删除后：
- 文档阅读功能正常
- 问答功能正常（但会使用所有文档内容，可能较慢）
- 向量搜索功能不可用（直到重新创建）

### Q: 删除模型缓存会影响其他项目吗？

A: 会。如果其他项目也使用相同的模型，删除后它们也需要重新下载。

### Q: 可以只删除部分向量数据吗？

A: 目前不支持部分删除。如果需要，可以：
1. 删除整个向量数据库
2. 重新加载需要的文档
3. 创建新的向量数据库

### Q: 向量数据库可以移动到其他位置吗？

A: 可以，但需要修改代码中的 `persist_directory` 参数。或者：
1. 删除现有向量数据库
2. 修改代码中的路径
3. 重新创建向量数据库


