# 使用示例

本文档提供 VCU QA Document Generator 的常见使用场景和示例。

## 目录

1. [Markdown 转 HTML](#markdown-转-html)
2. [项目分析报告](#项目分析报告)
3. [批量转换](#批量转换)
4. [自定义主题](#自定义主题)
5. [集成到 CI/CD](#集成到-cicd)

---

## Markdown 转 HTML

### 基本转换

```bash
# 转换单个文件
python md2html.py report.md

# 指定输出路径
python md2html.py report.md -o output/report.html

# 使用特定主题
python md2html.py report.md -t professional
```

### 高级选项

```bash
# 嵌入图片为 Base64
python md2html.py report.md --embed-images

# 处理 Mermaid 图表
python md2html.py report.md --mermaid

# 组合使用
python md2html.py report.md -t minimal --embed-images --mermaid -o final_report.html
```

### 交互式模式

```bash
# 启动交互式界面
python md2html.py

# 按照提示选择：
# 1. 选择 Markdown 文件
# 2. 选择主题
# 3. 配置选项
# 4. 生成报告
```

---

## 项目分析报告

### 快速分析

```bash
# 分析当前项目
python analyze_project.py

# 分析指定项目
python analyze_project.py /path/to/project

# 生成 HTML 报告
python analyze_project.py -f html -o project_analysis
```

### 详细分析

```bash
# 生成完整报告（Markdown + HTML）
python analyze_project.py -f both -o reports/full_analysis

# 查看详细错误信息
python analyze_project.py -v
```

### Python API 使用

```python
from pathlib import Path
from src.analyzers import (
    ProjectAnalyzer,
    CodeQualityAnalyzer,
    DependencyAnalyzer,
    MetricsCollector,
    ReportGenerator
)

# 1. 单独使用各个分析器
project_path = Path('/path/to/project')

# 项目结构分析
project_analyzer = ProjectAnalyzer(project_path)
project_result = project_analyzer.analyze()
print(f"总文件数: {project_result.data['file_structure']['total_files']}")

# 代码质量分析
quality_analyzer = CodeQualityAnalyzer(project_path)
quality_result = quality_analyzer.analyze()
print(f"平均复杂度: {quality_result.data['complexity_analysis']['average_complexity']}")

# 依赖分析
dep_analyzer = DependencyAnalyzer(project_path)
dep_result = dep_analyzer.analyze()
print(f"Python 包数量: {dep_result.data['python_dependencies']['total_count']}")

# 2. 使用指标收集器（汇总所有分析）
collector = MetricsCollector(project_path)
metrics = collector.analyze()
score = metrics.data['overall_score']
print(f"项目评分: {score['total']}/100 ({score['grade']})")

# 3. 生成完整报告
generator = ReportGenerator(project_path)
output_files = generator.generate_report(
    output_path=Path('analysis_report'),
    format='both'
)
print(f"报告已生成: {output_files}")
```

### 自定义分析器

```python
from src.analyzers.base import BaseAnalyzer, AnalysisResult
from pathlib import Path

class SecurityAnalyzer(BaseAnalyzer):
    """安全性分析器示例"""

    def analyze(self) -> AnalysisResult:
        # 检查敏感文件
        sensitive_files = [
            '.env', 'credentials.json', 'secrets.yaml',
            'id_rsa', 'id_dsa', '*.pem', '*.key'
        ]

        found_sensitive = []
        for pattern in sensitive_files:
            files = list(self.project_path.rglob(pattern))
            if files:
                found_sensitive.extend([str(f.relative_to(self.project_path)) for f in files])

        self.result.data['sensitive_files'] = found_sensitive

        if found_sensitive:
            self.result.add_warning(f"发现 {len(found_sensitive)} 个敏感文件")

        # 检查硬编码密钥
        python_files = self._scan_files(pattern="*.py")
        hardcoded_secrets = []

        for file_path in python_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                # 简单的正则检查（实际应用中应使用更复杂的规则）
                import re
                if re.search(r'(password|secret|api_key)\s*=\s*["\'][^"\']+["\']', content, re.IGNORECASE):
                    hardcoded_secrets.append(str(file_path.relative_to(self.project_path)))
            except:
                pass

        self.result.data['hardcoded_secrets'] = hardcoded_secrets

        if hardcoded_secrets:
            self.result.add_error(f"发现 {len(hardcoded_secrets)} 个文件可能包含硬编码密钥")

        return self.result

# 使用自定义分析器
security_analyzer = SecurityAnalyzer(Path('.'))
security_result = security_analyzer.analyze()

print("安全分析结果:")
print(f"敏感文件: {security_result.data['sensitive_files']}")
print(f"硬编码密钥: {security_result.data['hardcoded_secrets']}")
print(f"错误: {security_result.errors}")
print(f"警告: {security_result.warnings}")
```

---

## 批量转换

### 转换整个目录

```bash
# 递归转换所有 Markdown 文件
python md2html.py docs/ -r -o output/

# 只转换特定模式的文件
python md2html.py docs/ -r --pattern "report_*.md" -o output/

# 使用多线程加速
python md2html.py docs/ -r --workers 4 -o output/
```

### 批量处理脚本

```python
from pathlib import Path
from src.batch_processor import BatchProcessor
from src.core.converter import HTMLConverter

# 配置批量处理
processor = BatchProcessor(
    source_dir=Path('docs'),
    output_dir=Path('output'),
    theme='professional',
    embed_images=True,
    process_mermaid=True,
    recursive=True,
    max_workers=4
)

# 执行批量转换
results = processor.process_all()

# 查看结果
print(f"成功: {results['success_count']}")
print(f"失败: {results['failure_count']}")
for error in results['errors']:
    print(f"错误: {error}")
```

---

## 自定义主题

### 创建新主题

```python
# 1. 创建主题文件: src/themes/my_theme.py
from .base import BaseTheme

class MyTheme(BaseTheme):
    """自定义主题"""

    def get_styles(self) -> str:
        return """
        <style>
            body {
                font-family: 'Arial', sans-serif;
                max-width: 900px;
                margin: 0 auto;
                padding: 20px;
                background: #f5f5f5;
            }
            h1 {
                color: #2c3e50;
                border-bottom: 3px solid #3498db;
            }
            code {
                background: #ecf0f1;
                padding: 2px 6px;
                border-radius: 3px;
            }
            /* 更多自定义样式 */
        </style>
        """

    def get_scripts(self) -> str:
        return """
        <script>
            // 自定义 JavaScript
            console.log('My custom theme loaded');
        </script>
        """

# 2. 注册主题: src/themes/__init__.py
from .my_theme import MyTheme

def get_theme(name: str) -> BaseTheme:
    themes = {
        'default': DefaultTheme,
        'minimal': MinimalTheme,
        'professional': ProfessionalTheme,
        'my_theme': MyTheme,  # 添加新主题
    }
    # ...

# 3. 使用新主题
python md2html.py report.md -t my_theme
```

---

## 集成到 CI/CD

### GitHub Actions

```yaml
# .github/workflows/generate-reports.yml
name: Generate Reports

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  generate-reports:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v3

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'

    - name: Install dependencies
      run: |
        pip install -r requirements.txt

    - name: Generate project analysis report
      run: |
        python analyze_project.py -o reports/project_analysis -f html

    - name: Convert documentation to HTML
      run: |
        python md2html.py docs/ -r -o reports/docs/ -t professional

    - name: Upload reports
      uses: actions/upload-artifact@v3
      with:
        name: reports
        path: reports/

    - name: Deploy to GitHub Pages (optional)
      if: github.ref == 'refs/heads/main'
      uses: peaceiris/actions-gh-pages@v3
      with:
        github_token: ${{ secrets.GITHUB_TOKEN }}
        publish_dir: ./reports
```

### GitLab CI

```yaml
# .gitlab-ci.yml
stages:
  - analyze
  - deploy

generate_reports:
  stage: analyze
  image: python:3.9
  script:
    - pip install -r requirements.txt
    - python analyze_project.py -o project_analysis -f html
    - python md2html.py docs/ -r -o html_docs/ -t professional
  artifacts:
    paths:
      - project_analysis.html
      - html_docs/
    expire_in: 1 week

pages:
  stage: deploy
  dependencies:
    - generate_reports
  script:
    - mkdir -p public
    - cp -r html_docs/* public/
    - cp project_analysis.html public/
  artifacts:
    paths:
      - public
  only:
    - main
```

### Pre-commit Hook

```bash
# .git/hooks/pre-commit
#!/bin/bash

echo "生成项目分析报告..."
python analyze_project.py -o .reports/pre_commit_analysis -f markdown

# 检查代码质量评分
SCORE=$(grep "综合评分" .reports/pre_commit_analysis.md | grep -oE '[0-9]+' | head -1)

if [ "$SCORE" -lt 60 ]; then
    echo "❌ 代码质量评分过低 ($SCORE/100)，请改进后再提交"
    exit 1
fi

echo "✅ 代码质量检查通过 ($SCORE/100)"
exit 0
```

---

## 高级用例

### 1. 定期生成项目健康报告

```bash
#!/bin/bash
# weekly_report.sh

DATE=$(date +%Y%m%d)
REPORT_DIR="reports/weekly"

mkdir -p "$REPORT_DIR"

# 生成项目分析报告
python analyze_project.py -o "$REPORT_DIR/analysis_$DATE" -f both

# 转换所有文档
python md2html.py docs/ -r -o "$REPORT_DIR/docs_$DATE/" -t professional

# 发送邮件通知（需要配置邮件服务）
echo "Weekly project report generated: $REPORT_DIR/analysis_$DATE.html" | \
    mail -s "Weekly Project Report" team@example.com
```

### 2. 多项目对比分析

```python
from pathlib import Path
from src.analyzers import MetricsCollector
import json

projects = [
    Path('/path/to/project1'),
    Path('/path/to/project2'),
    Path('/path/to/project3'),
]

comparison = []

for project_path in projects:
    collector = MetricsCollector(project_path)
    result = collector.analyze()

    comparison.append({
        'name': project_path.name,
        'score': result.data['overall_score']['total'],
        'grade': result.data['overall_score']['grade'],
        'files': result.data['summary']['key_metrics']['total_files'],
        'lines': result.data['summary']['key_metrics']['code_lines'],
    })

# 保存对比结果
with open('project_comparison.json', 'w', encoding='utf-8') as f:
    json.dump(comparison, f, indent=2, ensure_ascii=False)

# 打印对比表格
print("\n项目对比:")
print(f"{'项目名称':<20} {'评分':<10} {'等级':<10} {'文件数':<10} {'代码行数':<10}")
print("-" * 70)
for proj in sorted(comparison, key=lambda x: x['score'], reverse=True):
    print(f"{proj['name']:<20} {proj['score']:<10} {proj['grade']:<10} {proj['files']:<10} {proj['lines']:<10}")
```

### 3. 自动化文档发布流程

```python
from pathlib import Path
from src.core.converter import HTMLConverter
import shutil

def publish_documentation():
    """自动化文档发布流程"""

    # 1. 转换所有 Markdown 文档
    docs_dir = Path('docs')
    output_dir = Path('public')

    converter = HTMLConverter()

    for md_file in docs_dir.rglob('*.md'):
        relative_path = md_file.relative_to(docs_dir)
        output_path = output_dir / relative_path.with_suffix('.html')

        output_path.parent.mkdir(parents=True, exist_ok=True)

        converter.convert(
            source_path=md_file,
            output_path=output_path,
            theme='professional',
            embed_images=True,
            process_mermaid=True
        )

    # 2. 生成项目分析报告
    from src.analyzers import ReportGenerator

    generator = ReportGenerator(Path('.'))
    generator.generate_report(
        output_path=output_dir / 'project_analysis',
        format='html'
    )

    # 3. 复制静态资源
    if (Path('assets')).exists():
        shutil.copytree('assets', output_dir / 'assets', dirs_exist_ok=True)

    # 4. 生成索引页面
    create_index_page(output_dir)

    print(f"✅ 文档已发布到: {output_dir}")

def create_index_page(output_dir: Path):
    """生成索引页面"""
    html_files = list(output_dir.rglob('*.html'))

    index_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Documentation Index</title>
        <style>
            body { font-family: Arial, sans-serif; max-width: 800px; margin: 50px auto; }
            h1 { color: #333; }
            ul { list-style: none; padding: 0; }
            li { margin: 10px 0; }
            a { color: #3498db; text-decoration: none; }
            a:hover { text-decoration: underline; }
        </style>
    </head>
    <body>
        <h1>Documentation Index</h1>
        <ul>
    """

    for html_file in sorted(html_files):
        if html_file.name != 'index.html':
            relative_path = html_file.relative_to(output_dir)
            index_html += f'<li><a href="{relative_path}">{relative_path}</a></li>\n'

    index_html += """
        </ul>
    </body>
    </html>
    """

    with open(output_dir / 'index.html', 'w', encoding='utf-8') as f:
        f.write(index_html)

if __name__ == '__main__':
    publish_documentation()
```

---

## 故障排除

### 常见问题

1. **图片无法显示**
   - 使用 `--embed-images` 将图片嵌入为 Base64
   - 检查图片路径是否正确（相对于 Markdown 文件）

2. **Mermaid 图表不渲染**
   - 确保使用 `--mermaid` 选项
   - 检查浏览器 JavaScript 是否启用
   - 查看浏览器控制台是否有错误

3. **分析报告评分异常**
   - 使用 `-v` 查看详细错误信息
   - 检查项目结构是否符合预期
   - 确保 Git 仓库初始化正确

4. **批量转换失败**
   - 检查文件权限
   - 减少并发线程数 `--workers 2`
   - 逐个文件测试找出问题文件

---

**最后更新**: 2025-12-11
