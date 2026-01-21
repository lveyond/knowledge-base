# 符号化流程图转 draw.io 工具使用指南

## 📖 简介

`flowchart_to_drawio.py` 是一个将大模型生成的符号化流程图转换为 draw.io 可识别 XML 文件的工具。

## ✨ 功能特性

- ✅ 解析符号化流程图文本（支持方括号、箭头、缩进）
- ✅ 识别主要阶段（用 `[]` 包裹，通过 `↓` 连接）
- ✅ 识别子任务（通过 `→` 连接）
- ✅ 自动生成 draw.io XML 格式文件
- ✅ 支持命令行和交互式使用

## 🚀 快速开始

### 1. 基本使用

```bash
# 从文件读取并转换
python flowchart_to_drawio.py -i example_flowchart.txt -o output.drawio

# 从标准输入读取
python flowchart_to_drawio.py -i - -o output.drawio < flowchart.txt

# 交互式输入
python flowchart_to_drawio.py
```

### 2. 在 Python 代码中使用

```python
from flowchart_to_drawio import convert_flowchart_to_drawio

# 流程图文本
flowchart_text = """
[阶段一]
↓
[阶段二]
→ 子任务1 → 子任务2
↓
[阶段三]
"""

# 转换为 draw.io XML
xml_content = convert_flowchart_to_drawio(flowchart_text, "output.drawio")
print("转换完成！")
```

## 📝 流程图格式说明

### 主要阶段

主要阶段使用方括号 `[]` 包裹，通过向下箭头 `↓` 连接：

```
[阶段一]
↓
[阶段二]
↓
[阶段三]
```

### 子任务

子任务通过向右箭头 `→` 连接，可以放在主要阶段同一行或单独一行：

```
[主要阶段]
→ 子任务1 → 子任务2 → 子任务3
```

或者：

```
[主要阶段]
↓
→ 子任务1 → 子任务2
```

### 缩进层级

使用缩进表示层级关系（每2个空格为一级）：

```
[主要阶段]
  → 一级子任务
    → 二级子任务
```

### 完整示例

```
技术路线图:

[行业需求与痛点]
↓
[需求调研与分析]
→输出《需求分析说明书》
↓
[核心算法研究]
→ CNN目标检测(YOLO) → 烟包识别模型
→ CNN人脸识别 → 人脸比对模型
→ OCR技术 → 店招文字识别模型
↓
[智能预警引擎构建]
→ "规则引擎 + 机器学习"融合
```

## 🎨 输出格式

生成的 draw.io 文件包含：

- **主要阶段节点**：绿色背景，加粗字体
- **子任务节点**：蓝色背景，普通字体
- **连接线**：自动连接主要阶段（向下）和子任务（水平或向下）

## 📋 命令行参数

```
python flowchart_to_drawio.py [选项]

选项:
  -i, --input FILE    输入文件路径（使用 - 表示从标准输入读取）
  -o, --output FILE   输出文件路径（默认: flowchart.drawio）
  -h, --help          显示帮助信息
```

## 🔧 使用示例

### 示例 1: 从文件转换

```bash
python flowchart_to_drawio.py -i example_flowchart.txt -o my_flowchart.drawio
```

### 示例 2: 交互式输入

```bash
python flowchart_to_drawio.py
# 然后输入流程图文本，输入空行结束
```

### 示例 3: 管道输入

```bash
echo "[阶段一]\n↓\n[阶段二]" | python flowchart_to_drawio.py -i - -o output.drawio
```

## 📂 文件说明

- `flowchart_to_drawio.py` - 主程序文件
- `example_flowchart.txt` - 示例流程图文本
- `docs/FLOWCHART_CONVERTER.md` - 本文档

## ⚠️ 注意事项

1. **编码格式**：确保输入文件使用 UTF-8 编码
2. **箭头符号**：使用中文箭头 `→` 和 `↓`，不是英文箭头
3. **方括号**：主要阶段必须使用方括号 `[]` 包裹
4. **缩进**：使用空格缩进，每2个空格为一级

## 🐛 常见问题

### Q: 生成的 draw.io 文件无法打开？

A: 确保文件扩展名为 `.drawio` 或 `.xml`，并使用 draw.io 或 diagrams.net 打开。

### Q: 节点位置不理想？

A: 可以在 draw.io 中手动调整节点位置，工具会自动生成基本的布局。

### Q: 如何自定义节点样式？

A: 可以修改 `flowchart_to_drawio.py` 中的 `_get_node_style()` 方法来调整样式。

## 📄 许可证

本项目仅供学习和研究使用。
