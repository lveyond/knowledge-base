#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
符号化流程图转 draw.io 工具
将大模型生成的符号化流程图转换为 draw.io 可识别的 XML 文件

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


class FlowchartParser:
    """解析符号化流程图文本"""
    
    def __init__(self, text: str):
        self.text = text
        self.lines = [line.rstrip() for line in text.strip().split('\n')]
        self.nodes = []  # 存储解析后的节点信息
        self.edges = []  # 存储连接关系
        
    def parse(self) -> Tuple[List[Dict], List[Dict]]:
        """
        解析流程图文本
        返回: (nodes, edges)
        """
        # 移除标题行（如果存在）
        if self.lines and ':' in self.lines[0]:
            self.lines = self.lines[1:]
        
        node_map = {}  # 节点ID -> 节点信息
        node_counter = 0
        previous_main_node = None  # 上一个主要阶段节点
        
        i = 0
        while i < len(self.lines):
            line = self.lines[i]
            if not line.strip():
                i += 1
                continue
            
            # 计算缩进层级
            indent = len(line) - len(line.lstrip())
            level = indent // 2  # 假设每2个空格为一级
            
            # 检查是否是主要阶段（包含方括号）
            if '[' in line and ']' in line:
                # 提取主要阶段文本
                bracket_match = re.search(r'\[([^\]]+)\]', line)
                if bracket_match:
                    main_text = bracket_match.group(1)
                    main_node_id = f"node_{node_counter}"
                    node_counter += 1
                    
                    node_info = {
                        'id': main_node_id,
                        'text': main_text,
                        'level': level,
                        'parent': None,
                        'type': 'main_stage'
                    }
                    
                    node_map[main_node_id] = node_info
                    
                    # 如果有上一个主要阶段，创建向下连接
                    if previous_main_node:
                        self.edges.append({
                            'from': previous_main_node,
                            'to': main_node_id,
                            'type': 'sequence'
                        })
                    
                    previous_main_node = main_node_id
                    
                    # 检查是否有子任务（→ 箭头）
                    if '→' in line:
                        self._parse_subtasks(line, main_node_id, level, node_map, node_counter)
                        node_counter = len(node_map)
            
            # 检查是否是子任务行（以 → 开头或包含 →）
            elif '→' in line and level > 0:
                # 查找父节点（上一个主要阶段）
                if previous_main_node:
                    self._parse_subtasks(line, previous_main_node, level, node_map, node_counter)
                    node_counter = len(node_map)
            
            i += 1
        
        self.nodes = list(node_map.values())
        return self.nodes, self.edges
    
    def _parse_subtasks(self, line: str, parent_id: str, level: int, 
                       node_map: Dict, start_counter: int) -> int:
        """解析子任务"""
        node_counter = start_counter
        
        # 分割箭头
        parts = [p.strip() for p in line.split('→')]
        
        previous_node_id = None
        
        for part in parts:
            if not part:
                continue
            
            # 移除方括号（如果有）
            part = re.sub(r'[\[\]]', '', part).strip()
            if not part:
                continue
            
            node_id = f"node_{node_counter}"
            node_counter += 1
            
            node_info = {
                'id': node_id,
                'text': part,
                'level': level + 1,
                'parent': parent_id,
                'type': 'subtask'
            }
            
            node_map[node_id] = node_info
            
            # 创建与父节点的连接
            if parent_id:
                self.edges.append({
                    'from': parent_id,
                    'to': node_id,
                    'type': 'child'
                })
            
            # 创建同级连接（序列）
            if previous_node_id:
                self.edges.append({
                    'from': previous_node_id,
                    'to': node_id,
                    'type': 'sequence'
                })
            
            previous_node_id = node_id
        
        return node_counter
    
    def _extract_node_text(self, line: str) -> str:
        """从行中提取节点文本"""
        # 移除缩进
        line = line.lstrip()
        
        # 提取方括号中的内容
        bracket_match = re.search(r'\[([^\]]+)\]', line)
        if bracket_match:
            return bracket_match.group(1)
        
        # 提取箭头后的文本
        if '→' in line:
            parts = line.split('→')
            # 第一部分可能是节点文本
            first_part = parts[0].strip()
            if first_part and not first_part.startswith('['):
                return first_part
        
        # 如果没有方括号，提取箭头前的文本
        if '→' in line:
            before_arrow = line.split('→')[0].strip()
            if before_arrow:
                return before_arrow
        
        # 如果没有箭头，返回整行（去除特殊符号）
        text = re.sub(r'[→↓]', '', line).strip()
        return text if text else None
    
    def _determine_node_type(self, line: str) -> str:
        """确定节点类型"""
        if '[' in line and ']' in line:
            return 'process'  # 主要阶段
        elif '→' in line:
            return 'process'  # 子任务
        else:
            return 'process'


class DrawIOGenerator:
    """生成 draw.io XML 文件"""
    
    def __init__(self, nodes: List[Dict], edges: List[Dict]):
        self.nodes = nodes
        self.edges = edges
        self.node_positions = {}  # 节点ID -> (x, y)
        
    def generate(self) -> str:
        """生成 draw.io XML 内容"""
        # 计算节点位置
        self._calculate_positions()
        
        # 创建 XML 根元素
        root = ET.Element('mxfile', {
            'host': 'app.diagrams.net',
            'modified': '2024-01-01T00:00:00.000Z',
            'agent': '5.0',
            'version': '21.0.0',
            'etag': 'xxx',
            'type': 'device'
        })
        
        diagram = ET.SubElement(root, 'diagram', {
            'id': 'flowchart',
            'name': '流程图'
        })
        
        mx_graph_model = ET.SubElement(diagram, 'mxGraphModel', {
            'dx': '1422',
            'dy': '794',
            'grid': '1',
            'gridSize': '10',
            'guides': '1',
            'tooltips': '1',
            'connect': '1',
            'arrows': '1',
            'fold': '1',
            'page': '1',
            'pageScale': '1',
            'pageWidth': '1169',
            'pageHeight': '827',
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
        
        # 添加节点
        for node in self.nodes:
            x, y = self.node_positions[node['id']]
            width = max(120, len(node['text']) * 8 + 40)
            height = 40
            
            mx_cell = ET.SubElement(root_element, 'mxCell', {
                'id': node['id'],
                'value': node['text'],
                'style': self._get_node_style(node),
                'vertex': '1',
                'parent': '1'
            })
            
            ET.SubElement(mx_cell, 'mxGeometry', {
                'x': str(x),
                'y': str(y),
                'width': str(width),
                'height': str(height),
                'as': 'geometry'
            })
        
        # 添加连接线
        for edge in self.edges:
            if edge['from'] in self.node_positions and edge['to'] in self.node_positions:
                edge_id = f"edge_{edge['from']}_{edge['to']}"
                
                mx_cell = ET.SubElement(root_element, 'mxCell', {
                    'id': edge_id,
                    'value': '',
                    'style': self._get_edge_style(edge),
                    'edge': '1',
                    'parent': '1',
                    'source': edge['from'],
                    'target': edge['to']
                })
                
                ET.SubElement(mx_cell, 'mxGeometry', {
                    'relative': '1',
                    'as': 'geometry'
                })
        
        # 转换为字符串
        rough_string = ET.tostring(root, encoding='unicode')
        reparsed = minidom.parseString(rough_string)
        return reparsed.toprettyxml(indent="  ")
    
    def _calculate_positions(self):
        """计算节点位置"""
        # 按层级和类型组织节点
        main_stages = [n for n in self.nodes if n['type'] == 'main_stage']
        subtasks = [n for n in self.nodes if n['type'] == 'subtask']
        
        # 计算主要阶段位置（垂直排列）
        y_start = 50
        y_spacing = 150
        x_main = 300
        
        for i, node in enumerate(main_stages):
            y = y_start + i * y_spacing
            width = max(200, len(node['text']) * 10 + 40)
            self.node_positions[node['id']] = (x_main, y)
        
        # 计算子任务位置（水平排列在父节点下方）
        x_subtask_start = 50
        x_subtask_spacing = 180
        y_subtask_offset = 80
        
        # 按父节点分组子任务
        subtasks_by_parent = {}
        for subtask in subtasks:
            parent_id = subtask['parent']
            if parent_id not in subtasks_by_parent:
                subtasks_by_parent[parent_id] = []
            subtasks_by_parent[parent_id].append(subtask)
        
        # 为每个父节点的子任务分配位置
        for parent_id, children in subtasks_by_parent.items():
            if parent_id not in self.node_positions:
                continue
            
            parent_x, parent_y = self.node_positions[parent_id]
            
            # 计算子任务的总宽度
            total_width = len(children) * x_subtask_spacing
            start_x = parent_x - total_width / 2 + x_subtask_spacing / 2
            
            for i, child in enumerate(children):
                x = start_x + i * x_subtask_spacing
                y = parent_y + y_subtask_offset
                width = max(120, len(child['text']) * 8 + 40)
                self.node_positions[child['id']] = (x, y)
    
    def _get_node_style(self, node: Dict) -> str:
        """获取节点样式"""
        base_style = "rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;"
        
        # 根据层级调整样式
        if node['level'] == 0:
            base_style = "rounded=1;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;fontStyle=1;"
        elif node['parent'] is None:
            base_style = "rounded=1;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;"
        
        return base_style
    
    def _get_edge_style(self, edge: Dict) -> str:
        """获取连接线样式"""
        if edge['type'] == 'child':
            return "edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;"
        else:
            return "edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;endArrow=block;endFill=1;"


def convert_flowchart_to_drawio(text: str, output_file: str = None) -> str:
    """
    将符号化流程图转换为 draw.io XML
    
    Args:
        text: 符号化流程图文本
        output_file: 输出文件路径（可选）
    
    Returns:
        draw.io XML 字符串
    """
    # 解析流程图
    parser = FlowchartParser(text)
    nodes, edges = parser.parse()
    
    # 生成 draw.io XML
    generator = DrawIOGenerator(nodes, edges)
    xml_content = generator.generate()
    
    # 保存到文件
    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(xml_content)
        print(f"[成功] 已成功生成 draw.io 文件: {output_file}")
    
    return xml_content


def main():
    """命令行入口"""
    parser = argparse.ArgumentParser(
        description='将符号化流程图转换为 draw.io XML 文件',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 从文件读取并转换
  python flowchart_to_drawio.py -i flowchart.txt -o output.drawio
  
  # 从标准输入读取
  python flowchart_to_drawio.py -i - -o output.drawio
  
  # 交互式输入
  python flowchart_to_drawio.py
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
        default='flowchart.drawio',
        help='输出文件路径（默认: flowchart.drawio）'
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
        print("请输入流程图文本（输入空行结束）:")
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
        convert_flowchart_to_drawio(text, args.output)
    except Exception as e:
        print(f"[错误] {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
