#!/usr/bin/env python3
"""
进度显示工具
===========

提供各种进度显示功能
"""

import sys
import time
import threading
from typing import Optional


class ProgressBar:
    """进度条类"""

    def __init__(
        self,
        total: int,
        prefix: str = "Progress",
        suffix: str = "Complete",
        length: int = 50,
        fill: str = "█",
        empty: str = "░"
    ):
        """
        初始化进度条

        Args:
            total: 总数
            prefix: 前缀文字
            suffix: 后缀文字
            length: 进度条长度
            fill: 填充字符
            empty: 空白字符
        """
        self.total = total
        self.prefix = prefix
        self.suffix = suffix
        self.length = length
        self.fill = fill
        self.empty = empty
        self.current = 0
        self.start_time = time.time()

    def update(self, current: Optional[int] = None):
        """
        更新进度

        Args:
            current: 当前进度（默认自增1）
        """
        if current is None:
            self.current += 1
        else:
            self.current = current

        self._display()

    def increment(self, amount: int = 1):
        """
        增加进度

        Args:
            amount: 增加量
        """
        self.current += amount
        self._display()

    def _display(self):
        """显示进度条"""
        if self.total == 0:
            percent = 100.0
        else:
            percent = min(100, (self.current / self.total) * 100)

        filled_length = int(self.length * self.current // max(self.total, 1))
        bar = self.fill * filled_length + self.empty * (self.length - filled_length)

        # 计算剩余时间
        elapsed_time = time.time() - self.start_time
        if self.current > 0:
            estimated_total = elapsed_time * self.total / self.current
            remaining_time = estimated_total - elapsed_time
            time_str = f" ETA: {self._format_time(remaining_time)}"
        else:
            time_str = ""

        # 显示进度条
        sys.stdout.write(f'\r{self.prefix} |{bar}| {percent:.1f}% {self.suffix}{time_str}')
        sys.stdout.flush()

        # 完成时换行
        if self.current >= self.total:
            print()

    def _format_time(self, seconds: float) -> str:
        """
        格式化时间

        Args:
            seconds: 秒数

        Returns:
            格式化的时间字符串
        """
        if seconds < 60:
            return f"{seconds:.0f}s"
        elif seconds < 3600:
            minutes = seconds // 60
            seconds = seconds % 60
            return f"{minutes:.0f}m {seconds:.0f}s"
        else:
            hours = seconds // 3600
            minutes = (seconds % 3600) // 60
            return f"{hours:.0f}h {minutes:.0f}m"

    def finish(self):
        """完成进度条"""
        self.current = self.total
        self._display()


class Spinner:
    """旋转指示器"""

    def __init__(self, message: str = "Processing"):
        """
        初始化旋转指示器

        Args:
            message: 显示消息
        """
        self.message = message
        self.spinning = False
        self.thread = None
        self.spinner_chars = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        self.current_char = 0

    def start(self):
        """开始旋转"""
        self.spinning = True
        self.thread = threading.Thread(target=self._spin)
        self.thread.daemon = True
        self.thread.start()

    def stop(self, final_message: Optional[str] = None):
        """
        停止旋转

        Args:
            final_message: 最终消息
        """
        self.spinning = False
        if self.thread:
            self.thread.join()

        # 清除当前行
        sys.stdout.write('\r' + ' ' * (len(self.message) + 10) + '\r')

        if final_message:
            print(final_message)
        sys.stdout.flush()

    def _spin(self):
        """旋转动画"""
        while self.spinning:
            char = self.spinner_chars[self.current_char]
            sys.stdout.write(f'\r{char} {self.message}')
            sys.stdout.flush()

            self.current_char = (self.current_char + 1) % len(self.spinner_chars)
            time.sleep(0.1)


class MultiProgressBar:
    """多进度条管理器"""

    def __init__(self):
        """初始化多进度条管理器"""
        self.bars = {}
        self.lock = threading.Lock()

    def add_bar(
        self,
        name: str,
        total: int,
        prefix: Optional[str] = None,
        **kwargs
    ) -> ProgressBar:
        """
        添加进度条

        Args:
            name: 进度条名称
            total: 总数
            prefix: 前缀（默认使用名称）
            **kwargs: 其他ProgressBar参数

        Returns:
            进度条实例
        """
        if prefix is None:
            prefix = name

        bar = ProgressBar(total, prefix=prefix, **kwargs)
        self.bars[name] = bar
        return bar

    def update(self, name: str, current: Optional[int] = None):
        """
        更新进度条

        Args:
            name: 进度条名称
            current: 当前进度
        """
        with self.lock:
            if name in self.bars:
                self.bars[name].update(current)

    def finish(self, name: str):
        """
        完成进度条

        Args:
            name: 进度条名称
        """
        with self.lock:
            if name in self.bars:
                self.bars[name].finish()
                del self.bars[name]

    def finish_all(self):
        """完成所有进度条"""
        with self.lock:
            for bar in self.bars.values():
                bar.finish()
            self.bars.clear()


def animated_print(text: str, delay: float = 0.03):
    """
    动画打印文本

    Args:
        text: 文本
        delay: 字符间延迟
    """
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()


def progress_context(total: int, message: str = "Processing"):
    """
    进度上下文管理器

    Args:
        total: 总数
        message: 消息

    Example:
        with progress_context(100, "Converting") as progress:
            for i in range(100):
                # 处理逻辑
                progress.update()
    """
    class ProgressContext:
        def __init__(self, bar):
            self.bar = bar

        def __enter__(self):
            return self.bar

        def __exit__(self, exc_type, exc_val, exc_tb):
            self.bar.finish()

    bar = ProgressBar(total, prefix=message)
    return ProgressContext(bar)


def spinner_context(message: str = "Processing"):
    """
    旋转指示器上下文管理器

    Args:
        message: 消息

    Example:
        with spinner_context("Loading") as spinner:
            # 长时间运行的任务
            time.sleep(5)
    """
    class SpinnerContext:
        def __init__(self, spinner):
            self.spinner = spinner

        def __enter__(self):
            self.spinner.start()
            return self.spinner

        def __exit__(self, exc_type, exc_val, exc_tb):
            if exc_type:
                self.spinner.stop(f"❌ {self.spinner.message} failed")
            else:
                self.spinner.stop(f"✅ {self.spinner.message} complete")

    return SpinnerContext(Spinner(message))


# 彩色输出
class Colors:
    """颜色常量"""
    RESET = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    # 前景色
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'

    # 背景色
    BG_BLACK = '\033[40m'
    BG_RED = '\033[41m'
    BG_GREEN = '\033[42m'
    BG_YELLOW = '\033[43m'
    BG_BLUE = '\033[44m'
    BG_MAGENTA = '\033[45m'
    BG_CYAN = '\033[46m'
    BG_WHITE = '\033[47m'


def colored_print(text: str, color: str = Colors.RESET, bold: bool = False):
    """
    彩色打印

    Args:
        text: 文本
        color: 颜色
        bold: 是否加粗
    """
    if bold:
        print(f"{Colors.BOLD}{color}{text}{Colors.RESET}")
    else:
        print(f"{color}{text}{Colors.RESET}")


def success(text: str):
    """成功消息"""
    colored_print(f"✅ {text}", Colors.GREEN, bold=True)


def error(text: str):
    """错误消息"""
    colored_print(f"❌ {text}", Colors.RED, bold=True)


def warning(text: str):
    """警告消息"""
    colored_print(f"⚠️ {text}", Colors.YELLOW, bold=True)


def info(text: str):
    """信息消息"""
    colored_print(f"ℹ️ {text}", Colors.CYAN)


if __name__ == '__main__':
    # 测试进度条
    print("测试进度条:")
    bar = ProgressBar(100, prefix="下载", suffix="完成")
    for i in range(100):
        time.sleep(0.01)
        bar.update()

    print("\n测试旋转指示器:")
    spinner = Spinner("处理中")
    spinner.start()
    time.sleep(3)
    spinner.stop("✅ 处理完成")

    print("\n测试彩色输出:")
    success("操作成功")
    error("操作失败")
    warning("请注意")
    info("提示信息")

    print("\n测试动画打印:")
    animated_print("Hello, World! 这是动画打印效果。")