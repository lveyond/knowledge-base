#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
甘特图转 draw.io 工具
将项目进度甘特图表信息转换为 draw.io 可识别的 XML 文件

Copyright (c) 2026 吕滢

Licensed under the MIT License (Non-Commercial) or Apache License 2.0 (Non-Commercial)
See LICENSE-MIT-NC or LICENSE-APACHE-NC for details.

This software is for NON-COMMERCIAL USE ONLY.
For commercial use, please contact the copyright holder.
"""

import re
import xml.etree.ElementTree as ET
from xml.dom import minidom
from typing import List, Dict, Tuple, Optional
import argparse
import sys
from datetime import datetime


class GanttParser:
    """解析甘特图表数据"""
    
    def __init__(self, text: str):
        self.text = text
        self.tasks = []  # 存储解析后的任务信息
        
    def parse(self) -> List[Dict]:
        """
        解析甘特图表文本
        返回: tasks列表，每个任务包含：
        - id: 任务ID
        - name: 任务名称
        - start_month: 开始月份（数字）
        - end_month: 结束月份（数字）
        - duration: 工期（月）
        - dependencies: 前置任务ID列表
        - responsible: 责任方/备注
        - level: 层级（根据任务ID的点号数量）
        """
        lines = [line.rstrip() for line in self.text.strip().split('\n')]
        
        # 跳过表头行
        header_found = False
        for i, line in enumerate(lines):
            if '任务ID' in line or '任务名称' in line:
                header_found = True
                continue
            
            if not header_found:
                continue
                
            if not line.strip() or line.strip().startswith('---'):
                continue
            
            # 解析表格行（支持制表符或空格分隔）
            parts = [p.strip() for p in re.split(r'\t+| {2,}', line)]
            if len(parts) < 3:
                continue
            
            task_id = parts[0].strip()
            task_name = parts[1].strip() if len(parts) > 1 else ''
            start_time = parts[2].strip() if len(parts) > 2 else ''
            end_time = parts[3].strip() if len(parts) > 3 else ''
            duration = parts[4].strip() if len(parts) > 4 else ''
            dependencies = parts[5].strip() if len(parts) > 5 else ''
            responsible = parts[6].strip() if len(parts) > 6 else ''
            
            # 解析时间
            start_month = self._parse_month(start_time)
            end_month = self._parse_month(end_time)
            
            # 计算层级（根据任务ID的点号数量）
            level = task_id.count('.')
            
            # 解析依赖关系
            dep_list = []
            if dependencies:
                # 支持逗号、空格、点号分隔
                dep_parts = re.split(r'[,，\s]+', dependencies)
                dep_list = [d.strip() for d in dep_parts if d.strip()]
            
            task_info = {
                'id': task_id,
                'name': task_name,
                'start_month': start_month,
                'end_month': end_month,
                'duration': duration,
                'dependencies': dep_list,
                'responsible': responsible,
                'level': level
            }
            
            self.tasks.append(task_info)
        
        return self.tasks
    
    def _parse_month(self, time_str: str) -> float:
        """
        解析时间字符串，返回月份数字
        支持格式：M0, M1, M1+0.5, M1.5, M7+0.5等
        """
        if not time_str:
            return 0.0
        
        time_str = time_str.strip()
        
        # 匹配 M数字 或 M数字+小数 或 M数字.小数
        match = re.match(r'M(\d+(?:\.\d+)?)(?:\+(\d+(?:\.\d+)?))?', time_str)
        if match:
            base = float(match.group(1))
            offset = float(match.group(2)) if match.group(2) else 0.0
            return base + offset
        
        # 如果没有匹配到，尝试提取数字
        numbers = re.findall(r'\d+\.?\d*', time_str)
        if numbers:
            return float(numbers[0])
        
        return 0.0


class GanttDrawIOGenerator:
    """生成 draw.io 甘特图 XML 文件"""
    
    def __init__(self, tasks: List[Dict]):
        self.tasks = tasks
        self.task_positions = {}  # 任务ID -> (x, y, width, height)
        
        # 计算时间范围
        self.min_month = min([t['start_month'] for t in tasks] + [0])
        self.max_month = max([t['end_month'] for t in tasks] + [12])
        
        # 检测是否有超长任务（超过12个月）
        max_duration = max([t['end_month'] - t['start_month'] for t in tasks] + [0])
        has_long_task = max_duration > 12
        
        # 配置
        # 如果有超长任务，压缩月份宽度以避免画布过宽
        if has_long_task and (self.max_month - self.min_month) > 20:
            # 对于超长跨度，使用较小的月份宽度
            self.month_width = max(30, 2000 / (self.max_month - self.min_month + 1))
        else:
            self.month_width = 80  # 每个月的宽度（像素）
        
        self.task_height = 30  # 每个任务条的高度
        self.task_spacing = 10  # 任务之间的间距
        self.label_width = 200  # 任务名称标签的宽度
        self.remark_width = 250  # 备注列（责任方/备注）的宽度
        self.time_header_height = 60  # 时间轴标题的高度
        self.left_margin = 20  # 左边距
        self.top_margin = 20  # 上边距
        
    def generate(self) -> str:
        """生成 draw.io XML 内容"""
        # 计算任务位置
        self._calculate_positions()
        
        # 创建 XML 根元素
        root = ET.Element('mxfile', {
            'host': 'app.diagrams.net',
            'modified': datetime.now().strftime('%Y-%m-%dT%H:%M:%S.000Z'),
            'agent': '5.0',
            'version': '21.0.0',
            'etag': 'xxx',
            'type': 'device'
        })
        
        diagram = ET.SubElement(root, 'diagram', {
            'id': 'gantt',
            'name': '甘特图'
        })
        
        # 计算画布大小（包含任务名称列、备注列和时间轴区域）
        canvas_width = self.label_width + self.remark_width + (self.max_month - self.min_month + 1) * self.month_width + 100
        canvas_height = self.time_header_height + len(self.tasks) * (self.task_height + self.task_spacing) + 100
        
        mx_graph_model = ET.SubElement(diagram, 'mxGraphModel', {
            'dx': str(canvas_width),
            'dy': str(canvas_height),
            'grid': '1',
            'gridSize': '10',
            'guides': '1',
            'tooltips': '1',
            'connect': '1',
            'arrows': '1',
            'fold': '1',
            'page': '1',
            'pageScale': '1',
            'pageWidth': str(canvas_width),
            'pageHeight': str(canvas_height),
            'math': '0',
            'shadow': '0'
        })
        
        root_element = ET.SubElement(mx_graph_model, 'root')
        
        # 添加默认的根 cell（draw.io 必需）
        root_cell = ET.SubElement(root_element, 'mxCell', {
            'id': '0'
        })
        
        default_parent = ET.SubElement(root_element, 'mxCell', {
            'id': '1',
            'parent': '0'
        })
        
        # 绘制列标题
        self._draw_column_headers(root_element, default_parent)
        
        # 绘制时间轴
        self._draw_time_axis(root_element, default_parent)
        
        # 绘制任务条
        self._draw_task_bars(root_element, default_parent)
        
        # 绘制依赖关系箭头（已禁用，避免图表杂乱）
        # self._draw_dependencies(root_element, default_parent)
        
        # 转换为字符串
        rough_string = ET.tostring(root, encoding='unicode')
        reparsed = minidom.parseString(rough_string)
        return reparsed.toprettyxml(indent="  ")
    
    def _calculate_positions(self):
        """计算任务条的位置"""
        y_start = self.top_margin + self.time_header_height
        
        for i, task in enumerate(self.tasks):
            # Y位置（垂直排列）
            y = y_start + i * (self.task_height + self.task_spacing)
            
            # X位置（根据开始月份，考虑任务名称列和备注列）
            x = self.left_margin + self.label_width + self.remark_width + (task['start_month'] - self.min_month) * self.month_width
            
            # 宽度（根据工期）
            width = (task['end_month'] - task['start_month']) * self.month_width
            
            self.task_positions[task['id']] = {
                'x': x,
                'y': y,
                'width': width,
                'height': self.task_height,
                'task': task
            }
    
    def _draw_column_headers(self, root_element, parent):
        """绘制列标题"""
        # 任务名称列标题
        name_header = ET.SubElement(root_element, 'mxCell', {
            'id': 'header_task_name',
            'value': '任务名称',
            'style': 'text;html=1;strokeColor=#666666;fillColor=#f5f5f5;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontStyle=1;fontSize=12;',
            'vertex': '1',
            'parent': parent.get('id')
        })
        
        ET.SubElement(name_header, 'mxGeometry', {
            'x': str(self.left_margin),
            'y': str(self.top_margin + 30),
            'width': str(self.label_width),
            'height': '30',
            'as': 'geometry'
        })
        
        # 备注列标题
        remark_header = ET.SubElement(root_element, 'mxCell', {
            'id': 'header_remark',
            'value': '责任方/备注',
            'style': 'text;html=1;strokeColor=#666666;fillColor=#f5f5f5;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontStyle=1;fontSize=12;',
            'vertex': '1',
            'parent': parent.get('id')
        })
        
        ET.SubElement(remark_header, 'mxGeometry', {
            'x': str(self.left_margin + self.label_width),
            'y': str(self.top_margin + 30),
            'width': str(self.remark_width),
            'height': '30',
            'as': 'geometry'
        })
    
    def _draw_time_axis(self, root_element, parent):
        """绘制时间轴"""
        # 绘制时间轴标题
        time_label = ET.SubElement(root_element, 'mxCell', {
            'id': 'time_label',
            'value': '时间轴 (月)',
            'style': 'text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontStyle=1;fontSize=14;',
            'vertex': '1',
            'parent': parent.get('id')
        })
        
        ET.SubElement(time_label, 'mxGeometry', {
            'x': str(self.left_margin + self.label_width + self.remark_width),
            'y': str(self.top_margin),
            'width': str((self.max_month - self.min_month + 1) * self.month_width),
            'height': '30',
            'as': 'geometry'
        })
        
        # 计算月份刻度间隔（如果跨度太大，只显示部分刻度）
        month_span = self.max_month - self.min_month
        if month_span > 24:
            # 跨度超过24个月，每3个月显示一个刻度
            step = 3
        elif month_span > 12:
            # 跨度超过12个月，每2个月显示一个刻度
            step = 2
        else:
            # 跨度较小，每个月都显示
            step = 1
        
            # 绘制月份刻度
        month_range = range(int(self.min_month), int(self.max_month) + 2)
        for month in month_range:
            # 根据步长决定是否显示
            if (month - int(self.min_month)) % step != 0 and month != int(self.max_month) + 1:
                continue
            
            x = self.left_margin + self.label_width + self.remark_width + (month - self.min_month) * self.month_width
            
            # 月份标签
            month_label = ET.SubElement(root_element, 'mxCell', {
                'id': f'month_label_{month}',
                'value': f'M{month}',
                'style': 'text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontSize=10;',
                'vertex': '1',
                'parent': parent.get('id')
            })
            
            ET.SubElement(month_label, 'mxGeometry', {
                'x': str(x - 20),
                'y': str(self.top_margin + 30),
                'width': '40',
                'height': '20',
                'as': 'geometry'
            })
            
            # 刻度线
            if month <= self.max_month:
                tick_line = ET.SubElement(root_element, 'mxCell', {
                    'id': f'tick_{month}',
                    'value': '',
                    'style': 'endArrow=none;html=1;strokeColor=#666666;strokeWidth=1;',
                    'edge': '1',
                    'parent': parent.get('id')
                })
                
                geometry = ET.SubElement(tick_line, 'mxGeometry', {
                    'relative': '1',
                    'as': 'geometry'
                })
                
                ET.SubElement(geometry, 'mxPoint', {
                    'x': str(x),
                    'y': str(self.top_margin + 50),
                    'as': 'sourcePoint'
                })
                
                ET.SubElement(geometry, 'mxPoint', {
                    'x': str(x),
                    'y': str(self.top_margin + self.time_header_height),
                    'as': 'targetPoint'
                })
    
    def _draw_task_bars(self, root_element, parent):
        """绘制任务条"""
        y_start = self.top_margin + self.time_header_height
        
        for i, task in enumerate(self.tasks):
            pos = self.task_positions[task['id']]
            
            # 任务名称标签
            label_x = self.left_margin
            label_y = pos['y']
            label_width = self.label_width - 10
            label_height = pos['height']
            
            # 根据层级添加缩进
            indent = task['level'] * 20
            
            task_label = ET.SubElement(root_element, 'mxCell', {
                'id': f'label_{task["id"]}',
                'value': task['name'],
                'style': f'text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontSize=11;spacingLeft={indent};',
                'vertex': '1',
                'parent': parent.get('id')
            })
            
            ET.SubElement(task_label, 'mxGeometry', {
                'x': str(label_x + indent),
                'y': str(label_y),
                'width': str(label_width - indent),
                'height': str(label_height),
                'as': 'geometry'
            })
            
            # 备注列（责任方/备注）
            remark_x = self.left_margin + self.label_width
            remark_y = pos['y']
            remark_text = task.get('responsible', '')
            
            if remark_text:
                remark_label = ET.SubElement(root_element, 'mxCell', {
                    'id': f'remark_{task["id"]}',
                    'value': remark_text,
                    'style': 'text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontSize=10;fontColor=#666666;',
                    'vertex': '1',
                    'parent': parent.get('id')
                })
                
                ET.SubElement(remark_label, 'mxGeometry', {
                    'x': str(remark_x + 5),
                    'y': str(remark_y),
                    'width': str(self.remark_width - 10),
                    'height': str(label_height),
                    'as': 'geometry'
                })
            
            # 任务条（矩形）- 不显示任何文字，保持简洁
            bar_style = self._get_task_bar_style(task)
            
            task_bar = ET.SubElement(root_element, 'mxCell', {
                'id': f'bar_{task["id"]}',
                'value': '',  # 进度条内不显示文字
                'style': bar_style,
                'vertex': '1',
                'parent': parent.get('id')
            })
            
            ET.SubElement(task_bar, 'mxGeometry', {
                'x': str(pos['x']),
                'y': str(pos['y']),
                'width': str(max(10, pos['width'])),  # 最小宽度10像素
                'height': str(pos['height']),
                'as': 'geometry'
            })
    
    def _draw_dependencies(self, root_element, parent):
        """绘制依赖关系箭头"""
        for task in self.tasks:
            if not task['dependencies']:
                continue
            
            task_pos = self.task_positions[task['id']]
            
            for dep_id in task['dependencies']:
                # 查找依赖任务
                dep_task = next((t for t in self.tasks if t['id'] == dep_id), None)
                if not dep_task or dep_id not in self.task_positions:
                    continue
                
                dep_pos = self.task_positions[dep_id]
                
                # 箭头起点（依赖任务的结束位置）
                start_x = dep_pos['x'] + dep_pos['width']
                start_y = dep_pos['y'] + dep_pos['height'] / 2
                
                # 箭头终点（当前任务的开始位置）
                end_x = task_pos['x']
                end_y = task_pos['y'] + task_pos['height'] / 2
                
                # 创建箭头
                arrow = ET.SubElement(root_element, 'mxCell', {
                    'id': f'arrow_{dep_id}_{task["id"]}',
                    'value': '',
                    'style': 'endArrow=block;html=1;strokeColor=#666666;strokeWidth=2;dashed=1;dashPattern=8 8;',
                    'edge': '1',
                    'parent': parent.get('id')
                })
                
                geometry = ET.SubElement(arrow, 'mxGeometry', {
                    'relative': '1',
                    'as': 'geometry'
                })
                
                # 如果起点和终点在同一水平线，直接连接
                if abs(start_y - end_y) < 5:
                    ET.SubElement(geometry, 'mxPoint', {
                        'x': str(start_x),
                        'y': str(start_y),
                        'as': 'sourcePoint'
                    })
                    
                    ET.SubElement(geometry, 'mxPoint', {
                        'x': str(end_x),
                        'y': str(end_y),
                        'as': 'targetPoint'
                    })
                else:
                    # 需要折线连接
                    mid_x = start_x + 30  # 中间点X坐标
                    
                    ET.SubElement(geometry, 'mxPoint', {
                        'x': str(start_x),
                        'y': str(start_y),
                        'as': 'sourcePoint'
                    })
                    
                    ET.SubElement(geometry, 'mxPoint', {
                        'x': str(mid_x),
                        'y': str(start_y),
                        'as': 'targetPoint'
                    })
                    
                    # 添加中间点
                    array = ET.SubElement(geometry, 'Array', {
                        'as': 'points'
                    })
                    
                    ET.SubElement(array, 'mxPoint', {
                        'x': str(mid_x),
                        'y': str(end_y)
                    })
                    
                    ET.SubElement(geometry, 'mxPoint', {
                        'x': str(end_x),
                        'y': str(end_y),
                        'as': 'targetPoint'
                    })
    
    def _get_task_bar_style(self, task: Dict) -> str:
        """获取任务条样式"""
        # 根据层级设置不同颜色
        level = task['level']
        
        # 检查是否是超长任务（超过12个月）
        duration = task['end_month'] - task['start_month']
        is_long_task = duration > 12
        
        colors = [
            '#d5e8d4',  # 绿色 - 主要阶段
            '#fff2cc',  # 黄色 - 二级任务
            '#dae8fc',  # 蓝色 - 三级任务
            '#e1d5e7',  # 紫色 - 四级任务
            '#f8cecc',  # 红色 - 五级任务
        ]
        
        stroke_colors = [
            '#82b366',
            '#d6b656',
            '#6c8ebf',
            '#9673a6',
            '#b85450',
        ]
        
        color_idx = min(level, len(colors) - 1)
        fill_color = colors[color_idx]
        stroke_color = stroke_colors[color_idx]
        
        # 如果是主要阶段（level=0），加粗边框
        stroke_width = '2' if level == 0 else '1'
        
        # 如果是超长任务，使用虚线边框
        dash_pattern = '8 8' if is_long_task else ''
        dash_style = f'dashed=1;dashPattern={dash_pattern};' if is_long_task else ''
        
        return f'rounded=1;whiteSpace=wrap;html=1;fillColor={fill_color};strokeColor={stroke_color};strokeWidth={stroke_width};{dash_style}fontSize=10;align=left;verticalAlign=middle;spacingLeft=4;'


def convert_gantt_to_drawio(text: str, output_file: str = None) -> str:
    """
    将甘特图表数据转换为 draw.io XML
    
    Args:
        text: 甘特图表文本（表格格式）
        output_file: 输出文件路径（可选）
    
    Returns:
        draw.io XML 字符串
    """
    # 解析甘特图数据
    parser = GanttParser(text)
    tasks = parser.parse()
    
    if not tasks:
        raise ValueError("未能解析到任何任务数据，请检查输入格式")
    
    # 生成 draw.io XML
    generator = GanttDrawIOGenerator(tasks)
    xml_content = generator.generate()
    
    # 保存到文件
    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(xml_content)
        print(f"[成功] 已成功生成甘特图 draw.io 文件: {output_file}")
        print(f"[信息] 共解析 {len(tasks)} 个任务")
    
    return xml_content


def main():
    """命令行入口"""
    parser = argparse.ArgumentParser(
        description='将项目进度甘特图表信息转换为 draw.io XML 文件',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 从文件读取并转换
  python gantt_to_drawio.py -i gantt.txt -o output.drawio
  
  # 从标准输入读取
  python gantt_to_drawio.py -i - -o output.drawio
  
  # 交互式输入
  python gantt_to_drawio.py
  
输入格式要求:
  表格格式，包含以下列：任务ID、任务名称、开始时间、结束时间、工期、前置任务、责任方/备注
  时间格式支持：M0, M1, M1+0.5, M1.5 等
        """
    )
    
    parser.add_argument(
        '-i', '--input',
        type=str,
        help='输入文件路径（使用 - 表示从标准输入读取）'
    )
    
    parser.add_argument(
        '-o', '--output',
        type=str,
        default='gantt.drawio',
        help='输出文件路径（默认: gantt.drawio）'
    )
    
    args = parser.parse_args()
    
    # 读取输入
    if args.input:
        if args.input == '-':
            text = sys.stdin.read()
        else:
            try:
                with open(args.input, 'r', encoding='utf-8') as f:
                    text = f.read()
            except FileNotFoundError:
                print(f"[错误] 文件 '{args.input}' 不存在")
                sys.exit(1)
    else:
        # 交互式输入
        print("请输入甘特图表数据（输入空行结束）:")
        lines = []
        while True:
            try:
                line = input()
                if not line.strip():
                    break
                lines.append(line)
            except EOFError:
                break
        text = '\n'.join(lines)
    
    if not text.strip():
        print("[错误] 输入为空")
        sys.exit(1)
    
    # 转换
    try:
        convert_gantt_to_drawio(text, args.output)
    except Exception as e:
        print(f"[错误] {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
