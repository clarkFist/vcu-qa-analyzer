#!/usr/bin/env python3
"""
HTML 转换器核心模块
==================

负责 Markdown 到 HTML 的转换核心逻辑
"""

import markdown
from pathlib import Path
from typing import Optional, Tuple, Dict, Any
from dataclasses import dataclass
from datetime import datetime

from src.processors import ImageProcessor, MermaidProcessor


@dataclass
class ConversionResult:
    """转换结果"""
    success: bool
    output_path: Path
    file_size: int
    image_count: int
    duration: float
    error_message: Optional[str] = None


class HTMLConverter:
    """HTML 转换器"""

    def __init__(self, config: Dict[str, Any] = None):
        """
        初始化转换器

        Args:
            config: 配置字典
        """
        self.config = config or {}
        self.image_processor = ImageProcessor()
        self.mermaid_processor = MermaidProcessor()

        # Markdown 扩展配置
        self.md_extensions = [
            'markdown.extensions.tables',
            'markdown.extensions.fenced_code',
            'markdown.extensions.codehilite',
            'markdown.extensions.toc',
            'markdown.extensions.sane_lists',
            'markdown.extensions.nl2br',
            'markdown.extensions.attr_list',
            'markdown.extensions.def_list',
            'markdown.extensions.footnotes',
            'markdown.extensions.meta',
            'markdown.extensions.abbr',
        ]

        self.md_extension_configs = {
            'codehilite': {
                'css_class': 'highlight',
                'linenums': False,
                'guess_lang': True
            },
            'toc': {
                'permalink': True,
                'toc_depth': 3,
                'title': '目录'
            }
        }

    def convert(
        self,
        source_path: Path,
        output_path: Optional[Path] = None,
        theme: str = "default",
        embed_images: bool = True,
        process_mermaid: bool = True
    ) -> ConversionResult:
        """
        转换 Markdown 文件为 HTML

        Args:
            source_path: 源文件路径
            output_path: 输出路径（可选）
            theme: 主题名称
            embed_images: 是否嵌入图片
            process_mermaid: 是否处理 Mermaid 图表

        Returns:
            转换结果
        """
        start_time = datetime.now()

        try:
            # 检查源文件
            if not source_path.exists():
                return ConversionResult(
                    success=False,
                    output_path=output_path or source_path.with_suffix('.html'),
                    file_size=0,
                    image_count=0,
                    duration=0,
                    error_message=f"文件不存在: {source_path}"
                )

            # 读取 Markdown 内容
            md_content = source_path.read_text(encoding='utf-8')

            # 处理图片
            image_count = 0
            if embed_images:
                md_content, image_count = self.image_processor.process(
                    md_content,
                    source_path.parent
                )

            # 处理 Mermaid
            if process_mermaid:
                md_content = self.mermaid_processor.process(md_content)

            # 转换为 HTML
            md = markdown.Markdown(
                extensions=self.md_extensions,
                extension_configs=self.md_extension_configs
            )

            html_body = md.convert(md_content)
            toc_html = getattr(md, 'toc', '')

            # 获取元数据
            metadata = getattr(md, 'Meta', {})
            title = metadata.get('title', [source_path.stem])[0] if metadata else source_path.stem

            # 生成完整 HTML
            full_html = self._create_html_document(
                html_body,
                toc_html,
                title,
                theme,
                image_count,
                process_mermaid
            )

            # 确定输出路径
            if output_path is None:
                output_path = source_path.with_suffix('.html')

            # 写入文件
            output_path.write_text(full_html, encoding='utf-8')

            # 计算耗时
            duration = (datetime.now() - start_time).total_seconds()

            return ConversionResult(
                success=True,
                output_path=output_path,
                file_size=output_path.stat().st_size,
                image_count=image_count,
                duration=duration
            )

        except Exception as e:
            duration = (datetime.now() - start_time).total_seconds()
            return ConversionResult(
                success=False,
                output_path=output_path or source_path.with_suffix('.html'),
                file_size=0,
                image_count=0,
                duration=duration,
                error_message=str(e)
            )

    def _create_html_document(
        self,
        body_html: str,
        toc_html: str,
        title: str,
        theme: str,
        image_count: int,
        has_mermaid: bool
    ) -> str:
        """
        创建完整的 HTML 文档

        Args:
            body_html: 主体 HTML
            toc_html: 目录 HTML
            title: 标题
            theme: 主题
            image_count: 图片数量
            has_mermaid: 是否包含 Mermaid

        Returns:
            完整的 HTML 文档
        """
        # 动态导入主题
        from src.themes import get_theme

        theme_instance = get_theme(theme)

        return theme_instance.render(
            body_html=body_html,
            toc_html=toc_html,
            title=title,
            image_count=image_count,
            has_mermaid=has_mermaid,
            config=self.config
        )

    def convert_batch(
        self,
        source_paths: list[Path],
        output_dir: Optional[Path] = None,
        theme: str = "default",
        embed_images: bool = True,
        process_mermaid: bool = True
    ) -> list[ConversionResult]:
        """
        批量转换

        Args:
            source_paths: 源文件路径列表
            output_dir: 输出目录
            theme: 主题
            embed_images: 是否嵌入图片
            process_mermaid: 是否处理 Mermaid

        Returns:
            转换结果列表
        """
        results = []

        for source_path in source_paths:
            if output_dir:
                output_path = output_dir / f"{source_path.stem}.html"
            else:
                output_path = None

            result = self.convert(
                source_path,
                output_path,
                theme,
                embed_images,
                process_mermaid
            )

            results.append(result)

        return results