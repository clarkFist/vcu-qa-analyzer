#!/usr/bin/env python3
"""
默认主题
=======

功能丰富的默认主题，支持侧边栏、图片放大等功能
"""

from .base import BaseTheme


class DefaultTheme(BaseTheme):
    """默认主题"""

    def __init__(self):
        """初始化主题"""
        super().__init__()
        self.name = "default"
        self.description = "功能丰富的默认主题"

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
            font-family: -apple-system, BlinkMacSystemFont, "PingFang SC", "Microsoft YaHei UI", "Microsoft YaHei", "Source Han Sans CN", "Noto Sans CJK SC", "WenQuanYi Micro Hei", "Segoe UI", Helvetica, Arial, sans-serif;
            font-size: 16px;
            line-height: 1.8;
            color: #2c3e50;
            font-weight: 400;
            text-rendering: optimizeLegibility;
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: #fff;
            box-shadow: 0 10px 60px rgba(0,0,0,0.3);
            border-radius: 12px;
            overflow: hidden;
        }

        /* 头部 */
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px 40px;
            position: sticky;
            top: 0;
            z-index: 1000;
        }

        .header h1 {
            font-size: 28px;
            margin-bottom: 10px;
        }

        .header .meta {
            opacity: 0.9;
            font-size: 14px;
        }

        /* 目录侧边栏 */
        .toc-sidebar {
            position: fixed;
            left: 20px;
            top: 160px;
            width: 260px;
            height: calc(100vh - 180px);
            background: #f8f9fa;
            border-right: 1px solid #e0e0e0;
            overflow-y: auto;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
        }

        .toc-sidebar h2 {
            font-size: 18px;
            margin-bottom: 15px;
            color: #667eea;
            border-bottom: 2px solid #667eea;
            padding-bottom: 8px;
        }

        .toc-sidebar ul {
            list-style: none;
            padding-left: 0;
        }

        .toc-sidebar li {
            margin: 8px 0;
        }

        .toc-sidebar a {
            color: #555;
            text-decoration: none;
            font-size: 14px;
            display: block;
            padding: 4px 8px;
            border-radius: 4px;
            transition: all 0.2s;
        }

        .toc-sidebar a:hover {
            background: #667eea;
            color: white;
        }

        /* 主内容 */
        .content {
            padding: 50px;
            margin-left: 300px;
            min-height: 600px;
        }

        /* 标题样式 */
        h1, h2, h3, h4, h5, h6 {
            font-family: -apple-system, BlinkMacSystemFont, "PingFang SC", "Microsoft YaHei UI", "Microsoft YaHei", "Source Han Sans CN", sans-serif;
            font-weight: 600;
            letter-spacing: 0.5px;
        }

        h1 {
            font-size: 32px;
            color: #1a1a1a;
            margin: 25px 0 15px 0;
            padding-bottom: 12px;
            border-bottom: 3px solid #667eea;
            font-weight: 700;
        }

        h2 {
            font-size: 26px;
            color: #2c3e50;
            margin: 20px 0 15px 0;
            padding-left: 15px;
            border-left: 5px solid #667eea;
            font-weight: 600;
        }

        h3 {
            font-size: 20px;
            color: #34495e;
            margin: 18px 0 12px 0;
            font-weight: 600;
        }

        h4 {
            font-size: 18px;
            color: #4a5568;
            margin: 15px 0 10px 0;
            font-weight: 500;
        }

        h5 {
            font-size: 16px;
            color: #5a6c7d;
            margin: 12px 0 8px 0;
            font-weight: 500;
        }

        /* 段落和文本 */
        p {
            margin: 12px 0;
            text-align: justify;
        }

        strong {
            color: #1a1a1a;
            font-weight: 600;
        }

        em {
            color: #667eea;
            font-style: normal;
        }

        /* 列表 */
        ul, ol {
            margin: 12px 0;
            padding-left: 30px;
        }

        li {
            margin: 6px 0;
        }

        /* 图片 */
        img {
            max-width: 100%;
            height: auto;
            display: block;
            margin: 15px auto;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            cursor: zoom-in;
        }

        /* 徽章图片 */
        p img[src*="shields.io"],
        p img[src*="badge"] {
            display: inline-block;
            margin: 2px 4px;
            box-shadow: none;
            cursor: default;
        }

        /* 表格 */
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 18px 0;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            border-radius: 8px;
            overflow: hidden;
        }

        thead {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }

        th {
            color: white;
            padding: 15px;
            text-align: left;
            font-weight: 600;
        }

        td {
            padding: 12px 15px;
            border-bottom: 1px solid #e0e0e0;
        }

        tbody tr:hover {
            background: #f8f9fa;
        }

        /* 代码块 */
        code {
            font-family: "SF Mono", "Fira Code", "Cascadia Code", "JetBrains Mono", Consolas, "Courier New", monospace;
            background: linear-gradient(135deg, #f6f8fa 0%, #f0f2f5 100%);
            color: #24292f;
            padding: 4px 8px;
            border-radius: 5px;
            font-size: 0.95em;
            font-weight: 600;
            border: 1px solid #d0d7de;
            box-shadow: 0 1px 3px rgba(0,0,0,0.08);
            display: inline-block;
            line-height: 1.4;
            white-space: nowrap;
            letter-spacing: -0.2px;
        }

        /* 列表中的代码优化 */
        li code {
            background: #e7f2ff;
            color: #0969da;
            border: 1px solid #b7d3f0;
            font-size: 0.94em;
            padding: 3px 7px;
        }

        pre {
            background: #2d3748;
            color: #e2e8f0;
            padding: 20px;
            border-radius: 8px;
            overflow-x: auto;
            margin: 15px 0;
            position: relative;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            border-left: 4px solid #667eea;
        }

        pre code {
            background: none;
            color: inherit;
            padding: 0;
            border: none;
            font-size: 14px;
            line-height: 1.6;
        }

        /* 引用块 */
        blockquote {
            border-left: 4px solid #f39c12;
            background: #fff9e6;
            margin: 15px 0;
            padding: 15px 20px;
            border-radius: 0 6px 6px 0;
            color: #856404;
        }

        /* 链接 */
        a {
            color: #667eea;
            text-decoration: none;
            border-bottom: 1px solid transparent;
            transition: all 0.2s;
        }

        a:hover {
            color: #764ba2;
            border-bottom-color: #764ba2;
        }

        /* 分隔线 */
        hr {
            border: none;
            height: 2px;
            background: linear-gradient(90deg, transparent 0%, #667eea 50%, transparent 100%);
            margin: 20px 0;
        }

        /* Mermaid */
        .mermaid {
            margin: 18px auto;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 8px;
            border: 1px solid #e0e0e0;
            text-align: center;
        }

        .mermaid-fallback {
            background: #fff9e6;
            border: 2px solid #f39c12;
            color: #856404;
        }

        .mermaid-fallback pre {
            background: transparent;
            color: inherit;
            border: none;
            padding: 0;
        }

        /* 页脚 */
        .footer {
            text-align: center;
            padding: 20px;
            color: #999;
            font-size: 12px;
            border-top: 1px solid #e0e0e0;
        }

        /* 响应式 */
        @media (max-width: 1024px) {
            .toc-sidebar {
                display: none;
            }

            .content {
                margin-left: 0;
            }
        }

        @media (max-width: 768px) {
            .content {
                padding: 20px;
            }

            h1 { font-size: 28px; }
            h2 { font-size: 24px; }
        }

        /* 滚动条美化 */
        ::-webkit-scrollbar {
            width: 10px;
            height: 10px;
        }

        ::-webkit-scrollbar-track {
            background: #f1f1f1;
        }

        ::-webkit-scrollbar-thumb {
            background: #667eea;
            border-radius: 5px;
        }

        ::-webkit-scrollbar-thumb:hover {
            background: #764ba2;
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

        // 代码块复制功能
        document.querySelectorAll('pre code').forEach(block => {
            const button = document.createElement('button');
            button.textContent = '复制';
            button.style.cssText = 'position:absolute;top:10px;right:10px;padding:5px 10px;background:#667eea;color:white;border:none;border-radius:4px;cursor:pointer;font-size:12px;';

            const pre = block.parentElement;
            pre.style.position = 'relative';
            pre.appendChild(button);

            button.addEventListener('click', () => {
                navigator.clipboard.writeText(block.textContent);
                button.textContent = '已复制';
                setTimeout(() => button.textContent = '复制', 2000);
            });
        });

        // 图片点击放大
        document.querySelectorAll('.content img:not([src*="shields.io"])').forEach(img => {
            img.addEventListener('click', function() {
                const overlay = document.createElement('div');
                overlay.style.cssText = 'position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(0,0,0,0.9);z-index:9999;display:flex;align-items:center;justify-content:center;cursor:zoom-out;';

                const enlargedImg = document.createElement('img');
                enlargedImg.src = this.src;
                enlargedImg.style.cssText = 'max-width:90%;max-height:90%;border-radius:8px;';

                overlay.appendChild(enlargedImg);
                document.body.appendChild(overlay);

                overlay.addEventListener('click', () => document.body.removeChild(overlay));
            });
        });
        """

        if has_mermaid:
            from src.processors import MermaidProcessor
            processor = MermaidProcessor()
            scripts += processor.get_mermaid_script()

        return scripts