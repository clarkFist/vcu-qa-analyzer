"""
指标收集器

收集和汇总各种项目指标。
"""

from pathlib import Path
from typing import Dict, Any
from datetime import datetime

from .base import BaseAnalyzer, AnalysisResult
from .project_analyzer import ProjectAnalyzer
from .code_quality_analyzer import CodeQualityAnalyzer
from .dependency_analyzer import DependencyAnalyzer


class MetricsCollector(BaseAnalyzer):
    """指标收集器"""

    def analyze(self) -> AnalysisResult:
        """
        收集所有指标

        Returns:
            AnalysisResult: 包含所有指标的分析结果
        """
        try:
            # 运行所有分析器
            project_result = ProjectAnalyzer(self.project_path).analyze()
            quality_result = CodeQualityAnalyzer(self.project_path).analyze()
            dependency_result = DependencyAnalyzer(self.project_path).analyze()

            # 汇总结果
            self.result.data['project'] = project_result.data
            self.result.data['quality'] = quality_result.data
            self.result.data['dependencies'] = dependency_result.data

            # 计算综合评分
            self.result.data['overall_score'] = self._calculate_overall_score()

            # 生成摘要
            self.result.data['summary'] = self._generate_summary()

            # 合并错误和警告
            self.result.errors.extend(project_result.errors)
            self.result.errors.extend(quality_result.errors)
            self.result.errors.extend(dependency_result.errors)

            self.result.warnings.extend(project_result.warnings)
            self.result.warnings.extend(quality_result.warnings)
            self.result.warnings.extend(dependency_result.warnings)

        except Exception as e:
            self.result.add_error(f"指标收集失败: {str(e)}")

        return self.result

    def _calculate_overall_score(self) -> Dict[str, Any]:
        """计算综合评分"""
        score = {
            'total': 0,
            'max': 100,
            'breakdown': {},
            'grade': 'N/A'
        }

        # 项目结构评分 (30分)
        structure_score = 0
        project_data = self.result.data.get('project', {})
        if project_data.get('project_info', {}).get('is_git_repo'):
            structure_score += 10
        if project_data.get('code_statistics', {}).get('total_lines', 0) > 0:
            structure_score += 10
        if len(project_data.get('file_type_distribution', {})) > 0:
            structure_score += 10
        score['breakdown']['structure'] = structure_score

        # 代码质量评分 (40分)
        quality_score = 40
        quality_data = self.result.data.get('quality', {})

        # 扣分项
        python_analysis = quality_data.get('python_analysis', {})
        if python_analysis.get('average_function_length', 0) > 30:
            quality_score -= 5

        style_issues = quality_data.get('style_issues', {})
        if style_issues.get('total_issues', 0) > 50:
            quality_score -= 10

        complexity = quality_data.get('complexity_analysis', {})
        if complexity.get('max_complexity', 0) > 15:
            quality_score -= 10

        score['breakdown']['quality'] = max(0, quality_score)

        # 最佳实践评分 (30分)
        practices_score = 0
        best_practices = quality_data.get('best_practices', )
        if best_practices.get('has_tests'):
            practices_score += 10
        if best_practices.get('has_readme'):
            practices_score += 5
        if best_practices.get('has_requirements'):
            practices_score += 5
        if best_practices.get('has_gitignore'):
            practices_score += 5
        if best_practices.get('has_license'):
            practices_score += 5
        score['breakdown']['practices'] = practices_score

        # 计算总分
        score['total'] = sum(score['breakdown'].values())

        # 评级
        if score['total'] >= 90:
            score['grade'] = 'A'
        elif score['total'] >= 80:
            score['grade'] = 'B'
        elif score['total'] >= 70:
            score['grade'] = 'C'
        elif score['total'] >= 60:
            score['grade'] = 'D'
        else:
            score['grade'] = 'F'

        return score

    def _generate_summary(self) -> Dict[str, Any]:
        """生成分析摘要"""
        summary = {
            'analysis_date': datetime.now().isoformat(),
            'project_name': self.project_path.name,
            'key_metrics': {},
            'highlights': [],
            'concerns': [],
        }

        # 关键指标
        project_data = self.result.data.get('project', {})
        quality_data = self.result.data.get('quality', {})

        code_stats = project_data.get('code_statistics', {})
        summary['key_metrics'] = {
            'total_files': project_data.get('file_structure', {}).get('total_files', 0),
            'total_lines': code_stats.get('total_lines', 0),
            'code_lines': code_stats.get('code_lines', 0),
            'total_functions': quality_data.get('python_analysis', {}).get('total_functions', 0),
            'total_classes': quality_data.get('python_analysis', {}).get('total_classes', 0),
        }

        # 亮点
        best_practices = quality_data.get('best_practices', {})
        if best_practices.get('has_tests'):
            summary['highlights'].append("项目包含测试用例")
        if best_practices.get('has_readme'):
            summary['highlights'].append("项目有完整的 README 文档")
        if code_stats.get('comment_lines', 0) / max(code_stats.get('code_lines', 1), 1) > 0.1:
            summary['highlights'].append("代码注释率良好")

        # 关注点
        complexity = quality_data.get('complexity_analysis', {})
        if complexity.get('max_complexity', 0) > 15:
            summary['concerns'].append(f"存在高复杂度函数 (最大复杂度: {complexity['max_complexity']})")

        style_issues = quality_data.get('style_issues', {})
        if style_issues.get('total_issues', 0) > 50:
            summary['concerns'].append(f"代码风格问题较多 ({style_issues['total_issues']} 个)")

        if not best_practices.get('has_tests'):
            summary['concerns'].append("缺少测试用例")

        return summary
