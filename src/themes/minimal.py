#!/usr/bin/env python3
"""
简约主题
=======

清爽简洁的主题，适合阅读
"""

from .base import BaseTheme


class MinimalTheme(BaseTheme):
    """简约主题"""

    def __init__(self):
        """初始化主题"""
        super().__init__()
        self.name = "minimal"
        self.description = "清爽简洁的主题"

    def get_styles(self) -> str:
        """获取 CSS 样式"""
        return """
        /* 全局样式 */
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, "PingFang SC", "Microsoft YaHei UI", "Microsoft YaHei", "Source Han Sans CN", "Noto Sans CJK SC", "Segoe UI", Helvetica, Arial, sans-serif;
            font-size: 16px;
            line-height: 1.75;
            color: #374151;
            text-rendering: optimizeLegibility;
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
            background: #f5f5f5;
            padding: 20px;
        }

        .container {
            max-width: 900px;
            margin: 0 auto;
            background: white;
            padding: 40px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }

        /* 头部 */
        .header {
            border-bottom: 2px solid #e0e0e0;
            padding-bottom: 20px;
            margin-bottom: 30px;
        }

        .header h1 {
            font-size: 32px;
            color: #2c3e50;
            margin: 0;
        }

        .header .meta {
            color: #7f8c8d;
            font-size: 14px;
            margin-top: 10px;
        }

        /* 内容 */
        .content {
            color: #2c3e50;
        }

        /* 标题 */
        h1, h2, h3, h4, h5, h6 {
            margin-top: 24px;
            margin-bottom: 16px;
            font-weight: 600;
            line-height: 1.25;
        }

        h1 {
            font-size: 28px;
            border-bottom: 1px solid #e0e0e0;
            padding-bottom: 10px;
        }

        h2 {
            font-size: 24px;
            border-bottom: 1px solid #f0f0f0;
            padding-bottom: 8px;
        }

        h3 {
            font-size: 20px;
        }

        /* 段落 */
        p {
            margin: 0 0 16px;
        }

        /* 列表 */
        ul, ol {
            margin: 0 0 16px;
            padding-left: 24px;
        }

        li {
            margin: 4px 0;
        }

        /* 图片 */
        img {
            max-width: 100%;
            height: auto;
            display: block;
            margin: 12px auto;
            border: 1px solid #e0e0e0;
            border-radius: 4px;
        }

        /* 表格 */
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 16px 0;
        }

        th, td {
            border: 1px solid #e0e0e0;
            padding: 8px 12px;
            text-align: left;
        }

        th {
            background: #f8f9fa;
            font-weight: 600;
        }

        tr:nth-child(even) {
            background: #fafbfc;
        }

        /* 代码 */
        code {
            font-family: "SF Mono", "Fira Code", "Cascadia Code", "JetBrains Mono", Consolas, "Courier New", monospace;
            background: #f6f8fa;
            padding: 3px 6px;
            border-radius: 4px;
            font-size: 0.92em;
            color: #0550ae;
            font-weight: 600;
            border: 1px solid #d1d9e0;
            display: inline-block;
            line-height: 1.3;
        }

        pre {
            background: #f6f8fa;
            padding: 16px;
            border-radius: 6px;
            overflow-x: auto;
            margin: 16px 0;
            border: 1px solid #e5e7eb;
        }

        pre code {
            background: none;
            padding: 0;
            color: #1f2937;
            font-size: 14px;
            line-height: 1.6;
            font-weight: 400;
        }

        /* 引用 */
        blockquote {
            border-left: 4px solid #e0e0e0;
            margin: 16px 0;
            padding: 0 16px;
            color: #6a737d;
        }

        /* 链接 */
        a {
            color: #0366d6;
            text-decoration: none;
        }

        a:hover {
            text-decoration: underline;
        }

        /* 分隔线 */
        hr {
            border: none;
            border-top: 1px solid #e0e0e0;
            margin: 16px 0;
        }

        /* Mermaid */
        .mermaid {
            margin: 12px 0;
            padding: 16px;
            background: #f6f8fa;
            border-radius: 6px;
            text-align: center;
        }

        /* 页脚 */
        .footer {
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid #e0e0e0;
            text-align: center;
            color: #999;
            font-size: 12px;
        }

        /* 响应式 */
        @media (max-width: 768px) {
            .container {
                padding: 20px;
            }

            h1 { font-size: 24px; }
            h2 { font-size: 20px; }
        }

        /* 打印优化 */
        @media print {
            body {
                background: white;
                padding: 0;
            }

            .container {
                box-shadow: none;
                padding: 0;
            }
        }
        """

    def get_scripts(self, has_mermaid: bool = False) -> str:
        """获取 JavaScript 脚本"""
        scripts = """
        // 平滑滚动
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            });
        });
        """

        if has_mermaid:
            from src.processors import MermaidProcessor
            processor = MermaidProcessor()
            scripts += processor.get_mermaid_script()

        return scripts