#!/usr/bin/env python3
"""
Markdown to HTML Converter
==========================

一个简洁高效的 Markdown 转 HTML 工具
"""

import sys
import os

# 添加src目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from cli import main

if __name__ == '__main__':
    main()