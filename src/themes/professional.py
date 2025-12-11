#!/usr/bin/env python3
"""
专业主题
=======

适合技术文档和报告的专业主题
"""

from .base import BaseTheme


class ProfessionalTheme(BaseTheme):
    """专业主题"""

    def __init__(self):
        """初始化主题"""
        super().__init__()
        self.name = "professional"
        self.description = "适合技术文档和报告的专业主题"

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
            font-family: "Source Serif Pro", "Noto Serif SC", "Songti SC", Georgia, "Times New Roman", "Microsoft YaHei", serif;
            font-size: 16px;
            line-height: 1.8;
            color: #1a1a1a;
            text-rendering: optimizeLegibility;
            -webkit-font-smoothing: antialiased;
            background: white;
            padding: 40px 20px;
        }

        .container {
            max-width: 800px;
            margin: 0 auto;
        }

        /* 头部 */
        .header {
            text-align: center;
            margin-bottom: 30px;
            padding-bottom: 20px;
            border-bottom: 3px double #333;
        }

        .header h1 {
            font-size: 36px;
            font-weight: 700;
            margin-bottom: 20px;
            letter-spacing: 1px;
            text-transform: uppercase;
        }

        .header .meta {
            font-size: 14px;
            color: #666;
            font-style: italic;
        }

        /* 目录 */
        .toc-sidebar {
            margin-bottom: 20px;
            padding: 15px;
            background: #f9f9f9;
            border: 1px solid #ddd;
        }

        .toc-sidebar h2 {
            font-size: 20px;
            margin-bottom: 15px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        .toc-sidebar ul {
            list-style: none;
            padding-left: 0;
        }

        .toc-sidebar li {
            margin: 8px 0;
            padding-left: 20px;
            position: relative;
        }

        .toc-sidebar li:before {
            content: '§';
            position: absolute;
            left: 0;
            color: #666;
        }

        .toc-sidebar a {
            color: #333;
            text-decoration: none;
        }

        .toc-sidebar a:hover {
            text-decoration: underline;
        }

        /* 内容 */
        .content {
            text-align: justify;
        }

        /* 标题 */
        h1, h2, h3, h4, h5, h6 {
            margin-top: 40px;
            margin-bottom: 20px;
            font-weight: 700;
            page-break-after: avoid;
        }

        h1 {
            font-size: 28px;
            text-align: center;
            text-transform: uppercase;
            letter-spacing: 2px;
            margin: 30px 0 20px;
        }

        h2 {
            font-size: 24px;
            border-bottom: 2px solid #333;
            padding-bottom: 10px;
            margin-top: 25px;
        }

        h3 {
            font-size: 20px;
            font-style: italic;
        }

        /* 段落 */
        p {
            margin: 0 0 20px;
            text-indent: 2em;
        }

        p:first-child,
        h1 + p,
        h2 + p,
        h3 + p,
        h4 + p {
            text-indent: 0;
        }

        /* 首字下沉 */
        .content > p:first-of-type:first-letter {
            float: left;
            font-size: 60px;
            line-height: 50px;
            padding: 0 8px 0 0;
            font-weight: 700;
        }

        /* 列表 */
        ul, ol {
            margin: 20px 0;
            padding-left: 40px;
        }

        li {
            margin: 8px 0;
        }

        /* 图片 */
        img {
            max-width: 100%;
            height: auto;
            display: block;
            margin: 15px auto;
            box-shadow: 0 0 10px rgba(0,0,0,0.2);
        }

        /* 图片说明 */
        img + em {
            display: block;
            text-align: center;
            color: #666;
            font-size: 14px;
            margin-top: -20px;
            margin-bottom: 20px;
        }

        /* 表格 */
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 18px 0;
            font-size: 14px;
        }

        caption {
            text-align: left;
            margin-bottom: 10px;
            font-weight: 700;
        }

        th, td {
            border: 1px solid #333;
            padding: 10px;
            text-align: left;
        }

        th {
            background: #f0f0f0;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 1px;
            font-size: 12px;
        }

        /* 代码 */
        code {
            font-family: "SF Mono", "Fira Code", "Cascadia Code", "IBM Plex Mono", "Courier New", monospace;
            background: #f7f7f7;
            padding: 3px 6px;
            font-size: 0.92em;
            color: #2d3748;
            border: 1px solid #d4d4d4;
            border-radius: 3px;
            font-weight: 600;
            display: inline-block;
            line-height: 1.3;
            letter-spacing: -0.2px;
        }

        pre {
            background: #f5f5f5;
            border-left: 4px solid #333;
            padding: 15px;
            margin: 15px 0;
            overflow-x: auto;
            font-family: "SF Mono", "Fira Code", "IBM Plex Mono", "Courier New", monospace;
            font-size: 14px;
            line-height: 1.5;
        }

        pre code {
            background: none;
            padding: 0;
            color: #1a1a1a;
            border: none;
            font-size: 14px;
        }

        /* 引用 */
        blockquote {
            margin: 15px 20px;
            padding: 0 20px;
            border-left: 4px solid #333;
            font-style: italic;
            color: #444;
        }

        blockquote p {
            text-indent: 0;
        }

        /* 链接 */
        a {
            color: #000;
            text-decoration: underline;
        }

        a:hover {
            color: #666;
        }

        /* 分隔线 */
        hr {
            border: none;
            margin: 20px 0;
            text-align: center;
            height: 20px;
        }

        hr:after {
            content: '⁂';
            font-size: 20px;
            color: #333;
        }

        /* 脚注 */
        .footnote {
            font-size: 14px;
            vertical-align: super;
        }

        /* 页脚 */
        .footer {
            margin-top: 30px;
            padding-top: 15px;
            border-top: 3px double #333;
            text-align: center;
            font-size: 12px;
            color: #666;
        }

        /* 打印样式 */
        @media print {
            body {
                font-size: 12pt;
                line-height: 1.5;
            }

            .container {
                max-width: 100%;
            }

            h1 {
                page-break-before: always;
            }

            h2, h3 {
                page-break-after: avoid;
            }

            table, pre, blockquote {
                page-break-inside: avoid;
            }
        }

        /* 响应式 */
        @media (max-width: 768px) {
            body {
                padding: 20px 15px;
            }

            h1 { font-size: 24px; }
            h2 { font-size: 20px; }

            p {
                text-indent: 0;
            }

            .content > p:first-of-type:first-letter {
                font-size: 40px;
                line-height: 35px;
            }
        }
        """

    def get_scripts(self, has_mermaid: bool = False) -> str:
        """获取 JavaScript 脚本"""
        scripts = """
        // 添加章节编号
        (function() {
            let h2Counter = 0;
            let h3Counter = 0;

            document.querySelectorAll('.content h2').forEach(h2 => {
                h2Counter++;
                h3Counter = 0;
                const text = h2.textContent;
                h2.textContent = `${h2Counter}. ${text}`;

                let nextEl = h2.nextElementSibling;
                while (nextEl && nextEl.tagName !== 'H2') {
                    if (nextEl.tagName === 'H3') {
                        h3Counter++;
                        const h3Text = nextEl.textContent;
                        nextEl.textContent = `${h2Counter}.${h3Counter} ${h3Text}`;
                    }
                    nextEl = nextEl.nextElementSibling;
                }
            });
        })();
        """

        if has_mermaid:
            from src.processors import MermaidProcessor
            processor = MermaidProcessor()
            scripts += processor.get_mermaid_script()

        return scripts