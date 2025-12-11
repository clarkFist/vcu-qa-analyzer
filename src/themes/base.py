#!/usr/bin/env python3
"""
基础主题类
=========

所有主题的基类
"""

from abc import ABC, abstractmethod
from typing import Dict, Any


class BaseTheme(ABC):
    """基础主题类"""

    def __init__(self):
        """初始化主题"""
        self.name = "base"
        self.description = "基础主题"

    @abstractmethod
    def get_styles(self) -> str:
        """
        获取 CSS 样式

        Returns:
            CSS 样式字符串
        """
        pass

    @abstractmethod
    def get_scripts(self, has_mermaid: bool = False) -> str:
        """
        获取 JavaScript 脚本

        Args:
            has_mermaid: 是否包含 Mermaid

        Returns:
            JavaScript 代码
        """
        pass

    def render(
        self,
        body_html: str,
        toc_html: str = "",
        title: str = "文档",
        image_count: int = 0,
        has_mermaid: bool = False,
        config: Dict[str, Any] = None
    ) -> str:
        """
        渲染完整的 HTML 文档

        Args:
            body_html: 主体 HTML
            toc_html: 目录 HTML
            title: 标题
            image_count: 图片数量
            has_mermaid: 是否包含 Mermaid
            config: 配置字典

        Returns:
            完整的 HTML 文档
        """
        config = config or {}

        # 获取样式和脚本
        styles = self.get_styles()
        scripts = self.get_scripts(has_mermaid)

        # 处理目录
        toc_section = self._create_toc_section(toc_html) if toc_html else ""

        # 构建 HTML
        return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        {styles}
    </style>
</head>
<body>
    <div class="container">
        {self._create_header(title, image_count)}
        {toc_section}
        <div class="content" id="main-content">
            {body_html}
        </div>
        {self._create_footer()}
    </div>
    <script>
        {scripts}
    </script>
</body>
</html>"""

    def _create_header(self, title: str, image_count: int) -> str:
        """
        创建页眉

        Args:
            title: 标题
            image_count: 图片数量

        Returns:
            页眉 HTML
        """
        return f"""
        <div class="header">
            <h1>{title}</h1>
            <p class="meta">包含 {image_count} 张图片</p>
        </div>
        """

    def _create_footer(self) -> str:
        """
        创建页脚

        Returns:
            页脚 HTML
        """
        return """
        <div class="footer">
            <p>由 Markdown to HTML Converter 生成</p>
        </div>
        """

    def _create_toc_section(self, toc_html: str) -> str:
        """
        创建目录部分

        Args:
            toc_html: 目录 HTML

        Returns:
            目录部分 HTML
        """
        if not toc_html:
            return ""

        return f"""
        <div class="toc-sidebar" id="toc-sidebar">
            <h2>目录</h2>
            {toc_html}
        </div>
        """