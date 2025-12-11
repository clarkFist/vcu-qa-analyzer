"""
代码质量分析器

分析代码复杂度、潜在问题、代码风格等质量指标。
"""

from pathlib import Path
from typing import Dict, Any, List
import ast
import re

from .base import BaseAnalyzer, AnalysisResult


class CodeQualityAnalyzer(BaseAnalyzer):
    """代码质量分析器"""

    def analyze(self) -> AnalysisResult:
        """
        执行代码质量分析

        Returns:
            AnalysisResult: 包含代码质量信息的分析结果
        """
        try:
            # 分析 Python 代码
            python_files = self._scan_files(pattern="*.py")
            if python_files:
                self.result.data['python_analysis'] = self._analyze_python_code(python_files)

            # 代码风格检查
            self.result.data['style_issues'] = self._check_code_style(python_files)

            # 复杂度分析
            self.result.data['complexity_analysis'] = self._analyze_complexity(python_files)

            # 最佳实践检查
            self.result.data['best_practices'] = self._check_best_practices()

        except Exception as e:
            self.result.add_error(f"代码质量分析失败: {str(e)}")

        return self.result

    def _analyze_python_code(self, python_files: List[Path]) -> Dict[str, Any]:
        """分析 Python 代码"""
        analysis = {
            'total_files': len(python_files),
            'total_functions': 0,
            'total_classes': 0,
            'average_function_length': 0,
            'files_with_issues': [],
        }

        total_function_lines = 0

        for file_path in python_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                tree = ast.parse(content)

                # 统计函数和类
                functions = [node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
                classes = [node for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]

                analysis['total_functions'] += len(functions)
                analysis['total_classes'] += len(classes)

                # 计算函数长度
                for func in functions:
                    if hasattr(func, 'end_lineno') and hasattr(func, 'lineno'):
                        func_length = func.end_lineno - func.lineno
                        total_function_lines += func_length

                        # 检查过长的函数
                        if func_length > 50:
                            analysis['files_with_issues'].append({
                                'file': str(file_path.relative_to(self.project_path)),
                                'issue': f"函数 '{func.name}' 过长 ({func_length} 行)",
                                'line': func.lineno
                            })

            except SyntaxError as e:
                self.result.add_warning(f"语法错误 {file_path}: {str(e)}")
            except Exception as e:
                self.result.add_warning(f"无法分析 {file_path}: {str(e)}")

        # 计算平均函数长度
        if analysis['total_functions'] > 0:
            analysis['average_function_length'] = round(
                total_function_lines / analysis['total_functions'], 2
            )

        return analysis

    def _check_code_style(self, python_files: List[Path]) -> Dict[str, Any]:
        """检查代码风格"""
        issues = {
            'total_issues': 0,
            'by_type': {
                'long_lines': 0,
                'missing_docstrings': 0,
                'naming_issues': 0,
            },
            'details': []
        }

        for file_path in python_files[:20]:  # 限制检查文件数
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()

                for i, line in enumerate(lines, 1):
                    # 检查行长度
                    if len(line.rstrip()) > 100:
                        issues['by_type']['long_lines'] += 1
                        issues['total_issues'] += 1

                # 检查是否有文档字符串
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                try:
                    tree = ast.parse(content)
                    for node in ast.walk(tree):
                        if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                            if not ast.get_docstring(node):
                                issues['by_type']['missing_docstrings'] += 1
                                issues['total_issues'] += 1
                except:
                    pass

            except Exception as e:
                self.result.add_warning(f"无法检查 {file_path}: {str(e)}")

        return issues

    def _analyze_complexity(self, python_files: List[Path]) -> Dict[str, Any]:
        """分析代码复杂度"""
        complexity = {
            'high_complexity_functions': [],
            'average_complexity': 0,
            'max_complexity': 0,
        }

        total_complexity = 0
        function_count = 0

        for file_path in python_files[:20]:  # 限制分析文件数
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                tree = ast.parse(content)

                for node in ast.walk(tree):
                    if isinstance(node, ast.FunctionDef):
                        func_complexity = self._calculate_cyclomatic_complexity(node)
                        total_complexity += func_complexity
                        function_count += 1

                        if func_complexity > complexity['max_complexity']:
                            complexity['max_complexity'] = func_complexity

                        if func_complexity > 10:
                            complexity['high_complexity_functions'].append({
                                'file': str(file_path.relative_to(self.project_path)),
                                'function': node.name,
                                'complexity': func_complexity,
                                'line': node.lineno
                            })

            except Exception as e:
                self.result.add_warning(f"无法分析复杂度 {file_path}: {str(e)}")

        if function_count > 0:
            complexity['average_complexity'] = round(total_complexity / function_count, 2)

        return complexity

    def _calculate_cyclomatic_complexity(self, node: ast.FunctionDef) -> int:
        """
        计算圈复杂度

        Args:
            node: AST 函数节点

        Returns:
            int: 圈复杂度值
        """
        complexity = 1  # 基础复杂度

        for child in ast.walk(node):
            # 条件语句增加复杂度
            if isinstance(child, (ast.If, ast.While, ast.For, ast.ExceptHandler)):
                complexity += 1
            # 布尔运算符增加复杂度
            elif isinstance(child, ast.BoolOp):
                complexity += len(child.values) - 1
            # 列表推导式增加复杂度
            elif isinstance(child, (ast.ListComp, ast.DictComp, ast.SetComp)):
                complexity += 1

        return complexity

    def _check_best_practices(self) -> Dict[str, Any]:
        """检查最佳实践"""
        practices = {
            'has_tests': False,
            'has_readme': False,
            'has_requirements': False,
            'has_gitignore': False,
            'has_license': False,
            'recommendations': []
        }

        # 检查测试目录
        if (self.project_path / 'tests').exists() or \
           (self.project_path / 'test').exists():
            practices['has_tests'] = True
        else:
            practices['recommendations'].append("建议添加测试目录和测试用例")

        # 检查 README
        readme_files = list(self.project_path.glob('README*'))
        if readme_files:
            practices['has_readme'] = True
        else:
            practices['recommendations'].append("建议添加 README 文档")

        # 检查依赖文件
        if (self.project_path / 'requirements.txt').exists() or \
           (self.project_path / 'pyproject.toml').exists():
            practices['has_requirements'] = True
        else:
            practices['recommendations'].append("建议添加依赖管理文件")

        # 检查 .gitignore
        if (self.project_path / '.gitignore').exists():
            practices['has_gitignore'] = True
        else:
            practices['recommendations'].append("建议添加 .gitignore 文件")

        # 检查 LICENSE
        license_files = list(self.project_path.glob('LICENSE*'))
        if license_files:
            practices['has_license'] = True
        else:
            practices['recommendations'].append("建议添加开源许可证")

        return practices
