"""
项目结构分析器

分析项目的文件结构、代码统计、文件类型分布等信息。
"""

from pathlib import Path
from typing import Dict, Any, List
from collections import defaultdict
import json

from .base import BaseAnalyzer, AnalysisResult


class ProjectAnalyzer(BaseAnalyzer):
    """项目结构分析器"""

    def analyze(self) -> AnalysisResult:
        """
        执行项目结构分析

        Returns:
            AnalysisResult: 包含项目结构信息的分析结果
        """
        try:
            # 收集项目基本信息
            self.result.data['project_info'] = self._collect_project_info()

            # 分析文件结构
            self.result.data['file_structure'] = self._analyze_file_structure()

            # 统计代码行数
            self.result.data['code_statistics'] = self._collect_code_statistics()

            # 分析文件类型分布
            self.result.data['file_type_distribution'] = self._analyze_file_types()

            # 生成目录树
            self.result.data['directory_tree'] = self._generate_directory_tree()

        except Exception as e:
            self.result.add_error(f"项目分析失败: {str(e)}")

        return self.result

    def _collect_project_info(self) -> Dict[str, Any]:
        """收集项目基本信息"""
        info = {
            'name': self.project_path.name,
            'path': str(self.project_path.absolute()),
            'size': self._calculate_project_size(),
        }

        # 检查是否为 Git 仓库
        if (self.project_path / '.git').exists():
            info['is_git_repo'] = True
            info['git_info'] = self._get_git_info()
        else:
            info['is_git_repo'] = False

        # 检查项目类型
        info['project_type'] = self._detect_project_type()

        return info

    def _calculate_project_size(self) -> str:
        """计算项目总大小"""
        total_size = 0
        for file_path in self._scan_files():
            try:
                total_size += file_path.stat().st_size
            except Exception:
                pass
        return self._format_size(total_size)

    def _get_git_info(self) -> Dict[str, str]:
        """获取 Git 仓库信息"""
        git_info = {}
        try:
            import subprocess

            # 获取当前分支
            result = subprocess.run(
                ['git', 'branch', '--show-current'],
                cwd=self.project_path,
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                git_info['current_branch'] = result.stdout.strip()

            # 获取最后一次提交
            result = subprocess.run(
                ['git', 'log', '-1', '--format=%H|%an|%ad|%s'],
                cwd=self.project_path,
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                parts = result.stdout.strip().split('|')
                if len(parts) == 4:
                    git_info['last_commit'] = {
                        'hash': parts[0][:8],
                        'author': parts[1],
                        'date': parts[2],
                        'message': parts[3]
                    }
        except Exception as e:
            self.result.add_warning(f"无法获取 Git 信息: {str(e)}")

        return git_info

    def _detect_project_type(self) -> List[str]:
        """检测项目类型"""
        project_types = []

        # Python 项目
        if (self.project_path / 'setup.py').exists() or \
           (self.project_path / 'pyproject.toml').exists() or \
           (self.project_path / 'requirements.txt').exists():
            project_types.append('Python')

        # Node.js 项目
        if (self.project_path / 'package.json').exists():
            project_types.append('Node.js')

        # Markdown 文档项目
        md_files = list(self.project_path.glob('*.md'))
        if len(md_files) > 3:
            project_types.append('Documentation')

        return project_types if project_types else ['Unknown']

    def _analyze_file_structure(self) -> Dict[str, Any]:
        """分析文件结构"""
        all_files = self._scan_files()

        return {
            'total_files': len(all_files),
            'total_directories': len(list(self.project_path.rglob('*'))),
            'file_list': [str(f.relative_to(self.project_path)) for f in all_files[:100]],
        }

    def _collect_code_statistics(self) -> Dict[str, Any]:
        """收集代码统计信息"""
        stats = {
            'total_lines': 0,
            'code_lines': 0,
            'comment_lines': 0,
            'blank_lines': 0,
            'by_extension': defaultdict(lambda: {
                'files': 0,
                'total_lines': 0,
                'code_lines': 0
            })
        }

        # 只统计代码文件
        code_extensions = ['.py', '.js', '.ts', '.jsx', '.tsx', '.java', '.cpp', '.c', '.h']
        code_files = [f for f in self._scan_files() if f.suffix in code_extensions]

        for file_path in code_files:
            line_counts = self._count_lines(file_path)
            ext = self._get_file_extension(file_path)

            stats['total_lines'] += line_counts['total']
            stats['code_lines'] += line_counts['code']
            stats['comment_lines'] += line_counts['comment']
            stats['blank_lines'] += line_counts['blank']

            stats['by_extension'][ext]['files'] += 1
            stats['by_extension'][ext]['total_lines'] += line_counts['total']
            stats['by_extension'][ext]['code_lines'] += line_counts['code']

        # 转换 defaultdict 为普通 dict
        stats['by_extension'] = dict(stats['by_extension'])

        return stats

    def _analyze_file_types(self) -> Dict[str, int]:
        """分析文件类型分布"""
        type_counts = defaultdict(int)

        for file_path in self._scan_files():
            ext = self._get_file_extension(file_path)
            if ext:
                type_counts[ext] += 1
            else:
                type_counts['no_extension'] += 1

        # 按数量排序
        sorted_types = dict(sorted(
            type_counts.items(),
            key=lambda x: x[1],
            reverse=True
        ))

        return sorted_types

    def _generate_directory_tree(self, max_depth: int = 3) -> List[str]:
        """
        生成目录树结构

        Args:
            max_depth: 最大深度

        Returns:
            List[str]: 目录树的每一行
        """
        tree_lines = []

        def add_tree_line(path: Path, prefix: str = "", depth: int = 0):
            if depth > max_depth:
                return

            # 排除的目录
            exclude_dirs = {
                '__pycache__', '.git', '.venv', 'venv',
                'node_modules', '.pytest_cache', '.mypy_cache',
                'dist', 'build'
            }

            if path.name in exclude_dirs:
                return

            # 添加当前项
            if depth > 0:
                tree_lines.append(f"{prefix}├── {path.name}")

            # 如果是目录，递归处理子项
            if path.is_dir():
                try:
                    children = sorted(path.iterdir(), key=lambda x: (not x.is_dir(), x.name))
                    for i, child in enumerate(children):
                        is_last = i == len(children) - 1
                        new_prefix = prefix + ("    " if is_last else "│   ")
                        add_tree_line(child, new_prefix, depth + 1)
                except PermissionError:
                    pass

        tree_lines.append(self.project_path.name)
        add_tree_line(self.project_path)

        return tree_lines[:100]  # 限制行数
