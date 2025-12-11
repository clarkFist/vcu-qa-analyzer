#!/usr/bin/env python3
"""
图片处理器
=========

处理 Markdown 中的图片，支持 base64 嵌入
"""

import re
import base64
from pathlib import Path
from typing import Tuple, Optional


class ImageProcessor:
    """图片处理器"""

    def __init__(self):
        """初始化处理器"""
        # 支持的图片格式
        self.supported_formats = {
            '.png': 'image/png',
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.gif': 'image/gif',
            '.bmp': 'image/bmp',
            '.webp': 'image/webp',
            '.svg': 'image/svg+xml'
        }

        # 图片匹配模式
        self.pattern = r'!\[([^\]]*)\]\(([^)]+)\)'

    def process(self, content: str, base_dir: Path) -> Tuple[str, int]:
        """
        处理 Markdown 中的图片引用

        Args:
            content: Markdown 内容
            base_dir: 基础目录

        Returns:
            (处理后的内容, 图片数量)
        """
        image_count = 0

        def replace_image(match):
            nonlocal image_count
            alt_text = match.group(1)
            image_path = match.group(2)

            # 跳过在线图片
            if image_path.startswith(('http://', 'https://', 'data:')):
                return match.group(0)

            # 查找并嵌入图片
            img_file = self._find_image_file(image_path, base_dir)

            if img_file and img_file.exists():
                try:
                    # 转换为 base64
                    data_url = self._to_base64(img_file)

                    if data_url:
                        print(f"  ✓ 嵌入图片: {img_file.name} ({img_file.stat().st_size/1024:.1f}KB)")
                        image_count += 1
                        return f'![{alt_text}]({data_url})'

                except Exception as e:
                    print(f"  ✗ 处理图片失败: {image_path} - {e}")

            else:
                print(f"  ⚠ 找不到图片: {image_path}")

            return match.group(0)

        # 替换所有图片引用
        processed = re.sub(self.pattern, replace_image, content)

        return processed, image_count

    def _find_image_file(self, image_path: str, base_dir: Path) -> Optional[Path]:
        """
        智能查找图片文件

        Args:
            image_path: 图片路径
            base_dir: 基础目录

        Returns:
            图片文件路径
        """
        # 尝试不同的路径组合
        path_attempts = [
            # 绝对路径
            Path(image_path),
            # 相对路径
            base_dir / image_path,
            # 只有文件名
            base_dir / Path(image_path).name,
            # 去掉前导斜杠
            base_dir / image_path.lstrip('/'),
        ]

        for path in path_attempts:
            if path.is_absolute() and path.exists():
                return path
            elif not path.is_absolute() and path.exists():
                return path

        # 尝试在常见位置查找
        common_dirs = ['images', 'img', 'assets', 'static', 'media']
        filename = Path(image_path).name

        for dir_name in common_dirs:
            img_dir = base_dir / dir_name
            if img_dir.exists():
                img_file = img_dir / filename
                if img_file.exists():
                    return img_file

        return None

    def _to_base64(self, file_path: Path) -> Optional[str]:
        """
        将图片文件转换为 base64 数据 URL

        Args:
            file_path: 文件路径

        Returns:
            base64 数据 URL
        """
        try:
            # 获取 MIME 类型
            mime_type = self.supported_formats.get(
                file_path.suffix.lower(),
                'image/png'
            )

            # 读取文件并编码
            with open(file_path, 'rb') as f:
                img_data = f.read()

            b64_data = base64.b64encode(img_data).decode('utf-8')

            return f"data:{mime_type};base64,{b64_data}"

        except Exception as e:
            print(f"  ✗ Base64 编码失败: {file_path} - {e}")
            return None

    def extract_images(self, content: str) -> list[str]:
        """
        提取 Markdown 中的所有图片引用

        Args:
            content: Markdown 内容

        Returns:
            图片路径列表
        """
        matches = re.findall(self.pattern, content)
        return [match[1] for match in matches]