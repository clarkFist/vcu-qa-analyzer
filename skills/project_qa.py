#!/usr/bin/env python3
"""
AI 驱动的项目问答 Skill

功能：
1. 分析项目结构和代码
2. 回答关于项目的问题
3. 提供智能建议和洞察
"""

import sys
import json
from pathlib import Path
from typing import Dict, Any, List, Optional

# 添加父目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.analyzers import (
    ProjectAnalyzer,
    CodeQualityAnalyzer,
    DependencyAnalyzer,
    MetricsCollector
)


class ProjectQASkill:
    """项目问答 Skill"""

    def __init__(self, project_path: Path):
        """
        初始化 Skill

        Args:
            project_path: 项目路径
        """
        self.project_path = Path(project_path)
        self.context = {}
        self._analyze_project()

    def _analyze_project(self):
        """分析项目并构建上下文"""
        print("🔍 正在分析项目...")

        # 收集项目信息
        collector = MetricsCollector(self.project_path)
        result = collector.analyze()

        self.context = {
            'project_name': self.project_path.name,
            'project_path': str(self.project_path),
            'analysis_result': result.data,
            'errors': result.errors,
            'warnings': result.warnings,
        }

        print("✅ 项目分析完成\n")

    def ask(self, question: str) -> Dict[str, Any]:
        """
        回答关于项目的问题

        Args:
            question: 用户问题

        Returns:
            Dict: 包含答案和相关信息
        """
        # 识别问题类型
        question_type = self._classify_question(question)

        # 根据问题类型生成答案
        if question_type == 'structure':
            return self._answer_structure_question(question)
        elif question_type == 'quality':
            return self._answer_quality_question(question)
        elif question_type == 'dependency':
            return self._answer_dependency_question(question)
        elif question_type == 'score':
            return self._answer_score_question(question)
        elif question_type == 'files':
            return self._answer_files_question(question)
        elif question_type == 'improvement':
            return self._answer_improvement_question(question)
        else:
            return self._answer_general_question(question)

    def _classify_question(self, question: str) -> str:
        """分类问题类型"""
        question_lower = question.lower()

        # 关键词映射
        keywords = {
            'structure': ['结构', '目录', '文件', '组织', 'structure', 'directory', 'file'],
            'quality': ['质量', '复杂度', '风格', 'quality', 'complexity', 'style'],
            'dependency': ['依赖', '包', '库', 'dependency', 'package', 'library'],
            'score': ['评分', '分数', '等级', 'score', 'grade', 'rating'],
            'files': ['有哪些', '包含', '列出', 'list', 'show', 'what'],
            'improvement': ['改进', '优化', '建议', 'improve', 'optimize', 'suggest'],
        }

        for qtype, words in keywords.items():
            if any(word in question_lower for word in words):
                return qtype

        return 'general'

    def _answer_structure_question(self, question: str) -> Dict[str, Any]:
        """回答结构相关问题"""
        project_data = self.context['analysis_result']['project']

        answer = {
            'question': question,
            'type': 'structure',
            'answer': self._format_structure_answer(project_data),
            'details': {
                'total_files': project_data['file_structure']['total_files'],
                'file_types': project_data['file_type_distribution'],
                'project_size': project_data['project_info']['size'],
            }
        }

        return answer

    def _format_structure_answer(self, project_data: Dict) -> str:
        """格式化结构答案"""
        info = project_data['project_info']
        structure = project_data['file_structure']
        file_types = project_data['file_type_distribution']

        answer = f"""
📁 项目结构分析：

**基本信息**
- 项目名称: {info['name']}
- 项目类型: {', '.join(info['project_type'])}
- 项目大小: {info['size']}
- 总文件数: {structure['total_files']}

**文件类型分布** (前5种)
"""
        for ext, count in list(file_types.items())[:5]:
            answer += f"- .{ext}: {count} 个文件\n"

        if info.get('is_git_repo'):
            git_info = info.get('git_info', {})
            answer += f"\n**Git 信息**\n"
            answer += f"- 当前分支: {git_info.get('current_branch', 'N/A')}\n"

        return answer.strip()

    def _answer_quality_question(self, question: str) -> Dict[str, Any]:
        """回答质量相关问题"""
        quality_data = self.context['analysis_result']['quality']

        answer = {
            'question': question,
            'type': 'quality',
            'answer': self._format_quality_answer(quality_data),
            'details': quality_data
        }

        return answer

    def _format_quality_answer(self, quality_data: Dict) -> str:
        """格式化质量答案"""
        python_analysis = quality_data.get('python_analysis', {})
        complexity = quality_data.get('complexity_analysis', {})
        style_issues = quality_data.get('style_issues', {})
        best_practices = quality_data.get('best_practices', {})

        answer = f"""
📊 代码质量分析：

**Python 代码统计**
- 总函数数: {python_analysis.get('total_functions', 0)}
- 总类数: {python_analysis.get('total_classes', 0)}
- 平均函数长度: {python_analysis.get('average_function_length', 0)} 行

**复杂度分析**
- 平均复杂度: {complexity.get('average_complexity', 0)}
- 最大复杂度: {complexity.get('max_complexity', 0)}
"""

        high_complexity = complexity.get('high_complexity_functions', [])
        if high_complexity:
            answer += f"\n⚠️ 发现 {len(high_complexity)} 个高复杂度函数\n"

        answer += f"""
**代码风格**
- 总问题数: {style_issues.get('total_issues', 0)}

**最佳实践**
- {'✅' if best_practices.get('has_tests') else '❌'} 测试用例
- {'✅' if best_practices.get('has_readme') else '❌'} README 文档
- {'✅' if best_practices.get('has_requirements') else '❌'} 依赖管理
- {'✅' if best_practices.get('has_gitignore') else '❌'} .gitignore
- {'✅' if best_practices.get('has_license') else '❌'} 开源许可证
"""

        return answer.strip()

    def _answer_dependency_question(self, question: str) -> Dict[str, Any]:
        """回答依赖相关问题"""
        dep_data = self.context['analysis_result']['dependencies']

        answer = {
            'question': question,
            'type': 'dependency',
            'answer': self._format_dependency_answer(dep_data),
            'details': dep_data
        }

        return answer

    def _format_dependency_answer(self, dep_data: Dict) -> str:
        """格式化依赖答案"""
        python_deps = dep_data.get('python_dependencies', {})
        nodejs_deps = dep_data.get('nodejs_dependencies', {})
        version_analysis = dep_data.get('version_analysis', {})

        answer = "📦 依赖分析：\n\n"

        if python_deps.get('found'):
            answer += f"**Python 依赖** ({python_deps.get('source', 'N/A')})\n"
            answer += f"- 总包数: {python_deps.get('total_count', 0)}\n"

            packages = python_deps.get('packages', [])
            if packages:
                answer += "\n主要依赖:\n"
                for pkg in packages[:10]:
                    answer += f"- {pkg['name']} {pkg.get('version_spec', '')}\n"

        if nodejs_deps.get('found'):
            answer += f"\n**Node.js 依赖**\n"
            answer += f"- 总包数: {nodejs_deps.get('total_count', 0)}\n"

        if version_analysis:
            answer += f"\n**版本管理**\n"
            answer += f"- 固定版本: {version_analysis.get('pinned_versions', 0)}\n"
            answer += f"- 灵活版本: {version_analysis.get('flexible_versions', 0)}\n"
            answer += f"- 未指定版本: {version_analysis.get('latest_versions', 0)}\n"

        return answer.strip()

    def _answer_score_question(self, question: str) -> Dict[str, Any]:
        """回答评分相关问题"""
        score = self.context['analysis_result']['overall_score']
        summary = self.context['analysis_result']['summary']

        answer = {
            'question': question,
            'type': 'score',
            'answer': self._format_score_answer(score, summary),
            'details': {'score': score, 'summary': summary}
        }

        return answer

    def _format_score_answer(self, score: Dict, summary: Dict) -> str:
        """格式化评分答案"""
        answer = f"""
🎯 项目评分：

**综合评分**: {score['total']}/100 ({score['grade']})

**评分细分**
"""
        for category, points in score['breakdown'].items():
            answer += f"- {category}: {points}分\n"

        if summary.get('highlights'):
            answer += "\n**✅ 亮点**\n"
            for highlight in summary['highlights']:
                answer += f"- {highlight}\n"

        if summary.get('concerns'):
            answer += "\n**⚠️ 需要关注**\n"
            for concern in summary['concerns']:
                answer += f"- {concern}\n"

        return answer.strip()

    def _answer_files_question(self, question: str) -> Dict[str, Any]:
        """回答文件列表相关问题"""
        project_data = self.context['analysis_result']['project']

        # 根据问题提取文件类型
        file_type = self._extract_file_type(question)

        if file_type:
            files = self._get_files_by_type(file_type)
            answer_text = f"项目中的 {file_type} 文件：\n\n"
            for f in files[:20]:
                answer_text += f"- {f}\n"
            if len(files) > 20:
                answer_text += f"\n... 还有 {len(files) - 20} 个文件"
        else:
            file_list = project_data['file_structure'].get('file_list', [])
            answer_text = f"项目文件列表（前20个）：\n\n"
            for f in file_list[:20]:
                answer_text += f"- {f}\n"

        answer = {
            'question': question,
            'type': 'files',
            'answer': answer_text.strip(),
            'details': {}
        }

        return answer

    def _extract_file_type(self, question: str) -> Optional[str]:
        """从问题中提取文件类型"""
        extensions = ['.py', '.js', '.ts', '.md', '.html', '.css', '.json', '.yaml', '.yml']
        for ext in extensions:
            if ext in question.lower():
                return ext
        return None

    def _get_files_by_type(self, file_type: str) -> List[str]:
        """获取指定类型的文件"""
        from src.analyzers import ProjectAnalyzer

        analyzer = ProjectAnalyzer(self.project_path)
        files = analyzer._scan_files(pattern=f"*{file_type}")
        return [str(f.relative_to(self.project_path)) for f in files]

    def _answer_improvement_question(self, question: str) -> Dict[str, Any]:
        """回答改进建议相关问题"""
        quality_data = self.context['analysis_result']['quality']
        best_practices = quality_data.get('best_practices', {})
        recommendations = best_practices.get('recommendations', [])

        answer_text = "💡 改进建议：\n\n"

        if recommendations:
            for i, rec in enumerate(recommendations, 1):
                answer_text += f"{i}. {rec}\n"
        else:
            answer_text += "项目整体状况良好，暂无重要改进建议。\n"

        # 添加基于评分的建议
        score = self.context['analysis_result']['overall_score']
        if score['total'] < 60:
            answer_text += "\n**优先改进项**\n"
            answer_text += "- 项目评分较低，建议优先关注代码质量和最佳实践\n"

        complexity = quality_data.get('complexity_analysis', {})
        if complexity.get('max_complexity', 0) > 15:
            answer_text += "- 降低高复杂度函数的复杂度\n"

        answer = {
            'question': question,
            'type': 'improvement',
            'answer': answer_text.strip(),
            'details': {'recommendations': recommendations}
        }

        return answer

    def _answer_general_question(self, question: str) -> Dict[str, Any]:
        """回答一般性问题"""
        # 提供项目概览
        summary = self.context['analysis_result']['summary']
        score = self.context['analysis_result']['overall_score']

        answer_text = f"""
关于项目 "{self.context['project_name']}" 的信息：

**项目概览**
- 评分: {score['total']}/100 ({score['grade']})
- 总文件数: {summary['key_metrics']['total_files']}
- 代码行数: {summary['key_metrics']['code_lines']}
- 函数数量: {summary['key_metrics']['total_functions']}
- 类数量: {summary['key_metrics']['total_classes']}

您可以问我：
- 项目结构如何？
- 代码质量怎么样？
- 有哪些依赖？
- 项目评分是多少？
- 有什么改进建议？
- 项目中有哪些 Python 文件？
"""

        answer = {
            'question': question,
            'type': 'general',
            'answer': answer_text.strip(),
            'details': summary
        }

        return answer

    def interactive_mode(self):
        """交互式问答模式"""
        print(f"\n{'='*60}")
        print(f"🤖 AI 项目分析助手")
        print(f"{'='*60}")
        print(f"项目: {self.context['project_name']}")
        print(f"路径: {self.context['project_path']}")
        print(f"评分: {self.context['analysis_result']['overall_score']['total']}/100")
        print(f"{'='*60}\n")
        print("💡 提示: 输入 'quit' 或 'exit' 退出\n")

        while True:
            try:
                question = input("❓ 您的问题: ").strip()

                if not question:
                    continue

                if question.lower() in ['quit', 'exit', 'q']:
                    print("\n👋 再见！")
                    break

                # 回答问题
                result = self.ask(question)

                print(f"\n💬 回答:\n")
                print(result['answer'])
                print(f"\n{'-'*60}\n")

            except KeyboardInterrupt:
                print("\n\n👋 再见！")
                break
            except Exception as e:
                print(f"\n❌ 错误: {str(e)}\n")


def main():
    """主函数"""
    import argparse

    parser = argparse.ArgumentParser(
        description='AI 驱动的项目问答 Skill',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 交互式模式
  python project_qa.py /path/to/project

  # 单个问题
  python project_qa.py /path/to/project -q "项目结构如何？"

  # JSON 输出
  python project_qa.py /path/to/project -q "代码质量怎么样？" --json
        """
    )

    parser.add_argument(
        'project_path',
        help='项目路径'
    )

    parser.add_argument(
        '-q', '--question',
        help='要问的问题（不指定则进入交互模式）'
    )

    parser.add_argument(
        '--json',
        action='store_true',
        help='以 JSON 格式输出'
    )

    args = parser.parse_args()

    # 验证项目路径
    project_path = Path(args.project_path)
    if not project_path.exists():
        print(f"❌ 错误: 项目路径不存在: {project_path}")
        return 1

    # 初始化 Skill
    skill = ProjectQASkill(project_path)

    # 单个问题模式
    if args.question:
        result = skill.ask(args.question)

        if args.json:
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            print(f"\n❓ 问题: {result['question']}\n")
            print(f"💬 回答:\n")
            print(result['answer'])

        return 0

    # 交互式模式
    skill.interactive_mode()

    return 0


if __name__ == '__main__':
    sys.exit(main())
