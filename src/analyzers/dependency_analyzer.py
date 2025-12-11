"""
依赖关系分析器

分析项目依赖、版本兼容性、安全漏洞等。
"""

from pathlib import Path
from typing import Dict, Any, List, Optional
import json
import re

from .base import BaseAnalyzer, AnalysisResult


class DependencyAnalyzer(BaseAnalyzer):
    """依赖关系分析器"""

    def analyze(self) -> AnalysisResult:
        """
        执行依赖关系分析

        Returns:
            AnalysisResult: 包含依赖信息的分析结果
        """
        try:
            # 分析 Python 依赖
            self.result.data['python_dependencies'] = self._analyze_python_dependencies()

            # 分析 Node.js 依赖
            self.result.data['nodejs_dependencies'] = self._analyze_nodejs_dependencies()

            # 检查依赖版本
            self.result.data['version_analysis'] = self._analyze_versions()

            # 生成依赖树
            self.result.data['dependency_tree'] = self._generate_dependency_tree()

        except Exception as e:
            self.result.add_error(f"依赖分析失败: {str(e)}")

        return self.result

    def _analyze_python_dependencies(self) -> Dict[str, Any]:
        """分析 Python 依赖"""
        dependencies = {
            'found': False,
            'source': None,
            'packages': [],
            'total_count': 0,
        }

        # 检查 requirements.txt
        req_file = self.project_path / 'requirements.txt'
        if req_file.exists():
            dependencies['found'] = True
            dependencies['source'] = 'requirements.txt'
            dependencies['packages'] = self._parse_requirements(req_file)
            dependencies['total_count'] = len(dependencies['packages'])

        # 检查 pyproject.toml
        elif (self.project_path / 'pyproject.toml').exists():
            dependencies['found'] = True
            dependencies['source'] = 'pyproject.toml'
            dependencies['packages'] = self._parse_pyproject()
            dependencies['total_count'] = len(dependencies['packages'])

        # 检查 setup.py
        elif (self.project_path / 'setup.py').exists():
            dependencies['found'] = True
            dependencies['source'] = 'setup.py'
            self.result.add_warning("检测到 setup.py，但需要手动解析")

        return dependencies

    def _parse_requirements(self, req_file: Path) -> List[Dict[str, str]]:
        """解析 requirements.txt"""
        packages = []

        try:
            with open(req_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()

                    # 跳过注释和空行
                    if not line or line.startswith('#'):
                        continue

                    # 解析包名和版本
                    match = re.match(r'^([a-zA-Z0-9_-]+)([>=<~!]+)?(.+)?', line)
                    if match:
                        name = match.group(1)
                        operator = match.group(2) or ''
                        version = match.group(3) or ''

                        packages.append({
                            'name': name,
                            'version_spec': f"{operator}{version}".strip(),
                            'raw': line
                        })

        except Exception as e:
            self.result.add_warning(f"无法解析 requirements.txt: {str(e)}")

        return packages

    def _parse_pyproject(self) -> List[Dict[str, str]]:
        """解析 pyproject.toml"""
        packages = []

        try:
            import tomli

            with open(self.project_path / 'pyproject.toml', 'rb') as f:
                data = tomli.load(f)

            # 提取依赖
            if 'project' in data and 'dependencies' in data['project']:
                for dep in data['project']['dependencies']:
                    match = re.match(r'^([a-zA-Z0-9_-]+)([>=<~!]+)?(.+)?', dep)
                    if match:
                        packages.append({
                            'name': match.group(1),
                            'version_spec': f"{match.group(2) or ''}{match.group(3) or ''}".strip(),
                            'raw': dep
                        })

        except ImportError:
            self.result.add_warning("需要安装 tomli 来解析 pyproject.toml")
        except Exception as e:
            self.result.add_warning(f"无法解析 pyproject.toml: {str(e)}")

        return packages

    def _analyze_nodejs_dependencies(self) -> Dict[str, Any]:
        """分析 Node.js 依赖"""
        dependencies = {
            'found': False,
            'packages': [],
            'dev_packages': [],
            'total_count': 0,
        }

        package_json = self.project_path / 'package.json'
        if not package_json.exists():
            return dependencies

        try:
            with open(package_json, 'r', encoding='utf-8') as f:
                data = json.load(f)

            dependencies['found'] = True

            # 生产依赖
            if 'dependencies' in data:
                for name, version in data['dependencies'].items():
                    dependencies['packages'].append({
                        'name': name,
                        'version': version,
                        'type': 'production'
                    })

            # 开发依赖
            if 'devDependencies' in data:
                for name, version in data['devDependencies'].items():
                    dependencies['dev_packages'].append({
                        'name': name,
                        'version': version,
                        'type': 'development'
                    })

            dependencies['total_count'] = len(dependencies['packages']) + len(dependencies['dev_packages'])

        except Exception as e:
            self.result.add_warning(f"无法解析 package.json: {str(e)}")

        return dependencies

    def _analyze_versions(self) -> Dict[str, Any]:
        """分析依赖版本"""
        analysis = {
            'pinned_versions': 0,
            'flexible_versions': 0,
            'latest_versions': 0,
            'issues': []
        }

        # 分析 Python 依赖版本
        python_deps = self.result.data.get('python_dependencies', {})
        if python_deps.get('found'):
            for pkg in python_deps.get('packages', []):
                version_spec = pkg.get('version_spec', '')

                if not version_spec:
                    analysis['latest_versions'] += 1
                elif '==' in version_spec:
                    analysis['pinned_versions'] += 1
                else:
                    analysis['flexible_versions'] += 1

                # 检查潜在问题
                if not version_spec:
                    analysis['issues'].append({
                        'package': pkg['name'],
                        'issue': '未指定版本，可能导致不稳定',
                        'recommendation': '建议固定版本号'
                    })

        return analysis

    def _generate_dependency_tree(self) -> List[str]:
        """生成依赖树"""
        tree = []

        # Python 依赖树
        python_deps = self.result.data.get('python_dependencies', {})
        if python_deps.get('found'):
            tree.append("Python Dependencies:")
            for pkg in python_deps.get('packages', [])[:20]:  # 限制显示数量
                tree.append(f"  ├── {pkg['name']} {pkg.get('version_spec', '')}")

        # Node.js 依赖树
        nodejs_deps = self.result.data.get('nodejs_dependencies', {})
        if nodejs_deps.get('found'):
            tree.append("\nNode.js Dependencies:")
            for pkg in nodejs_deps.get('packages', [])[:20]:
                tree.append(f"  ├── {pkg['name']}@{pkg['version']}")

        return tree if tree else ["未找到依赖信息"]
