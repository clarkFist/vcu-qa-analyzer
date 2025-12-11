#!/usr/bin/env python3
"""
交互式模式
=========

提供友好的交互式界面
"""

import os
import sys
from pathlib import Path
from typing import List, Optional

from src.utils.formatter import CLIFormatter
from src.utils.file_scanner import FileScanner
from src.themes import list_themes


class InteractiveMode:
    """交互式模式"""

    def __init__(self):
        """初始化交互模式"""
        self.formatter = CLIFormatter()
        self.scanner = FileScanner()

    def run(self) -> dict:
        """
        运行交互式模式

        Returns:
            用户选择的参数字典
        """
        self._print_welcome()

        # 选择文件
        input_file = self._select_file()
        if not input_file:
            return None

        # 选择主题
        theme = self._select_theme()

        # 选择选项
        options = self._select_options()

        # 确认
        if not self._confirm_choices(input_file, theme, options):
            return None

        return {
            'input': input_file,
            'theme': theme,
            'no_images': not options['embed_images'],
            'no_mermaid': not options['process_mermaid'],
            'output': options.get('output'),
            'stats': options['show_stats']
        }

    def _print_welcome(self):
        """打印欢迎信息"""
        print()
        print(self.formatter.title("🎨 Markdown to HTML Converter"))
        print("=" * 50)
        print("欢迎使用 Markdown 转 HTML 工具！")
        print()

    def _select_file(self) -> Optional[str]:
        """
        选择要转换的文件

        Returns:
            文件路径或 None
        """
        print(self.formatter.highlight("📄 选择 Markdown 文件"))
        print()

        # 扫描当前目录的 Markdown 文件
        md_files = self.scanner.scan_markdown_files(Path.cwd())

        if not md_files:
            print(self.formatter.warning("当前目录没有 Markdown 文件"))
            print()
            # 手动输入
            file_path = input("请输入文件路径（或按 Enter 退出）: ").strip()
            if not file_path:
                return None
            if not Path(file_path).exists():
                print(self.formatter.error(f"文件不存在: {file_path}"))
                return None
            return file_path

        # 显示文件列表
        print("找到以下 Markdown 文件:")
        for i, file_path in enumerate(md_files[:20], 1):
            size_kb = file_path.stat().st_size / 1024
            print(f"  {i:2}. {file_path.name:40} ({size_kb:.1f} KB)")

        if len(md_files) > 20:
            print(f"  ... 还有 {len(md_files) - 20} 个文件")

        print()
        print("  0. 手动输入路径")
        print("  q. 退出")
        print()

        # 用户选择
        while True:
            choice = input("请选择文件 [1]: ").strip().lower()

            if not choice:
                choice = "1"

            if choice == 'q':
                return None

            if choice == '0':
                file_path = input("请输入文件路径: ").strip()
                if Path(file_path).exists():
                    return file_path
                print(self.formatter.error("文件不存在"))
                continue

            try:
                index = int(choice) - 1
                if 0 <= index < len(md_files):
                    return str(md_files[index])
                print(self.formatter.error("无效的选择"))
            except ValueError:
                print(self.formatter.error("请输入数字"))

    def _select_theme(self) -> str:
        """
        选择主题

        Returns:
            主题名称
        """
        print()
        print(self.formatter.highlight("🎨 选择主题"))
        print()

        themes = {
            'default': '功能丰富的默认主题（侧边栏、图片放大）',
            'minimal': '清爽简洁的主题（适合阅读）',
            'professional': '专业文档主题（适合报告）'
        }

        for i, (theme, desc) in enumerate(themes.items(), 1):
            print(f"  {i}. {theme:15} - {desc}")

        print()
        choice = input("请选择主题 [1]: ").strip()

        if not choice:
            return 'default'

        try:
            index = int(choice) - 1
            if 0 <= index < len(themes):
                return list(themes.keys())[index]
        except ValueError:
            pass

        return 'default'

    def _select_options(self) -> dict:
        """
        选择转换选项

        Returns:
            选项字典
        """
        print()
        print(self.formatter.highlight("⚙️ 转换选项"))
        print()

        options = {
            'embed_images': True,
            'process_mermaid': True,
            'show_stats': False,
            'output': None
        }

        # 图片嵌入
        choice = input("嵌入图片到 HTML？[Y/n]: ").strip().lower()
        if choice == 'n':
            options['embed_images'] = False

        # Mermaid 处理
        choice = input("处理 Mermaid 图表？[Y/n]: ").strip().lower()
        if choice == 'n':
            options['process_mermaid'] = False

        # 统计信息
        choice = input("显示统计信息？[y/N]: ").strip().lower()
        if choice == 'y':
            options['show_stats'] = True

        # 输出文件
        output = input("输出文件名（留空使用默认）: ").strip()
        if output:
            options['output'] = output

        return options

    def _confirm_choices(self, input_file: str, theme: str, options: dict) -> bool:
        """
        确认用户选择

        Args:
            input_file: 输入文件
            theme: 主题
            options: 选项

        Returns:
            是否确认
        """
        print()
        print(self.formatter.highlight("📋 确认设置"))
        print()
        print(f"  输入文件: {Path(input_file).name}")
        print(f"  主题: {theme}")
        print(f"  图片嵌入: {'是' if options['embed_images'] else '否'}")
        print(f"  Mermaid: {'是' if options['process_mermaid'] else '否'}")

        if options.get('output'):
            print(f"  输出文件: {options['output']}")
        else:
            print(f"  输出文件: {Path(input_file).stem}.html")

        print()
        choice = input("开始转换？[Y/n]: ").strip().lower()

        return choice != 'n'


def interactive_mode():
    """运行交互式模式的入口函数"""
    mode = InteractiveMode()
    params = mode.run()

    if params:
        # 构建命令行参数
        args = [params['input']]

        if params.get('output'):
            args.extend(['-o', params['output']])

        args.extend(['-t', params['theme']])

        if params['no_images']:
            args.append('--no-images')

        if params['no_mermaid']:
            args.append('--no-mermaid')

        if params['stats']:
            args.append('--stats')

        # 模拟命令行参数
        sys.argv = ['md2html'] + args

        # 导入并运行主程序
        from src.cli import main
        return main()
    else:
        print()
        print("已取消")
        return 0