#!/usr/bin/env python3
"""
CLI 格式化器
===========

美化命令行输出
"""


class CLIFormatter:
    """CLI 格式化器"""

    def __init__(self, enable_color: bool = True):
        """初始化格式化器"""
        self.enable_color = enable_color

        # ANSI 颜色代码
        if enable_color:
            self.colors = {
                'reset': '\033[0m',
                'red': '\033[31m',
                'green': '\033[32m',
                'yellow': '\033[33m',
                'blue': '\033[34m',
                'magenta': '\033[35m',
                'cyan': '\033[36m',
                'bold': '\033[1m'
            }
        else:
            self.colors = {key: '' for key in [
                'reset', 'red', 'green', 'yellow', 'blue',
                'magenta', 'cyan', 'bold'
            ]}

    def success(self, text: str) -> str:
        """成功消息（绿色）"""
        return f"{self.colors['green']}✓ {text}{self.colors['reset']}"

    def error(self, text: str) -> str:
        """错误消息（红色）"""
        return f"{self.colors['red']}✗ {text}{self.colors['reset']}"

    def warning(self, text: str) -> str:
        """警告消息（黄色）"""
        return f"{self.colors['yellow']}⚠ {text}{self.colors['reset']}"

    def info(self, text: str) -> str:
        """信息消息（蓝色）"""
        return f"{self.colors['blue']}ℹ {text}{self.colors['reset']}"

    def highlight(self, text: str) -> str:
        """高亮文本（青色）"""
        return f"{self.colors['cyan']}{text}{self.colors['reset']}"

    def title(self, text: str) -> str:
        """标题（粗体）"""
        return f"{self.colors['bold']}{text}{self.colors['reset']}"

    def progress(self, current: int, total: int, width: int = 30) -> str:
        """进度条"""
        percent = current / total if total > 0 else 0
        filled = int(width * percent)
        bar = '█' * filled + '░' * (width - filled)
        return f"[{bar}] {percent*100:.1f}%"