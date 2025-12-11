"""
报告生成器

将分析结果生成为 Markdown 和 HTML 格式的报告。
"""

from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime
import json

from .base import AnalysisResult
from .metrics_collector import MetricsCollector


class ReportGenerator:
    """报告生成器"""

    def __init__(self, project_path: Path):
        """
        初始化报告生成器

        Args:
            project_path: 项目根目录路径
        """
        self.project_path = Path(project_path)
        self.template_dir = Path(__file__).parent / 'templates'

    def generate_report(
        self,
        output_path: Optional[Path] = None,
        format: str = 'both'
    ) -> Dict[str, Path]:
        """
        生成分析报告

        Args:
            output_path: 输出路径（不含扩展名）
            format: 输出格式 ('markdown', 'html', 'both')

        Returns:
            Dict[str, Path]: 生成的文件路径
        """
        # 收集指标
        collector = MetricsCollector(self.project_path)
        result = collector.analyze()

        # 确定输出路径
        if output_path is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_path = self.project_path / f'project_analysis_{timestamp}'

        output_files = {}

        # 生成 Markdown 报告
        if format in ['markdown', 'both']:
            md_path = output_path.with_suffix('.md')
            self._generate_markdown(result, md_path)
            output_files['markdown'] = md_path

        # 生成 HTML 报告
        if format in ['html', 'both']:
            html_path = output_path.with_suffix('.html')
            self._generate_html(result, html_path)
            output_files['html'] = html_path

        return output_files

    def _generate_markdown(self, result: AnalysisResult, output_path: Path) -> None:
        """生成 Markdown 报告"""
        content = []

        # 标题
        content.append("# 项目分析报告\n")
        content.append(f"**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        content.append(f"**项目路径**: `{self.project_path}`\n")
        content.append("\n---\n")

        # 执行摘要
        content.append("\n## 执行摘要\n")
        summary = result.data.get('summary', {})
        score = result.data.get('overall_score', {})

        content.append(f"**综合评分**: {score.get('total', 0)}/{score.get('max', 100)} ({score.get('grade', 'N/A')})\n")
        content.append("\n### 评分明细\n")
        for category, points in score.get('breakdown', {}).items():
            content.append(f"- **{category}**: {points}分\n")

        # 关键指标
        content.append("\n### 关键指标\n")
        metrics = summary.get('key_metrics', {})
        content.append(f"- 总文件数: {metrics.get('total_files', 0)}\n")
        content.append(f"- 总代码行数: {metrics.get('code_lines', 0)}\n")
        content.append(f"- 函数数量: {metrics.get('total_functions', 0)}\n")
        content.append(f"- 类数量: {metrics.get('total_classes', 0)}\n")

        # 亮点
        if summary.get('highlights'):
            content.append("\n### ✅ 亮点\n")
            for highlight in summary['highlights']:
                content.append(f"- {highlight}\n")

        # 关注点
        if summary.get('concerns'):
            content.append("\n### ⚠️ 需要关注\n")
            for concern in summary['concerns']:
                content.append(f"- {concern}\n")

        # 项目结构
        content.append("\n---\n\n## 项目结构\n")
        project_data = result.data.get('project', {})

        project_info = project_data.get('project_info', {})
        content.append(f"**项目名称**: {project_info.get('name', 'N/A')}\n")
        content.append(f"**项目大小**: {project_info.get('size', 'N/A')}\n")
        content.append(f"**项目类型**: {', '.join(project_info.get('project_type', []))}\n")

        if project_info.get('is_git_repo'):
            git_info = project_info.get('git_info', {})
            content.append(f"**Git 分支**: {git_info.get('current_branch', 'N/A')}\n")

        # 文件类型分布
        content.append("\n### 文件类型分布\n")
        file_types = project_data.get('file_type_distribution', {})
        for ext, count in list(file_types.items())[:10]:
            content.append(f"- `.{ext}`: {count} 个文件\n")

        # 代码统计
        content.append("\n### 代码统计\n")
        code_stats = project_data.get('code_statistics', {})
        content.append(f"- 总行数: {code_stats.get('total_lines', 0)}\n")
        content.append(f"- 代码行数: {code_stats.get('code_lines', 0)}\n")
        content.append(f"- 注释行数: {code_stats.get('comment_lines', 0)}\n")
        content.append(f"- 空行数: {code_stats.get('blank_lines', 0)}\n")

        # 目录树
        content.append("\n### 目录结构\n")
        content.append("```\n")
        tree = project_data.get('directory_tree', [])
        content.extend([line + '\n' for line in tree[:50]])
        content.append("```\n")

        # 代码质量
        content.append("\n---\n\n## 代码质量\n")
        quality_data = result.data.get('quality', {})

        # Python 代码分析
        python_analysis = quality_data.get('python_analysis', {})
        if python_analysis.get('total_files', 0) > 0:
            content.append("\n### Python 代码分析\n")
            content.append(f"- Python 文件数: {python_analysis.get('total_files', 0)}\n")
            content.append(f"- 函数总数: {python_analysis.get('total_functions', 0)}\n")
            content.append(f"- 类总数: {python_analysis.get('total_classes', 0)}\n")
            content.append(f"- 平均函数长度: {python_analysis.get('average_function_length', 0)} 行\n")

        # 复杂度分析
        complexity = quality_data.get('complexity_analysis', {})
        content.append("\n### 复杂度分析\n")
        content.append(f"- 平均复杂度: {complexity.get('average_complexity', 0)}\n")
        content.append(f"- 最大复杂度: {complexity.get('max_complexity', 0)}\n")

        high_complexity = complexity.get('high_complexity_functions', [])
        if high_complexity:
            content.append("\n**高复杂度函数**:\n")
            for func in high_complexity[:5]:
                content.append(f"- `{func['function']}` in {func['file']} (复杂度: {func['complexity']})\n")

        # 代码风格
        style_issues = quality_data.get('style_issues', {})
        content.append("\n### 代码风格\n")
        content.append(f"- 总问题数: {style_issues.get('total_issues', 0)}\n")
        for issue_type, count in style_issues.get('by_type', {}).items():
            content.append(f"- {issue_type}: {count}\n")

        # 最佳实践
        content.append("\n### 最佳实践检查\n")
        best_practices = quality_data.get('best_practices', {})
        content.append(f"- {'✅' if best_practices.get('has_tests') else '❌'} 测试用例\n")
        content.append(f"- {'✅' if best_practices.get('has_readme') else '❌'} README 文档\n")
        content.append(f"- {'✅' if best_practices.get('has_requirements') else '❌'} 依赖管理\n")
        content.append(f"- {'✅' if best_practices.get('has_gitignore') else '❌'} .gitignore\n")
        content.append(f"- {'✅' if best_practices.get('has_license') else '❌'} 开源许可证\n")

        recommendations = best_practices.get('recommendations', [])
        if recommendations:
            content.append("\n**改进建议**:\n")
            for rec in recommendations:
                content.append(f"- {rec}\n")

        # 依赖分析
        content.append("\n---\n\n## 依赖分析\n")
        dependencies = result.data.get('dependencies', {})

        # Python 依赖
        python_deps = dependencies.get('python_dependencies', {})
        if python_deps.get('found'):
            content.append(f"\n### Python 依赖 ({python_deps.get('source', 'N/A')})\n")
            content.append(f"**总计**: {python_deps.get('total_count', 0)} 个包\n\n")

            packages = python_deps.get('packages', [])
            if packages:
                content.append("| 包名 | 版本要求 |\n")
                content.append("|------|----------|\n")
                for pkg in packages[:20]:
                    content.append(f"| {pkg['name']} | {pkg.get('version_spec', '')} |\n")

        # Node.js 依赖
        nodejs_deps = dependencies.get('nodejs_dependencies', {})
        if nodejs_deps.get('found'):
            content.append(f"\n### Node.js 依赖\n")
            content.append(f"**总计**: {nodejs_deps.get('total_count', 0)} 个包\n")

        # 版本分析
        version_analysis = dependencies.get('version_analysis', )
        if version_analysis:
            content.append("\n### 版本管理\n")
            content.append(f"- 固定版本: {version_analysis.get('pinned_versions', 0)}\n")
            content.append(f"- 灵活版本: {version_analysis.get('flexible_versions', 0)}\n")
            content.append(f"- 未指定版本: {version_analysis.get('latest_versions', 0)}\n")

        # 错误和警告
        if result.errors or result.warnings:
            content.append("\n---\n\n## 诊断信息\n")

            if result.errors:
                content.append("\n### ❌ 错误\n")
                for error in result.errors:
                    content.append(f"- {error}\n")

            if result.warnings:
                content.append("\n### ⚠️ 警告\n")
                for warning in result.warnings:
                    content.append(f"- {warning}\n")

        # 写入文件
        with open(output_path, 'w', encoding='utf-8') as f:
            f.writelines(content)

    def _generate_html(self, result: AnalysisResult, output_path: Path) -> None:
        """生成 HTML 报告"""
        # 先生成 Markdown
        md_path = output_path.with_suffix('.md')
        self._generate_markdown(result, md_path)

        # 使用现有的 converter 转换为 HTML
        try:
            from ..core.converter import HTMLConverter

            converter = HTMLConverter()
            converter.convert(
                source_path=md_path,
                output_path=output_path,
                theme='professional',
                embed_images=True,
                process_mermaid=True
            )

            # 删除临时 Markdown 文件
            md_path.unlink()

        except Exception as e:
            raise RuntimeError(f"HTML 报告生成失败: {str(e)}")
