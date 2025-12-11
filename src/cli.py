#!/usr/bin/env python3
"""
命令行接口
=========

提供命令行交互功能
"""

import sys
import argparse
from pathlib import Path
from typing import List
import time

from src.core.converter import HTMLConverter
from src.core.stats import StatsTracker
from src.themes import list_themes
from src.utils.file_scanner import FileScanner
from src.utils.formatter import CLIFormatter


def main():
    """主函数"""
    # 检查是否无参数，直接进入交互模式
    if len(sys.argv) == 1:
        from src.interactive import interactive_mode
        return interactive_mode()

    parser = argparse.ArgumentParser(
        description="Markdown 转 HTML 报告工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s report.md                     # 转换单个文件（默认主题）
  %(prog)s report.md -t minimal          # 使用简约主题
  %(prog)s *.md -o output/                # 批量转换到指定目录
  %(prog)s docs/ -r                      # 递归转换目录中的所有文件
  %(prog)s report.md --no-images         # 不嵌入图片
  %(prog)s --list-themes                 # 列出所有可用主题

交互模式:
  不带参数运行时会自动进入交互式选择界面
        """
    )

    # 位置参数
    parser.add_argument(
        'input',
        nargs='?',
        help='输入文件或目录（支持通配符）'
    )

    # 可选参数
    parser.add_argument(
        '-o', '--output',
        help='输出文件或目录'
    )

    parser.add_argument(
        '-t', '--theme',
        default='default',
        choices=list_themes(),
        help='选择主题（默认: default）'
    )

    parser.add_argument(
        '-r', '--recursive',
        action='store_true',
        help='递归处理目录'
    )

    parser.add_argument(
        '--no-images',
        action='store_true',
        help='不嵌入图片（使用原始路径）'
    )

    parser.add_argument(
        '--no-mermaid',
        action='store_true',
        help='不处理 Mermaid 图表'
    )

    parser.add_argument(
        '--list-themes',
        action='store_true',
        help='列出所有可用主题'
    )

    parser.add_argument(
        '--stats',
        action='store_true',
        help='显示转换统计信息'
    )

    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='显示详细输出'
    )

    args = parser.parse_args()

    # CLI 格式化器
    formatter = CLIFormatter()

    # 列出主题
    if args.list_themes:
        print_themes(formatter)
        return 0

    # 检查输入
    if not args.input:
        # 进入交互式模式
        from src.interactive import interactive_mode
        return interactive_mode()

    try:
        # 运行转换
        return run_conversion(args, formatter)

    except KeyboardInterrupt:
        print("\n" + formatter.warning("用户中断"))
        return 130

    except Exception as e:
        print(formatter.error(f"错误: {e}"))
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


def print_themes(formatter: CLIFormatter):
    """打印可用主题"""
    print(formatter.title("可用主题"))
    print()

    themes_info = {
        'default': '功能丰富的默认主题，包含侧边栏、图片放大等功能',
        'minimal': '清爽简洁的主题，适合阅读',
        'professional': '专业的文档主题，适合技术报告'
    }

    for theme in list_themes():
        desc = themes_info.get(theme, '自定义主题')
        print(f"  {formatter.highlight(theme):15} - {desc}")

    print()


def run_conversion(args, formatter: CLIFormatter) -> int:
    """运行转换"""
    # 初始化组件
    converter = HTMLConverter()
    stats_tracker = StatsTracker()
    scanner = FileScanner()

    # 查找文件
    input_path = Path(args.input)
    files = []

    if input_path.is_file():
        # 单个文件
        files = [input_path]
    elif input_path.is_dir():
        # 目录
        files = scanner.scan_markdown_files(input_path, args.recursive)
    else:
        # 通配符
        files = list(Path.cwd().glob(args.input))
        files = [f for f in files if f.suffix == '.md']

    if not files:
        print(formatter.warning("未找到 Markdown 文件"))
        return 1

    # 确定输出目录
    output_dir = None
    if args.output:
        output_path = Path(args.output)
        if output_path.suffix == '.html' and len(files) == 1:
            # 单个文件，指定了输出文件名
            output_dir = None
        else:
            # 批量转换，使用输出目录
            output_dir = output_path
            output_dir.mkdir(parents=True, exist_ok=True)

    # 打印开始信息
    print(formatter.title("Markdown 转 HTML 报告工具"))
    print("=" * 60)
    print()

    if len(files) == 1:
        print(f"📄 正在处理: {files[0].name}")
    else:
        print(f"📚 批量处理: {len(files)} 个文件")
    print(f"🎨 主题: {args.theme}")
    print(f"🖼️ 图片嵌入: {'否' if args.no_images else '是'}")
    print(f"📊 Mermaid 支持: {'否' if args.no_mermaid else '是'}")
    print()

    # 批量转换
    total = len(files)
    success_count = 0

    for i, file_path in enumerate(files, 1):
        # 显示进度
        if total > 1:
            print(f"[{i}/{total}] {file_path.name}")

        # 确定输出路径
        if args.output and Path(args.output).suffix == '.html' and total == 1:
            output_path = Path(args.output)
        elif output_dir:
            output_path = output_dir / f"{file_path.stem}.html"
        else:
            output_path = None

        # 转换文件
        start_time = time.time()

        result = converter.convert(
            source_path=file_path,
            output_path=output_path,
            theme=args.theme,
            embed_images=not args.no_images,
            process_mermaid=not args.no_mermaid
        )

        # 更新统计
        stats_tracker.track_result(result, file_path)

        if result.success:
            success_count += 1
            if args.verbose or total == 1:
                print(f"  ✓ 转换成功: {result.output_path.name}")
                print(f"    文件大小: {result.file_size / 1024:.1f} KB")
                print(f"    嵌入图片: {result.image_count} 张")
                print(f"    耗时: {result.duration:.2f}s")
        else:
            print(f"  ✗ 转换失败: {result.error_message}")

        if total > 1 and i < total:
            print()

    # 显示统计
    if args.stats or total > 1:
        print()
        print("=" * 60)
        print(stats_tracker.generate_summary())

    # 返回状态码
    if success_count == total:
        return 0
    elif success_count > 0:
        return 2  # 部分成功
    else:
        return 1  # 全部失败


if __name__ == '__main__':
    sys.exit(main())