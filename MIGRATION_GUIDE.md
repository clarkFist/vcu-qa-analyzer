# 项目迁移指南

本指南说明如何将 `analyzers` 模块应用到其他项目，或如何分析其他项目。

## 目录

1. [直接使用（无需迁移）](#直接使用无需迁移)
2. [复制模块到其他项目](#复制模块到其他项目)
3. [作为独立工具安装](#作为独立工具安装)
4. [集成到现有项目](#集成到现有项目)

---

## 直接使用（无需迁移）

### 方式 1: 命令行分析任何项目

```bash
# 在当前项目目录下，分析任何其他项目
cd /path/to/error_report

# 分析目标项目
python analyze_project.py /path/to/target/project -o target_analysis

# 示例
python analyze_project.py ~/projects/my-web-app -o ~/reports/webapp_analysis
python analyze_project.py ~/work/backend-api -o ~/reports/api_analysis -f html
```

### 方式 2: Python 脚本批量分析

创建一个脚本来分析多个项目：

```python
#!/usr/bin/env python3
# batch_analyze.py

import sys
from pathlib import Path

# 添加 error_report 到 Python 路径
sys.path.insert(0, '/path/to/error_report')

from src.analyzers import ReportGenerator

# 要分析的项目列表
projects = [
    Path('~/projects/project1'),
    Path('~/projects/project2'),
    Path('~/projects/project3'),
]

output_dir = Path('~/reports')
output_dir.mkdir(exist_ok=True)

for project_path in projects:
    project_path = project_path.expanduser()
    if not project_path.exists():
        print(f"⚠️  跳过不存在的项目: {project_path}")
        continue

    print(f"📊 分析项目: {project_path.name}")

    try:
        generator = ReportGenerator(project_path)
        output_files = generator.generate_report(
            output_path=output_dir / f"{project_path.name}_analysis",
            format='html'
        )
        print(f"✅ 完成: {output_files['html']}\n")
    except Exception as e:
        print(f"❌ 失败: {e}\n")
```

---

## 复制模块到其他项目

### 步骤 1: 复制必要文件

```bash
# 目标项目目录
TARGET_PROJECT="/path/to/your/project"

# 复制分析器模块
cp -r src/analyzers "$TARGET_PROJECT/src/"

# 复制命令行工具
cp analyze_project.py "$TARGET_PROJECT/"

# 复制依赖的核心模块（如果需要 HTML 报告）
cp -r src/core "$TARGET_PROJECT/src/"
cp -r src/themes "$TARGET_PROJECT/src/"
cp -r src/processors "$TARGET_PROJECT/src/"
```

### 步骤 2: 安装依赖

在目标项目中添加依赖到 `requirements.txt`：

```txt
# 分析器依赖
markdown>=3.4.0
Pygments>=2.15.0

# 如果需要解析 pyproject.toml
tomli>=2.0.0; python_version < '3.11'
```

安装依赖：

```bash
cd "$TARGET_PROJECT"
pip install -r requirements.txt
```

### 步骤 3: 使用

```bash
cd "$TARGET_PROJECT"

# 分析当前项目
python analyze_project.py

# 分析其他项目
python analyze_project.py /path/to/another/project
```

---

## 作为独立工具安装

### 方式 1: 创建可执行脚本

```bash
# 1. 创建全局脚本目录
mkdir -p ~/.local/bin

# 2. 创建包装脚本
cat > ~/.local/bin/analyze-project << 'EOF'
#!/bin/bash
ANALYZER_PATH="/path/to/error_report"
cd "$ANALYZER_PATH"
python analyze_project.py "$@"
EOF

# 3. 添加执行权限
chmod +x ~/.local/bin/analyze-project

# 4. 确保 ~/.local/bin 在 PATH 中
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc

# 5. 现在可以在任何地方使用
analyze-project ~/projects/my-app -o ~/reports/my-app-analysis
```

### 方式 2: 创建 Python 包

```bash
# 1. 在 error_report 项目中创建 setup.py
cat > setup.py << 'EOF'
from setuptools import setup, find_packages

setup(
    name='project-analyzer',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'markdown>=3.4.0',
        'Pygments>=2.15.0',
    ],
    entry_points={
        'console_scripts': [
            'analyze-project=analyze_project:main',
        ],
    },
)
EOF

# 2. 安装到系统
pip install -e .

# 3. 现在可以在任何地方使用
analyze-project ~/projects/my-app
```

---

## 集成到现有项目

### 场景 1: 作为 Git Submodule

```bash
# 在目标项目中
cd /path/to/your/project

# 添加为 submodule
git submodule add https://github.com/your/error_report.git tools/analyzer

# 使用
python tools/analyzer/analyze_project.py . -o reports/analysis
```

### 场景 2: 集成到项目的 Makefile

```makefile
# Makefile

.PHONY: analyze
analyze:
	@echo "📊 分析项目..."
	python /path/to/error_report/analyze_project.py . -o reports/analysis -f html
	@echo "✅ 报告已生成: reports/analysis.html"

.PHONY: analyze-verbose
analyze-verbose:
	python /path/to/error_report/analyze_project.py . -o reports/analysis -f both -v
```

使用：

```bash
make analyze
```

### 场景 3: 集成到 Python 项目

在您的项目中创建分析脚本：

```python
# scripts/analyze.py

import sys
from pathlib import Path

# 添加 analyzer 路径
ANALYZER_PATH = Path('/path/to/error_report')
sys.path.insert(0, str(ANALYZER_PATH))

from src.analyzers import (
    ProjectAnalyzer,
    CodeQualityAnalyzer,
    DependencyAnalyzer,
    ReportGenerator
)

def main():
    project_path = Path(__file__).parent.parent

    print(f"📊 分析项目: {project_path.name}")

    # 生成报告
    generator = ReportGenerator(project_path)
    output_files = generator.generate_report(
        output_path=project_path / 'reports' / 'analysis',
        format='html'
    )

    print(f"✅ 报告已生成: {output_files['html']}")

    # 检查评分
    from src.analyzers import MetricsCollector
    collector = MetricsCollector(project_path)
    result = collector.analyze()
    score = result.data['overall_score']

    print(f"\n📈 项目评分: {score['total']}/100 ({score['grade']})")

    # 如果评分过低，返回错误码
    if score['total'] < 60:
        print("⚠️  项目质量需要改进")
        return 1

    return 0

if __name__ == '__main__':
    sys.exit(main())
```

---

## 配置不同项目类型

### Python 项目

默认配置已优化，无需修改。

### JavaScript/TypeScript 项目

修改 `src/analyzers/project_analyzer.py`：

```python
# 在 _collect_code_statistics 方法中
code_extensions = ['.js', '.ts', '.jsx', '.tsx', '.vue']
```

### Java 项目

```python
code_extensions = ['.java', '.kt', '.scala']
```

### C/C++ 项目

```python
code_extensions = ['.c', '.cpp', '.h', '.hpp', '.cc']
```

### 多语言项目

```python
code_extensions = [
    '.py', '.js', '.ts', '.jsx', '.tsx',
    '.java', '.c', '.cpp', '.h',
    '.go', '.rs', '.rb', '.php'
]
```

---

## 自定义分析规则

### 修改评分权重

编辑 `src/analyzers/metrics_collector.py`：

```python
def _calculate_overall_score(self) -> Dict[str, Any]:
    # 修改权重
    structure_weight = 20  # 原 30
    quality_weight = 50    # 原 40
    practices_weight = 30  # 原 30

    # ... 其余代码
```

### 添加自定义检查

创建自定义分析器：

```python
# src/analyzers/custom_analyzer.py

from .base import BaseAnalyzer, AnalysisResult

class CustomAnalyzer(BaseAnalyzer):
    def analyze(self) -> AnalysisResult:
        # 您的自定义检查逻辑
        self.result.data['custom_metric'] = self._check_custom_rules()
        return self.result

    def _check_custom_rules(self):
        # 实现自定义规则
        return {"status": "ok"}
```

在 `metrics_collector.py` 中注册：

```python
from .custom_analyzer import CustomAnalyzer

class MetricsCollector(BaseAnalyzer):
    def analyze(self) -> AnalysisResult:
        # ... 现有代码 ...

        # 添加自定义分析
        custom_result = CustomAnalyzer(self.project_path).analyze()
        self.result.data['custom'] = custom_result.data

        return self.result
```

---

## CI/CD 集成示例

### GitHub Actions

```yaml
# .github/workflows/analyze.yml
name: Project Analysis

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  analyze:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v3

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'

    - name: Clone analyzer
      run: |
        git clone https://github.com/your/error_report.git /tmp/analyzer

    - name: Install dependencies
      run: |
        pip install -r /tmp/analyzer/requirements.txt

    - name: Run analysis
      run: |
        python /tmp/analyzer/analyze_project.py . -o analysis_report -f html

    - name: Upload report
      uses: actions/upload-artifact@v3
      with:
        name: analysis-report
        path: analysis_report.html

    - name: Check quality score
      run: |
        SCORE=$(grep "综合评分" analysis_report.md | grep -oE '[0-9]+' | head -1)
        echo "Project score: $SCORE/100"
        if [ "$SCORE" -lt 60 ]; then
          echo "::error::Project quality score is too low ($SCORE/100)"
          exit 1
        fi
```

### GitLab CI

```yaml
# .gitlab-ci.yml
stages:
  - analyze

project_analysis:
  stage: analyze
  image: python:3.9
  before_script:
    - git clone https://github.com/your/error_report.git /tmp/analyzer
    - pip install -r /tmp/analyzer/requirements.txt
  script:
    - python /tmp/analyzer/analyze_project.py . -o analysis_report -f html
  artifacts:
    paths:
      - analysis_report.html
    expire_in: 1 week
  only:
    - main
    - develop
```

---

## 常见问题

### Q: 如何分析远程 Git 仓库？

```bash
# 克隆仓库
git clone https://github.com/user/repo.git /tmp/repo

# 分析
python analyze_project.py /tmp/repo -o repo_analysis

# 清理
rm -rf /tmp/repo
```

### Q: 如何排除特定目录？

修改 `src/analyzers/base.py` 中的 `_scan_files` 方法：

```python
exclude_dirs = [
    '__pycache__', '.git', '.venv', 'venv',
    'node_modules', '.pytest_cache', '.mypy_cache',
    'dist', 'build', '*.egg-info',
    'your_custom_dir',  # 添加自定义排除
]
```

### Q: 如何只分析特定文件类型？

```python
# 在 ProjectAnalyzer 中
python_files = self._scan_files(pattern="*.py")
js_files = self._scan_files(pattern="*.js")
```

### Q: 分析大型项目很慢怎么办？

1. 增加排除目录
2. 限制分析文件数量（修改代码中的切片 `[:20]`）
3. 使用 SSD 存储
4. 考虑实现多进程并行分析

---

## 最佳实践

1. **定期分析**: 设置定时任务每周生成报告
2. **版本对比**: 保存历史报告，对比趋势
3. **质量门禁**: 在 CI/CD 中设置最低评分要求
4. **团队共享**: 将报告发布到内部文档站点
5. **持续改进**: 根据报告建议逐步优化代码

---

**最后更新**: 2025-12-11
