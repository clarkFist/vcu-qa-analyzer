#!/usr/bin/env python3
"""
项目分析工具

分析项目结构、代码质量、依赖关系，并生成规范的 HTML 报告。
"""

import argparse
import sys
from pathlib import Path

from src.analyzers.report_generator import ReportGenerator


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='分析项目并生成 HTML 报告',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 分析当前项目
  python analyze_project.py

  # 分析指定项目
  python analyze_project.py /path/to/project

  # 指定输出文件
  python analyze_project.py -o my_report

  # 只生成 Markdown
  python analyze_project.py -f markdown

  # 只生成 HTML
  python analyze_project.py -f html
        """
    )

    parser.add_argument(
        'project_path',
        nargs='?',
        default='.',
        help='项目路径 (默认: 当前目录)'
    )

    parser.add_argument(
        '-o', '--output',
        help='输出文件路径（不含扩展名）'
    )

    parser.add_argument(
        '-f', '--format',
        choices=['markdown', 'html', 'both'],
        default='both',
        help='输出格式 (默认: both)'
    )

    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='显示详细信息'
    )

    args = parser.parse_args()

    try:
        # 验证项目路径
        project_path = Path(args.project_path).resolve()
        if not project_path.exists():
            print(f"❌ 错误: 项目路径不存在: {project_path}", file=sys.stderr)
            return 1

        if not project_path.is_dir():
            print(f"❌ 错误: 路径不是目录: {project_path}", file=sys.stderr)
            return 1

        print(f"📊 正在分析项目: {project_path.name}")
        print(f"📁 项目路径: {project_path}")
        print()

        # 生成报告
        generator = ReportGenerator(project_path)

        output_path = None
        if args.output:
            output_path = Path(args.output)

        print("🔍 收集项目信息...")
        output_files = generator.generate_report(
            output_path=output_path,
            format=args.format
        )

        # 显示结果
        print("\n✅ 分析完成！\n")
        print("生成的报告:")
        for format_type, file_path in output_files.items():
            print(f"  - {format_type.upper()}: {file_path}")

        print("\n💡 提示: 使用浏览器打开 HTML 文件查看完整报告")

        return 0

    except KeyboardInterrupt:
        print("\n\n⚠️  分析已取消", file=sys.stderr)
        return 130

    except Exception as e:
        print(f"\n❌ 错误: {str(e)}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
