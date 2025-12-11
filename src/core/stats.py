#!/usr/bin/env python3
"""
统计追踪器
=========

追踪转换统计数据
"""

from dataclasses import dataclass, field
from typing import List
from datetime import datetime
from pathlib import Path


@dataclass
class ConversionStats:
    """转换统计数据"""
    total_files: int = 0
    successful: int = 0
    failed: int = 0
    total_duration: float = 0.0
    total_size: int = 0
    total_images: int = 0
    start_time: datetime = field(default_factory=datetime.now)

    @property
    def success_rate(self) -> float:
        """成功率"""
        if self.total_files == 0:
            return 0.0
        return (self.successful / self.total_files) * 100

    @property
    def avg_duration(self) -> float:
        """平均耗时"""
        if self.total_files == 0:
            return 0.0
        return self.total_duration / self.total_files


class StatsTracker:
    """统计追踪器"""

    def __init__(self):
        """初始化追踪器"""
        self.stats = ConversionStats()
        self.file_records = []

    def track_result(self, result, file_path: Path):
        """
        追踪转换结果

        Args:
            result: ConversionResult 对象
            file_path: 源文件路径
        """
        self.stats.total_files += 1

        if result.success:
            self.stats.successful += 1
            self.stats.total_size += result.file_size
            self.stats.total_images += result.image_count
        else:
            self.stats.failed += 1

        self.stats.total_duration += result.duration

        # 记录文件信息
        self.file_records.append({
            'filename': file_path.name,
            'success': result.success,
            'duration': result.duration,
            'size': result.file_size,
            'images': result.image_count,
            'error': result.error_message if not result.success else None
        })

    def generate_summary(self) -> str:
        """
        生成统计摘要

        Returns:
            统计摘要文本
        """
        elapsed = (datetime.now() - self.stats.start_time).total_seconds()

        summary = f"""
转换统计报告
════════════════════════════════════════
总文件数: {self.stats.total_files}
成功数量: {self.stats.successful}
失败数量: {self.stats.failed}
成功率: {self.stats.success_rate:.1f}%
────────────────────────────────────────
总耗时: {self.stats.total_duration:.2f}s
平均耗时: {self.stats.avg_duration:.2f}s/file
总大小: {self.stats.total_size / (1024 * 1024):.2f}MB
嵌入图片: {self.stats.total_images} 张
实际耗时: {elapsed:.2f}s
════════════════════════════════════════
"""
        return summary

    def reset(self):
        """重置统计数据"""
        self.stats = ConversionStats()
        self.file_records = []