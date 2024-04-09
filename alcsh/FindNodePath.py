#!/usr/bin/python3
"""
    @Python:   Version 3.5
    @File:     FindNodePath.py
    @Author:   Leo
    @Date:     2019/11/8
    @license: BSD, see LICENSE for more details.
    @Desc:  根据codec.txt找到给定节点所有可能的正反向路径
"""

import sys
import re


class Node(object):
    """
    name: 节点字符串, 如: 0x14
    desc: 节点类型描述
    parent_list: 父节点对象列表，如: [<Node 1>, <Node 2>, ...]
    child_name_list: 子节点字符串列表, 如: ['0x13', '0x14', ...]
    child_obj_list: 子节点对象列表，如: [<Node 1>, <Node 2>, ...]
    """
    def __init__(self, name, desc):
        self.name = name
        self.desc = desc

        self.parent_list = []
        self.child_name_list = []
        self.child_obj_list = []

    def add_parent(self, node):
        self.parent_list.append(node)

    def get_parent_paths(self):
        if len(self.parent_list) == 0:
            print('\033[33m节点: %s 未检索到父节点, 因此无反向路径\033[0m' % self.name)
            return
        paths = []

        def find_path(node, path):
            if node.name in path:   # 回路, 抛弃该路径
                return
            path.append(node.name)
            if len(node.parent_list) == 0:
                path.reverse()
                paths.append(path)
                return
            for parent in node.parent_list:
                _path_list_copy = list(path)
                find_path(parent, _path_list_copy)

        find_path(self, [])
        paths.sort(key=lambda x: len(x))    # 排序，最短的放前面打印
        print('\033[32m节点: %s 找到以下反向路径(输入类: 如mic, line in), 共 %d 条路径, 仅显示路径长度小等于4的路径' %
              (self.name, len(paths)))
        for _ in paths:
            if len(_) <= 4:
                print(' → '.join(_))
        print('\033[0m')

    def get_child_paths(self):
        if len(self.child_obj_list) == 0:
            print('\033[33m节点: %s 未检索到子节点, 因此无正向路径\033[0m' % self.name)
            return
        paths = []

        def find_path(node, path):
            if node.name in path:   # 回路, 抛弃该路径
                return
            path.append(node.name)
            if len(node.child_obj_list) == 0:
                paths.append(path)
                return
            for child in node.child_obj_list:
                _path_list_copy = list(path)
                find_path(child, _path_list_copy)

        find_path(self, [])
        paths.sort(key=lambda x: len(x))    # 排序，最短的放前面打印
        print('\033[32m节点: %s 找到以下正向路径(输出类, 如: Line Out, HeadPhone), 共 %d 条路径, 仅显示路径长度小等于4的路径' %
              (self.name, len(paths)))
        for _ in paths:
            if len(_) <= 4:     # 仅显示路径长度小等于4的路径
                print(' → '.join(_))
        print('\033[0m')

    def __repr__(self):
        return '<Node %s>' % self.name


nodes = {}


def init_nodes():
    """
    读取codec.txt每行文本, 初始化节点对象, 并建立父子关系列表
        1. 找到有一个节点初始化一个节点对象放入 nodes 里, 如: {'0x14': <Node 0x14>}
           在每个节点段里面找到该节点连接的子节点信息, 并填充当前节点的子节点信息
        2. 所有节点都读取完毕, 遍历每一个节点, 根据该节点的子节点列表, 为每一个子节点列表中添加一个父节点(该节点自身)
    :return: None
    """
    try:
        f = open(sys.argv[1])
    except (IndexError, IOError):
        print('请提供正确的文件路径名!')
        f = None    # Bypass pycharm warning "Local variable 'f' might be referenced before assignment"
        exit(1)
    line = f.readline()
    current_node = None
    while line != '':
        match = re.match(r'Node (\w+) (\[.+\])', line, re.IGNORECASE)
        if match:
            current_node = Node(match.group(1).lower(), match.group(2))
            nodes[match.group(1)] = current_node
            print('Debug: 找到节点 %s %s' % (current_node.name, current_node.desc))
            line = f.readline()
            continue
        match = re.match(r'\s+Connection: \d+', line, re.IGNORECASE)
        if match:
            line = f.readline()
            if 'In-driver Connection' in line:  # HDMI codec
                line = f.readline()
            current_node.child_name_list = re.findall(r'\w+', line)
            print('\t\t节点 %s 下连接到以下节点 %s' % (current_node.name, ' '.join(current_node.child_name_list)))
            line = f.readline()
            continue
        line = f.readline()
    # 初始化各节点的子节点
    for node in nodes.values():
        for child_name in node.child_name_list:
            child_name = child_name.lower()
            child_node = nodes[child_name]
            node.child_obj_list.append(child_node)
            # 为子节点添加父节点
            child_node.add_parent(node)


init_nodes()
_name = input('\n\033[33m请输入节点名称, 如0x10\033[0m\n:').lower()
try:
    _node = nodes[_name]
    _node.get_parent_paths()
    _node.get_child_paths()
except KeyError:
    print('找不到节点: %s , 节点名称输入是否有误?' % _name)
    exit(1)

