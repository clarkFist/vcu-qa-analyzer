#!/usr/bin/env python3
"""
批量处理器
=========

批量转换Markdown文件
"""

import os
import sys
from pathlib import Path
from typing import List, Tuple, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
import time

from src.core.converter import HTMLConverter
from src.utils.file_scanner import FileScanner


class BatchProcessor:
    """批量处理器"""

    def __init__(self, max_workers: int = 4):
        """
        初始化批量处理器

        Args:
            max_workers: 最大并发数
        """
        self.converter = HTMLConverter()
        self.scanner = FileScanner()
        self.max_workers = max_workers
        self.results = []

    def process_directory(
        self,
        input_dir: Path,
        output_dir: Optional[Path] = None,
        theme: str = "default",
        embed_images: bool = True,
        process_mermaid: bool = True,
        recursive: bool = True,
        pattern: str = "*.md"
    ) -> List[dict]:
        """
        批量处理目录中的Markdown文件

        Args:
            input_dir: 输入目录
            output_dir: 输出目录（默认为输入目录下的html子目录）
            theme: 主题
            embed_images: 是否嵌入图片
            process_mermaid: 是否处理Mermaid
            recursive: 是否递归子目录
            pattern: 文件匹配模式

        Returns:
            处理结果列表
        """
        input_dir = Path(input_dir)
        if not input_dir.exists():
            raise ValueError(f"输入目录不存在: {input_dir}")

        # 设置输出目录
        if output_dir is None:
            output_dir = input_dir / "html_output"
        else:
            output_dir = Path(output_dir)

        output_dir.mkdir(parents=True, exist_ok=True)

        # 扫描Markdown文件
        if recursive:
            md_files = list(input_dir.rglob(pattern))
        else:
            md_files = list(input_dir.glob(pattern))

        if not md_files:
            print(f"⚠️ 未找到匹配的Markdown文件: {pattern}")
            return []

        print(f"\n📂 找到 {len(md_files)} 个Markdown文件")
        print(f"📁 输出目录: {output_dir}")
        print(f"🎨 主题: {theme}")
        print()

        # 显示进度
        self._show_progress_header()

        # 批量处理
        start_time = time.time()
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # 提交任务
            futures = {}
            for md_file in md_files:
                # 计算输出路径，保持相对目录结构
                relative_path = md_file.relative_to(input_dir)
                output_file = output_dir / relative_path.with_suffix('.html')
                output_file.parent.mkdir(parents=True, exist_ok=True)

                future = executor.submit(
                    self._process_file,
                    md_file,
                    output_file,
                    theme,
                    embed_images,
                    process_mermaid
                )
                futures[future] = (md_file, output_file)

            # 收集结果
            completed = 0
            for future in as_completed(futures):
                completed += 1
                md_file, output_file = futures[future]

                try:
                    result = future.result()
                    self.results.append(result)
                    self._show_progress(completed, len(md_files), result)
                except Exception as e:
                    result = {
                        'source': str(md_file),
                        'output': str(output_file),
                        'success': False,
                        'error': str(e),
                        'size': 0,
                        'duration': 0
                    }
                    self.results.append(result)
                    self._show_progress(completed, len(md_files), result)

        # 显示总结
        total_time = time.time() - start_time
        self._show_summary(total_time)

        return self.results

    def _process_file(
        self,
        source: Path,
        output: Path,
        theme: str,
        embed_images: bool,
        process_mermaid: bool
    ) -> dict:
        """
        处理单个文件

        Args:
            source: 源文件
            output: 输出文件
            theme: 主题
            embed_images: 是否嵌入图片
            process_mermaid: 是否处理Mermaid

        Returns:
            处理结果
        """
        start_time = time.time()

        try:
            result = self.converter.convert(
                source_path=source,
                output_path=output,
                theme=theme,
                embed_images=embed_images,
                process_mermaid=process_mermaid
            )

            duration = time.time() - start_time
            file_size = output.stat().st_size / 1024  # KB

            return {
                'source': str(source),
                'output': str(output),
                'success': result.success,
                'error': result.error_message,
                'size': file_size,
                'duration': duration,
                'image_count': result.image_count
            }

        except Exception as e:
            duration = time.time() - start_time
            return {
                'source': str(source),
                'output': str(output),
                'success': False,
                'error': str(e),
                'size': 0,
                'duration': duration,
                'image_count': 0
            }

    def _show_progress_header(self):
        """显示进度头"""
        print("=" * 70)
        print(f"{'文件名':<30} {'状态':<8} {'大小':<10} {'耗时':<8}")
        print("=" * 70)

    def _show_progress(self, completed: int, total: int, result: dict):
        """
        显示进度

        Args:
            completed: 已完成数
            total: 总数
            result: 处理结果
        """
        filename = Path(result['source']).name
        if len(filename) > 28:
            filename = filename[:25] + "..."

        status = "✅ 成功" if result['success'] else "❌ 失败"
        size = f"{result['size']:.1f}KB" if result['success'] else "-"
        duration = f"{result['duration']:.2f}s"

        # 显示进度条
        progress = completed / total
        bar_length = 20
        filled = int(bar_length * progress)
        bar = "█" * filled + "░" * (bar_length - filled)

        print(f"{filename:<30} {status:<8} {size:<10} {duration:<8}")
        print(f"进度: [{bar}] {completed}/{total} ({progress*100:.1f}%)")

        if not result['success'] and result['error']:
            print(f"  └─ 错误: {result['error']}")

    def _show_summary(self, total_time: float):
        """
        显示总结

        Args:
            total_time: 总耗时
        """
        print("=" * 70)

        success_count = sum(1 for r in self.results if r['success'])
        failed_count = len(self.results) - success_count
        total_size = sum(r['size'] for r in self.results if r['success'])
        total_images = sum(r.get('image_count', 0) for r in self.results if r['success'])

        print(f"\n📊 批量转换完成")
        print(f"  ✅ 成功: {success_count} 个文件")
        if failed_count > 0:
            print(f"  ❌ 失败: {failed_count} 个文件")
        print(f"  📦 总大小: {total_size:.1f} KB")
        print(f"  🖼️ 嵌入图片: {total_images} 张")
        print(f"  ⏱️ 总耗时: {total_time:.2f} 秒")
        print(f"  ⚡ 平均速度: {len(self.results)/total_time:.2f} 文件/秒")

        if failed_count > 0:
            print("\n❌ 失败文件列表:")
            for result in self.results:
                if not result['success']:
                    print(f"  - {Path(result['source']).name}: {result['error']}")

    def process_list(
        self,
        file_list: List[Path],
        output_dir: Path,
        theme: str = "default",
        embed_images: bool = True,
        process_mermaid: bool = True
    ) -> List[dict]:
        """
        批量处理文件列表

        Args:
            file_list: 文件列表
            output_dir: 输出目录
            theme: 主题
            embed_images: 是否嵌入图片
            process_mermaid: 是否处理Mermaid

        Returns:
            处理结果列表
        """
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        print(f"\n📋 处理文件列表: {len(file_list)} 个文件")
        print(f"📁 输出目录: {output_dir}")
        print(f"🎨 主题: {theme}")
        print()

        self._show_progress_header()

        start_time = time.time()

        for i, md_file in enumerate(file_list, 1):
            md_file = Path(md_file)
            if not md_file.exists():
                print(f"⚠️ 文件不存在: {md_file}")
                continue

            output_file = output_dir / md_file.with_suffix('.html').name

            result = self._process_file(
                md_file,
                output_file,
                theme,
                embed_images,
                process_mermaid
            )

            self.results.append(result)
            self._show_progress(i, len(file_list), result)

        total_time = time.time() - start_time
        self._show_summary(total_time)

        return self.results


def batch_convert_cli():
    """命令行入口"""
    import argparse

    parser = argparse.ArgumentParser(
        description='批量转换Markdown文件到HTML'
    )

    parser.add_argument(
        'input_dir',
        help='输入目录路径'
    )

    parser.add_argument(
        '-o', '--output',
        help='输出目录路径（默认为输入目录下的html_output）'
    )

    parser.add_argument(
        '-t', '--theme',
        default='default',
        choices=['default', 'minimal', 'professional'],
        help='选择主题'
    )

    parser.add_argument(
        '-r', '--recursive',
        action='store_true',
        help='递归处理子目录'
    )

    parser.add_argument(
        '-p', '--pattern',
        default='*.md',
        help='文件匹配模式（默认: *.md）'
    )

    parser.add_argument(
        '--no-images',
        action='store_true',
        help='不嵌入图片'
    )

    parser.add_argument(
        '--no-mermaid',
        action='store_true',
        help='不处理Mermaid图表'
    )

    parser.add_argument(
        '-w', '--workers',
        type=int,
        default=4,
        help='并发处理数（默认: 4）'
    )

    args = parser.parse_args()

    # 创建批量处理器
    processor = BatchProcessor(max_workers=args.workers)

    # 执行批量转换
    try:
        processor.process_directory(
            input_dir=Path(args.input_dir),
            output_dir=Path(args.output) if args.output else None,
            theme=args.theme,
            embed_images=not args.no_images,
            process_mermaid=not args.no_mermaid,
            recursive=args.recursive,
            pattern=args.pattern
        )
    except Exception as e:
        print(f"❌ 错误: {e}")
        sys.exit(1)


if __name__ == '__main__':
    batch_convert_cli()