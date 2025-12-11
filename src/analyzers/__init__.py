"""
项目分析模块

提供项目结构分析、代码质量评估、依赖关系检查等功能，
并生成规范的HTML分析报告。
"""

from .base import BaseAnalyzer
from .project_analyzer import ProjectAnalyzer
from .code_quality_analyzer import CodeQualityAnalyzer
from .dependency_analyzer import DependencyAnalyzer
from .metrics_collector import MetricsCollector
from .report_generator import ReportGenerator

__all__ = [
    'BaseAnalyzer',
    'ProjectAnalyzer',
    'CodeQualityAnalyzer',
    'DependencyAnalyzer',
    'MetricsCollector',
    'ReportGenerator',
]

__version__ = '1.0.0'
