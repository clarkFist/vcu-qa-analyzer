"""
AI 驱动的 Skills 系统

提供智能项目分析和问答功能。
"""

from .project_qa import ProjectQASkill
from .code_insight import CodeInsightSkill
from .skill_manager import SkillManager

__all__ = [
    'ProjectQASkill',
    'CodeInsightSkill',
    'SkillManager',
]

__version__ = '1.0.0'
