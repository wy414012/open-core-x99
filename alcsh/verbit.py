#!/bin/python3
import os
import sys
import re
import traceback


BASE_DIR = os.path.dirname(__file__)
CODEC_TXT = ' '.join(sys.argv[1:])

try:
    with open(CODEC_TXT, 'r') as f:
        content = f.read()
        NAME = re.findall(r'^Codec: (.+)$', content, re.MULTILINE)[0]
        ADDRESS = re.findall(r'Address: (\d+)$', content, re.MULTILINE)[0]
except IOError:
    print('ERROR: 打开codec文件失败, 路径: %s' % CODEC_TXT)
    exit(1)
except IndexError:
    print('ERROR: codec文件格式是否不正确?')
    exit(1)


class Node(object):
    __slots__ = ['Jack', 'Color', 'Description', 'Node', 'PinDefault', 'Verbs']

    def __getattr__(self, item):
        if item == 'Verbs':
            return '%s%s71c%s %s%s71d%s %s%s71e%s %s%s71f%s' % (ADDRESS, self.Node, self.PinDefault[-2:],
                                                                ADDRESS, self.Node, self.PinDefault[-4:-2],
                                                                ADDRESS, self.Node, self.PinDefault[-6:-4],
                                                                ADDRESS, self.Node, self.PinDefault[-8:-6])


def init_nodes(text: str) -> [Node]:
    """
    分析codec.txt, 提取有效节点信息(含有Jack, Color, ... 等信息的节点)
        a). 先将文本分割为以Node 0x...隔开的段, 并剔除不包含"Pin Default"的段
            Node 0x02 [Audio Output] wcaps 0x41d: Stereo Amp-Out
            ...
            ------------------------------------------------------
            Node  0x03 [Audio Output] wcaps 0x41d: Stereo Amp-Out
            ...
            ------------------------------------------------------
        b). 依次解析每个文本段, 并初始化Node对象, 放入一个列表中, 所有解析完毕, 返回该数组
    :param text: str , codec.txt 文本内容
    :return [Node<1>, Node<2>, ...]
    """
    # 先添加一个特殊前缀'----------', 再切割, 以防止切割后Node 0x丢失
    text = re.sub(r'^Node 0x', '----------Node 0x', text, flags=re.MULTILINE)
    node_texts = re.split(r'----------', text)
    node_texts = [_ for _ in node_texts if 'Pin Default ' in _]
    node_list = []
    for node_text in node_texts:
        node = Node()
        try:
            node.Node = re.findall(r'^Node 0x(\w+) ', node_text, re.MULTILINE)[0]
            node.Jack = re.findall(r'Conn = (.+),', node_text)[0]
            node.Color = re.findall(r'Color = (\w+)', node_text)[0]
            node.PinDefault, node.Description = re.findall(r'Pin Default (\w+): (.+)$', node_text, re.MULTILINE)[0]
            if '[N/A]' in node.Description:
                print('WARN: 忽略无效节点信息: Node 0x%s\n%s' % (node.Node, node.Description))
                continue
            print('INFO: 找到节点信息: Node 0x%s\n%s' % (node.Node, node.Description))
            node_list.append(node)
        except IndexError:
            print('ERROR: 搜索节点信息出错, 错误信息如下:\n%s\n 文本内容如下:\n%s' % (traceback.format_exc(), node_text))
    return node_list


nodes = init_nodes(content)
markdwon = '|%s|\n|%s\n' % ('|'.join(Node.__slots__), ':---:|' * len(Node.__slots__))
for _node in nodes:
    markdwon += '|%s|%s|%s|0x%s|%s|%s|\n' % (_node.Jack, _node.Color, _node.Description,
                                             _node.Node, _node.PinDefault, _node.Verbs)
print('\n\n\n%s' % markdwon)
