"""
基础分析器抽象类

定义所有分析器的通用接口和行为。
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime


@dataclass
class AnalysisResult:
    """分析结果数据类"""
    analyzer_name: str
    timestamp: datetime = field(default_factory=datetime.now)
    success: bool = True
    data: Dict[str, Any] = field(default_factory=dict)
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)

    def add_error(self, error: str) -> None:
        """添加错误信息"""
        self.errors.append(error)
        self.success = False

    def add_warning(self, warning: str) -> None:
        """添加警告信息"""
        self.warnings.append(warning)

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return {
            'analyzer_name': self.analyzer_name,
            'timestamp': self.timestamp.isoformat(),
            'success': self.success,
            'data': self.data,
            'errors': self.errors,
            'warnings': self.warnings,
        }


class BaseAnalyzer(ABC):
    """分析器基类"""

    def __init__(self, project_path: Path):
        """
        初始化分析器

        Args:
            project_path: 项目根目录路径
        """
        self.project_path = Path(project_path)
        if not self.project_path.exists():
            raise FileNotFoundError(f"项目路径不存在: {project_path}")

        self.result = AnalysisResult(analyzer_name=self.__class__.__name__)

    @abstractmethod
    def analyze(self) -> AnalysisResult:
        """
        执行分析

        Returns:
            AnalysisResult: 分析结果
        """
        pass

    def _scan_files(
        self,
        pattern: str = "*",
        recursive: bool = True,
        exclude_dirs: Optional[List[str]] = None
    ) -> List[Path]:
        """
        扫描项目文件

        Args:
            pattern: 文件匹配模式
            recursive: 是否递归扫描
            exclude_dirs: 排除的目录列表

        Returns:
            List[Path]: 匹配的文件列表
        """
        if exclude_dirs is None:
            exclude_dirs = [
                '__pycache__', '.git', '.venv', 'venv',
                'node_modules', '.pytest_cache', '.mypy_cache',
                'dist', 'build', '*.egg-info'
            ]

        files = []
        glob_pattern = f"**/{pattern}" if recursive else pattern

        for file_path in self.project_path.glob(glob_pattern):
            if file_path.is_file():
                # 检查是否在排除目录中
                if not any(excluded in file_path.parts for excluded in exclude_dirs):
                    files.append(file_path)

        return files

    def _count_lines(self, file_path: Path) -> Dict[str, int]:
        """
        统计文件行数

        Args:
            file_path: 文件路径

        Returns:
            Dict[str, int]: 包含总行数、代码行数、注释行数、空行数
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            total = len(lines)
            blank = sum(1 for line in lines if line.strip() == '')
            comment = sum(1 for line in lines if line.strip().startswith('#'))
            code = total - blank - comment

            return {
                'total': total,
                'code': code,
                'comment': comment,
                'blank': blank
            }
        except Exception as e:
            self.result.add_warning(f"无法读取文件 {file_path}: {str(e)}")
            return {'total': 0, 'code': 0, 'comment': 0, 'blank': 0}

    def _get_file_extension(self, file_path: Path) -> str:
        """获取文件扩展名（小写，不含点）"""
        return file_path.suffix.lower().lstrip('.')

    def _format_size(self, size_bytes: int) -> str:
        """格式化文件大小"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.2f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.2f} TB"
