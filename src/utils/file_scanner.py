#!/usr/bin/env python3
"""
文件扫描器
=========

扫描和查找 Markdown 文件
"""

from pathlib import Path
from typing import List


class FileScanner:
    """文件扫描器"""

    def __init__(self):
        """初始化扫描器"""
        self.markdown_extensions = {'.md', '.markdown', '.mdown', '.mkd'}

    def scan_markdown_files(
        self,
        directory: Path = None,
        recursive: bool = False
    ) -> List[Path]:
        """
        扫描目录中的 Markdown 文件

        Args:
            directory: 目录路径（默认当前目录）
            recursive: 是否递归扫描

        Returns:
            Markdown 文件路径列表
        """
        if directory is None:
            directory = Path.cwd()
        elif not isinstance(directory, Path):
            directory = Path(directory)

        if not directory.exists():
            return []

        files = []

        if recursive:
            # 递归扫描
            for ext in self.markdown_extensions:
                pattern = f"**/*{ext}"
                files.extend(directory.glob(pattern))
        else:
            # 仅扫描当前目录
            for ext in self.markdown_extensions:
                pattern = f"*{ext}"
                files.extend(directory.glob(pattern))

        # 排序并去重
        files = sorted(set(files))

        return files

    def find_images(self, directory: Path = None) -> List[Path]:
        """
        查找目录中的图片文件

        Args:
            directory: 目录路径

        Returns:
            图片文件路径列表
        """
        if directory is None:
            directory = Path.cwd()
        elif not isinstance(directory, Path):
            directory = Path(directory)

        if not directory.exists():
            return []

        image_extensions = {
            '.png', '.jpg', '.jpeg', '.gif',
            '.bmp', '.webp', '.svg'
        }

        images = []
        for ext in image_extensions:
            images.extend(directory.glob(f"**/*{ext}"))

        return sorted(images)

    def get_file_info(self, file_path: Path) -> dict:
        """
        获取文件信息

        Args:
            file_path: 文件路径

        Returns:
            文件信息字典
        """
        if not file_path.exists():
            return {}

        stat = file_path.stat()

        return {
            'name': file_path.name,
            'path': str(file_path),
            'size': stat.st_size,
            'size_kb': stat.st_size / 1024,
            'size_mb': stat.st_size / (1024 * 1024),
            'modified': stat.st_mtime,
            'extension': file_path.suffix,
            'parent': str(file_path.parent)
        }
