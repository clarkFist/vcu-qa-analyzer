#!/usr/bin/env python3
"""
AI 驱动的智能代码洞察 Skill

功能：
1. 深度代码分析
2. 架构模式识别
3. 潜在问题检测
4. 重构建议
"""

import sys
import ast
import json
from pathlib import Path
from typing import Dict, Any, List, Set
from collections import defaultdict

# 添加父目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.analyzers.base import BaseAnalyzer


class CodeInsightSkill:
    """智能代码洞察 Skill"""

    def __init__(self, project_path: Path):
        """初始化 Skill"""
        self.project_path = Path(project_path)
        self.insights = {}
        self._analyze_code()

    def _analyze_code(self):
        """深度代码分析"""
        print("🔍 正在进行深度代码分析...")

        # 使用 ProjectAnalyzer 来扫描文件
        from src.analyzers import ProjectAnalyzer
        analyzer = ProjectAnalyzer(self.project_path)
        python_files = analyzer._scan_files(pattern="*.py")

        self.insights = {
            'architecture_patterns': self._detect_architecture_patterns(python_files),
            'code_smells': self._detect_code_smells(python_files),
            'import_graph': self._build_import_graph(python_files),
            'function_analysis': self._analyze_functions(python_files),
            'class_hierarchy': self._analyze_class_hierarchy(python_files),
        }

        print("✅ 深度分析完成\n")

    def _detect_architecture_patterns(self, python_files: List[Path]) -> Dict[str, Any]:
        """检测架构模式"""
        patterns = {
            'mvc': False,
            'mvvm': False,
            'layered': False,
            'microservices': False,
            'detected_patterns': []
        }

        # 检查目录结构
        dirs = set()
        for file in python_files:
            parts = file.relative_to(self.project_path).parts
            if len(parts) > 1:
                dirs.add(parts[0])

        # MVC 模式检测
        mvc_keywords = {'models', 'views', 'controllers'}
        if mvc_keywords.issubset(dirs):
            patterns['mvc'] = True
            patterns['detected_patterns'].append('MVC (Model-View-Controller)')

        # 分层架构检测
        layered_keywords = {'api', 'service', 'repository', 'domain'}
        if len(layered_keywords.intersection(dirs)) >= 2:
            patterns['layered'] = True
            patterns['detected_patterns'].append('Layered Architecture')

        # 微服务检测
        if 'services' in dirs or 'microservices' in dirs:
            patterns['microservices'] = True
            patterns['detected_patterns'].append('Microservices')

        return patterns

    def _detect_code_smells(self, python_files: List[Path]) -> List[Dict[str, Any]]:
        """检测代码异味"""
        smells = []

        for file_path in python_files[:20]:  # 限制分析文件数
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                tree = ast.parse(content)
                relative_path = str(file_path.relative_to(self.project_path))

                # 检测长方法
                for node in ast.walk(tree):
                    if isinstance(node, ast.FunctionDef):
                        if hasattr(node, 'end_lineno') and hasattr(node, 'lineno'):
                            length = node.end_lineno - node.lineno
                            if length > 50:
                                smells.append({
                                    'type': 'Long Method',
                                    'severity': 'medium',
                                    'file': relative_path,
                                    'function': node.name,
                                    'line': node.lineno,
                                    'description': f'函数过长 ({length} 行)',
                                    'suggestion': '考虑将函数拆分为更小的函数'
                                })

                        # 检测参数过多
                        param_count = len(node.args.args)
                        if param_count > 5:
                            smells.append({
                                'type': 'Too Many Parameters',
                                'severity': 'low',
                                'file': relative_path,
                                'function': node.name,
                                'line': node.lineno,
                                'description': f'参数过多 ({param_count} 个)',
                                'suggestion': '考虑使用参数对象或配置类'
                            })

                    # 检测大类
                    if isinstance(node, ast.ClassDef):
                        methods = [n for n in node.body if isinstance(n, ast.FunctionDef)]
                        if len(methods) > 20:
                            smells.append({
                                'type': 'Large Class',
                                'severity': 'high',
                                'file': relative_path,
                                'class': node.name,
                                'line': node.lineno,
                                'description': f'类过大 ({len(methods)} 个方法)',
                                'suggestion': '考虑拆分类或使用组合模式'
                            })

            except Exception:
                pass

        return smells

    def _build_import_graph(self, python_files: List[Path]) -> Dict[str, List[str]]:
        """构建导入依赖图"""
        import_graph = defaultdict(list)

        for file_path in python_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                tree = ast.parse(content)
                relative_path = str(file_path.relative_to(self.project_path))

                for node in ast.walk(tree):
                    if isinstance(node, ast.Import):
                        for alias in node.names:
                            import_graph[relative_path].append(alias.name)
                    elif isinstance(node, ast.ImportFrom):
                        if node.module:
                            import_graph[relative_path].append(node.module)

            except Exception:
                pass

        return dict(import_graph)

    def _analyze_functions(self, python_files: List[Path]) -> Dict[str, Any]:
        """分析函数特征"""
        analysis = {
            'total_functions': 0,
            'recursive_functions': [],
            'generator_functions': [],
            'async_functions': [],
            'decorators_used': defaultdict(int),
        }

        for file_path in python_files[:20]:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                tree = ast.parse(content)
                relative_path = str(file_path.relative_to(self.project_path))

                for node in ast.walk(tree):
                    if isinstance(node, ast.FunctionDef):
                        analysis['total_functions'] += 1

                        # 检测递归
                        if self._is_recursive(node):
                            analysis['recursive_functions'].append({
                                'file': relative_path,
                                'function': node.name,
                                'line': node.lineno
                            })

                        # 检测生成器
                        if any(isinstance(n, ast.Yield) for n in ast.walk(node)):
                            analysis['generator_functions'].append({
                                'file': relative_path,
                                'function': node.name,
                                'line': node.lineno
                            })

                        # 检测装饰器
                        for decorator in node.decorator_list:
                            if isinstance(decorator, ast.Name):
                                analysis['decorators_used'][decorator.id] += 1

                    # 检测异步函数
                    if isinstance(node, ast.AsyncFunctionDef):
                        analysis['async_functions'].append({
                            'file': relative_path,
                            'function': node.name,
                            'line': node.lineno
                        })

            except Exception:
                pass

        analysis['decorators_used'] = dict(analysis['decorators_used'])
        return analysis

    def _is_recursive(self, func_node: ast.FunctionDef) -> bool:
        """检测函数是否递归"""
        func_name = func_node.name
        for node in ast.walk(func_node):
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name) and node.func.id == func_name:
                    return True
        return False

    def _analyze_class_hierarchy(self, python_files: List[Path]) -> Dict[str, Any]:
        """分析类继承层次"""
        hierarchy = {
            'total_classes': 0,
            'inheritance_depth': {},
            'abstract_classes': [],
            'dataclasses': [],
        }

        for file_path in python_files[:20]:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                tree = ast.parse(content)
                relative_path = str(file_path.relative_to(self.project_path))

                for node in ast.walk(tree):
                    if isinstance(node, ast.ClassDef):
                        hierarchy['total_classes'] += 1

                        # 检测继承
                        if node.bases:
                            base_names = []
                            for base in node.bases:
                                if isinstance(base, ast.Name):
                                    base_names.append(base.id)
                            hierarchy['inheritance_depth'][node.name] = base_names

                        # 检测抽象类
                        for decorator in node.decorator_list:
                            if isinstance(decorator, ast.Name):
                                if decorator.id in ['abstractmethod', 'ABC']:
                                    hierarchy['abstract_classes'].append({
                                        'file': relative_path,
                                        'class': node.name,
                                        'line': node.lineno
                                    })

                        # 检测 dataclass
                        for decorator in node.decorator_list:
                            if isinstance(decorator, ast.Name) and decorator.id == 'dataclass':
                                hierarchy['dataclasses'].append({
                                    'file': relative_path,
                                    'class': node.name,
                                    'line': node.lineno
                                })

            except Exception:
                pass

        return hierarchy

    def get_insights(self, category: str = 'all') -> Dict[str, Any]:
        """获取洞察"""
        if category == 'all':
            return self.insights
        return self.insights.get(category, {})

    def format_insights(self) -> str:
        """格式化洞察为可读文本"""
        output = []

        # 架构模式
        output.append("🏗️  架构模式分析")
        output.append("=" * 60)
        patterns = self.insights['architecture_patterns']
        if patterns['detected_patterns']:
            output.append("检测到的模式:")
            for pattern in patterns['detected_patterns']:
                output.append(f"  ✓ {pattern}")
        else:
            output.append("  未检测到明显的架构模式")
        output.append("")

        # 代码异味
        output.append("👃 代码异味检测")
        output.append("=" * 60)
        smells = self.insights['code_smells']
        if smells:
            output.append(f"发现 {len(smells)} 个潜在问题:\n")
            for smell in smells[:10]:
                output.append(f"  [{smell['severity'].upper()}] {smell['type']}")
                output.append(f"  文件: {smell['file']}")
                output.append(f"  位置: 第 {smell['line']} 行")
                output.append(f"  描述: {smell['description']}")
                output.append(f"  建议: {smell['suggestion']}")
                output.append("")
        else:
            output.append("  未发现明显的代码异味")
        output.append("")

        # 函数分析
        output.append("⚙️  函数特征分析")
        output.append("=" * 60)
        func_analysis = self.insights['function_analysis']
        output.append(f"总函数数: {func_analysis['total_functions']}")
        output.append(f"递归函数: {len(func_analysis['recursive_functions'])}")
        output.append(f"生成器函数: {len(func_analysis['generator_functions'])}")
        output.append(f"异步函数: {len(func_analysis['async_functions'])}")

        if func_analysis['decorators_used']:
            output.append("\n常用装饰器:")
            for decorator, count in sorted(
                func_analysis['decorators_used'].items(),
                key=lambda x: x[1],
                reverse=True
            )[:5]:
                output.append(f"  - @{decorator}: {count} 次")
        output.append("")

        # 类层次
        output.append("🏛️  类层次分析")
        output.append("=" * 60)
        class_hierarchy = self.insights['class_hierarchy']
        output.append(f"总类数: {class_hierarchy['total_classes']}")
        output.append(f"抽象类: {len(class_hierarchy['abstract_classes'])}")
        output.append(f"数据类: {len(class_hierarchy['dataclasses'])}")

        if class_hierarchy['inheritance_depth']:
            output.append(f"\n继承关系: {len(class_hierarchy['inheritance_depth'])} 个类有继承")

        return "\n".join(output)


def main():
    """主函数"""
    import argparse

    parser = argparse.ArgumentParser(
        description='AI 驱动的智能代码洞察 Skill'
    )

    parser.add_argument(
        'project_path',
        help='项目路径'
    )

    parser.add_argument(
        '-c', '--category',
        choices=['all', 'architecture_patterns', 'code_smells', 'import_graph', 'function_analysis', 'class_hierarchy'],
        default='all',
        help='洞察类别'
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
    skill = CodeInsightSkill(project_path)

    # 获取洞察
    insights = skill.get_insights(args.category)

    if args.json:
        print(json.dumps(insights, indent=2, ensure_ascii=False))
    else:
        print(skill.format_insights())

    return 0


if __name__ == '__main__':
    sys.exit(main())
