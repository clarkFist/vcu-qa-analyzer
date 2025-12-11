"""
主题模块
=======

提供不同的 HTML 输出主题
"""

from .base import BaseTheme
from .default import DefaultTheme
from .minimal import MinimalTheme
from .professional import ProfessionalTheme


def get_theme(name: str) -> BaseTheme:
    """
    获取主题实例

    Args:
        name: 主题名称

    Returns:
        主题实例
    """
    themes = {
        'default': DefaultTheme,
        'minimal': MinimalTheme,
        'professional': ProfessionalTheme
    }

    theme_class = themes.get(name, DefaultTheme)
    return theme_class()


def list_themes() -> list[str]:
    """
    列出所有可用主题

    Returns:
        主题名称列表
    """
    return ['default', 'minimal', 'professional']


__all__ = [
    'BaseTheme',
    'DefaultTheme',
    'MinimalTheme',
    'ProfessionalTheme',
    'get_theme',
    'list_themes'
]